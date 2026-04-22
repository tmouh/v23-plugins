from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional, Literal


Classification = Literal[
    "rent_roll", "t12", "lease", "appraisal", "seller_om",
    "photo", "plan", "esa_pca", "market_study", "zoning", "other",
]


@dataclass(frozen=True)
class RentRollRow:
    unit: str
    tenant: Optional[str]
    sqft: int
    lease_start: Optional[date]
    lease_end: Optional[date]
    base_rent_annual: Decimal
    base_rent_psf: Decimal
    recoveries: str
    options: str
    security_deposit: Decimal
    notes: str


@dataclass(frozen=True)
class RentRollSummary:
    total_sqft: int
    occupied_sqft: int
    vacancy_pct: Decimal
    walt_years: Decimal
    avg_base_rent_psf: Decimal
    total_annual_base_rent: Decimal


@dataclass(frozen=True)
class T12Row:
    category: str           # revenue | controllable_opex | non_controllable_opex | below_line
    subcategory: str
    line_item: str
    month_values: dict[str, Decimal]
    total: Decimal


@dataclass(frozen=True)
class T12Summary:
    gross_revenue: Decimal
    effective_gross_income: Decimal
    opex_total: Decimal
    opex_per_sqft: Decimal
    noi: Decimal
    noi_per_sqft: Decimal


@dataclass(frozen=True)
class Derived:
    noi_margin: Decimal
    implied_cap_rate_at_ask: Optional[Decimal]
    expense_ratio: Decimal


@dataclass(frozen=True)
class InventoryItem:
    source_path: str
    classified_as: Classification
    classification_confidence: Literal["high", "medium", "low"]
    preview: str
