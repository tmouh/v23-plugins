from __future__ import annotations

import csv
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from deal_pack._money import parse_decimal, quantize
from deal_pack.models import RentRollRow, RentRollSummary


_DAYS_PER_YEAR = Decimal("365.25")


def _parse_int(value: str) -> int:
    value = (value or "").strip().replace(",", "")
    if not value:
        return 0
    return int(Decimal(value))


def _parse_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_optional_str(value: str) -> str | None:
    value = (value or "").strip()
    return value or None


def parse_rent_roll_csv(path: Path) -> list[RentRollRow]:
    """Parse a canonical rent-roll CSV (produced by the LLM extractor)."""
    rows: list[RentRollRow] = []
    with open(path, newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            rows.append(RentRollRow(
                unit=raw["unit"].strip(),
                tenant=_parse_optional_str(raw.get("tenant", "")),
                sqft=_parse_int(raw.get("sqft", "")),
                lease_start=_parse_date(raw.get("lease_start", "")),
                lease_end=_parse_date(raw.get("lease_end", "")),
                base_rent_annual=parse_decimal(raw.get("base_rent_annual", "")),
                base_rent_psf=parse_decimal(raw.get("base_rent_psf", "")),
                recoveries=(raw.get("recoveries") or "").strip(),
                options=(raw.get("options") or "").strip(),
                security_deposit=parse_decimal(raw.get("security_deposit", "")),
                notes=(raw.get("notes") or "").strip(),
            ))
    return rows


def _is_occupied(row: RentRollRow, reference_date: date) -> bool:
    if row.tenant is None:
        return False
    if row.lease_end is None:
        return False
    return row.lease_end >= reference_date


def compute_rent_roll_summary(
    rows: Iterable[RentRollRow],
    *,
    reference_date: date,
) -> RentRollSummary:
    rows = list(rows)
    total_sqft = sum(r.sqft for r in rows)
    occupied_rows = [r for r in rows if _is_occupied(r, reference_date)]
    occupied_sqft = sum(r.sqft for r in occupied_rows)

    if total_sqft == 0:
        vacancy_pct = Decimal("0.00")
    else:
        vacancy_pct = quantize(
            Decimal(total_sqft - occupied_sqft) * Decimal("100") / Decimal(total_sqft)
        )

    if occupied_sqft == 0:
        walt_years = Decimal("0.00")
    else:
        weighted_days = Decimal("0")
        for r in occupied_rows:
            remaining_days = max((r.lease_end - reference_date).days, 0)
            weighted_days += Decimal(remaining_days) * Decimal(r.sqft)
        walt_years = quantize(
            (weighted_days / Decimal(occupied_sqft)) / _DAYS_PER_YEAR
        )

    total_annual_base_rent = sum(
        (r.base_rent_annual for r in occupied_rows), start=Decimal("0")
    )

    if occupied_sqft == 0:
        avg_base_rent_psf = Decimal("0.00")
    else:
        avg_base_rent_psf = quantize(
            total_annual_base_rent / Decimal(occupied_sqft)
        )

    return RentRollSummary(
        total_sqft=total_sqft,
        occupied_sqft=occupied_sqft,
        vacancy_pct=vacancy_pct,
        walt_years=walt_years,
        avg_base_rent_psf=avg_base_rent_psf,
        total_annual_base_rent=total_annual_base_rent,
    )
