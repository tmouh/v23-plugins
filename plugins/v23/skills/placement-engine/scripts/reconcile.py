"""Entity reconciliation for V23 Placement Engine.

Fuzzy-matches investor names to find potential duplicates.
"""

import argparse
import json
import re
import sys

from rapidfuzz import fuzz


# Corporate suffixes to strip (order matters: multi-word before single-word)
_SUFFIXES = [
    "real estate",
    "capital",
    "partners",
    "investments",
    "advisors",
    "management",
    "holdings",
    "properties",
    "company",
    "group",
    "realty",
    "fund",
    "corp",
    "inc",
    "llc",
    "lp",
    "co",
]

# Punctuation characters to remove
_PUNCT_RE = re.compile(r"[,.'\"()\-]")
# Slash replaced with space (so "Sagard/Everwest" -> "Sagard Everwest")
_SLASH_RE = re.compile(r"/")
# Collapse whitespace
_WS_RE = re.compile(r"\s+")


def normalize_name(name: str | None) -> str:
    """Normalize an investor name for comparison.

    - Lowercase
    - Remove punctuation: , . ' " ( ) / -
    - Strip common corporate suffixes
    - Collapse whitespace
    - None -> "", empty -> ""
    """
    if name is None:
        return ""
    s = str(name).lower()
    # Replace slash with space before removing other punctuation
    s = _SLASH_RE.sub(" ", s)
    # Remove punctuation
    s = _PUNCT_RE.sub("", s)
    # Collapse whitespace
    s = _WS_RE.sub(" ", s).strip()
    # Strip suffixes iteratively (multiple passes to catch stacked suffixes)
    changed = True
    while changed:
        changed = False
        for suffix in _SUFFIXES:
            pattern = re.compile(r"\s+" + re.escape(suffix) + r"$")
            new_s = pattern.sub("", s)
            if new_s != s:
                s = new_s.strip()
                changed = True
    return s


def find_duplicates(
    investors: list[dict], threshold: int = 80
) -> list[dict]:
    """Find potential duplicate investor names using fuzzy matching.

    Args:
        investors: list of dicts with 'id' and 'canonical_name'.
        threshold: minimum fuzzy match score (0-100) to consider a pair.

    Returns:
        Sorted list (by score desc) of proposal dicts:
        [{"keep": {"id": N, "name": "..."}, "merge": {"id": M, "name": "..."},
          "score": int, "reason": "Fuzzy match score: X/100"}, ...]
    """
    # Pre-normalize all names
    normalized = []
    for inv in investors:
        norm = normalize_name(inv.get("canonical_name"))
        normalized.append((inv["id"], inv["canonical_name"], norm))

    proposals = []
    n = len(normalized)
    for i in range(n):
        id_a, name_a, norm_a = normalized[i]
        if not norm_a:
            continue
        for j in range(i + 1, n):
            id_b, name_b, norm_b = normalized[j]
            if not norm_b:
                continue
            score = int(fuzz.token_sort_ratio(norm_a, norm_b))
            if score >= threshold:
                # "keep" gets the lower id
                if id_a <= id_b:
                    keep = {"id": id_a, "name": name_a}
                    merge = {"id": id_b, "name": name_b}
                else:
                    keep = {"id": id_b, "name": name_b}
                    merge = {"id": id_a, "name": name_a}
                proposals.append(
                    {
                        "keep": keep,
                        "merge": merge,
                        "score": score,
                        "reason": f"Fuzzy match score: {score}/100",
                    }
                )

    # Sort by score descending
    proposals.sort(key=lambda p: p["score"], reverse=True)
    return proposals


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_find_duplicates(args):
    with open(args.input, "r") as f:
        investors = json.load(f)
    results = find_duplicates(investors, threshold=args.threshold)
    json.dump(results, sys.stdout, indent=2)
    print()  # trailing newline


def main():
    parser = argparse.ArgumentParser(
        description="Entity reconciliation for V23 Placement Engine"
    )
    sub = parser.add_subparsers(dest="command")

    find_dup = sub.add_parser(
        "find-duplicates",
        help="Find potential duplicate investor names",
    )
    find_dup.add_argument(
        "--input", required=True, help="Path to JSON file with investor list"
    )
    find_dup.add_argument(
        "--threshold",
        type=int,
        default=80,
        help="Minimum fuzzy match score (0-100, default 80)",
    )
    find_dup.set_defaults(func=_cli_find_duplicates)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
