#!/usr/bin/env python3
"""
V23 Comp Merger v3 — Combines JSON outputs from 5 parallel zone agents into a
single deduplicated, filtered, and sorted dataset ready for export.

Usage:
  python3 merge_results.py --input-dir /tmp/comp-search/ \
    --output /tmp/comp-search/merged.json \
    --asset-type hospitality --geography Texas --transaction-type both \
    --date-from 2020 --date-to 2024 \
    --price-min 10000000 --price-max 80000000 \
    --cap-rate-min 0.05 --cap-rate-max 0.07 \
    --units-min 50 \
    --counterparty "Blackstone"
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def normalize_address(addr):
    if not addr:
        return ''
    s = re.sub(r'[^\w\s]', '', str(addr).lower())
    s = re.sub(r'\s+', ' ', s).strip()
    abbrevs = {
        r'\bave\b': 'avenue', r'\bblvd\b': 'boulevard', r'\bst\b': 'street',
        r'\bdr\b': 'drive', r'\bpl\b': 'place', r'\brd\b': 'road',
        r'\bct\b': 'court', r'\bln\b': 'lane', r'\bpkwy\b': 'parkway',
        r'\bn\b': 'north', r'\bs\b': 'south', r'\be\b': 'east', r'\bw\b': 'west',
    }
    for pattern, repl in abbrevs.items():
        s = re.sub(pattern, repl, s)
    return re.sub(r'\s+', ' ', s).strip()


def to_float(val):
    """Safely coerce a value to float; returns None on failure."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(',', '').replace('$', '').replace('%', '')
    try:
        return float(s)
    except ValueError:
        return None


def parse_year_from_date(date_val):
    """Extract a 4-digit year from a date string or number. Returns None if not found."""
    if date_val is None:
        return None
    s = str(date_val)
    # Look for 4-digit year pattern
    m = re.search(r'\b(19|20)\d{2}\b', s)
    if m:
        return int(m.group(0))
    # Handle Excel serial date (number of days since 1900-01-01)
    try:
        n = float(s)
        if 20000 < n < 60000:  # roughly 1954-2064
            year = 1900 + int((n - 1) / 365.25)
            return year
    except (ValueError, TypeError):
        pass
    return None


# ---------------------------------------------------------------------------
# Core filter functions
# ---------------------------------------------------------------------------

def matches_geography(comp, geography):
    if not geography:
        return True
    geo_lower = geography.lower()
    geo_terms = [t.strip() for t in geo_lower.replace(',', ' ').split()]
    searchable = ['address', 'property_name', 'city', 'state', 'submarket',
                  '_source_file', 'notes']
    for field in searchable:
        val = str(comp.get(field, '')).lower()
        if any(term in val for term in geo_terms):
            return True
    return False


def matches_asset_type(comp, asset_type):
    if not asset_type:
        return True
    at_lower = asset_type.lower()
    asset_keywords = {
        "hospitality": ["hotel", "hospitality", "resort", "motel", "inn", "suite",
                         "marriott", "hilton", "hyatt", "sheraton", "westin",
                         "hampton", "courtyard", "holiday inn", "select service",
                         "full service", "boutique"],
        "office": ["office", "tower", "corporate"],
        "retail": ["retail", "shopping", "mall", "plaza"],
        "multifamily": ["multifamily", "apartment", "residential", "rental"],
        "industrial": ["industrial", "warehouse", "logistics", "distribution"],
    }
    keywords = []
    for key, kws in asset_keywords.items():
        if key in at_lower or at_lower in key:
            keywords = kws
            break
    if not keywords:
        keywords = [at_lower]
    searchable = ['asset_type', 'property_name', 'address', 'brand',
                  'notes', '_source_file']
    for field in searchable:
        val = str(comp.get(field, '')).lower()
        if any(kw in val for kw in keywords):
            return True
    if at_lower in ('hospitality', 'hotel'):
        for field in ['rooms_keys', 'revpar', 'adr', 'price_per_key']:
            if comp.get(field) is not None:
                return True
    return False


def matches_date_range(comp, year_from, year_to):
    """Return True if comp date falls in [year_from, year_to].
    Unknown dates are included rather than excluded."""
    if year_from is None and year_to is None:
        return True
    year = parse_year_from_date(comp.get('date'))
    if year is None:
        return True  # unknown date — include
    if year_from and year < year_from:
        return False
    if year_to and year > year_to:
        return False
    return True


def matches_price_range(comp, price_min, price_max):
    if price_min is None and price_max is None:
        return True
    price = to_float(comp.get('price'))
    if price is None:
        return True  # unknown price — include
    if price_min and price < price_min:
        return False
    if price_max and price > price_max:
        return False
    return True


def matches_cap_rate(comp, cap_min, cap_max):
    if cap_min is None and cap_max is None:
        return True
    cap = to_float(comp.get('cap_rate'))
    if cap is None:
        return True
    # Normalize: 6.5 (percent stored as number) → 0.065
    if cap > 1:
        cap = cap / 100
    if cap_min and cap < cap_min:
        return False
    if cap_max and cap > cap_max:
        return False
    return True


def matches_sf_range(comp, sf_min, sf_max):
    if sf_min is None and sf_max is None:
        return True
    sf = to_float(comp.get('sf'))
    if sf is None:
        return True
    if sf_min and sf < sf_min:
        return False
    if sf_max and sf > sf_max:
        return False
    return True


def matches_units_range(comp, units_min, units_max):
    if units_min is None and units_max is None:
        return True
    # Check 'units' and 'rooms_keys'
    units = to_float(comp.get('units')) or to_float(comp.get('rooms_keys'))
    if units is None:
        return True
    if units_min and units < units_min:
        return False
    if units_max and units > units_max:
        return False
    return True


def matches_year_built(comp, year_from, year_to):
    if year_from is None and year_to is None:
        return True
    yb = to_float(comp.get('year_built'))
    if yb is None:
        return True
    if year_from and yb < year_from:
        return False
    if year_to and yb > year_to:
        return False
    return True


def matches_noi(comp, noi_min, noi_max):
    if noi_min is None and noi_max is None:
        return True
    noi = to_float(comp.get('noi'))
    if noi is None:
        return True
    if noi_min and noi < noi_min:
        return False
    if noi_max and noi > noi_max:
        return False
    return True


def matches_revpar(comp, revpar_min):
    if revpar_min is None:
        return True
    revpar = to_float(comp.get('revpar'))
    if revpar is None:
        return True
    return revpar >= revpar_min


def matches_occupancy(comp, occ_min):
    if occ_min is None:
        return True
    occ = to_float(comp.get('occupancy'))
    if occ is None:
        return True
    if occ > 1:
        occ = occ / 100  # normalize 85 → 0.85
    return occ >= occ_min


def matches_counterparty(comp, counterparty):
    """Search buyer, seller, sponsor, and tenant fields for counterparty name."""
    if not counterparty:
        return True
    cp_lower = counterparty.lower()
    cp_terms = [t.strip() for t in cp_lower.split()]
    searchable = ['buyer', 'seller', 'sponsor', 'tenant', 'lender', 'notes',
                  'property_name', '_source_file']
    for field in searchable:
        val = str(comp.get(field, '')).lower()
        if all(term in val for term in cp_terms):
            return True
    return False


def matches_property_class(comp, prop_class):
    if not prop_class:
        return True
    pc_lower = prop_class.lower().replace('class', '').strip()
    val = str(comp.get('property_class', '')).lower()
    return pc_lower in val


def matches_brand(comp, brand):
    """Match hotel brand — supports space-separated list (e.g. 'Hilton Marriott')."""
    if not brand:
        return True
    brands = [b.lower().strip() for b in brand.split()]
    for field in ['brand', 'property_name', 'notes']:
        val = str(comp.get(field, '') or '').lower()
        for b in brands:
            if b in val:
                return True
    return False


def matches_submarket(comp, submarket):
    if not submarket:
        return True
    sm_lower = submarket.lower()
    for field in ['submarket', 'address', 'property_name', 'notes']:
        val = str(comp.get(field, '') or '').lower()
        if sm_lower in val:
            return True
    return False


def matches_lender(comp, lender):
    if not lender:
        return True
    lender_lower = lender.lower()
    for field in ['lender', 'notes', '_source_file']:
        val = str(comp.get(field, '') or '').lower()
        if lender_lower in val:
            return True
    return False


# ---------------------------------------------------------------------------
# Relevance scoring
# ---------------------------------------------------------------------------

def relevance_score(comp):
    score = 0
    valuable = ['price', 'price_psf', 'price_per_key', 'cap_rate', 'noi',
                 'revpar', 'adr', 'occupancy', 'sf', 'rooms_keys',
                 'rent_psf', 'buyer', 'seller', 'date']
    for field in valuable:
        if comp.get(field) is not None:
            score += 10
    if comp.get('address') or comp.get('property_name'):
        score += 5
    if comp.get('date'):
        score += 5
    return score


# ---------------------------------------------------------------------------
# Loading and main
# ---------------------------------------------------------------------------

def load_zone_files(input_dir):
    zone_data = []
    for f in sorted(Path(input_dir).glob("zone-*.json")):
        try:
            with open(f) as fh:
                data = json.load(fh)
                zone_data.append(data)
                print(f"  Loaded {f.name}: {len(data.get('comps', []))} comps", file=sys.stderr)
        except Exception as e:
            print(f"  WARNING: Failed to load {f.name}: {e}", file=sys.stderr)
    return zone_data


def apply_filter(comps, label, fn):
    before = len(comps)
    result = [c for c in comps if fn(c)]
    if len(result) < before:
        print(f"  After {label}: {len(result)} (removed {before - len(result)})", file=sys.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description="V23 Comp Merger v3")
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--output', required=True)
    # Core filters
    parser.add_argument('--asset-type')
    parser.add_argument('--geography')
    parser.add_argument('--transaction-type', choices=['sale', 'lease', 'both'], default='both')
    # Date range
    parser.add_argument('--date-from', type=int, help='Earliest year (e.g. 2020)')
    parser.add_argument('--date-to', type=int, help='Latest year (e.g. 2024)')
    # Price range
    parser.add_argument('--price-min', type=float, help='Min sale price in dollars')
    parser.add_argument('--price-max', type=float, help='Max sale price in dollars')
    # Cap rate range
    parser.add_argument('--cap-rate-min', type=float, help='Min cap rate as decimal (e.g. 0.05)')
    parser.add_argument('--cap-rate-max', type=float, help='Max cap rate as decimal (e.g. 0.07)')
    # SF range
    parser.add_argument('--sf-min', type=float, help='Min square feet')
    parser.add_argument('--sf-max', type=float, help='Max square feet')
    # Units / rooms / keys
    parser.add_argument('--units-min', type=float, help='Min units/rooms/keys')
    parser.add_argument('--units-max', type=float, help='Max units/rooms/keys')
    # Year built
    parser.add_argument('--year-built-from', type=int)
    parser.add_argument('--year-built-to', type=int)
    # NOI
    parser.add_argument('--noi-min', type=float)
    parser.add_argument('--noi-max', type=float)
    # RevPAR / occupancy
    parser.add_argument('--revpar-min', type=float)
    parser.add_argument('--occupancy-min', type=float, help='Min occupancy as decimal (e.g. 0.85)')
    # Text / name filters
    parser.add_argument('--counterparty', help='Buyer/seller/sponsor name to search')
    parser.add_argument('--property-class', help='Property class: A, B, or C')
    parser.add_argument('--brand', help='Hotel brand/flag (space-separated for multiple: "Hilton Marriott")')
    parser.add_argument('--submarket', help='Submarket or neighborhood')
    parser.add_argument('--lender', help='Lender name filter')
    args = parser.parse_args()

    print("Merging zone results...", file=sys.stderr)
    zone_data = load_zone_files(args.input_dir)
    if not zone_data:
        print("No zone files found.", file=sys.stderr)
        sys.exit(1)

    all_comps = []
    all_cloud_only = []
    all_encrypted = []
    total_files_searched = 0
    zone_summary = []

    for zd in zone_data:
        comps = zd.get('comps', [])
        for comp in comps:
            comp['_zone'] = zd.get('zone_name', 'Unknown')
        all_comps.extend(comps)
        all_cloud_only.extend(zd.get('files_cloud_only', []))
        all_encrypted.extend(zd.get('files_encrypted', []))
        total_files_searched += zd.get('files_searched', 0) + zd.get('files_with_data', 0)
        zone_summary.append({
            "zone": zd.get('zone'),
            "zone_name": zd.get('zone_name'),
            "comps_found": len(comps),
            "files_cloud_only": len(zd.get('files_cloud_only', [])),
        })

    print(f"  Total raw comps before filters: {len(all_comps)}", file=sys.stderr)

    # Apply filters in sequence — each one is skipped if its arg is None/default
    filtered = all_comps

    if args.geography:
        filtered = apply_filter(filtered, f"geography ({args.geography})",
                                lambda c, g=args.geography: matches_geography(c, g))
    if args.asset_type:
        filtered = apply_filter(filtered, f"asset-type ({args.asset_type})",
                                lambda c, a=args.asset_type: matches_asset_type(c, a))
    if args.transaction_type != 'both':
        t = args.transaction_type
        filtered = apply_filter(filtered, f"transaction-type ({t})",
                                lambda c, tt=t: c.get('_comp_type') == tt)
    if args.date_from or args.date_to:
        df, dt = args.date_from, args.date_to
        filtered = apply_filter(filtered, f"date ({df}-{dt})",
                                lambda c, f=df, t=dt: matches_date_range(c, f, t))
    if args.price_min or args.price_max:
        pn, px = args.price_min, args.price_max
        filtered = apply_filter(filtered, f"price (${pn}-${px})",
                                lambda c, mn=pn, mx=px: matches_price_range(c, mn, mx))
    if args.cap_rate_min or args.cap_rate_max:
        cn, cx = args.cap_rate_min, args.cap_rate_max
        filtered = apply_filter(filtered, f"cap-rate ({cn}-{cx})",
                                lambda c, mn=cn, mx=cx: matches_cap_rate(c, mn, mx))
    if args.sf_min or args.sf_max:
        sn, sx = args.sf_min, args.sf_max
        filtered = apply_filter(filtered, f"SF ({sn}-{sx})",
                                lambda c, mn=sn, mx=sx: matches_sf_range(c, mn, mx))
    if args.units_min or args.units_max:
        un, ux = args.units_min, args.units_max
        filtered = apply_filter(filtered, f"units ({un}-{ux})",
                                lambda c, mn=un, mx=ux: matches_units_range(c, mn, mx))
    if args.year_built_from or args.year_built_to:
        yf, yt = args.year_built_from, args.year_built_to
        filtered = apply_filter(filtered, f"year-built ({yf}-{yt})",
                                lambda c, f=yf, t=yt: matches_year_built(c, f, t))
    if args.noi_min or args.noi_max:
        nn, nx = args.noi_min, args.noi_max
        filtered = apply_filter(filtered, f"NOI ({nn}-{nx})",
                                lambda c, mn=nn, mx=nx: matches_noi(c, mn, mx))
    if args.revpar_min:
        rm = args.revpar_min
        filtered = apply_filter(filtered, f"RevPAR (>={rm})",
                                lambda c, r=rm: matches_revpar(c, r))
    if args.occupancy_min:
        om = args.occupancy_min
        filtered = apply_filter(filtered, f"occupancy (>={om:.0%})",
                                lambda c, o=om: matches_occupancy(c, o))
    if args.counterparty:
        cp = args.counterparty
        filtered = apply_filter(filtered, f"counterparty ({cp})",
                                lambda c, p=cp: matches_counterparty(c, p))
    if args.property_class:
        pc = args.property_class
        filtered = apply_filter(filtered, f"class ({pc})",
                                lambda c, p=pc: matches_property_class(c, p))
    if args.brand:
        br = args.brand
        filtered = apply_filter(filtered, f"brand ({br})",
                                lambda c, b=br: matches_brand(c, b))
    if args.submarket:
        sm = args.submarket
        filtered = apply_filter(filtered, f"submarket ({sm})",
                                lambda c, s=sm: matches_submarket(c, s))
    if args.lender:
        ln = args.lender
        filtered = apply_filter(filtered, f"lender ({ln})",
                                lambda c, l=ln: matches_lender(c, l))

    # Deduplicate by normalized address + comp type
    seen = set()
    unique = []
    for comp in filtered:
        key = (normalize_address(comp.get('address', '') or comp.get('property_name', '')),
               comp.get('_comp_type', ''))
        if key not in seen:
            seen.add(key)
            unique.append(comp)

    print(f"  After dedup: {len(unique)} (removed {len(filtered) - len(unique)} duplicates)", file=sys.stderr)

    # Sort by relevance
    unique.sort(key=lambda c: -relevance_score(c))

    result = {
        "total_comps": len(unique),
        "zones_searched": len(zone_data),
        "total_files_searched": total_files_searched,
        "files_cloud_only": all_cloud_only,
        "files_encrypted": all_encrypted,
        "zone_summary": zone_summary,
        "filters_applied": {k: v for k, v in vars(args).items()
                            if v is not None and k not in ('input_dir', 'output')},
        "comps": unique,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nMerged: {len(unique)} comps → {args.output}", file=sys.stderr)
    parts = ["{}: {}".format(z["zone_name"], z["comps_found"]) for z in zone_summary]
    print(f"Zone breakdown: {', '.join(parts)}", file=sys.stderr)


if __name__ == "__main__":
    main()
