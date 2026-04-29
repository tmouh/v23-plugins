from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Iterable


_BASENAME_BY_CLASS = {
    "rent_roll": "rent-roll",
    "t12": "t12",
    "appraisal": "appraisal",
    "seller_om": "seller-om",
    "plan": "plan",
    "esa_pca": "third-party-report",
    "market_study": "market-study",
    "zoning": "zoning",
    # lease, photo, other handled specially
}


def _slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "file"


def _next_unique_path(parent: Path, base: str, suffix: str) -> Path:
    """Return first non-colliding path. Counter starts at 2 (macOS Finder-style)."""
    candidate = parent / f"{base}{suffix}"
    i = 2
    while candidate.exists():
        candidate = parent / f"{base}-{i}{suffix}"
        i += 1
    return candidate


def _clear_sources(sources: Path) -> None:
    """Remove all files and subfolders inside `sources` but keep `sources` itself."""
    if not sources.exists():
        return
    for child in sources.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def copy_sources(
    pack_root: Path,
    classifications: Iterable[dict],
) -> list[str]:
    """Copy originals into `<pack_root>/sources/` with predictable names.

    Idempotent: clears `<pack_root>/sources/` contents at start of every run,
    so repeated invocations with the same classifications produce the same
    folder layout rather than accumulating numbered duplicates.

    Routing policy:
      - `classified_as == "lease"`  → `sources/leases/<slug>{suffix}` (any confidence)
      - `classified_as == "photo"`  → `sources/photos/<slug>{suffix}` (any confidence)
      - `classified_as == "other"` OR `classification_confidence == "low"`
        (for all non-lease/non-photo classes) → `sources/unclassified/<slug>{suffix}`
      - Named classes with high/medium confidence → `sources/<basename>{suffix}`
        where basenames are: rent-roll, t12, appraisal, seller-om, plan,
        third-party-report, market-study, zoning.
      - Unknown `classified_as` → `sources/unclassified/<slug>{suffix}`.

    Within a single run, collisions on the same destination name get a `-2`, `-3`, …
    suffix (macOS Finder-style).

    Returns a list of warning strings for any source files that could not be copied
    (missing file, permission error, etc). An empty list means every file copied cleanly.
    """
    pack_root = Path(pack_root)
    sources = pack_root / "sources"
    sources.mkdir(parents=True, exist_ok=True)
    _clear_sources(sources)

    leases_dir = sources / "leases"
    unclassified_dir = sources / "unclassified"
    photos_dir = sources / "photos"

    warnings: list[str] = []

    for entry in classifications:
        src = Path(entry["source_path"])
        cls = entry.get("classified_as", "other")
        confidence = entry.get("classification_confidence", "low")
        suffix = src.suffix.lower()

        if cls == "lease":
            leases_dir.mkdir(exist_ok=True)
            target = _next_unique_path(leases_dir, _slugify(src.stem), suffix)
        elif cls == "photo":
            photos_dir.mkdir(exist_ok=True)
            target = _next_unique_path(photos_dir, _slugify(src.stem), suffix)
        elif cls == "other" or confidence == "low":
            unclassified_dir.mkdir(exist_ok=True)
            target = _next_unique_path(unclassified_dir, _slugify(src.stem), suffix)
        elif cls in _BASENAME_BY_CLASS:
            target = _next_unique_path(sources, _BASENAME_BY_CLASS[cls], suffix)
        else:
            unclassified_dir.mkdir(exist_ok=True)
            target = _next_unique_path(unclassified_dir, _slugify(src.stem), suffix)

        try:
            shutil.copy2(src, target)
        except OSError as e:
            warnings.append(f"{src}: {e}")

    return warnings
