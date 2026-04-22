from decimal import Decimal
from pathlib import Path

from deal_pack.t12 import parse_t12_csv, compute_t12_summary


def test_parse_t12_csv(fixtures_dir: Path):
    rows = parse_t12_csv(fixtures_dir / "t12s" / "standard_office.csv")
    assert len(rows) == 12
    assert rows[0].category == "revenue"
    assert rows[0].subcategory == "base_rent"
    assert rows[0].total == Decimal("800000")


def test_summary_standard_office(fixtures_dir: Path):
    rows = parse_t12_csv(fixtures_dir / "t12s" / "standard_office.csv")
    s = compute_t12_summary(rows, total_sqft=Decimal("100000"))
    assert s.gross_revenue == Decimal("1000000")
    assert s.effective_gross_income == Decimal("950000")
    assert s.opex_total == Decimal("330000")
    assert s.noi == Decimal("620000")
    assert s.opex_per_sqft == Decimal("3.30")
    assert s.noi_per_sqft == Decimal("6.20")


def test_summary_zero_sqft_safe(fixtures_dir: Path):
    rows = parse_t12_csv(fixtures_dir / "t12s" / "standard_office.csv")
    s = compute_t12_summary(rows, total_sqft=Decimal("0"))
    assert s.opex_per_sqft == Decimal("0.00")
    assert s.noi_per_sqft == Decimal("0.00")


def test_summary_empty_list():
    s = compute_t12_summary([], total_sqft=Decimal("10000"))
    assert s.gross_revenue == Decimal("0")
    assert s.effective_gross_income == Decimal("0")
    assert s.opex_total == Decimal("0")
    assert s.noi == Decimal("0")
