#!/usr/bin/env python3
"""
V23 Comp File Finder v2 — Searches a single zone of the V23 Database for files
likely containing comp data. Designed to be called per-zone by parallel agents.

Usage:
  python3 find_comps.py --db-root /path/to/V23-Database --zone 1 --type both \
    --market "Brooklyn" --asset-type "office" --output /tmp/comp-search/zone-1.json
"""

import argparse
import json
import os
import re
import sys

STATE_FOLDERS = {
    "NY": "aa NY", "CA": "CA", "FL": "FL", "TX": "TX", "IL": "IL",
    "NJ": "NJ", "PA": "PA", "MA": "MA", "CT": "CT", "VA": "VA",
    "MD": "MD", "GA": "GA", "NC": "NC", "OH": "OH", "MI": "MI",
    "WA": "WA", "CO": "CO", "AZ": "AZ", "TN": "TN", "OR": "OR",
    "MN": "MN", "MO": "MO", "WI": "WI", "IN": "IN", "SC": "SC",
    "NV": "NV", "DC": "DC", "LA": "LA", "HI": "HI",
}

MARKET_STATE_MAP = {
    "boston": "MA", "chicago": "IL", "los angeles": "CA", "la": "CA",
    "san francisco": "CA", "sf": "CA", "miami": "FL", "fort lauderdale": "FL",
    "dallas": "TX", "houston": "TX", "austin": "TX", "san antonio": "TX",
    "seattle": "WA", "washington": "DC", "dc": "DC", "denver": "CO",
    "atlanta": "GA", "nashville": "TN", "philadelphia": "PA", "phoenix": "AZ",
    "newark": "NJ", "jersey city": "NJ", "hoboken": "NJ",
    "brooklyn": "NY", "manhattan": "NY", "queens": "NY", "bronx": "NY",
    "williamsburg": "NY", "nyc": "NY", "new york": "NY",
    "the woodlands": "TX", "irving": "TX", "plano": "TX", "garland": "TX",
    "orlando": "FL", "tampa": "FL", "fort worth": "TX",
}

ASSET_KEYWORDS = {
    "hospitality": ["hotel", "hospitality", "resort", "motel", "inn", "suite",
                     "marriott", "hilton", "hyatt", "sheraton", "westin", "fairfield",
                     "hampton", "courtyard", "holiday inn", "select service",
                     "full service", "boutique hotel", "revpar", "adr"],
    "office": ["office", "tower", "corporate", "class a", "class b"],
    "retail": ["retail", "shopping", "mall", "center", "plaza", "shops"],
    "multifamily": ["multifamily", "apartment", "residential", "unit", "rental",
                     "loft", "condo", "garden style"],
    "industrial": ["industrial", "warehouse", "logistics", "distribution", "flex"],
    "mixed-use": ["mixed-use", "mixed use"],
    "land": ["land", "site", "parcel", "acreage", "acre"],
}

COMP_EXTENSIONS = {'.xlsx', '.xlsm', '.xls', '.csv', '.pdf'}


def infer_state(market_query):
    q = market_query.lower().strip()
    for city, state in MARKET_STATE_MAP.items():
        if city in q or q in city:
            return state
    if q.upper() in STATE_FOLDERS or len(q) == 2:
        return q.upper()
    return None


def get_asset_keywords(asset_type):
    if not asset_type:
        return []
    at = asset_type.lower()
    for key, kws in ASSET_KEYWORDS.items():
        if key in at or at in key:
            return kws
    return [at]


def score_file(filepath, comp_type, market_query=None, asset_type=None):
    fname = os.path.basename(filepath).lower()
    fpath = filepath.lower()
    score = 0

    if comp_type in ("sale", "both"):
        for kw in ['sale comp', 'sales comp', 'sale', 'sold', 'purchase', 'acquisition']:
            if kw in fname: score += 10
            elif kw in fpath: score += 3
    if comp_type in ("lease", "both"):
        for kw in ['lease comp', 'leasing comp', 'lease', 'leasing', 'rent roll', 'tenant']:
            if kw in fname: score += 10
            elif kw in fpath: score += 3

    for kw in ['comp', 'market data', 'comparable', 'proforma', 'financials',
               'underwriting', 'offering memorandum']:
        if kw in fname: score += 5
        elif kw in fpath: score += 2

    for kw in get_asset_keywords(asset_type):
        if kw in fname: score += 8
        elif kw in fpath: score += 4

    if market_query:
        mq = market_query.lower()
        if mq in fname: score += 15
        elif mq in fpath: score += 8

    if re.findall(r'20(2[0-9]|[3-9]\d)', fname):
        score += 5
    if "1- realty" in fpath or "1- deals" in fpath:
        score += 3
    if any(skip in fname for skip in ['template', 'blank', 'draft', 'backup', '~$']):
        score -= 10

    return score


def find_files_in_zone(zone_path, comp_type="both", market=None, asset_type=None,
                        state=None, max_results=100):
    results = []
    if not os.path.exists(zone_path):
        print(f"  Zone path does not exist: {zone_path}", file=sys.stderr)
        return results

    for root, dirs, files in os.walk(zone_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in COMP_EXTENSIONS or f.startswith('~$'):
                continue
            filepath = os.path.join(root, f)
            relevance = score_file(filepath, comp_type, market, asset_type)
            if relevance > 0:
                try:
                    size = os.path.getsize(filepath)
                except OSError:
                    size = 0
                results.append({
                    "path": filepath,
                    "filename": f,
                    "relevance_score": relevance,
                    "size_bytes": size,
                    "extension": ext,
                })

    results.sort(key=lambda x: -x['relevance_score'])
    return results[:max_results]


def narrow_archive_path(archive_base, state=None, market=None):
    target_state = state
    if not target_state and market:
        target_state = infer_state(market)
    if target_state:
        # Check override name first (e.g., "aa NY" for NY)
        if target_state in STATE_FOLDERS:
            state_folder = os.path.join(archive_base, STATE_FOLDERS[target_state])
            if os.path.exists(state_folder):
                return state_folder
        # Fall back to raw abbreviation
        state_folder = os.path.join(archive_base, target_state)
        if os.path.exists(state_folder):
            return state_folder
    return archive_base


def main():
    parser = argparse.ArgumentParser(description="V23 Comp File Finder v2")
    parser.add_argument('--db-root', required=True, help='V23 Database root path')
    parser.add_argument('--zone', type=int, required=True, choices=[1, 2, 3, 4, 5])
    parser.add_argument('--type', choices=['sale', 'lease', 'both'], default='both')
    parser.add_argument('--market', help='City, neighborhood, or submarket')
    parser.add_argument('--asset-type', help='Asset type filter')
    parser.add_argument('--state', help='Two-letter state code')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--top', type=int, default=100)
    args = parser.parse_args()

    zone_map = {
        1: ("Active Deals", os.path.join(args.db_root, "1- Realty", "1- Deals")),
        2: ("Portfolio", os.path.join(args.db_root, "2- Vanadium Group")),
        3: ("Marketed Deals", os.path.join(args.db_root, "4- Marketed Deals")),
        4: ("Archive", os.path.join(args.db_root, "x- Deals Archive")),
        5: ("Market Data", os.path.join(args.db_root, "x- Market Data")),
    }

    zone_name, zone_path = zone_map[args.zone]
    if args.zone == 4:
        zone_path = narrow_archive_path(zone_path, args.state, args.market)

    print(f"Zone {args.zone} ({zone_name}): Searching {zone_path}", file=sys.stderr)
    results = find_files_in_zone(
        zone_path, comp_type=args.type, market=args.market,
        asset_type=args.asset_type, state=args.state, max_results=args.top
    )
    print(f"  Found {len(results)} relevant files.", file=sys.stderr)

    output = {
        "zone": args.zone,
        "zone_name": zone_name,
        "zone_path": zone_path,
        "files_found": len(results),
        "files": results,
    }

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"  Saved to: {args.output}", file=sys.stderr)
    else:
        for r in results[:20]:
            print(f"  [{r['relevance_score']:3d}] {r['filename']}")
            print(f"        {r['path']}")


if __name__ == "__main__":
    main()
