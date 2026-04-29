from __future__ import annotations

from decimal import Decimal
from typing import Optional

from deal_pack._money import quantize
from deal_pack.models import RentRollSummary, T12Summary, Derived


def compute_derived(
    rent_roll: RentRollSummary,
    t12: T12Summary,
    *,
    ask_price: Optional[Decimal],
) -> Derived:
    egi = t12.effective_gross_income

    if egi == 0:
        noi_margin = Decimal("0.00")
        expense_ratio = Decimal("0.00")
    else:
        noi_margin = quantize(t12.noi / egi)
        expense_ratio = quantize(t12.opex_total / egi)

    if ask_price is None or ask_price == 0:
        implied_cap_rate = None
    else:
        implied_cap_rate = quantize(t12.noi / ask_price, places=3)

    return Derived(
        noi_margin=noi_margin,
        implied_cap_rate_at_ask=implied_cap_rate,
        expense_ratio=expense_ratio,
    )
