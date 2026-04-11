"""Tests for V23 Placement Engine database layer (db.py)."""

import json
import os
import sqlite3
import subprocess
import sys

import pytest

# The conftest.py already adds scripts/ to sys.path
import db


# ---------------------------------------------------------------------------
# 1. get_connection
# ---------------------------------------------------------------------------

class TestGetConnection:
    def test_returns_connection(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_wal_mode(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        mode = conn.execute("PRAGMA journal_mode").fetchone()
        # Row factory means we access by index or key
        assert mode["journal_mode"] == "wal"
        conn.close()

    def test_foreign_keys_on(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        fk = conn.execute("PRAGMA foreign_keys").fetchone()
        assert fk["foreign_keys"] == 1
        conn.close()

    def test_row_factory(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        row = conn.execute("SELECT 1 AS val").fetchone()
        # Should be accessible by key like a dict
        assert row["val"] == 1
        conn.close()


# ---------------------------------------------------------------------------
# 2. create_database
# ---------------------------------------------------------------------------

class TestCreateDatabase:
    def test_creates_tables(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        tables = {
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        assert "investors" in tables
        assert "deals" in tables
        assert "interactions" in tables
        conn.close()

    def test_idempotent(self, tmp_db):
        """Calling create_database twice should not error."""
        db.create_database(tmp_db)
        db.create_database(tmp_db)  # should not raise
        stats = db.get_database_stats(tmp_db)
        assert stats["investor_count"] == 0

    def test_indexes_exist(self, tmp_db):
        db.create_database(tmp_db)
        conn = db.get_connection(tmp_db)
        indexes = {
            r["name"]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
        }
        # At minimum we expect indexes on interaction foreign keys
        assert any("interaction" in idx for idx in indexes)
        conn.close()


# ---------------------------------------------------------------------------
# 3. insert_deal
# ---------------------------------------------------------------------------

class TestInsertDeal:
    def test_basic_insert(self, tmp_db):
        db.create_database(tmp_db)
        deal_id = db.insert_deal(tmp_db, "My Deal", deal_date="2026-01-01")
        assert isinstance(deal_id, int)
        assert deal_id >= 1

    def test_deal_name_unique(self, tmp_db):
        db.create_database(tmp_db)
        db.insert_deal(tmp_db, "My Deal")
        with pytest.raises(sqlite3.IntegrityError):
            db.insert_deal(tmp_db, "My Deal")

    def test_deal_fields_stored(self, tmp_db):
        db.create_database(tmp_db)
        deal_id = db.insert_deal(
            tmp_db, "Alpha Deal",
            deal_date="2026-03-01",
            asset_class="multifamily",
            geography="Tampa, FL",
            strategy="value-add",
            capital_stack_position="LP equity",
            estimated_equity_need="$50M",
        )
        conn = db.get_connection(tmp_db)
        row = conn.execute("SELECT * FROM deals WHERE id=?", (deal_id,)).fetchone()
        assert row["deal_name"] == "Alpha Deal"
        assert row["deal_date"] == "2026-03-01"
        assert row["asset_class"] == "multifamily"
        assert row["geography"] == "Tampa, FL"
        assert row["strategy"] == "value-add"
        assert row["capital_stack_position"] == "LP equity"
        assert row["estimated_equity_need"] == "$50M"
        assert row["deal_status"] == "active"
        conn.close()

    def test_seeded_deals(self, seeded_db):
        stats = db.get_database_stats(seeded_db)
        assert stats["deal_count"] == 2


# ---------------------------------------------------------------------------
# 4. insert_investor
# ---------------------------------------------------------------------------

class TestInsertInvestor:
    def test_basic_insert(self, tmp_db):
        db.create_database(tmp_db)
        inv_id = db.insert_investor(tmp_db, "Acme Capital")
        assert isinstance(inv_id, int)
        assert inv_id >= 1

    def test_canonical_name_unique(self, tmp_db):
        db.create_database(tmp_db)
        db.insert_investor(tmp_db, "Acme Capital")
        with pytest.raises(sqlite3.IntegrityError):
            db.insert_investor(tmp_db, "Acme Capital")

    def test_aliases_stored_as_json(self, tmp_db):
        db.create_database(tmp_db)
        inv_id = db.insert_investor(
            tmp_db, "Acme Capital", aliases=["Acme", "ACME LP"]
        )
        conn = db.get_connection(tmp_db)
        row = conn.execute(
            "SELECT aliases FROM investors WHERE id=?", (inv_id,)
        ).fetchone()
        aliases = json.loads(row["aliases"])
        assert aliases == ["Acme", "ACME LP"]
        conn.close()

    def test_default_aliases_empty_list(self, tmp_db):
        db.create_database(tmp_db)
        inv_id = db.insert_investor(tmp_db, "Gamma Group")
        conn = db.get_connection(tmp_db)
        row = conn.execute(
            "SELECT aliases FROM investors WHERE id=?", (inv_id,)
        ).fetchone()
        aliases = json.loads(row["aliases"])
        assert aliases == []
        conn.close()

    def test_extra_fields(self, tmp_db):
        db.create_database(tmp_db)
        inv_id = db.insert_investor(
            tmp_db, "Acme Capital",
            coverage_owner="HC",
            contact_name="John",
            email="john@acme.com",
            phone="555-1234",
            new_contact="Jane",
            new_contact_role="VP",
            new_contact_email="jane@acme.com",
        )
        conn = db.get_connection(tmp_db)
        row = conn.execute(
            "SELECT * FROM investors WHERE id=?", (inv_id,)
        ).fetchone()
        assert row["coverage_owner"] == "HC"
        assert row["contact_name"] == "John"
        assert row["email"] == "john@acme.com"
        assert row["phone"] == "555-1234"
        assert row["new_contact"] == "Jane"
        assert row["new_contact_role"] == "VP"
        assert row["new_contact_email"] == "jane@acme.com"
        conn.close()

    def test_seeded_investors(self, seeded_db):
        stats = db.get_database_stats(seeded_db)
        assert stats["investor_count"] == 3


# ---------------------------------------------------------------------------
# 5. find_investor
# ---------------------------------------------------------------------------

class TestFindInvestor:
    def test_find_by_canonical_name(self, seeded_db):
        result = db.find_investor(seeded_db, "Acme Capital")
        assert result is not None
        assert result["canonical_name"] == "Acme Capital"

    def test_find_by_alias(self, seeded_db):
        result = db.find_investor(seeded_db, "Acme")
        assert result is not None
        assert result["canonical_name"] == "Acme Capital"

    def test_find_by_alias_beta(self, seeded_db):
        result = db.find_investor(seeded_db, "Beta LP")
        assert result is not None
        assert result["canonical_name"] == "Beta Partners"

    def test_not_found(self, seeded_db):
        result = db.find_investor(seeded_db, "Nonexistent Fund")
        assert result is None

    def test_returns_dict(self, seeded_db):
        result = db.find_investor(seeded_db, "Gamma Group")
        assert isinstance(result, dict)
        assert "id" in result
        assert "canonical_name" in result


# ---------------------------------------------------------------------------
# 6. insert_interaction
# ---------------------------------------------------------------------------

class TestInsertInteraction:
    def test_basic_insert(self, seeded_db):
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Reviewing", coverage_code="HC",
        )
        assert isinstance(iid, int)
        assert iid >= 1

    def test_unique_investor_deal(self, seeded_db):
        db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Reviewing")
        with pytest.raises(sqlite3.IntegrityError):
            db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Pass")

    def test_interaction_fields(self, seeded_db):
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Reviewing", coverage_code="HC",
            raw_comments="Interested", old_comments="Prior note",
            date_last_contact="2026-01-15", date_om_sent="2026-01-10",
        )
        conn = db.get_connection(seeded_db)
        row = conn.execute(
            "SELECT * FROM interactions WHERE id=?", (iid,)
        ).fetchone()
        assert row["status"] == "Reviewing"
        assert row["coverage_code"] == "HC"
        assert row["raw_comments"] == "Interested"
        assert row["old_comments"] == "Prior note"
        assert row["date_last_contact"] == "2026-01-15"
        assert row["date_om_sent"] == "2026-01-10"
        conn.close()

    def test_foreign_key_enforcement(self, seeded_db):
        """Inserting interaction for nonexistent investor should fail."""
        with pytest.raises(sqlite3.IntegrityError):
            db.insert_interaction(seeded_db, investor_id=999, deal_id=1, status="Sent")


# ---------------------------------------------------------------------------
# 7. get_investor_batch
# ---------------------------------------------------------------------------

class TestGetInvestorBatch:
    def test_returns_list(self, seeded_db):
        batch = db.get_investor_batch(seeded_db, offset=0, limit=10)
        assert isinstance(batch, list)
        assert len(batch) == 3

    def test_pagination(self, seeded_db):
        batch = db.get_investor_batch(seeded_db, offset=0, limit=2)
        assert len(batch) == 2
        batch2 = db.get_investor_batch(seeded_db, offset=2, limit=2)
        assert len(batch2) == 1

    def test_investor_dict_shape(self, seeded_db):
        batch = db.get_investor_batch(seeded_db, offset=0, limit=1)
        inv = batch[0]
        assert "id" in inv
        assert "canonical_name" in inv
        assert "interactions" in inv
        assert isinstance(inv["interactions"], list)

    def test_interactions_include_deal_metadata(self, seeded_db):
        """When investor has interactions, they include deal fields."""
        db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Reviewing", coverage_code="HC",
        )
        batch = db.get_investor_batch(seeded_db, offset=0, limit=1)
        inv = batch[0]
        assert len(inv["interactions"]) == 1
        inter = inv["interactions"][0]
        assert "deal_name" in inter
        assert inter["deal_name"] == "Test Deal Alpha"
        assert "deal_date" in inter
        assert "asset_class" in inter
        assert "geography" in inter
        assert "strategy" in inter
        assert "capital_stack_position" in inter

    def test_order_investors_by_id(self, seeded_db):
        batch = db.get_investor_batch(seeded_db, offset=0, limit=10)
        ids = [inv["id"] for inv in batch]
        assert ids == sorted(ids)

    def test_interactions_ordered_by_deal_date_desc(self, seeded_db):
        # Investor 1 interacts with deal 1 (2026-01-01) and deal 2 (2025-06-15)
        db.insert_interaction(seeded_db, investor_id=1, deal_id=2, status="Sent")
        db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Reviewing")
        batch = db.get_investor_batch(seeded_db, offset=0, limit=1)
        dates = [i["deal_date"] for i in batch[0]["interactions"]]
        assert dates == ["2026-01-01", "2025-06-15"]

    def test_empty_interactions_list(self, seeded_db):
        batch = db.get_investor_batch(seeded_db, offset=0, limit=10)
        # No interactions inserted yet, each investor should have empty list
        for inv in batch:
            assert inv["interactions"] == []


# ---------------------------------------------------------------------------
# 8. merge_investors
# ---------------------------------------------------------------------------

class TestMergeInvestors:
    def test_merge_moves_interactions(self, seeded_db):
        db.insert_interaction(seeded_db, investor_id=2, deal_id=1, status="Pass")
        db.merge_investors(seeded_db, keep_id=1, merge_id=2)
        # Interaction should now belong to investor 1
        conn = db.get_connection(seeded_db)
        rows = conn.execute(
            "SELECT * FROM interactions WHERE investor_id=?", (1,)
        ).fetchall()
        assert len(rows) == 1
        assert rows[0]["deal_id"] == 1
        conn.close()

    def test_merge_deletes_merged_investor(self, seeded_db):
        db.merge_investors(seeded_db, keep_id=1, merge_id=2)
        conn = db.get_connection(seeded_db)
        row = conn.execute(
            "SELECT * FROM investors WHERE id=?", (2,)
        ).fetchone()
        assert row is None
        conn.close()

    def test_merge_adds_alias(self, seeded_db):
        db.merge_investors(seeded_db, keep_id=1, merge_id=2)
        inv = db.find_investor(seeded_db, "Beta Partners")
        assert inv is not None
        assert inv["canonical_name"] == "Acme Capital"

    def test_merge_handles_duplicate_deal(self, seeded_db):
        """Both investors have interaction with same deal; merge keeps richer data."""
        db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Sent", raw_comments="",
        )
        db.insert_interaction(
            seeded_db, investor_id=2, deal_id=1,
            status="Reviewing", raw_comments="Very interested",
            date_last_contact="2026-02-01",
        )
        db.merge_investors(seeded_db, keep_id=1, merge_id=2)
        conn = db.get_connection(seeded_db)
        rows = conn.execute(
            "SELECT * FROM interactions WHERE investor_id=? AND deal_id=?",
            (1, 1),
        ).fetchall()
        assert len(rows) == 1
        # Should keep the richer data (more non-empty fields or more recent)
        row = rows[0]
        assert row["raw_comments"] == "Very interested"
        conn.close()

    def test_merge_updates_count(self, seeded_db):
        db.merge_investors(seeded_db, keep_id=1, merge_id=2)
        stats = db.get_database_stats(seeded_db)
        assert stats["investor_count"] == 2


# ---------------------------------------------------------------------------
# 9. get_database_stats
# ---------------------------------------------------------------------------

class TestGetDatabaseStats:
    def test_empty_db(self, tmp_db):
        db.create_database(tmp_db)
        stats = db.get_database_stats(tmp_db)
        assert stats == {
            "investor_count": 0,
            "deal_count": 0,
            "interaction_count": 0,
        }

    def test_seeded_counts(self, seeded_db):
        stats = db.get_database_stats(seeded_db)
        assert stats["investor_count"] == 3
        assert stats["deal_count"] == 2
        assert stats["interaction_count"] == 0

    def test_with_interactions(self, seeded_db):
        db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Sent")
        db.insert_interaction(seeded_db, investor_id=2, deal_id=1, status="Pass")
        stats = db.get_database_stats(seeded_db)
        assert stats["interaction_count"] == 2


# ---------------------------------------------------------------------------
# 10. update_interaction
# ---------------------------------------------------------------------------

class TestUpdateInteraction:
    def test_update_status(self, seeded_db):
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1, status="Sent",
        )
        db.update_interaction(seeded_db, iid, status="Reviewing")
        conn = db.get_connection(seeded_db)
        row = conn.execute(
            "SELECT status FROM interactions WHERE id=?", (iid,)
        ).fetchone()
        assert row["status"] == "Reviewing"
        conn.close()

    def test_update_multiple_fields(self, seeded_db):
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1, status="Sent",
        )
        db.update_interaction(
            seeded_db, iid,
            status="Pass",
            raw_comments="Not interested",
            date_last_contact="2026-03-01",
        )
        conn = db.get_connection(seeded_db)
        row = conn.execute(
            "SELECT * FROM interactions WHERE id=?", (iid,)
        ).fetchone()
        assert row["status"] == "Pass"
        assert row["raw_comments"] == "Not interested"
        assert row["date_last_contact"] == "2026-03-01"
        conn.close()

    def test_update_disallowed_field(self, seeded_db):
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1, status="Sent",
        )
        with pytest.raises(ValueError):
            db.update_interaction(seeded_db, iid, investor_id=999)

    def test_update_allowed_fields_only(self, seeded_db):
        """All six allowed fields should be updatable."""
        iid = db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1, status="Sent",
        )
        db.update_interaction(
            seeded_db, iid,
            status="Reviewing",
            coverage_code="MS",
            raw_comments="notes",
            old_comments="old notes",
            date_last_contact="2026-04-01",
            date_om_sent="2026-03-15",
        )
        conn = db.get_connection(seeded_db)
        row = conn.execute(
            "SELECT * FROM interactions WHERE id=?", (iid,)
        ).fetchone()
        assert row["status"] == "Reviewing"
        assert row["coverage_code"] == "MS"
        assert row["raw_comments"] == "notes"
        assert row["old_comments"] == "old notes"
        assert row["date_last_contact"] == "2026-04-01"
        assert row["date_om_sent"] == "2026-03-15"
        conn.close()


# ---------------------------------------------------------------------------
# 11. update_deal_stats
# ---------------------------------------------------------------------------

class TestUpdateDealStats:
    def test_recalculates_stats(self, seeded_db):
        db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Pass")
        db.insert_interaction(seeded_db, investor_id=2, deal_id=1, status="Reviewing")
        db.insert_interaction(seeded_db, investor_id=3, deal_id=1, status="Sent")
        db.update_deal_stats(seeded_db, deal_id=1)
        conn = db.get_connection(seeded_db)
        row = conn.execute("SELECT * FROM deals WHERE id=?", (1,)).fetchone()
        assert row["total_contacted"] == 3
        assert row["pass_count"] == 1
        assert abs(row["pass_rate"] - (1 / 3)) < 0.01
        assert row["reviewing_count"] == 1
        conn.close()

    def test_zero_interactions(self, seeded_db):
        db.update_deal_stats(seeded_db, deal_id=1)
        conn = db.get_connection(seeded_db)
        row = conn.execute("SELECT * FROM deals WHERE id=?", (1,)).fetchone()
        assert row["total_contacted"] == 0
        assert row["pass_count"] == 0
        assert row["pass_rate"] == 0.0
        assert row["reviewing_count"] == 0
        conn.close()


# ---------------------------------------------------------------------------
# 12. get_deal_interactions
# ---------------------------------------------------------------------------

class TestGetDealInteractions:
    def test_returns_list(self, seeded_db):
        result = db.get_deal_interactions(seeded_db, deal_id=1)
        assert isinstance(result, list)

    def test_includes_investor_name(self, seeded_db):
        db.insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Reviewing", coverage_code="HC",
        )
        result = db.get_deal_interactions(seeded_db, deal_id=1)
        assert len(result) == 1
        assert result[0]["investor_name"] == "Acme Capital"
        assert result[0]["status"] == "Reviewing"

    def test_empty_deal(self, seeded_db):
        result = db.get_deal_interactions(seeded_db, deal_id=2)
        assert result == []

    def test_multiple_interactions(self, seeded_db):
        db.insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Reviewing")
        db.insert_interaction(seeded_db, investor_id=2, deal_id=1, status="Pass")
        db.insert_interaction(seeded_db, investor_id=3, deal_id=1, status="Sent")
        result = db.get_deal_interactions(seeded_db, deal_id=1)
        assert len(result) == 3
        names = {r["investor_name"] for r in result}
        assert names == {"Acme Capital", "Beta Partners", "Gamma Group"}


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..")


class TestCLI:
    """Test db.py CLI subcommands."""

    def _run(self, args, db_path):
        cmd = [sys.executable, os.path.join(SCRIPTS_DIR, "db.py")] + args + [
            "--db-path", db_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result

    def test_cli_init(self, tmp_db):
        r = self._run(["init"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output["status"] == "ok"

    def test_cli_insert_deal(self, tmp_db):
        self._run(["init"], tmp_db)
        r = self._run([
            "insert-deal", "--deal-name", "CLI Deal",
            "--deal-date", "2026-01-01",
            "--asset-class", "industrial",
        ], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert "id" in output

    def test_cli_insert_investor(self, tmp_db):
        self._run(["init"], tmp_db)
        r = self._run([
            "insert-investor", "--canonical-name", "CLI Investor",
            "--aliases", "CLI", "CLII",
            "--coverage-owner", "HC",
        ], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert "id" in output

    def test_cli_find_investor(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run([
            "insert-investor", "--canonical-name", "CLI Investor",
            "--aliases", "CLI",
        ], tmp_db)
        r = self._run(["find-investor", "--name", "CLI"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output["canonical_name"] == "CLI Investor"

    def test_cli_find_investor_not_found(self, tmp_db):
        self._run(["init"], tmp_db)
        r = self._run(["find-investor", "--name", "Nobody"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output is None or output == {}

    def test_cli_stats(self, tmp_db):
        self._run(["init"], tmp_db)
        r = self._run(["stats"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert "investor_count" in output

    def test_cli_insert_interaction(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-deal", "--deal-name", "D1"], tmp_db)
        self._run([
            "insert-investor", "--canonical-name", "Inv1",
        ], tmp_db)
        r = self._run([
            "insert-interaction",
            "--investor-id", "1", "--deal-id", "1",
            "--status", "Reviewing",
        ], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert "id" in output

    def test_cli_get_batch(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-investor", "--canonical-name", "Inv1"], tmp_db)
        r = self._run(["get-batch", "--offset", "0", "--limit", "10"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert isinstance(output, list)
        assert len(output) == 1

    def test_cli_get_batch_strip_pii(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run([
            "insert-investor", "--canonical-name", "Inv1",
            "--contact-name", "Secret Person",
            "--email", "secret@example.com",
            "--phone", "555-0000",
        ], tmp_db)
        r = self._run([
            "get-batch", "--offset", "0", "--limit", "10", "--strip-pii",
        ], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        inv = output[0]
        pii_fields = [
            "contact_name", "email", "phone",
            "new_contact", "new_contact_role", "new_contact_email",
        ]
        for field in pii_fields:
            assert field not in inv

    def test_cli_merge(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-investor", "--canonical-name", "Keep"], tmp_db)
        self._run(["insert-investor", "--canonical-name", "Remove"], tmp_db)
        r = self._run(["merge", "--keep-id", "1", "--merge-id", "2"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output["status"] == "ok"

    def test_cli_get_deal_interactions(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-deal", "--deal-name", "D1"], tmp_db)
        self._run(["insert-investor", "--canonical-name", "Inv1"], tmp_db)
        self._run([
            "insert-interaction",
            "--investor-id", "1", "--deal-id", "1",
            "--status", "Pass",
        ], tmp_db)
        r = self._run(["get-deal-interactions", "--deal-id", "1"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert isinstance(output, list)
        assert len(output) == 1

    def test_cli_update_interaction(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-deal", "--deal-name", "D1"], tmp_db)
        self._run(["insert-investor", "--canonical-name", "Inv1"], tmp_db)
        self._run([
            "insert-interaction",
            "--investor-id", "1", "--deal-id", "1",
            "--status", "Sent",
        ], tmp_db)
        r = self._run([
            "update-interaction", "--interaction-id", "1",
            "--status", "Pass",
            "--raw-comments", "Not interested",
        ], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output["status"] == "ok"

    def test_cli_update_deal_stats(self, tmp_db):
        self._run(["init"], tmp_db)
        self._run(["insert-deal", "--deal-name", "D1"], tmp_db)
        r = self._run(["update-deal-stats", "--deal-id", "1"], tmp_db)
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert output["status"] == "ok"
