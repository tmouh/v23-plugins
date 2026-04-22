from decimal import Decimal

from deal_pack.derived import compute_derived
from deal_pack.models import RentRollSummary, T12Summary


def _rent_roll(total_sqft=100000, total_annual_base_rent=Decimal("800000")):
    return RentRollSummary(
        total_sqft=total_sqft, occupied_sqft=total_sqft,
        vacancy_pct=Decimal("0.00"), walt_years=Decimal("5.00"),
        avg_base_rent_psf=Decimal("8.00"),
        total_annual_base_rent=total_annual_base_rent,
    )


def _t12(egi=Decimal("950000"), opex=Decimal("330000"), noi=Decimal("620000")):
    return T12Summary(
        gross_revenue=Decimal("1000000"),
        effective_gross_income=egi,
        opex_total=opex, opex_per_sqft=Decimal("3.30"),
        noi=noi, noi_per_sqft=Decimal("6.20"),
    )


def test_derived_no_ask_price():
    d = compute_derived(_rent_roll(), _t12(), ask_price=None)
    # noi_margin = 620000 / 950000 = 0.6526... -> 0.65
    assert d.noi_margin == Decimal("0.65")
    assert d.implied_cap_rate_at_ask is None
    # expense_ratio = 330000 / 950000 = 0.3473... -> 0.35
    assert d.expense_ratio == Decimal("0.35")


def test_derived_with_ask_price():
    d = compute_derived(_rent_roll(), _t12(), ask_price=Decimal("10000000"))
    # cap = 620000 / 10000000 = 0.062 -> 6.20%
    assert d.implied_cap_rate_at_ask == Decimal("0.062")


def test_derived_safe_on_zero_egi():
    t12_zero = T12Summary(
        gross_revenue=Decimal("0"), effective_gross_income=Decimal("0"),
        opex_total=Decimal("0"), opex_per_sqft=Decimal("0.00"),
        noi=Decimal("0"), noi_per_sqft=Decimal("0.00"),
    )
    d = compute_derived(_rent_roll(), t12_zero, ask_price=None)
    assert d.noi_margin == Decimal("0.00")
    assert d.expense_ratio == Decimal("0.00")


def test_derived_negative_noi():
    """Contract: a property operating at a loss produces negative NOI margin and
    negative implied cap rate. compute_derived does not raise or clamp."""
    t12_loss = T12Summary(
        gross_revenue=Decimal("1000000"),
        effective_gross_income=Decimal("950000"),
        opex_total=Decimal("1100000"),
        opex_per_sqft=Decimal("11.00"),
        noi=Decimal("-150000"),
        noi_per_sqft=Decimal("-1.50"),
    )
    d = compute_derived(_rent_roll(), t12_loss, ask_price=Decimal("10000000"))
    # noi_margin = -150000 / 950000 = -0.1578... -> -0.16
    assert d.noi_margin == Decimal("-0.16")
    # expense_ratio = 1100000 / 950000 = 1.1578... -> 1.16
    assert d.expense_ratio == Decimal("1.16")
    # implied_cap_rate = -150000 / 10000000 = -0.015
    assert d.implied_cap_rate_at_ask == Decimal("-0.015")
