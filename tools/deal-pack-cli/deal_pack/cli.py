from __future__ import annotations

import argparse
import dataclasses
import decimal
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from deal_pack import inventory, rent_roll, t12, derived, writer, sources
from deal_pack.models import RentRollSummary, T12Summary, Derived


def _json_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    raise TypeError(f"not serializable: {type(obj).__name__}")


def _dump(obj) -> str:
    return json.dumps(obj, indent=2, default=_json_default, ensure_ascii=False)


def _d(v):
    """Parse a JSON scalar into Decimal, treating None and "" as missing."""
    if v is None or v == "":
        return None
    return Decimal(v)


def _load_rr_summary(path: Path) -> RentRollSummary:
    rr_dict = json.loads(Path(path).read_text(encoding="utf-8"))
    return RentRollSummary(
        total_sqft=int(rr_dict["total_sqft"]),
        occupied_sqft=int(rr_dict["occupied_sqft"]),
        vacancy_pct=_d(rr_dict["vacancy_pct"]),
        walt_years=_d(rr_dict["walt_years"]),
        avg_base_rent_psf=_d(rr_dict["avg_base_rent_psf"]),
        total_annual_base_rent=_d(rr_dict["total_annual_base_rent"]),
    )


def _load_t12_summary(path: Path) -> T12Summary:
    t12_dict = json.loads(Path(path).read_text(encoding="utf-8"))
    return T12Summary(
        gross_revenue=_d(t12_dict["gross_revenue"]),
        effective_gross_income=_d(t12_dict["effective_gross_income"]),
        opex_total=_d(t12_dict["opex_total"]),
        opex_per_sqft=_d(t12_dict["opex_per_sqft"]),
        noi=_d(t12_dict["noi"]),
        noi_per_sqft=_d(t12_dict["noi_per_sqft"]),
    )


def _cmd_inventory(args: argparse.Namespace) -> int:
    items = inventory.scan_folder(Path(args.root))
    print(_dump(items))
    return 0


def _cmd_rent_roll_summary(args: argparse.Namespace) -> int:
    rows = rent_roll.parse_rent_roll_csv(Path(args.csv))
    ref = date.fromisoformat(args.reference_date)
    summary = rent_roll.compute_rent_roll_summary(rows, reference_date=ref)
    print(_dump(dataclasses.asdict(summary)))
    return 0


def _cmd_t12_summary(args: argparse.Namespace) -> int:
    rows = t12.parse_t12_csv(Path(args.csv))
    summary = t12.compute_t12_summary(rows, total_sqft=args.total_sqft)
    print(_dump(dataclasses.asdict(summary)))
    return 0


def _cmd_derived(args: argparse.Namespace) -> int:
    rr = _load_rr_summary(Path(args.rent_roll_summary))
    t12s = _load_t12_summary(Path(args.t12_summary))
    ask = Decimal(args.ask_price) if args.ask_price else None
    out = derived.compute_derived(rr, t12s, ask_price=ask)
    print(_dump(dataclasses.asdict(out)))
    return 0


def _cmd_write_financials(args: argparse.Namespace) -> int:
    rr = _load_rr_summary(Path(args.rent_roll_summary))
    t12s = _load_t12_summary(Path(args.t12_summary))
    der_dict = json.loads(Path(args.derived).read_text(encoding="utf-8"))
    d = Derived(
        noi_margin=_d(der_dict["noi_margin"]),
        implied_cap_rate_at_ask=_d(der_dict.get("implied_cap_rate_at_ask")),
        expense_ratio=_d(der_dict["expense_ratio"]),
    )

    writer.write_financials_xlsx(
        path=Path(args.out),
        rent_roll_rows_csv=Path(args.rent_roll_csv) if args.rent_roll_csv else None,
        rent_roll_summary=rr,
        t12_rows_csv=Path(args.t12_csv) if args.t12_csv else None,
        t12_summary=t12s,
        derived=d,
        raw_rent_roll_csv=Path(args.raw_rent_roll_csv) if args.raw_rent_roll_csv else None,
        raw_t12_csv=Path(args.raw_t12_csv) if args.raw_t12_csv else None,
    )
    print(_dump({"wrote": str(Path(args.out).resolve())}))
    return 0


def _cmd_write_manifest(args: argparse.Namespace) -> int:
    manifest = json.loads(sys.stdin.read())
    writer.write_manifest(Path(args.out), manifest)
    print(_dump({"wrote": str(Path(args.out).resolve())}))
    return 0


def _cmd_copy_sources(args: argparse.Namespace) -> int:
    classifications = json.loads(Path(args.classifications).read_text(encoding="utf-8"))
    warnings = sources.copy_sources(Path(args.pack_root), classifications)
    # copy_sources now returns a list of per-file warnings (missing source, permission error).
    # Print them to stderr so the orchestrating skill can surface them to the user, but
    # do not fail the command — partial success is the expected behavior.
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(_dump({"copied": True}))
    return 0


def _cmd_check_facts_edited(args: argparse.Namespace) -> int:
    edited = writer.is_facts_modified_by_user(Path(args.facts_path))
    print(_dump({"edited": edited}))
    return 0


def _cmd_write_facts_sidecar(args: argparse.Namespace) -> int:
    facts_path = Path(args.facts_path)
    writer.write_facts_sidecar(facts_path)
    sidecar_path = facts_path.parent / writer.SIDECAR_NAME
    print(_dump({"wrote": str(sidecar_path)}))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="deal-pack")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("inventory")
    sp.add_argument("root")
    sp.set_defaults(func=_cmd_inventory)

    sp = sub.add_parser("rent-roll-summary")
    sp.add_argument("csv")
    sp.add_argument("--reference-date", required=True)
    sp.set_defaults(func=_cmd_rent_roll_summary)

    sp = sub.add_parser("t12-summary")
    sp.add_argument("csv")
    sp.add_argument("--total-sqft", type=Decimal, required=True)
    sp.set_defaults(func=_cmd_t12_summary)

    sp = sub.add_parser("derived")
    sp.add_argument("rent_roll_summary")
    sp.add_argument("t12_summary")
    sp.add_argument("--ask-price", default=None)
    sp.set_defaults(func=_cmd_derived)

    sp = sub.add_parser("write-financials")
    sp.add_argument("--out", required=True)
    sp.add_argument("--rent-roll-csv", default=None)
    sp.add_argument("--rent-roll-summary", required=True)
    sp.add_argument("--t12-csv", default=None)
    sp.add_argument("--t12-summary", required=True)
    sp.add_argument("--derived", required=True)
    sp.add_argument("--raw-rent-roll-csv", default=None)
    sp.add_argument("--raw-t12-csv", default=None)
    sp.set_defaults(func=_cmd_write_financials)

    sp = sub.add_parser("write-manifest")
    sp.add_argument("--out", required=True)
    sp.set_defaults(func=_cmd_write_manifest)

    sp = sub.add_parser("copy-sources")
    sp.add_argument("classifications")
    sp.add_argument("--pack-root", required=True)
    sp.set_defaults(func=_cmd_copy_sources)

    sp = sub.add_parser("check-facts-edited")
    sp.add_argument("facts_path")
    sp.set_defaults(func=_cmd_check_facts_edited)

    sp = sub.add_parser("write-facts-sidecar")
    sp.add_argument("facts_path")
    sp.set_defaults(func=_cmd_write_facts_sidecar)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, json.JSONDecodeError, FileNotFoundError, decimal.InvalidOperation) as e:
        # The CLI contract is JSON-out. Runtime data errors must be serialized as JSON
        # so the caller (SKILL.md) can json.loads(stdout) without hitting a traceback.
        # Argparse errors (missing args, etc.) still go to stderr — those are
        # caller-programming-errors, not runtime data errors.
        print(json.dumps({"error": type(e).__name__ + ": " + str(e)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
