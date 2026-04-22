import hashlib
import json
from decimal import Decimal
from pathlib import Path

import openpyxl

from deal_pack.models import RentRollSummary, T12Summary, Derived
from deal_pack.writer import (
    write_financials_xlsx, write_manifest, write_facts_sidecar,
    is_facts_modified_by_user,
)


def _rr_summary():
    return RentRollSummary(
        total_sqft=10000, occupied_sqft=10000, vacancy_pct=Decimal("0.00"),
        walt_years=Decimal("5.00"), avg_base_rent_psf=Decimal("30.00"),
        total_annual_base_rent=Decimal("300000"),
    )


def _t12_summary():
    return T12Summary(
        gross_revenue=Decimal("300000"), effective_gross_income=Decimal("290000"),
        opex_total=Decimal("100000"), opex_per_sqft=Decimal("10.00"),
        noi=Decimal("190000"), noi_per_sqft=Decimal("19.00"),
    )


def _derived():
    return Derived(
        noi_margin=Decimal("0.66"), implied_cap_rate_at_ask=None,
        expense_ratio=Decimal("0.34"),
    )


def test_write_financials_creates_all_tabs(tmp_pack_dir: Path):
    write_financials_xlsx(
        path=tmp_pack_dir / "financials.xlsx",
        rent_roll_rows_csv=None,
        rent_roll_summary=_rr_summary(),
        t12_rows_csv=None,
        t12_summary=_t12_summary(),
        derived=_derived(),
    )
    wb = openpyxl.load_workbook(tmp_pack_dir / "financials.xlsx")
    assert set(wb.sheetnames) >= {
        "rent_roll_summary", "t12_summary", "derived",
    }


def test_write_manifest_roundtrip(tmp_pack_dir: Path):
    manifest = {
        "deal_name": "Test Deal",
        "generated_at": "2026-04-22T00:00:00Z",
        "skill_version": "0.1.0",
        "input_root": "C:/tmp/in",
        "files": [],
        "arithmetic_checks": [],
        "warnings": [],
    }
    write_manifest(tmp_pack_dir / "pack-manifest.json", manifest)
    loaded = json.loads((tmp_pack_dir / "pack-manifest.json").read_text())
    assert loaded["deal_name"] == "Test Deal"


def test_facts_sidecar_detects_user_edits(tmp_pack_dir: Path):
    facts = tmp_pack_dir / "facts.md"
    facts.write_text("# Original\n", encoding="utf-8")
    write_facts_sidecar(facts)

    # No edits yet:
    assert is_facts_modified_by_user(facts) is False

    # User edits facts.md:
    facts.write_text("# Edited by human\n", encoding="utf-8")
    assert is_facts_modified_by_user(facts) is True


def test_facts_sidecar_missing_file_is_safe(tmp_pack_dir: Path):
    assert is_facts_modified_by_user(tmp_pack_dir / "facts.md") is False


def test_sidecar_corrupted_json_is_safe(tmp_pack_dir: Path):
    """A corrupted sidecar must not crash — it must be treated as 'no recorded hashes'."""
    facts = tmp_pack_dir / "facts.md"
    facts.write_text("# Original\n", encoding="utf-8")
    sidecar = tmp_pack_dir / ".v23-deal-pack.sha"

    # Simulate a truncated/corrupted write from OneDrive or antivirus:
    sidecar.write_text("{not valid json", encoding="utf-8")

    # Must not raise:
    assert is_facts_modified_by_user(facts) is False

    # write_facts_sidecar must also tolerate the corruption and overwrite cleanly:
    write_facts_sidecar(facts)
    loaded = json.loads(sidecar.read_text(encoding="utf-8"))
    assert "facts.md" in loaded


def test_sidecar_empty_file_is_safe(tmp_pack_dir: Path):
    """A zero-byte sidecar (classic partial-write scenario) must be treated as empty."""
    facts = tmp_pack_dir / "facts.md"
    facts.write_text("# x\n", encoding="utf-8")
    sidecar = tmp_pack_dir / ".v23-deal-pack.sha"
    sidecar.write_text("", encoding="utf-8")

    assert is_facts_modified_by_user(facts) is False
    write_facts_sidecar(facts)
    assert sidecar.stat().st_size > 0
