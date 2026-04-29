from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


def parse_decimal(value: str) -> Decimal:
    """Parse a string value into a Decimal, stripping commas and dollar signs.

    Empty or whitespace-only input returns Decimal("0").
    """
    value = (value or "").strip()
    if not value:
        return Decimal("0")
    return Decimal(value.replace(",", "").replace("$", ""))


def quantize(value: Decimal, places: int = 2) -> Decimal:
    """Quantize a Decimal to the given number of decimal places using ROUND_HALF_UP."""
    exp = Decimal("1").scaleb(-places)
    return value.quantize(exp, rounding=ROUND_HALF_UP)
