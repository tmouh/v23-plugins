from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from deal_pack._money import parse_decimal, quantize
from deal_pack.models import T12Row, T12Summary


def parse_t12_csv(path: Path) -> list[T12Row]:
    """Parse canonical T-12 CSV with columns: category, subcategory, line_item, total.

    Full monthly breakdowns are preserved elsewhere for the xlsx writer; this
    parser is summary-math-only.
    """
    rows: list[T12Row] = []
    with open(path, newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            rows.append(T12Row(
                category=raw["category"].strip(),
                subcategory=raw["subcategory"].strip(),
                line_item=raw["line_item"].strip(),
                month_values={},
                total=parse_decimal(raw.get("total", "")),
            ))
    return rows


def compute_t12_summary(
    rows: Iterable[T12Row],
    *,
    total_sqft: Decimal,
) -> T12Summary:
    rows = list(rows)

    gross_revenue = sum(
        (r.total for r in rows
         if r.category == "revenue" and r.subcategory != "less_vacancy"),
        start=Decimal("0"),
    )
    less_vacancy = sum(
        (r.total for r in rows
         if r.category == "revenue" and r.subcategory == "less_vacancy"),
        start=Decimal("0"),
    )
    # less_vacancy values are stored as negative, so addition subtracts.
    effective_gross_income = gross_revenue + less_vacancy

    opex_total = sum(
        (r.total for r in rows
         if r.category in ("controllable_opex", "non_controllable_opex")),
        start=Decimal("0"),
    )

    noi = effective_gross_income - opex_total

    if total_sqft == Decimal("0"):
        opex_per_sqft = Decimal("0.00")
        noi_per_sqft = Decimal("0.00")
    else:
        opex_per_sqft = quantize(opex_total / total_sqft)
        noi_per_sqft = quantize(noi / total_sqft)

    return T12Summary(
        gross_revenue=gross_revenue,
        effective_gross_income=effective_gross_income,
        opex_total=opex_total,
        opex_per_sqft=opex_per_sqft,
        noi=noi,
        noi_per_sqft=noi_per_sqft,
    )
