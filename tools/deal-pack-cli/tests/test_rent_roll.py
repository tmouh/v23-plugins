from datetime import date
from decimal import Decimal
from pathlib import Path

from deal_pack.rent_roll import parse_rent_roll_csv, compute_rent_roll_summary


REFERENCE_DATE = date(2025, 1, 1)


def test_parse_rent_roll_csv_basic(fixtures_dir: Path):
    rows = parse_rent_roll_csv(fixtures_dir / "rent_rolls" / "office_standard.csv")
    assert len(rows) == 3
    assert rows[0].tenant == "Acme Corp"
    assert rows[0].sqft == 5000
    assert rows[0].base_rent_annual == Decimal("150000")


def test_parse_rent_roll_handles_vacant_row(fixtures_dir: Path):
    rows = parse_rent_roll_csv(fixtures_dir / "rent_rolls" / "vacant_units.csv")
    vacant = [r for r in rows if r.tenant is None]
    assert len(vacant) == 1
    assert vacant[0].sqft == 2000
    assert vacant[0].notes == "vacant"


def test_summary_fully_occupied(fixtures_dir: Path):
    rows = parse_rent_roll_csv(fixtures_dir / "rent_rolls" / "office_standard.csv")
    s = compute_rent_roll_summary(rows, reference_date=REFERENCE_DATE)
    assert s.total_sqft == 12000
    assert s.occupied_sqft == 12000
    assert s.vacancy_pct == Decimal("0.00")
    assert s.total_annual_base_rent == Decimal("366000")
    # avg = 366000 / 12000 = 30.50
    assert s.avg_base_rent_psf == Decimal("30.50")


def test_summary_walt_fully_occupied(fixtures_dir: Path):
    """WALT = sum(remaining_term_years * sqft) / occupied_sqft.

    From REFERENCE_DATE 2025-01-01:
      - 101 Acme: end 2027-12-31 -> ~2.997 yrs * 5000 = 14986
      - 102 Beta: end 2028-05-31 -> ~3.411 yrs * 3000 = 10233
      - 201 Gamma: end 2026-02-28 -> ~1.159 yrs * 4000 = 4634
      Total weighted ~29853 / 12000 -> ~2.488
    Allow small tolerance for day-count rounding.
    """
    rows = parse_rent_roll_csv(fixtures_dir / "rent_rolls" / "office_standard.csv")
    s = compute_rent_roll_summary(rows, reference_date=REFERENCE_DATE)
    assert Decimal("2.40") <= s.walt_years <= Decimal("2.55")


def test_summary_with_vacancy(fixtures_dir: Path):
    rows = parse_rent_roll_csv(fixtures_dir / "rent_rolls" / "vacant_units.csv")
    s = compute_rent_roll_summary(rows, reference_date=REFERENCE_DATE)
    assert s.total_sqft == 10000
    assert s.occupied_sqft == 8000
    # 2000/10000 = 20.00
    assert s.vacancy_pct == Decimal("20.00")
    # avg = 246000 / 8000 = 30.75
    assert s.avg_base_rent_psf == Decimal("30.75")


def test_summary_empty_list():
    s = compute_rent_roll_summary([], reference_date=REFERENCE_DATE)
    assert s.total_sqft == 0
    assert s.occupied_sqft == 0
    assert s.vacancy_pct == Decimal("0.00")
    assert s.walt_years == Decimal("0.00")
    assert s.avg_base_rent_psf == Decimal("0.00")
    assert s.total_annual_base_rent == Decimal("0")
