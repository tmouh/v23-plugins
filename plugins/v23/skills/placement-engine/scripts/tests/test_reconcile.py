"""Tests for V23 Placement Engine entity reconciliation (reconcile.py)."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

# The conftest.py already adds scripts/ to sys.path
import reconcile


SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..")


# ---------------------------------------------------------------------------
# 1. normalize_name
# ---------------------------------------------------------------------------

class TestNormalizeName:
    def test_lowercases(self):
        assert reconcile.normalize_name("Canyon Partners") == "canyon"

    def test_strips_llc(self):
        assert reconcile.normalize_name("Acme LLC") == "acme"

    def test_strips_real_estate(self):
        result = reconcile.normalize_name("Sagard Real Estate")
        assert result == "sagard"

    def test_strips_multiple_suffixes(self):
        result = reconcile.normalize_name("Brookfield Capital Group LLC")
        assert result == "brookfield"

    def test_removes_slash_punctuation(self):
        result = reconcile.normalize_name("Sagard/Everwest")
        assert result == "sagard everwest"

    def test_removes_other_punctuation(self):
        result = reconcile.normalize_name("O'Brien, Inc.")
        assert result == "obrien"

    def test_handles_none(self):
        assert reconcile.normalize_name(None) == ""

    def test_handles_empty_string(self):
        assert reconcile.normalize_name("") == ""

    def test_collapses_whitespace(self):
        assert reconcile.normalize_name("  Acme   Capital  ") == "acme"

    def test_strips_lp_suffix(self):
        assert reconcile.normalize_name("Starwood LP") == "starwood"

    def test_strips_inc(self):
        assert reconcile.normalize_name("Blackstone Inc") == "blackstone"

    def test_strips_corp(self):
        assert reconcile.normalize_name("CBRE Corp") == "cbre"

    def test_strips_investments(self):
        assert reconcile.normalize_name("Ares Investments") == "ares"

    def test_strips_advisors(self):
        assert reconcile.normalize_name("Goldman Advisors") == "goldman"

    def test_strips_management(self):
        assert reconcile.normalize_name("Greystar Management") == "greystar"

    def test_strips_fund(self):
        assert reconcile.normalize_name("Apollo Fund") == "apollo"

    def test_strips_holdings(self):
        assert reconcile.normalize_name("Prologis Holdings") == "prologis"

    def test_strips_properties(self):
        assert reconcile.normalize_name("Lincoln Properties") == "lincoln"

    def test_strips_realty(self):
        assert reconcile.normalize_name("Simon Realty") == "simon"

    def test_strips_co(self):
        assert reconcile.normalize_name("Hines Co") == "hines"

    def test_strips_company(self):
        assert reconcile.normalize_name("Hines Company") == "hines"


# ---------------------------------------------------------------------------
# 2. find_duplicates
# ---------------------------------------------------------------------------

class TestFindDuplicates:
    def test_finds_similar_names(self):
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
        ]
        results = reconcile.find_duplicates(investors, threshold=50)
        assert len(results) >= 1
        pair = results[0]
        assert "keep" in pair
        assert "merge" in pair
        assert "score" in pair
        assert "reason" in pair
        assert pair["score"] >= 50
        # One should be id 1, other id 2
        ids = {pair["keep"]["id"], pair["merge"]["id"]}
        assert ids == {1, 2}

    def test_no_false_positives(self):
        investors = [
            {"id": 1, "canonical_name": "Canyon Partners"},
            {"id": 2, "canonical_name": "Brookfield Asset Management"},
        ]
        results = reconcile.find_duplicates(investors, threshold=80)
        assert len(results) == 0

    def test_empty_list(self):
        results = reconcile.find_duplicates([], threshold=80)
        assert results == []

    def test_single_investor(self):
        investors = [{"id": 1, "canonical_name": "Acme Capital"}]
        results = reconcile.find_duplicates(investors, threshold=80)
        assert results == []

    def test_sorted_by_score_descending(self):
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
            {"id": 3, "canonical_name": "Brookfield Capital"},
            {"id": 4, "canonical_name": "Brookfield Capital Group"},
        ]
        results = reconcile.find_duplicates(investors, threshold=50)
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_skips_empty_normalized_names(self):
        investors = [
            {"id": 1, "canonical_name": "LLC"},
            {"id": 2, "canonical_name": "Acme Capital"},
        ]
        results = reconcile.find_duplicates(investors, threshold=80)
        assert len(results) == 0

    def test_skips_none_names(self):
        investors = [
            {"id": 1, "canonical_name": None},
            {"id": 2, "canonical_name": "Acme Capital"},
        ]
        results = reconcile.find_duplicates(investors, threshold=80)
        assert len(results) == 0

    def test_no_duplicate_pairs(self):
        """Should not return both A-B and B-A."""
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
        ]
        results = reconcile.find_duplicates(investors, threshold=50)
        assert len(results) == 1

    def test_result_structure(self):
        investors = [
            {"id": 1, "canonical_name": "Acme Capital"},
            {"id": 2, "canonical_name": "Acme Cap"},
        ]
        results = reconcile.find_duplicates(investors, threshold=50)
        assert len(results) >= 1
        r = results[0]
        assert isinstance(r["keep"]["id"], int)
        assert isinstance(r["keep"]["name"], str)
        assert isinstance(r["merge"]["id"], int)
        assert isinstance(r["merge"]["name"], str)
        assert isinstance(r["score"], int)
        assert r["reason"].startswith("Fuzzy match score:")

    def test_keep_is_lower_id(self):
        """The 'keep' entry should have the lower id."""
        investors = [
            {"id": 5, "canonical_name": "Acme Capital"},
            {"id": 2, "canonical_name": "Acme Cap"},
        ]
        results = reconcile.find_duplicates(investors, threshold=50)
        assert len(results) >= 1
        r = results[0]
        assert r["keep"]["id"] < r["merge"]["id"]


# ---------------------------------------------------------------------------
# 3. CLI: find-duplicates
# ---------------------------------------------------------------------------

class TestCLI:
    def test_find_duplicates_cli(self, tmp_dir):
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
        ]
        input_file = os.path.join(tmp_dir, "investors.json")
        with open(input_file, "w") as f:
            json.dump(investors, f)

        result = subprocess.run(
            [
                sys.executable, os.path.join(SCRIPTS_DIR, "reconcile.py"),
                "find-duplicates", "--input", input_file, "--threshold", "50",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        output = json.loads(result.stdout)
        assert isinstance(output, list)
        assert len(output) >= 1
        assert "keep" in output[0]
        assert "merge" in output[0]

    def test_find_duplicates_cli_default_threshold(self, tmp_dir):
        investors = [
            {"id": 1, "canonical_name": "Canyon Partners"},
            {"id": 2, "canonical_name": "Brookfield Asset Management"},
        ]
        input_file = os.path.join(tmp_dir, "investors.json")
        with open(input_file, "w") as f:
            json.dump(investors, f)

        result = subprocess.run(
            [
                sys.executable, os.path.join(SCRIPTS_DIR, "reconcile.py"),
                "find-duplicates", "--input", input_file,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        output = json.loads(result.stdout)
        assert isinstance(output, list)
        assert len(output) == 0
