from datetime import date
from decimal import Decimal
from deal_pack.models import (
    RentRollRow, RentRollSummary, T12Row, T12Summary, Derived, InventoryItem,
)


def test_rent_roll_row_required_fields():
    row = RentRollRow(
        unit="101",
        tenant="Acme Corp",
        sqft=5000,
        lease_start=date(2022, 1, 1),
        lease_end=date(2027, 12, 31),
        base_rent_annual=Decimal("150000"),
        base_rent_psf=Decimal("30"),
        recoveries="NNN",
        options="1x5yr",
        security_deposit=Decimal("12500"),
        notes="",
    )
    assert row.sqft == 5000
    assert row.base_rent_annual == Decimal("150000")


def test_rent_roll_row_vacant_has_none_tenant():
    row = RentRollRow(
        unit="102", tenant=None, sqft=2000,
        lease_start=None, lease_end=None,
        base_rent_annual=Decimal("0"), base_rent_psf=Decimal("0"),
        recoveries="", options="", security_deposit=Decimal("0"), notes="vacant",
    )
    assert row.tenant is None


def test_rent_roll_summary_fields():
    s = RentRollSummary(
        total_sqft=10000, occupied_sqft=8000, vacancy_pct=Decimal("20.00"),
        walt_years=Decimal("4.5"), avg_base_rent_psf=Decimal("28.75"),
        total_annual_base_rent=Decimal("230000"),
    )
    assert s.vacancy_pct == Decimal("20.00")


def test_t12_row_fields():
    row = T12Row(
        category="revenue", subcategory="base_rent",
        line_item="Tenant A base rent",
        month_values={"2024-04": Decimal("12000")},
        total=Decimal("144000"),
    )
    assert row.total == Decimal("144000")


def test_t12_summary_fields():
    s = T12Summary(
        gross_revenue=Decimal("1000000"),
        effective_gross_income=Decimal("950000"),
        opex_total=Decimal("400000"), opex_per_sqft=Decimal("4.00"),
        noi=Decimal("550000"), noi_per_sqft=Decimal("5.50"),
    )
    assert s.noi == Decimal("550000")


def test_derived_optional_cap_rate():
    d = Derived(
        noi_margin=Decimal("0.55"), implied_cap_rate_at_ask=None,
        expense_ratio=Decimal("0.40"),
    )
    assert d.implied_cap_rate_at_ask is None


def test_inventory_item_fields():
    it = InventoryItem(
        source_path="C:/tmp/x.pdf", classified_as="rent_roll",
        classification_confidence="high", preview="Tenant | SF | Rent",
    )
    assert it.classified_as == "rent_roll"
