# V23 Placement Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill backed by a local SQLite database that generates ranked investor placement lists for commercial real estate capital raises, drawing on historical placement data.

**Architecture:** Python utility scripts handle all data operations (parsing xlsx, SQLite CRUD, fuzzy matching, xlsx export). A SKILL.md orchestrates the workflow: bootstrap ingests ~70 historical placement files into a local SQLite "living memory," then at query time Claude reads raw investor interaction history in batches and applies matching intelligence to rank investors for a new deal. Personal contact info stays local; only firm names and interaction history go through the Claude API.

**Tech Stack:** Python 3 (invoked as `python`), SQLite3 (stdlib), openpyxl (xlsx read/write), rapidfuzz (entity reconciliation), pytest (testing). Claude Code skill (SKILL.md + scripts/).

---

## Path Definitions

These paths are used throughout the plan. The engineer should verify them at the start.

| Variable | Value |
|----------|-------|
| `V23_SKILLS` | `C:/Users/tmouh/AppData/Roaming/Claude/local-agent-mode-sessions/a3a9017a-f820-4de8-97dc-b36a476243c0/552560ee-3dfe-40eb-96b4-15c3f6bf4334/rpm/plugin_01MgSv2u4RQoK99JK9yxGrSX/skills` |
| `SKILL_DIR` | `${V23_SKILLS}/placement-engine` |
| `SCRIPTS` | `${SKILL_DIR}/scripts` |
| `TESTS` | `${SCRIPTS}/tests` |
| `DB_PATH` | `~/.v23/placement-engine/placement.db` (runtime default) |

**Dynamic discovery** (if the session ID has changed):
```bash
COMP_SEARCH=$(find "$APPDATA/Claude" -path "*/skills/comp-search/SKILL.md" 2>/dev/null | head -1)
V23_SKILLS=$(dirname "$(dirname "$COMP_SEARCH")")
echo "V23 skills directory: $V23_SKILLS"
```

---

## File Structure

```
placement-engine/
├── SKILL.md                          # Skill definition — orchestration instructions for Claude
└── scripts/
    ├── requirements.txt              # Python dependencies
    ├── db.py                         # SQLite database schema + CRUD + CLI
    ├── parse_xlsx.py                 # Parse placement xlsx files (Format A, B, edge) + CLI
    ├── reconcile.py                  # Fuzzy entity name matching + CLI
    ├── export_xlsx.py                # Generate placement list xlsx + CLI
    └── tests/
        ├── conftest.py               # Shared pytest fixtures (temp dirs, test DBs, sample xlsx)
        ├── test_db.py                # Tests for db.py
        ├── test_parse_xlsx.py        # Tests for parse_xlsx.py
        ├── test_reconcile.py         # Tests for reconcile.py
        └── test_export_xlsx.py       # Tests for export_xlsx.py
```

**Responsibilities:**
- `db.py` — All SQLite operations. CLI subcommands for init, insert, query, merge, stats, update. Outputs JSON to stdout.
- `parse_xlsx.py` — Reads placement xlsx files, auto-detects format (A/B/edge), returns structured JSON. No database dependency.
- `reconcile.py` — Takes a JSON list of investor names, finds fuzzy duplicates. No database dependency.
- `export_xlsx.py` — Takes a JSON list of ranked investors, generates formatted xlsx. No database dependency.
- `SKILL.md` — Tells Claude how to orchestrate these scripts for bootstrap, query/match, and import workflows.

---

### Task 1: Project Scaffolding

**Files:**
- Create: `${SKILL_DIR}/scripts/requirements.txt`
- Create: `${SCRIPTS}/tests/conftest.py`

- [ ] **Step 1: Create directory structure and requirements.txt**

```bash
mkdir -p "${V23_SKILLS}/placement-engine/scripts/tests"
```

Write `${SCRIPTS}/requirements.txt`:
```
openpyxl>=3.1.0
rapidfuzz>=3.0.0
pytest>=7.0.0
```

- [ ] **Step 2: Install dependencies**

```bash
pip install openpyxl rapidfuzz pytest
```

Expected: Successfully installed (or "already satisfied").

- [ ] **Step 3: Create shared test fixtures**

Write `${SCRIPTS}/tests/conftest.py`:

```python
"""Shared pytest fixtures for V23 Placement Engine tests."""

import pytest
import tempfile
import os
import sys
import openpyxl

# Add scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def tmp_dir():
    """Temporary directory, cleaned up after each test."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def tmp_db(tmp_dir):
    """Path for a temporary test database (file does not exist yet)."""
    return os.path.join(tmp_dir, "test.db")


@pytest.fixture
def seeded_db(tmp_db):
    """Database with 3 investors and 2 deals pre-loaded. No interactions."""
    from db import create_database, insert_deal, insert_investor

    create_database(tmp_db)
    insert_deal(
        tmp_db, "Test Deal Alpha", deal_date="2026-01-01",
        asset_class="multifamily", geography="Tampa, FL",
        strategy="value-add", capital_stack_position="LP equity",
    )
    insert_deal(
        tmp_db, "Test Deal Beta", deal_date="2025-06-15",
        asset_class="industrial", geography="Dallas, TX",
        strategy="ground-up", capital_stack_position="LP equity",
    )
    insert_investor(tmp_db, "Acme Capital", aliases=["Acme"], coverage_owner="HC")
    insert_investor(tmp_db, "Beta Partners", aliases=["Beta LP"], coverage_owner="MS")
    insert_investor(tmp_db, "Gamma Group", coverage_owner="SM")
    return tmp_db


@pytest.fixture
def format_a_xlsx(tmp_dir):
    """Sample Format A placement xlsx (Capital Group columns)."""
    path = os.path.join(tmp_dir, "format_a.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Detail"

    # Deal header in row 1
    ws["A1"] = "Deal: Test Deal Alpha  01-Jan-26"

    # Column headers in row 3
    headers = [
        "Row #", "Status", "Cov.", "Capital Group", "Contact", "Email",
        "Contact - Notes", "New Contact", "New - Role", "New - Email",
        "Date - Last", "Placement Comments", "Old Comments",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col, value=h)

    # Data rows starting at row 4
    data = [
        [1, "Pass", "HC", "Acme Capital", "John Smith", "john@acme.com",
         "", "", "", "", "2025-12-01", "Not interested in this market",
         "Previous pass on similar deal"],
        [2, "Reviewing", "MS", "Beta Partners", "Jane Doe", "jane@beta.com",
         "", "", "", "", "2026-01-15", "Reviewing terms", ""],
        [3, "Sent", "SM", "Gamma Group", "Bob Wilson", "bob@gamma.com",
         "", "Alice Brown", "VP", "alice@gamma.com", "", "", ""],
    ]
    for row_idx, row_data in enumerate(data, 4):
        for col_idx, val in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)

    wb.save(path)
    return path


@pytest.fixture
def format_b_xlsx(tmp_dir):
    """Sample Format B placement xlsx (Capital Provider columns)."""
    path = os.path.join(tmp_dir, "format_b.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Detail"

    ws["A1"] = "Deal: Test Deal Beta  15-Feb-26"

    headers = [
        "Status", "Coverage", "Capital Provider", "Contact Person",
        "Contact Email", "Contact Numbers", "Date Sent",
        "Placement Comments", "Previous / Other Commentary",
    ]
    for col, h in enumerate(headers, 1):
        ws.cell(row=3, column=col, value=h)

    data = [
        ["1.Actively Reviewing", "HC", "Delta Fund", "Tom Lee",
         "tom@delta.com", "555-0001", "2026-01-20",
         "Very interested", "Met at conference"],
        ["5.Pass", "MS", "Epsilon LLC", "Sara Chen",
         "sara@epsilon.com", "555-0002", "2026-01-10",
         "Too small", ""],
        ["2.Reviewing", "SM", "Zeta Investments", "Mike Park",
         "mike@zeta.com", "555-0003", "2026-01-25",
         "Under review by IC", "Previous interest"],
    ]
    for row_idx, row_data in enumerate(data, 4):
        for col_idx, val in enumerate(row_data, 1):
            ws.cell(row=row_idx, column=col_idx, value=val)

    wb.save(path)
    return path
```

---

### Task 2: Database Layer

**Files:**
- Create: `${SCRIPTS}/tests/test_db.py`
- Create: `${SCRIPTS}/db.py`

- [ ] **Step 1: Write the complete test file**

Write `${SCRIPTS}/tests/test_db.py`:

```python
"""Tests for db.py — V23 Placement Engine Database Layer."""

import pytest
import json
import os
import sys
import sqlite3
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from db import (
    create_database, insert_deal, insert_investor, find_investor,
    insert_interaction, get_investor_batch, merge_investors,
    get_database_stats, update_interaction, update_deal_stats,
    get_deal_interactions,
)


class TestSchemaCreation:
    def test_creates_database_file(self, tmp_db):
        create_database(tmp_db)
        assert os.path.exists(tmp_db)

    def test_creates_all_tables(self, tmp_db):
        create_database(tmp_db)
        conn = sqlite3.connect(tmp_db)
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        conn.close()
        assert "investors" in tables
        assert "deals" in tables
        assert "interactions" in tables

    def test_idempotent(self, tmp_db):
        create_database(tmp_db)
        create_database(tmp_db)  # should not raise


class TestDealCRUD:
    def test_insert_returns_positive_id(self, tmp_db):
        create_database(tmp_db)
        deal_id = insert_deal(
            tmp_db, "Test Deal", deal_date="2026-01-01",
            asset_class="multifamily", geography="Tampa, FL",
        )
        assert isinstance(deal_id, int) and deal_id > 0

    def test_unique_deal_name(self, tmp_db):
        create_database(tmp_db)
        insert_deal(tmp_db, "Test Deal")
        with pytest.raises(Exception):
            insert_deal(tmp_db, "Test Deal")


class TestInvestorCRUD:
    def test_insert_returns_positive_id(self, tmp_db):
        create_database(tmp_db)
        inv_id = insert_investor(
            tmp_db, "Canyon Partners", aliases=["Canyon"], coverage_owner="HC",
        )
        assert isinstance(inv_id, int) and inv_id > 0

    def test_find_by_canonical_name(self, tmp_db):
        create_database(tmp_db)
        insert_investor(tmp_db, "Canyon Partners", coverage_owner="HC")
        result = find_investor(tmp_db, "Canyon Partners")
        assert result is not None
        assert result["canonical_name"] == "Canyon Partners"
        assert result["coverage_owner"] == "HC"

    def test_find_by_alias(self, tmp_db):
        create_database(tmp_db)
        insert_investor(
            tmp_db, "Canyon Partners", aliases=["Canyon", "Canyon RE"],
        )
        result = find_investor(tmp_db, "Canyon")
        assert result is not None
        assert result["canonical_name"] == "Canyon Partners"

    def test_find_returns_none_for_unknown(self, tmp_db):
        create_database(tmp_db)
        assert find_investor(tmp_db, "Nonexistent") is None


class TestInteractions:
    def test_insert_returns_positive_id(self, seeded_db):
        ix_id = insert_interaction(
            seeded_db, investor_id=1, deal_id=1,
            status="Pass", raw_comments="Too small",
        )
        assert isinstance(ix_id, int) and ix_id > 0

    def test_unique_investor_deal_pair(self, seeded_db):
        insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Pass")
        with pytest.raises(Exception):
            insert_interaction(seeded_db, investor_id=1, deal_id=1, status="Reviewing")


class TestBatchRetrieval:
    def test_returns_all_investors_with_interactions(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass",
                           raw_comments="Not our market")
        insert_interaction(seeded_db, 2, 1, status="Reviewing",
                           raw_comments="Under review")
        batch = get_investor_batch(seeded_db, offset=0, limit=50)
        assert len(batch) == 3
        for inv in batch:
            assert "interactions" in inv
            assert isinstance(inv["interactions"], list)

    def test_includes_deal_metadata_in_interactions(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass")
        batch = get_investor_batch(seeded_db, offset=0, limit=50)
        inv1 = next(i for i in batch if i["canonical_name"] == "Acme Capital")
        assert len(inv1["interactions"]) == 1
        assert inv1["interactions"][0]["deal_name"] == "Test Deal Alpha"
        assert inv1["interactions"][0]["asset_class"] == "multifamily"

    def test_offset_and_limit(self, seeded_db):
        batch1 = get_investor_batch(seeded_db, offset=0, limit=2)
        assert len(batch1) == 2
        batch2 = get_investor_batch(seeded_db, offset=2, limit=2)
        assert len(batch2) == 1


class TestMerge:
    def test_merge_moves_interactions_and_adds_alias(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass", raw_comments="No")
        insert_interaction(seeded_db, 2, 2, status="Reviewing", raw_comments="Yes")
        merge_investors(seeded_db, keep_id=1, merge_id=2)

        # Merged investor should be gone
        assert find_investor(seeded_db, "Beta Partners") is None

        # Kept investor should have new alias
        inv1 = find_investor(seeded_db, "Acme Capital")
        assert "Beta Partners" in inv1["aliases"]

        # Total investors should be 2 (was 3)
        stats = get_database_stats(seeded_db)
        assert stats["investor_count"] == 2

    def test_merge_handles_overlapping_deals(self, seeded_db):
        """When both investors have interactions on the same deal, keep the richer one."""
        insert_interaction(seeded_db, 1, 1, status="Sent", raw_comments=None)
        insert_interaction(seeded_db, 2, 1, status="Pass",
                           raw_comments="Not interested")
        merge_investors(seeded_db, keep_id=1, merge_id=2)
        interactions = get_deal_interactions(seeded_db, 1)
        inv1_ix = [i for i in interactions if i["investor_name"] == "Acme Capital"]
        # Should have kept the richer interaction data
        assert len(inv1_ix) == 1


class TestStats:
    def test_returns_correct_counts(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass")
        stats = get_database_stats(seeded_db)
        assert stats["investor_count"] == 3
        assert stats["deal_count"] == 2
        assert stats["interaction_count"] == 1


class TestUpdateInteraction:
    def test_updates_status_and_comments(self, seeded_db):
        ix_id = insert_interaction(seeded_db, 1, 1, status="Reviewing")
        update_interaction(seeded_db, ix_id, status="Pass",
                           raw_comments="Decided to pass")
        interactions = get_deal_interactions(seeded_db, 1)
        ix = next(i for i in interactions if i["id"] == ix_id)
        assert ix["status"] == "Pass"
        assert ix["raw_comments"] == "Decided to pass"


class TestDealStats:
    def test_computes_pass_and_reviewing_counts(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass")
        insert_interaction(seeded_db, 2, 1, status="Reviewing")
        insert_interaction(seeded_db, 3, 1, status="Pass")
        update_deal_stats(seeded_db, 1)

        conn = sqlite3.connect(seeded_db)
        conn.row_factory = sqlite3.Row
        deal = dict(conn.execute("SELECT * FROM deals WHERE id = 1").fetchone())
        conn.close()
        assert deal["total_contacted"] == 3
        assert deal["pass_count"] == 2
        assert deal["reviewing_count"] == 1
        assert abs(deal["pass_rate"] - 2 / 3) < 0.01


class TestGetDealInteractions:
    def test_returns_interactions_with_investor_names(self, seeded_db):
        insert_interaction(seeded_db, 1, 1, status="Pass",
                           raw_comments="No thanks")
        insert_interaction(seeded_db, 2, 1, status="Reviewing")
        result = get_deal_interactions(seeded_db, 1)
        assert len(result) == 2
        names = {r["investor_name"] for r in result}
        assert "Acme Capital" in names
        assert "Beta Partners" in names


class TestCLI:
    def test_init_creates_database(self, tmp_dir):
        db = os.path.join(tmp_dir, "cli_test.db")
        script = os.path.join(os.path.dirname(__file__), "..", "db.py")
        result = subprocess.run(
            ["python", script, "--db-path", db, "init"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["status"] == "ok"
        assert os.path.exists(db)

    def test_stats_returns_json(self, seeded_db):
        script = os.path.join(os.path.dirname(__file__), "..", "db.py")
        result = subprocess.run(
            ["python", script, "--db-path", seeded_db, "stats"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        stats = json.loads(result.stdout)
        assert stats["investor_count"] == 3

    def test_get_batch_strip_pii(self, seeded_db):
        script = os.path.join(os.path.dirname(__file__), "..", "db.py")
        result = subprocess.run(
            ["python", script, "--db-path", seeded_db,
             "get-batch", "--offset", "0", "--limit", "50", "--strip-pii"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        batch = json.loads(result.stdout)
        for inv in batch:
            assert "contact_name" not in inv
            assert "email" not in inv
            assert "phone" not in inv
            # canonical_name should still be present
            assert "canonical_name" in inv
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_db.py -v 2>&1 | head -30
```

Expected: FAIL — `ModuleNotFoundError: No module named 'db'`

- [ ] **Step 3: Write the complete implementation**

Write `${SCRIPTS}/db.py`:

```python
"""V23 Placement Engine — SQLite Database Management.

Provides schema creation, CRUD operations, batch retrieval, entity merging,
and a CLI interface. All operations output JSON to stdout for skill orchestration.
"""

import sqlite3
import json
import os
import sys
import argparse

DEFAULT_DB_DIR = os.path.join(os.path.expanduser("~"), ".v23", "placement-engine")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "placement.db")


def get_connection(db_path=None):
    """Get a database connection with WAL mode and foreign keys enabled."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def create_database(db_path=None):
    """Create the database schema (idempotent)."""
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS investors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canonical_name TEXT NOT NULL UNIQUE,
            aliases TEXT DEFAULT '[]',
            coverage_owner TEXT,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            new_contact TEXT,
            new_contact_role TEXT,
            new_contact_email TEXT
        );

        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deal_name TEXT NOT NULL UNIQUE,
            deal_date TEXT,
            asset_class TEXT,
            geography TEXT,
            strategy TEXT,
            capital_stack_position TEXT,
            estimated_equity_need TEXT,
            deal_status TEXT DEFAULT 'active',
            total_contacted INTEGER,
            pass_count INTEGER,
            pass_rate REAL,
            reviewing_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            investor_id INTEGER NOT NULL,
            deal_id INTEGER NOT NULL,
            status TEXT,
            coverage_code TEXT,
            raw_comments TEXT,
            old_comments TEXT,
            date_last_contact TEXT,
            date_om_sent TEXT,
            FOREIGN KEY (investor_id) REFERENCES investors(id),
            FOREIGN KEY (deal_id) REFERENCES deals(id),
            UNIQUE(investor_id, deal_id)
        );

        CREATE INDEX IF NOT EXISTS idx_interactions_investor
            ON interactions(investor_id);
        CREATE INDEX IF NOT EXISTS idx_interactions_deal
            ON interactions(deal_id);
    """)
    conn.commit()
    conn.close()


def insert_deal(db_path, deal_name, deal_date=None, asset_class=None,
                geography=None, strategy=None, capital_stack_position=None,
                estimated_equity_need=None, deal_status="active"):
    """Insert a deal. Returns the deal id."""
    conn = get_connection(db_path)
    cur = conn.execute(
        """INSERT INTO deals (deal_name, deal_date, asset_class, geography,
           strategy, capital_stack_position, estimated_equity_need, deal_status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (deal_name, deal_date, asset_class, geography, strategy,
         capital_stack_position, estimated_equity_need, deal_status),
    )
    deal_id = cur.lastrowid
    conn.commit()
    conn.close()
    return deal_id


def insert_investor(db_path, canonical_name, aliases=None, coverage_owner=None,
                    contact_name=None, email=None, phone=None,
                    new_contact=None, new_contact_role=None, new_contact_email=None):
    """Insert an investor. Returns the investor id."""
    if aliases is None:
        aliases = []
    conn = get_connection(db_path)
    cur = conn.execute(
        """INSERT INTO investors (canonical_name, aliases, coverage_owner,
           contact_name, email, phone, new_contact, new_contact_role,
           new_contact_email)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (canonical_name, json.dumps(aliases), coverage_owner,
         contact_name, email, phone, new_contact, new_contact_role,
         new_contact_email),
    )
    investor_id = cur.lastrowid
    conn.commit()
    conn.close()
    return investor_id


def find_investor(db_path, name):
    """Find an investor by canonical name or alias. Returns dict or None."""
    conn = get_connection(db_path)
    # Try exact canonical name match first
    row = conn.execute(
        "SELECT * FROM investors WHERE canonical_name = ?", (name,)
    ).fetchone()
    if row:
        result = dict(row)
        result["aliases"] = json.loads(result["aliases"])
        conn.close()
        return result
    # Search aliases
    rows = conn.execute("SELECT * FROM investors").fetchall()
    for row in rows:
        aliases = json.loads(row["aliases"])
        if name in aliases:
            result = dict(row)
            result["aliases"] = aliases
            conn.close()
            return result
    conn.close()
    return None


def insert_interaction(db_path, investor_id, deal_id, status=None,
                       coverage_code=None, raw_comments=None, old_comments=None,
                       date_last_contact=None, date_om_sent=None):
    """Insert an interaction. Returns the interaction id."""
    conn = get_connection(db_path)
    cur = conn.execute(
        """INSERT INTO interactions (investor_id, deal_id, status, coverage_code,
           raw_comments, old_comments, date_last_contact, date_om_sent)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (investor_id, deal_id, status, coverage_code, raw_comments,
         old_comments, date_last_contact, date_om_sent),
    )
    interaction_id = cur.lastrowid
    conn.commit()
    conn.close()
    return interaction_id


def get_investor_batch(db_path, offset=0, limit=50):
    """Return a batch of investors with their full interaction history.

    Returns list of dicts, each with investor fields plus an 'interactions'
    list containing interaction fields joined with deal metadata.
    """
    conn = get_connection(db_path)
    investors = conn.execute(
        "SELECT * FROM investors ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()

    result = []
    for inv in investors:
        inv_dict = dict(inv)
        inv_dict["aliases"] = json.loads(inv_dict["aliases"])

        interactions = conn.execute(
            """SELECT i.*, d.deal_name, d.deal_date, d.asset_class,
                      d.geography, d.strategy, d.capital_stack_position
               FROM interactions i
               JOIN deals d ON i.deal_id = d.id
               WHERE i.investor_id = ?
               ORDER BY d.deal_date DESC""",
            (inv_dict["id"],),
        ).fetchall()

        inv_dict["interactions"] = [dict(ix) for ix in interactions]
        result.append(inv_dict)

    conn.close()
    return result


def merge_investors(db_path, keep_id, merge_id):
    """Merge two investor records.

    Moves interactions from merge_id to keep_id (handling duplicates),
    adds merged name to aliases, deletes the merged investor.
    """
    conn = get_connection(db_path)
    merge_inv = conn.execute(
        "SELECT * FROM investors WHERE id = ?", (merge_id,)
    ).fetchone()
    keep_inv = conn.execute(
        "SELECT * FROM investors WHERE id = ?", (keep_id,)
    ).fetchone()

    if not merge_inv or not keep_inv:
        conn.close()
        raise ValueError(f"Investor not found: keep={keep_id}, merge={merge_id}")

    # Combine aliases
    keep_aliases = json.loads(keep_inv["aliases"])
    merge_aliases = json.loads(merge_inv["aliases"])
    new_aliases = list(set(
        keep_aliases + merge_aliases + [merge_inv["canonical_name"]]
    ))
    conn.execute(
        "UPDATE investors SET aliases = ? WHERE id = ?",
        (json.dumps(new_aliases), keep_id),
    )

    # Move interactions, handling overlapping deals
    merge_interactions = conn.execute(
        "SELECT * FROM interactions WHERE investor_id = ?", (merge_id,)
    ).fetchall()

    for ix in merge_interactions:
        existing = conn.execute(
            "SELECT id, raw_comments FROM interactions "
            "WHERE investor_id = ? AND deal_id = ?",
            (keep_id, ix["deal_id"]),
        ).fetchone()

        if existing:
            # Keep the one with richer data
            if ix["raw_comments"] and not existing["raw_comments"]:
                conn.execute(
                    "UPDATE interactions SET status = ?, raw_comments = ?, "
                    "old_comments = ?, coverage_code = ?, "
                    "date_last_contact = ?, date_om_sent = ? WHERE id = ?",
                    (ix["status"], ix["raw_comments"], ix["old_comments"],
                     ix["coverage_code"], ix["date_last_contact"],
                     ix["date_om_sent"], existing["id"]),
                )
            conn.execute(
                "DELETE FROM interactions WHERE id = ?", (ix["id"],)
            )
        else:
            conn.execute(
                "UPDATE interactions SET investor_id = ? WHERE id = ?",
                (keep_id, ix["id"]),
            )

    conn.execute("DELETE FROM investors WHERE id = ?", (merge_id,))
    conn.commit()
    conn.close()


def get_database_stats(db_path):
    """Return summary statistics as a dict."""
    conn = get_connection(db_path)
    stats = {
        "investor_count": conn.execute(
            "SELECT COUNT(*) FROM investors"
        ).fetchone()[0],
        "deal_count": conn.execute(
            "SELECT COUNT(*) FROM deals"
        ).fetchone()[0],
        "interaction_count": conn.execute(
            "SELECT COUNT(*) FROM interactions"
        ).fetchone()[0],
    }
    conn.close()
    return stats


def update_interaction(db_path, interaction_id, **updates):
    """Update fields on an existing interaction."""
    allowed = {
        "status", "coverage_code", "raw_comments", "old_comments",
        "date_last_contact", "date_om_sent",
    }
    updates = {k: v for k, v in updates.items() if k in allowed and v is not None}
    if not updates:
        return
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [interaction_id]
    conn = get_connection(db_path)
    conn.execute(f"UPDATE interactions SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()


def update_deal_stats(db_path, deal_id):
    """Recalculate and update summary stats for a deal."""
    conn = get_connection(db_path)
    total = conn.execute(
        "SELECT COUNT(*) FROM interactions WHERE deal_id = ?", (deal_id,)
    ).fetchone()[0]
    passes = conn.execute(
        "SELECT COUNT(*) FROM interactions WHERE deal_id = ? AND status = 'Pass'",
        (deal_id,),
    ).fetchone()[0]
    reviewing = conn.execute(
        """SELECT COUNT(*) FROM interactions WHERE deal_id = ?
           AND status IN ('Reviewing', 'Reviewing - Pref', 'Reviewing - GL',
                          'Actively Reviewing', 'Reviewing - Unlikely')""",
        (deal_id,),
    ).fetchone()[0]
    pass_rate = passes / total if total > 0 else 0.0
    conn.execute(
        """UPDATE deals SET total_contacted = ?, pass_count = ?,
           pass_rate = ?, reviewing_count = ? WHERE id = ?""",
        (total, passes, pass_rate, reviewing, deal_id),
    )
    conn.commit()
    conn.close()


def get_deal_interactions(db_path, deal_id):
    """Get all interactions for a deal, joined with investor names."""
    conn = get_connection(db_path)
    rows = conn.execute(
        """SELECT i.*, inv.canonical_name AS investor_name
           FROM interactions i
           JOIN investors inv ON i.investor_id = inv.id
           WHERE i.deal_id = ?""",
        (deal_id,),
    ).fetchall()
    result = [dict(r) for r in rows]
    conn.close()
    return result


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="V23 Placement Engine Database")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH)
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init")

    # insert-deal
    p = sub.add_parser("insert-deal")
    p.add_argument("--name", required=True)
    p.add_argument("--date")
    p.add_argument("--asset-class")
    p.add_argument("--geography")
    p.add_argument("--strategy")
    p.add_argument("--capital-stack")
    p.add_argument("--equity-need")
    p.add_argument("--status", default="active")

    # insert-investor
    p = sub.add_parser("insert-investor")
    p.add_argument("--name", required=True)
    p.add_argument("--aliases", default="[]")
    p.add_argument("--coverage")
    p.add_argument("--contact-name")
    p.add_argument("--email")
    p.add_argument("--phone")
    p.add_argument("--new-contact")
    p.add_argument("--new-contact-role")
    p.add_argument("--new-contact-email")

    # insert-interaction
    p = sub.add_parser("insert-interaction")
    p.add_argument("--investor-id", type=int, required=True)
    p.add_argument("--deal-id", type=int, required=True)
    p.add_argument("--status")
    p.add_argument("--coverage-code")
    p.add_argument("--raw-comments")
    p.add_argument("--old-comments")
    p.add_argument("--date-last-contact")
    p.add_argument("--date-om-sent")

    # find-investor
    p = sub.add_parser("find-investor")
    p.add_argument("--name", required=True)

    # get-batch
    p = sub.add_parser("get-batch")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--strip-pii", action="store_true",
                   help="Remove personal contact info from output")

    # merge
    p = sub.add_parser("merge")
    p.add_argument("--keep-id", type=int, required=True)
    p.add_argument("--merge-id", type=int, required=True)

    # stats
    sub.add_parser("stats")

    # get-deal-interactions
    p = sub.add_parser("get-deal-interactions")
    p.add_argument("--deal-id", type=int, required=True)

    # update-interaction
    p = sub.add_parser("update-interaction")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--status")
    p.add_argument("--coverage-code")
    p.add_argument("--raw-comments")
    p.add_argument("--old-comments")
    p.add_argument("--date-last-contact")
    p.add_argument("--date-om-sent")

    # update-deal-stats
    p = sub.add_parser("update-deal-stats")
    p.add_argument("--deal-id", type=int, required=True)

    args = parser.parse_args()
    db = args.db_path

    if args.command == "init":
        create_database(db)
        print(json.dumps({"status": "ok", "db_path": db}))

    elif args.command == "insert-deal":
        deal_id = insert_deal(
            db, args.name, args.date, args.asset_class, args.geography,
            args.strategy, args.capital_stack, args.equity_need, args.status,
        )
        print(json.dumps({"deal_id": deal_id}))

    elif args.command == "insert-investor":
        aliases = json.loads(args.aliases)
        inv_id = insert_investor(
            db, args.name, aliases, args.coverage, args.contact_name,
            args.email, args.phone, args.new_contact, args.new_contact_role,
            args.new_contact_email,
        )
        print(json.dumps({"investor_id": inv_id}))

    elif args.command == "insert-interaction":
        ix_id = insert_interaction(
            db, args.investor_id, args.deal_id, args.status,
            args.coverage_code, args.raw_comments, args.old_comments,
            args.date_last_contact, args.date_om_sent,
        )
        print(json.dumps({"interaction_id": ix_id}))

    elif args.command == "find-investor":
        result = find_investor(db, args.name)
        print(json.dumps(result))

    elif args.command == "get-batch":
        result = get_investor_batch(db, args.offset, args.limit)
        if args.strip_pii:
            pii_fields = [
                "contact_name", "email", "phone",
                "new_contact", "new_contact_role", "new_contact_email",
            ]
            for inv in result:
                for field in pii_fields:
                    inv.pop(field, None)
        print(json.dumps(result))

    elif args.command == "merge":
        merge_investors(db, args.keep_id, args.merge_id)
        print(json.dumps({"status": "merged"}))

    elif args.command == "stats":
        print(json.dumps(get_database_stats(db)))

    elif args.command == "get-deal-interactions":
        result = get_deal_interactions(db, args.deal_id)
        print(json.dumps(result))

    elif args.command == "update-interaction":
        updates = {}
        for field in ["status", "coverage_code", "raw_comments",
                       "old_comments", "date_last_contact", "date_om_sent"]:
            val = getattr(args, field.replace("-", "_"), None)
            if val is not None:
                updates[field] = val
        update_interaction(db, args.id, **updates)
        print(json.dumps({"status": "updated"}))

    elif args.command == "update-deal-stats":
        update_deal_stats(db, args.deal_id)
        print(json.dumps({"status": "updated"}))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_db.py -v
```

Expected: All tests PASS.

---

### Task 3: XLSX Parser

**Files:**
- Create: `${SCRIPTS}/tests/test_parse_xlsx.py`
- Create: `${SCRIPTS}/parse_xlsx.py`

- [ ] **Step 1: Write the complete test file**

Write `${SCRIPTS}/tests/test_parse_xlsx.py`:

```python
"""Tests for parse_xlsx.py — Placement XLSX Parser."""

import pytest
import json
import os
import sys
import subprocess
import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from parse_xlsx import (
    detect_format, find_header_row, extract_deal_header,
    parse_format_a, parse_format_b, parse_placement_file,
)


class TestDetectFormat:
    def test_detects_format_a(self, format_a_xlsx):
        assert detect_format(format_a_xlsx) == "A"

    def test_detects_format_b(self, format_b_xlsx):
        assert detect_format(format_b_xlsx) == "B"

    def test_detects_edge_case(self, tmp_dir):
        path = os.path.join(tmp_dir, "edge.xlsx")
        wb = openpyxl.Workbook()
        ws = wb.active
        ws["A1"] = "Company"
        ws["B1"] = "Feedback"
        wb.save(path)
        assert detect_format(path) == "edge"


class TestFindHeaderRow:
    def test_finds_header_in_row_3(self, format_a_xlsx):
        wb = openpyxl.load_workbook(format_a_xlsx, read_only=True)
        ws = wb[wb.sheetnames[0]]
        row_num, col_map = find_header_row(
            ws, ["Status", "Capital Group", "Placement Comments"]
        )
        wb.close()
        assert row_num == 3
        assert "Capital Group" in col_map

    def test_returns_none_when_no_match(self, tmp_dir):
        path = os.path.join(tmp_dir, "empty.xlsx")
        wb = openpyxl.Workbook()
        wb.save(path)
        wb2 = openpyxl.load_workbook(path, read_only=True)
        ws = wb2[wb2.sheetnames[0]]
        row_num, col_map = find_header_row(ws, ["Nonexistent", "Columns"])
        wb2.close()
        assert row_num is None


class TestExtractDealHeader:
    def test_extracts_deal_name_and_date(self, format_a_xlsx):
        wb = openpyxl.load_workbook(format_a_xlsx, read_only=True)
        ws = wb[wb.sheetnames[0]]
        header = extract_deal_header(ws)
        wb.close()
        assert header["deal_name"] is not None
        assert "Test Deal Alpha" in header["deal_name"]


class TestParseFormatA:
    def test_returns_correct_row_count(self, format_a_xlsx):
        result = parse_format_a(format_a_xlsx)
        assert len(result["rows"]) == 3

    def test_extracts_investor_name_and_status(self, format_a_xlsx):
        result = parse_format_a(format_a_xlsx)
        row0 = result["rows"][0]
        assert row0["investor_name"] == "Acme Capital"
        assert row0["status"] == "Pass"
        assert row0["coverage_code"] == "HC"

    def test_extracts_comments(self, format_a_xlsx):
        result = parse_format_a(format_a_xlsx)
        row0 = result["rows"][0]
        assert row0["raw_comments"] == "Not interested in this market"
        assert row0["old_comments"] == "Previous pass on similar deal"

    def test_extracts_contact_info(self, format_a_xlsx):
        result = parse_format_a(format_a_xlsx)
        row0 = result["rows"][0]
        assert row0["contact_name"] == "John Smith"
        assert row0["email"] == "john@acme.com"

    def test_extracts_new_contact(self, format_a_xlsx):
        result = parse_format_a(format_a_xlsx)
        row2 = result["rows"][2]
        assert row2["new_contact"] == "Alice Brown"
        assert row2["new_contact_role"] == "VP"
        assert row2["new_contact_email"] == "alice@gamma.com"


class TestParseFormatB:
    def test_strips_numeric_status_prefix(self, format_b_xlsx):
        result = parse_format_b(format_b_xlsx)
        assert result["rows"][0]["status"] == "Actively Reviewing"
        assert result["rows"][1]["status"] == "Pass"
        assert result["rows"][2]["status"] == "Reviewing"

    def test_returns_correct_row_count(self, format_b_xlsx):
        result = parse_format_b(format_b_xlsx)
        assert len(result["rows"]) == 3

    def test_extracts_investor_name(self, format_b_xlsx):
        result = parse_format_b(format_b_xlsx)
        assert result["rows"][0]["investor_name"] == "Delta Fund"

    def test_extracts_phone(self, format_b_xlsx):
        result = parse_format_b(format_b_xlsx)
        assert result["rows"][0]["phone"] == "555-0001"

    def test_maps_old_comments_field(self, format_b_xlsx):
        result = parse_format_b(format_b_xlsx)
        assert result["rows"][0]["old_comments"] == "Met at conference"


class TestParsePlacementFile:
    def test_auto_detects_format_a(self, format_a_xlsx):
        result = parse_placement_file(format_a_xlsx)
        assert result["format"] == "A"
        assert len(result["rows"]) == 3

    def test_auto_detects_format_b(self, format_b_xlsx):
        result = parse_placement_file(format_b_xlsx)
        assert result["format"] == "B"
        assert len(result["rows"]) == 3

    def test_includes_source_file(self, format_a_xlsx):
        result = parse_placement_file(format_a_xlsx)
        assert result["source_file"] == "format_a.xlsx"


class TestCLI:
    def test_detect_command(self, format_a_xlsx):
        script = os.path.join(os.path.dirname(__file__), "..", "parse_xlsx.py")
        result = subprocess.run(
            ["python", script, "detect", format_a_xlsx],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert json.loads(result.stdout)["format"] == "A"

    def test_parse_command(self, format_b_xlsx):
        script = os.path.join(os.path.dirname(__file__), "..", "parse_xlsx.py")
        result = subprocess.run(
            ["python", script, "parse", format_b_xlsx],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["format"] == "B"
        assert len(data["rows"]) == 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_parse_xlsx.py -v 2>&1 | head -20
```

Expected: FAIL — `ModuleNotFoundError: No module named 'parse_xlsx'`

- [ ] **Step 3: Write the complete implementation**

Write `${SCRIPTS}/parse_xlsx.py`:

```python
"""V23 Placement Engine — Parse Placement XLSX Files.

Auto-detects Format A (Capital Group), Format B (Capital Provider),
or edge cases. Returns structured JSON for database ingestion.
"""

import openpyxl
import json
import sys
import re
import os
import argparse

# Column name → schema field mappings
FORMAT_A_COLUMNS = {
    "Status": "status",
    "Cov.": "coverage_code",
    "Capital Group": "investor_name",
    "Contact": "contact_name",
    "Email": "email",
    "Contact - Notes": "contact_notes",
    "New Contact": "new_contact",
    "New - Role": "new_contact_role",
    "New - Email": "new_contact_email",
    "Date - Last": "date_last_contact",
    "Last": "date_last_contact",
    "Placement Comments": "raw_comments",
    "Old Comments": "old_comments",
    "OM": "date_om_sent",
}

FORMAT_B_COLUMNS = {
    "Status": "status",
    "Coverage": "coverage_code",
    "Capital Provider": "investor_name",
    "Contact Person": "contact_name",
    "Contact Email": "email",
    "Contact Numbers": "phone",
    "Date Sent": "date_last_contact",
    "Placement Comments": "raw_comments",
    "Previous / Other Commentary": "old_comments",
}


def detect_format(file_path):
    """Detect the format of a placement xlsx file.

    Returns 'A' (Capital Group), 'B' (Capital Provider), or 'edge'.
    """
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for row in ws.iter_rows(max_row=10, values_only=True):
            if row is None:
                continue
            cells = [str(c).strip() if c is not None else "" for c in row]
            if "Capital Group" in cells:
                wb.close()
                return "A"
            if "Capital Provider" in cells:
                wb.close()
                return "B"
    wb.close()
    return "edge"


def find_header_row(ws, target_columns):
    """Find the row containing header columns.

    Args:
        ws: openpyxl worksheet
        target_columns: iterable of column names to look for

    Returns:
        (row_number, {col_name: col_index}) or (None, None)
    """
    target_set = set(target_columns)
    for row_idx, row in enumerate(ws.iter_rows(max_row=15, values_only=True), start=1):
        if row is None:
            continue
        cells = [str(c).strip() if c is not None else "" for c in row]
        matches = sum(1 for col in target_set if col in cells)
        if matches >= 2:
            col_map = {}
            for col_name in target_set:
                if col_name in cells:
                    col_map[col_name] = cells.index(col_name)
            return row_idx, col_map
    return None, None


def extract_deal_header(ws):
    """Extract deal name and date from the header area (first 5 rows).

    Looks for patterns like 'Deal: 105 N 13 St  09-Apr-26'.
    Returns dict with deal_name and deal_date (both may be None).
    """
    deal_name = None
    deal_date = None

    for row in ws.iter_rows(max_row=5, values_only=True):
        if row is None:
            continue
        for cell in row:
            if cell is None:
                continue
            cell_str = str(cell).strip()
            if not cell_str:
                continue

            # "Deal: Name  Date" pattern (double-space or tab separator)
            match = re.match(r"Deal:\s*(.+?)(?:\s{2,}|\t)(.+)", cell_str)
            if match:
                deal_name = match.group(1).strip()
                deal_date = match.group(2).strip()
                return {"deal_name": deal_name, "deal_date": deal_date}

            # "Deal: Name" without date
            match2 = re.match(r"Deal:\s*(.+)", cell_str)
            if match2:
                deal_name = match2.group(1).strip()
                return {"deal_name": deal_name, "deal_date": deal_date}

            # Fallback: first non-empty cell longer than 3 chars
            if deal_name is None and len(cell_str) > 3:
                deal_name = cell_str

    return {"deal_name": deal_name, "deal_date": deal_date}


def _pick_detail_sheet(wb):
    """Return the detail sheet if one exists, else the first sheet."""
    for name in wb.sheetnames:
        if "detail" in name.lower():
            return wb[name]
    return wb[wb.sheetnames[0]]


def _parse_rows(ws, header_row, col_map, column_mapping, strip_status_prefix=False):
    """Generic row parser for both formats."""
    rows = []
    for row in ws.iter_rows(min_row=header_row + 1, values_only=True):
        if row is None:
            continue
        record = {}
        for col_name, col_idx in col_map.items():
            field = column_mapping.get(col_name)
            if field is None or field.startswith("_"):
                continue
            val = row[col_idx] if col_idx < len(row) else None
            record[field] = str(val).strip() if val is not None else None
            # Normalize "None" strings from openpyxl
            if record[field] == "None":
                record[field] = None

        if strip_status_prefix and record.get("status"):
            record["status"] = re.sub(r"^\d+\.\s*", "", record["status"])

        # Skip rows without an investor name
        if not record.get("investor_name"):
            continue

        rows.append(record)
    return rows


def parse_format_a(file_path):
    """Parse a Format A placement file (Capital Group columns)."""
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    ws = _pick_detail_sheet(wb)
    deal_header = extract_deal_header(ws)
    header_row, col_map = find_header_row(ws, FORMAT_A_COLUMNS.keys())

    if header_row is None:
        wb.close()
        return {"deal_header": deal_header, "rows": [],
                "error": "No header row found"}

    rows = _parse_rows(ws, header_row, col_map, FORMAT_A_COLUMNS)
    wb.close()
    return {"deal_header": deal_header, "rows": rows}


def parse_format_b(file_path):
    """Parse a Format B placement file (Capital Provider columns)."""
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    ws = _pick_detail_sheet(wb)
    deal_header = extract_deal_header(ws)
    header_row, col_map = find_header_row(ws, FORMAT_B_COLUMNS.keys())

    if header_row is None:
        wb.close()
        return {"deal_header": deal_header, "rows": [],
                "error": "No header row found"}

    rows = _parse_rows(ws, header_row, col_map, FORMAT_B_COLUMNS,
                        strip_status_prefix=True)
    wb.close()
    return {"deal_header": deal_header, "rows": rows}


def parse_placement_file(file_path):
    """Parse a placement xlsx file. Auto-detects format.

    Returns dict with format, deal_header, rows, and source_file.
    """
    fmt = detect_format(file_path)

    if fmt == "A":
        result = parse_format_a(file_path)
    elif fmt == "B":
        result = parse_format_b(file_path)
    else:
        result = {"deal_header": {"deal_name": None, "deal_date": None},
                  "rows": [], "note": "Edge case format — manual parsing needed"}

    result["format"] = fmt
    result["source_file"] = os.path.basename(file_path)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Parse V23 Placement XLSX Files"
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("detect")
    p.add_argument("file_path")

    p = sub.add_parser("parse")
    p.add_argument("file_path")

    args = parser.parse_args()

    if args.command == "detect":
        fmt = detect_format(args.file_path)
        print(json.dumps({"format": fmt}))

    elif args.command == "parse":
        result = parse_placement_file(args.file_path)
        print(json.dumps(result, default=str))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_parse_xlsx.py -v
```

Expected: All tests PASS.

---

### Task 4: Entity Reconciliation

**Files:**
- Create: `${SCRIPTS}/tests/test_reconcile.py`
- Create: `${SCRIPTS}/reconcile.py`

- [ ] **Step 1: Write the complete test file**

Write `${SCRIPTS}/tests/test_reconcile.py`:

```python
"""Tests for reconcile.py — Fuzzy Entity Name Matching."""

import pytest
import json
import os
import sys
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reconcile import normalize_name, find_duplicates


class TestNormalizeName:
    def test_lowercases_and_strips_common_suffixes(self):
        assert "canyon" in normalize_name("Canyon Partners")

    def test_strips_real_estate_suffix(self):
        result = normalize_name("Sagard Real Estate")
        assert "sagard" in result
        assert "real" not in result
        assert "estate" not in result

    def test_strips_llc(self):
        result = normalize_name("Koch RE Investments LLC")
        assert "llc" not in result

    def test_removes_punctuation(self):
        result = normalize_name("Sagard/Everwest")
        assert "/" not in result
        assert "sagard" in result
        assert "everwest" in result

    def test_handles_none(self):
        assert normalize_name(None) == ""

    def test_handles_empty_string(self):
        assert normalize_name("") == ""


class TestFindDuplicates:
    def test_finds_similar_names(self):
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
            {"id": 3, "canonical_name": "Canyon Partners"},
        ]
        dupes = find_duplicates(investors, threshold=50)
        sagard_pair = [
            d for d in dupes
            if {d["keep"]["name"], d["merge"]["name"]}
            == {"Sagard Real Estate", "Sagard/Everwest"}
        ]
        assert len(sagard_pair) == 1

    def test_no_false_positives(self):
        investors = [
            {"id": 1, "canonical_name": "Canyon Partners"},
            {"id": 2, "canonical_name": "Brookfield Asset Management"},
        ]
        dupes = find_duplicates(investors, threshold=80)
        assert len(dupes) == 0

    def test_empty_list(self):
        assert find_duplicates([], threshold=80) == []

    def test_single_investor(self):
        investors = [{"id": 1, "canonical_name": "Acme Capital"}]
        assert find_duplicates(investors, threshold=80) == []

    def test_sorted_by_score_descending(self):
        investors = [
            {"id": 1, "canonical_name": "Koch Real Estate Investments"},
            {"id": 2, "canonical_name": "Koch RE"},
            {"id": 3, "canonical_name": "Sagard Real Estate"},
            {"id": 4, "canonical_name": "Sagard/Everwest"},
        ]
        dupes = find_duplicates(investors, threshold=40)
        if len(dupes) >= 2:
            assert dupes[0]["score"] >= dupes[1]["score"]


class TestCLI:
    def test_find_duplicates_command(self, tmp_dir):
        input_file = os.path.join(tmp_dir, "investors.json")
        investors = [
            {"id": 1, "canonical_name": "Sagard Real Estate"},
            {"id": 2, "canonical_name": "Sagard/Everwest"},
        ]
        with open(input_file, "w") as f:
            json.dump(investors, f)

        script = os.path.join(os.path.dirname(__file__), "..", "reconcile.py")
        result = subprocess.run(
            ["python", script, "find-duplicates",
             "--input", input_file, "--threshold", "50"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        dupes = json.loads(result.stdout)
        assert isinstance(dupes, list)
        assert len(dupes) >= 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_reconcile.py -v 2>&1 | head -20
```

Expected: FAIL — `ModuleNotFoundError: No module named 'reconcile'`

- [ ] **Step 3: Write the complete implementation**

Write `${SCRIPTS}/reconcile.py`:

```python
"""V23 Placement Engine — Fuzzy Entity Reconciliation.

Compares investor names to find potential duplicates. Takes a JSON list
of investors as input (no database dependency). Uses rapidfuzz for
fast fuzzy matching.
"""

import json
import re
import sys
import argparse

from rapidfuzz import fuzz

# Common suffixes to strip for comparison
STRIP_SUFFIXES = [
    "llc", "lp", "inc", "corp", "co", "company", "group", "partners",
    "capital", "real estate", "investments", "advisors", "management",
    "fund", "holdings", "properties", "realty",
]


def normalize_name(name):
    """Normalize an investor name for fuzzy comparison.

    Lowercases, removes punctuation, strips common corporate suffixes,
    and collapses whitespace.
    """
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r"[,.'\"()/-]", " ", n)
    for suffix in STRIP_SUFFIXES:
        n = re.sub(rf"\b{suffix}\b", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def find_duplicates(investors, threshold=80):
    """Find potential duplicate investor names.

    Args:
        investors: list of dicts with at least 'id' and 'canonical_name'
        threshold: minimum fuzzy match score (0-100) to propose a merge

    Returns:
        list of proposal dicts sorted by score descending:
        [{"keep": {"id": N, "name": "..."}, "merge": {"id": M, "name": "..."},
          "score": int, "reason": "..."}, ...]
    """
    names = [
        (inv["id"], inv["canonical_name"], normalize_name(inv["canonical_name"]))
        for inv in investors
    ]

    proposals = []
    seen = set()

    for i, (id1, name1, norm1) in enumerate(names):
        if not norm1:
            continue
        for j, (id2, name2, norm2) in enumerate(names):
            if i >= j or not norm2:
                continue
            pair_key = (min(id1, id2), max(id1, id2))
            if pair_key in seen:
                continue

            score = fuzz.token_sort_ratio(norm1, norm2)
            if score >= threshold:
                seen.add(pair_key)
                proposals.append({
                    "keep": {"id": id1, "name": name1},
                    "merge": {"id": id2, "name": name2},
                    "score": score,
                    "reason": f"Fuzzy match score: {score}/100",
                })

    proposals.sort(key=lambda x: x["score"], reverse=True)
    return proposals


def main():
    parser = argparse.ArgumentParser(
        description="V23 Placement Engine — Entity Reconciliation"
    )
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("find-duplicates")
    p.add_argument("--input", required=True,
                   help="JSON file with investor list")
    p.add_argument("--threshold", type=int, default=80)

    args = parser.parse_args()

    if args.command == "find-duplicates":
        with open(args.input) as f:
            investors = json.load(f)
        dupes = find_duplicates(investors, args.threshold)
        print(json.dumps(dupes, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_reconcile.py -v
```

Expected: All tests PASS.

---

### Task 5: XLSX Export

**Files:**
- Create: `${SCRIPTS}/tests/test_export_xlsx.py`
- Create: `${SCRIPTS}/export_xlsx.py`

- [ ] **Step 1: Write the complete test file**

Write `${SCRIPTS}/tests/test_export_xlsx.py`:

```python
"""Tests for export_xlsx.py — Placement List XLSX Generator."""

import pytest
import json
import os
import sys
import subprocess
import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from export_xlsx import export_placement_list


class TestExportPlacementList:
    def test_creates_file(self, tmp_dir):
        ranked = [
            {"investor_name": "Acme Capital", "coverage_owner": "HC",
             "contact_name": "John Smith", "email": "john@acme.com",
             "match_notes": "Strong fit", "tier": 1},
        ]
        output = os.path.join(tmp_dir, "output.xlsx")
        export_placement_list(ranked, output, deal_name="Test Deal")
        assert os.path.exists(output)

    def test_has_correct_column_headers(self, tmp_dir):
        ranked = [
            {"investor_name": "Acme Capital", "coverage_owner": "HC",
             "contact_name": "", "email": "", "match_notes": "Good",
             "tier": 1},
        ]
        output = os.path.join(tmp_dir, "output.xlsx")
        export_placement_list(ranked, output)
        wb = openpyxl.load_workbook(output)
        ws = wb.active
        headers = [ws.cell(row=3, column=c).value for c in range(1, 10)]
        wb.close()
        assert "Status" in headers
        assert "Capital Group" in headers
        assert "Match Notes" in headers
        assert "Cov." in headers

    def test_writes_investor_data(self, tmp_dir):
        ranked = [
            {"investor_name": "Acme Capital", "coverage_owner": "HC",
             "contact_name": "John", "email": "j@a.com",
             "match_notes": "Strong", "tier": 1},
            {"investor_name": "Beta Fund", "coverage_owner": "MS",
             "contact_name": "Jane", "email": "j@b.com",
             "match_notes": "Possible", "tier": 2},
        ]
        output = os.path.join(tmp_dir, "output.xlsx")
        export_placement_list(ranked, output, deal_name="Test")
        wb = openpyxl.load_workbook(output)
        ws = wb.active
        # Collect Capital Group column values
        capital_groups = []
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[2]:  # Column C = Capital Group
                capital_groups.append(row[2])
        wb.close()
        assert "Acme Capital" in capital_groups
        assert "Beta Fund" in capital_groups

    def test_includes_tier_separator_rows(self, tmp_dir):
        ranked = [
            {"investor_name": "A", "tier": 1, "coverage_owner": "",
             "contact_name": "", "email": "", "match_notes": ""},
            {"investor_name": "B", "tier": 2, "coverage_owner": "",
             "contact_name": "", "email": "", "match_notes": ""},
            {"investor_name": "C", "tier": 3, "coverage_owner": "",
             "contact_name": "", "email": "", "match_notes": ""},
        ]
        output = os.path.join(tmp_dir, "output.xlsx")
        export_placement_list(ranked, output)
        wb = openpyxl.load_workbook(output)
        ws = wb.active
        tier_labels = []
        for row in ws.iter_rows(min_row=4, values_only=True):
            cell_a = str(row[0]) if row[0] else ""
            if "Tier" in cell_a:
                tier_labels.append(cell_a)
        wb.close()
        assert any("Tier 1" in t for t in tier_labels)
        assert any("Tier 2" in t for t in tier_labels)
        assert any("Tier 3" in t for t in tier_labels)

    def test_deal_name_in_header(self, tmp_dir):
        ranked = [
            {"investor_name": "A", "tier": 1, "coverage_owner": "",
             "contact_name": "", "email": "", "match_notes": ""},
        ]
        output = os.path.join(tmp_dir, "output.xlsx")
        export_placement_list(ranked, output, deal_name="My Big Deal")
        wb = openpyxl.load_workbook(output)
        ws = wb.active
        assert "My Big Deal" in str(ws["A1"].value)
        wb.close()


class TestCLI:
    def test_export_command(self, tmp_dir):
        input_file = os.path.join(tmp_dir, "ranked.json")
        ranked = [
            {"investor_name": "Acme Capital", "coverage_owner": "HC",
             "contact_name": "John", "email": "j@a.com",
             "match_notes": "Strong", "tier": 1},
        ]
        with open(input_file, "w") as f:
            json.dump(ranked, f)

        output = os.path.join(tmp_dir, "output.xlsx")
        script = os.path.join(os.path.dirname(__file__), "..", "export_xlsx.py")
        result = subprocess.run(
            ["python", script, "--input", input_file,
             "--output", output, "--deal-name", "Test Deal"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output)
        data = json.loads(result.stdout)
        assert data["status"] == "ok"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_export_xlsx.py -v 2>&1 | head -20
```

Expected: FAIL — `ModuleNotFoundError: No module named 'export_xlsx'`

- [ ] **Step 3: Write the complete implementation**

Write `${SCRIPTS}/export_xlsx.py`:

```python
"""V23 Placement Engine — Export Placement List to XLSX.

Generates a formatted Excel file matching the team's standard placement
list format, with tier separators and a Match Notes column.
"""

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json
import sys
import argparse

# Standard placement list columns: (header, column width)
COLUMNS = [
    ("Status", 12),
    ("Cov.", 6),
    ("Capital Group", 30),
    ("Contact", 25),
    ("Email", 30),
    ("Last", 12),
    ("OM", 12),
    ("Placement Comments", 40),
    ("Match Notes", 50),
]

TIER_FILLS = {
    1: PatternFill(start_color="E2EFDA", end_color="E2EFDA",
                   fill_type="solid"),  # Green
    2: PatternFill(start_color="FFF2CC", end_color="FFF2CC",
                   fill_type="solid"),  # Yellow
    3: PatternFill(start_color="FCE4D6", end_color="FCE4D6",
                   fill_type="solid"),  # Orange
}

TIER_LABELS = {
    1: "Tier 1 \u2014 Strong Match",
    2: "Tier 2 \u2014 Possible Match",
    3: "Tier 3 \u2014 Long Shot",
}


def export_placement_list(ranked_investors, output_path, deal_name=None):
    """Generate a placement list xlsx file.

    Args:
        ranked_investors: list of dicts, each with keys:
            investor_name, coverage_owner, contact_name, email,
            match_notes, tier (1/2/3)
        output_path: file path for the xlsx output
        deal_name: optional deal name for the header row
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement List"

    # Row 1: Deal header
    if deal_name:
        ws.merge_cells("A1:I1")
        ws["A1"] = f"Deal: {deal_name}"
        ws["A1"].font = Font(bold=True, size=14)

    # Row 3: Column headers
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4",
                              fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=10)

    for col_idx, (col_name, col_width) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=3, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width

    # Data rows with tier separators
    current_row = 4
    current_tier = None

    for inv in ranked_investors:
        tier = inv.get("tier", 2)

        # Insert tier separator when tier changes
        if tier != current_tier:
            current_tier = tier
            ws.merge_cells(f"A{current_row}:I{current_row}")
            cell = ws.cell(row=current_row, column=1,
                           value=TIER_LABELS.get(tier, f"Tier {tier}"))
            cell.font = Font(bold=True, size=11)
            fill = TIER_FILLS.get(tier)
            if fill:
                cell.fill = fill
            current_row += 1

        # Investor data row
        row_data = [
            "",                                  # Status (blank for new outreach)
            inv.get("coverage_owner", ""),        # Cov.
            inv.get("investor_name", ""),         # Capital Group
            inv.get("contact_name", ""),          # Contact
            inv.get("email", ""),                 # Email
            "",                                  # Last (blank)
            "",                                  # OM (blank)
            "",                                  # Placement Comments (blank)
            inv.get("match_notes", ""),           # Match Notes
        ]

        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=current_row, column=col_idx, value=value)
            fill = TIER_FILLS.get(tier)
            if fill:
                cell.fill = fill

        current_row += 1

    wb.save(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Export V23 Placement List to XLSX"
    )
    parser.add_argument("--input", required=True,
                        help="JSON file with ranked investors")
    parser.add_argument("--output", required=True,
                        help="Output xlsx path")
    parser.add_argument("--deal-name",
                        help="Deal name for the header row")

    args = parser.parse_args()

    with open(args.input) as f:
        ranked = json.load(f)

    export_placement_list(ranked, args.output, args.deal_name)
    print(json.dumps({
        "status": "ok",
        "output": args.output,
        "count": len(ranked),
    }))


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/test_export_xlsx.py -v
```

Expected: All tests PASS.

---

### Task 6: Run Full Test Suite

- [ ] **Step 1: Run all tests together**

Run:
```bash
cd "${SCRIPTS}" && python -m pytest tests/ -v
```

Expected: All tests across all 4 test files PASS.

- [ ] **Step 2: Fix any failures**

If any tests fail, read the error output, diagnose the root cause, and fix the relevant implementation file. Re-run until all pass.

---

### Task 7: SKILL.md — Placement Engine Skill Definition

**Files:**
- Create: `${SKILL_DIR}/SKILL.md`

- [ ] **Step 1: Write the complete SKILL.md**

Write `${SKILL_DIR}/SKILL.md`:

````markdown
---
name: placement-engine
description: "Generate ranked investor placement lists for commercial real estate capital raises. Use this skill when the user wants to: build a placement list, find investors for a deal, run a placement, generate investor rankings, bootstrap the placement database, import placement files, update placement data, or anything related to V23 capital placement and investor matching. Trigger phrases: 'placement engine', 'placement list', 'investor list', 'who should we approach', 'run placement', 'bootstrap placement', 'import placement', 'update placement', 'find investors for', 'investor matching', 'placement database'."
metadata:
  version: "1.0.0"
  author: "Vanadium Group"
---

# V23 Placement Engine

You are a capital placement assistant for Vanadium Group (V23). Your job is to help the team build ranked investor placement lists for commercial real estate deals by mining historical placement data stored in a local SQLite database (the "living memory").

## Critical Rules

1. **Privacy: Personal contact info stays local.** Individual contact names, emails, and phone numbers are stored only in the local SQLite database and are NEVER sent to external APIs. When preparing investor data for matching/ranking, ALWAYS use the `--strip-pii` flag on the `get-batch` command. Firm/fund names (e.g., "Canyon Partners," "Monomoit") are public entities — they are safe to process in conversation.

2. **Scripts for this skill are at:** `${SKILL_PATH}/scripts/`

3. **Database location:** `~/.v23/placement-engine/placement.db` — create the directory if it does not exist. The database is outside the OneDrive sync folder to prevent corruption.

4. **Python command:** Use `python` (not `python3`) on this Windows machine.

5. **Output files:** Save xlsx exports to the user's current working directory or a path they specify.

6. **Never modify source data.** Placement xlsx files on SharePoint/OneDrive are read-only inputs. All writes go to the SQLite database or output xlsx files.

## Path Resolution

At the start of any workflow, resolve these paths:

```bash
DB_PATH="$HOME/.v23/placement-engine/placement.db"
SCRIPTS="${SKILL_PATH}/scripts"
REALTY_ROOT="C:/Users/tmouh/Vanadium Group LLC/V23 - Database/1- Realty"
```

## Database Schema

The living memory has 3 tables:

**investors** — One row per unique investor entity.
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| canonical_name | TEXT UNIQUE | e.g., "Sagard Real Estate" |
| aliases | TEXT | JSON array of name variations |
| coverage_owner | TEXT | Primary coverage code: HC, MS, SM, YP |
| contact_name | TEXT | Primary contact (PII — local only) |
| email | TEXT | Contact email (PII — local only) |
| phone | TEXT | Contact phone (PII — local only) |
| new_contact | TEXT | Secondary contact (PII) |
| new_contact_role | TEXT | Secondary contact role (PII) |
| new_contact_email | TEXT | Secondary email (PII) |

**deals** — One row per placement campaign.
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| deal_name | TEXT UNIQUE | From file header |
| deal_date | TEXT | ISO date or original format |
| asset_class | TEXT | Office, multifamily, industrial, etc. |
| geography | TEXT | Market/submarket/state |
| strategy | TEXT | Ground-up, value-add, stabilized, etc. |
| capital_stack_position | TEXT | LP equity, pref equity, mezz, debt |
| estimated_equity_need | TEXT | e.g., "$30M" |
| deal_status | TEXT | active, closed, inactive |
| total_contacted | INTEGER | Summary stat |
| pass_count | INTEGER | Summary stat |
| pass_rate | REAL | Summary stat |
| reviewing_count | INTEGER | Summary stat |

**interactions** — One row per investor × deal pair. UNIQUE(investor_id, deal_id).
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| investor_id | INTEGER FK | → investors.id |
| deal_id | INTEGER FK | → deals.id |
| status | TEXT | Pass, Reviewing, Sent, Hold, etc. |
| coverage_code | TEXT | HC, MS, SM, YP for this interaction |
| raw_comments | TEXT | Verbatim Placement Comments |
| old_comments | TEXT | Old Comments / Previous Commentary |
| date_last_contact | TEXT | Last contact date |
| date_om_sent | TEXT | Date OM was sent |

**Status values (union across all historical files):** Pass, Reviewing, Reviewing - Pref, Reviewing - GL, Reviewing - Unlikely, Actively Reviewing, Sent, Initial, Hold, Provided Terms, Next on the list, Issued Terms, Interested, Potential, - (blank/not contacted)

**Coverage codes:** HC, MS, SM, YP (primary), also LO, SL, HC/MS, SM/HC, ? (historical)

---

## Workflow 1: Bootstrap (One-Time)

**Trigger:** User says "bootstrap", "initialize", "load historical data", or "set up the placement engine".

### Step 1: Initialize the database

```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" init
```

### Step 2: Discover placement files

Search the local filesystem (OneDrive-synced copies):

```bash
find "${REALTY_ROOT}/1- Deals" \
  \( -iname "*placement*" -o -iname "*equity list*" \) \
  -iname "*.xlsx" ! -name "~\$*" 2>/dev/null
```

Present the list to the user. Ask:
- Should any files be excluded?
- Are there additional files not found by this search?

### Step 3: Version deduplication

For deals with multiple dated versions of the same placement list (e.g., "Hermit Smith Placement v1.xlsx" through "v5.xlsx"), keep only the most recent version. Sort by filename date or modification time. Present the deduplication decisions to the user for confirmation.

### Step 4: Parse each file

For each file, run:

```bash
python "${SCRIPTS}/parse_xlsx.py" parse "<file_path>"
```

This returns JSON: `{format, deal_header: {deal_name, deal_date}, rows: [{investor_name, status, coverage_code, raw_comments, ...}], source_file}`.

If format is "edge", read the file manually and extract data by hand — present what you find to the user for validation.

### Step 5: Extract deal metadata

For each parsed file, the deal header may only have a name and date. Infer additional metadata from:
- **Folder path**: e.g., `Katy Asian Town/V23 - Bridge Debt` → strategy=debt, geography=Katy TX
- **Context in comments**: pass reasons often mention asset class/geography
- **Deal name**: e.g., "105 N 13th" + folder "DL" → geography=Brooklyn, strategy=development

Present inferred metadata to the user for confirmation/correction:

> **Deal:** 105 N 13th Street
> **Asset class:** Mixed-use / Multifamily
> **Geography:** Brooklyn, NY (Williamsburg)
> **Strategy:** Development
> **Capital stack:** LP equity
> **Inferred from:** folder path + deal name
>
> Does this look right? Any corrections?

### Step 6: Insert into database

For each file, process in order:

1. **Insert the deal** (if not already in DB):
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" insert-deal \
  --name "<deal_name>" --date "<date>" --asset-class "<class>" \
  --geography "<geo>" --strategy "<strategy>" \
  --capital-stack "<position>" --equity-need "<amount>"
```

2. **For each investor row**, check if the investor exists:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" find-investor --name "<investor_name>"
```

3. **If not found**, insert a new investor:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" insert-investor \
  --name "<canonical_name>" --coverage "<coverage_code>" \
  --contact-name "<contact>" --email "<email>" --phone "<phone>" \
  --new-contact "<new_contact>" --new-contact-role "<role>" \
  --new-contact-email "<new_email>"
```

4. **Insert the interaction**:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" insert-interaction \
  --investor-id <ID> --deal-id <ID> --status "<status>" \
  --coverage-code "<cov>" --raw-comments "<comments>" \
  --old-comments "<old>" --date-last-contact "<date>" \
  --date-om-sent "<om_date>"
```

5. **Update deal stats**:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" update-deal-stats --deal-id <ID>
```

### Step 7: Entity reconciliation

After all files are ingested, export the investor list and run fuzzy matching:

```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" get-batch \
  --offset 0 --limit 10000 --strip-pii > /tmp/pe_investors.json

python "${SCRIPTS}/reconcile.py" find-duplicates \
  --input /tmp/pe_investors.json --threshold 75
```

Present each proposed merge to the user:

> **Proposed merge:** "Sagard/Everwest" → "Sagard Real Estate" (score: 85/100)
> Confirm? (y/n)

For each confirmed merge:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" merge \
  --keep-id <KEEP_ID> --merge-id <MERGE_ID>
```

### Step 8: Review

Show final summary:

```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" stats
```

Report: "Bootstrap complete. X unique investors, Y interactions across Z deals."

---

## Workflow 2: Generate Placement List

**Trigger:** User describes a deal and wants investor recommendations (e.g., "build a placement list for...", "who should we approach for...", "run a placement for...").

### Step 1: Accept deal description

The user may provide:
- **Text** — typed in conversation (e.g., "200-unit multifamily value-add in Tampa, $30M equity need")
- **PDF** — upload an OM or investment memo (use the Read tool)
- **Excel** — upload a proforma or deal summary

### Step 2: Extract deal parameters

From the input, extract:
- **Asset class**: office, multifamily, industrial, retail, mixed-use, student housing, IOS, hospitality, etc.
- **Geography**: market, submarket, state
- **Strategy**: ground-up, value-add, stabilized, distressed, repositioning
- **Capital stack position**: LP equity, co-GP, preferred equity, mezz, debt
- **Estimated equity check size**
- **Distinguishing features**: IOS, opportunity zone, programmatic, etc.

### Step 3: Ask clarifying questions

If any critical parameters are missing or ambiguous, ask BEFORE proceeding. Do NOT guess. Examples:
- "Is this LP equity, preferred equity, or both?"
- "What's the approximate equity check size?"
- "Is this a ground-up development or value-add repositioning?"

### Step 4: Confirm parameters

Present the extracted parameters for user confirmation:

> **Deal:** 315 Meserole Street
> **Asset class:** Office / Mixed-use
> **Geography:** Brooklyn, NY (Williamsburg)
> **Strategy:** Value-add / lease-up
> **Capital stack:** LP equity + preferred equity
> **Equity need:** ~$15-20M
>
> Does this look right?

Wait for confirmation or corrections before proceeding.

### Step 5: Query investor batches

Get total investor count:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" stats
```

Then retrieve investors in batches of ~50 with PII stripped:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" get-batch \
  --offset 0 --limit 50 --strip-pii
```

Increment offset by 50 for each subsequent batch until all investors are processed.

### Step 6: Evaluate each batch

For each batch of ~50 investors, read their full interaction history and categorize each investor against the current deal.

**Evaluation criteria — 5 dimensions (weighted equally, all evidence-based):**

1. **Asset class fit**
   - Reviewed / provided terms on similar asset class → positive
   - "We don't do [asset class]" → hard negative
   - No history with this asset class → neutral (not negative)

2. **Geography fit**
   - Active in the same market/region → positive
   - "Not our market" / "we focus on [other region]" → negative
   - National / no geographic restriction → neutral positive

3. **Check size fit**
   - Past deals with similar equity checks → positive
   - "Too small" / "too large" → negative
   - Unknown size range → neutral

4. **Strategy fit**
   - History of similar strategy deals → positive
   - "We only do [other strategy]" → negative
   - Mixed history → neutral

5. **Capital stack fit**
   - History in same position (equity, pref, mezz, debt) → positive
   - "We only do [other position]" → hard negative
   - Unknown → neutral

**Additional signals:**
- **Recency**: Interactions from the last 6 months weigh more than older ones. A 2024 pass is less predictive than a 2026 pass.
- **Structural vs. deal-specific**: "We don't do office" = structural hard signal. "Pricing didn't work on that one" = deal-specific soft signal that may not apply.
- **Positive actions**: "Provided Terms", "Actively Reviewing", expressed interest in programmatic deals = strong positive.
- **Repetition**: 3+ passes on similar deals = strong negative pattern. One pass = could be timing.

**Categorize each investor as:**
- **Strong match**: 3+ positive dimensions, no hard negatives. Clear behavioral evidence of fit.
- **Possible match**: Mixed signals, limited history, or 1-2 positive dimensions. Worth approaching but less certain.
- **Likely mismatch**: More negative than positive signals. Not a hard no, but low probability.
- **Definite mismatch**: Hard structural conflicts — explicitly stated they never do this asset class, geography, or capital stack position. EXCLUDE from output.

### Step 7: Merge batch results

After all batches are processed:
1. Combine all "strong match" → **Tier 1** (rank by strength of evidence)
2. Combine all "possible match" → **Tier 2** (rank by likelihood)
3. Combine all "likely mismatch" → **Tier 3** (flag as long shots)
4. "Definite mismatch" → **excluded entirely** (do not show)

### Step 8: Present ranked list

Display in conversation, grouped by tier:

**Tier 1 — Strong Match** (X investors)
1. **[Investor Name]** — [1-2 sentence reasoning]. [Key history: "Provided terms on [similar deal], active in [geography], [check size] range"]
2. ...

**Tier 2 — Possible Match** (X investors)
1. **[Investor Name]** — [Reasoning]. [What's known vs. uncertain]
2. ...

**Tier 3 — Long Shot** (X investors)
1. **[Investor Name]** — [Why included despite weak signals]. [Warning: "Passed on 3 similar deals"]
2. ...

### Step 9: Export to xlsx

When the user asks to export, prepare the ranked list with contact info:

1. Retrieve full investor data (with PII) for the ranked investors:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" get-batch \
  --offset 0 --limit 10000
```

2. Build a JSON array of ranked investors with the contact info injected, then write to a temp file:
```bash
echo '<JSON array>' > /tmp/pe_ranked.json
```

3. Export:
```bash
python "${SCRIPTS}/export_xlsx.py" \
  --input /tmp/pe_ranked.json \
  --output "<deal_name> Placement List.xlsx" \
  --deal-name "<deal_name>"
```

4. Provide the file path to the user.

---

## Workflow 3: Import Updated Placement List

**Trigger:** User says "import", "update the placement data", or provides a new/updated placement file for an existing deal.

### Step 1: Parse the file

```bash
python "${SCRIPTS}/parse_xlsx.py" parse "<file_path>"
```

### Step 2: Identify the deal

Match the parsed deal name against existing deals in the database. If the deal exists, proceed with diff. If new, treat as a new deal (same as bootstrap Step 6).

### Step 3: Compute diff

Get existing interactions for the deal:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" get-deal-interactions \
  --deal-id <DEAL_ID>
```

Compare against the new file's rows. Report to the user:
- **New investors** added to the list since last import
- **Status changes** (e.g., Reviewing → Pass)
- **New or updated comments** / pass reasons
- **New contact information**

### Step 4: Apply updates on confirmation

After user confirms:

For **new investors**: insert investor + interaction (same as bootstrap Step 6).

For **updated interactions**:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" update-interaction \
  --id <INTERACTION_ID> --status "<new_status>" \
  --raw-comments "<new_comments>"
```

Update deal stats:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" update-deal-stats \
  --deal-id <DEAL_ID>
```

---

## Example Interactions

**"Bootstrap the placement engine"**
→ Workflow 1. Discover ~70 xlsx files, parse each, insert into DB, reconcile entities, show stats.

**"Build a placement list for a 200-unit multifamily value-add in Tampa, $30M equity need"**
→ Workflow 2. Extract params → confirm → batch-process all investors → present tiered list → offer export.

**"Import the updated Tarpon Springs placement list"**
→ Workflow 3. Parse file → diff against existing → show changes → apply on confirmation.

**"Who has been active on industrial deals in Texas?"**
→ Ad-hoc query. Get all investors, filter for those with interactions on industrial/TX deals, show their history.

**"How many investors are in the database?"**
→ Quick stat: `python db.py --db-path "$DB_PATH" stats`

**"Export the last placement list to Excel"**
→ Re-export the most recent ranking results to xlsx.

## Troubleshooting

- **Cloud-only files (errno 22 / "Invalid argument")**: The file is not synced locally from OneDrive. Use SharePoint MCP to read it: `mcp__7c83d698-13fd-42a4-9813-685c8f8a4ba7__read_resource`. Or trigger a local sync in OneDrive.
- **Edge case xlsx format (format="edge")**: Non-standard layout. Read the file manually with openpyxl and extract data by hand, presenting findings to the user for validation.
- **Entity reconciliation misses**: If fuzzy matching misses a known alias, manually merge: `python db.py merge --keep-id X --merge-id Y`
- **UNIQUE constraint error on insert-interaction**: The investor already has an interaction for that deal. Use `update-interaction` instead.
- **Database corruption**: The database uses WAL mode for crash resistance. If corrupted beyond repair, delete `~/.v23/placement-engine/placement.db` and re-run bootstrap.
- **Context too long during batch matching**: Reduce batch size from 50 to 25 investors per batch.
- **Missing deal metadata**: If the deal header doesn't parse cleanly, the user can provide metadata manually during bootstrap.
````

- [ ] **Step 2: Verify the skill loads**

After writing SKILL.md, verify it appears in the available skills list. The skill should show as `v23:placement-engine` in a new Claude Code session. If it does not appear, check:
1. The SKILL.md is in the correct directory (sibling to `comp-search/`)
2. The frontmatter is valid YAML
3. Restart Claude Code to pick up the new skill

---

### Task 8: Integration Verification with Real Data

**Files:** None (read-only verification)

This task verifies the scripts work against real local placement files.

- [ ] **Step 1: Parse a real Format A file**

Run:
```bash
python "${SCRIPTS}/parse_xlsx.py" parse \
  "C:/Users/tmouh/Vanadium Group LLC/V23 - Database/1- Realty/1- Deals/0 105 North 13 Street - DL/4. Equity Placement/105 N 13 Street - Placement List.xlsx"
```

Expected: JSON output with format "A", a populated deal_header, and rows with investor_name, status, coverage_code, raw_comments fields. If the file is cloud-only (errno 22), try a different file:

```bash
python "${SCRIPTS}/parse_xlsx.py" parse \
  "C:/Users/tmouh/Vanadium Group LLC/V23 - Database/1- Realty/1- Deals/0 NPV FL IOS Deals/Tarpon Springs Placement List - 2026-02-26.xlsx"
```

Review the output. Verify:
- Investor names are correctly extracted
- Status values make sense (Pass, Reviewing, Sent, etc.)
- Comments are verbatim from the spreadsheet
- No data corruption

- [ ] **Step 2: Run full pipeline on the parsed data**

Using the output from Step 1, insert into a test database:

```bash
# Initialize a test DB
python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db init

# Insert a deal (use data from the parsed output)
python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db insert-deal \
  --name "<deal_name_from_output>" --asset-class "<inferred>"

# Insert a few investors and interactions from the parsed rows
# (repeat for 3-5 rows to verify the pipeline)
python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db insert-investor \
  --name "<investor_name>" --coverage "<cov>"

python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db insert-interaction \
  --investor-id 1 --deal-id 1 --status "<status>" \
  --raw-comments "<comments>"

# Verify stats
python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db stats

# Get batch (verify data comes back correctly)
python "${SCRIPTS}/db.py" --db-path /tmp/pe_integration_test.db get-batch \
  --offset 0 --limit 50 --strip-pii
```

Expected: Stats show correct counts. Batch data includes interaction history joined with deal metadata.

- [ ] **Step 3: Test export pipeline**

```bash
# Write a small ranked JSON for export test
echo '[{"investor_name":"Test Investor","coverage_owner":"HC","contact_name":"John","email":"j@t.com","match_notes":"Strong fit - multifamily focus in FL","tier":1}]' > /tmp/pe_ranked_test.json

python "${SCRIPTS}/export_xlsx.py" \
  --input /tmp/pe_ranked_test.json \
  --output /tmp/pe_integration_test_output.xlsx \
  --deal-name "Integration Test Deal"
```

Expected: xlsx file created at `/tmp/pe_integration_test_output.xlsx`. Open it to verify:
- Deal name in header row
- Correct column headers (Status, Cov., Capital Group, Contact, Email, Last, OM, Placement Comments, Match Notes)
- Tier separator row
- Investor data in correct columns

- [ ] **Step 4: Clean up**

```bash
rm -f /tmp/pe_integration_test.db /tmp/pe_investors.json \
      /tmp/pe_ranked_test.json /tmp/pe_integration_test_output.xlsx
```

---

## Notes for the Implementing Engineer

1. **This is NOT a git repository.** The working directory is a OneDrive-synced folder. Do not run `git init` or try to commit. Just create the files directly.

2. **Python is `python`, not `python3`** on this Windows machine.

3. **The skill directory** must be a sibling of the existing `comp-search/` skill directory. Use the dynamic discovery command in the Path Definitions section if the session ID has changed.

4. **Test commands** should be run from the `scripts/` directory so that `sys.path.insert` in conftest.py resolves correctly: `cd "${SCRIPTS}" && python -m pytest tests/ -v`

5. **The database path** (`~/.v23/placement-engine/placement.db`) is outside the OneDrive folder intentionally. SQLite and cloud sync do not mix well.

6. **Real data sensitivity:** The local placement xlsx files contain real investor contact information. Do not copy them to temp directories or send their contents to external services. The `--strip-pii` flag exists for this reason.
