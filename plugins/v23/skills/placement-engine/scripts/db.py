"""V23 Placement Engine — SQLite database layer.

Provides functions for managing investors, deals, and interactions
for a commercial real estate placement engine, plus a CLI.
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys


# ---------------------------------------------------------------------------
# 1. get_connection
# ---------------------------------------------------------------------------

def get_connection(db_path: str) -> sqlite3.Connection:
    """Return a sqlite3 connection with WAL mode, foreign keys ON, Row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------------------------------------------------------------------
# 2. create_database
# ---------------------------------------------------------------------------

def create_database(db_path: str) -> None:
    """Create investors, deals, and interactions tables. Idempotent."""
    conn = get_connection(db_path)
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS investors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                canonical_name TEXT NOT NULL UNIQUE,
                aliases TEXT DEFAULT '[]',
                coverage_owner TEXT
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
                pass_reason TEXT,
                date_last_contact TEXT,
                date_om_sent TEXT,
                FOREIGN KEY (investor_id) REFERENCES investors(id),
                FOREIGN KEY (deal_id) REFERENCES deals(id),
                UNIQUE(investor_id, deal_id)
            );

            CREATE INDEX IF NOT EXISTS idx_interaction_investor
                ON interactions(investor_id);
            CREATE INDEX IF NOT EXISTS idx_interaction_deal
                ON interactions(deal_id);
            CREATE INDEX IF NOT EXISTS idx_interaction_investor_deal
                ON interactions(investor_id, deal_id);

            CREATE TABLE IF NOT EXISTS source_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                deal_id INTEGER,
                last_imported TEXT,
                file_modified TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );
        """)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 3. insert_deal
# ---------------------------------------------------------------------------

def insert_deal(
    db_path: str,
    deal_name: str,
    deal_date: str = None,
    asset_class: str = None,
    geography: str = None,
    strategy: str = None,
    capital_stack_position: str = None,
    estimated_equity_need: str = None,
    deal_status: str = "active",
) -> int:
    """Insert a deal and return its id. deal_name must be unique."""
    conn = get_connection(db_path)
    try:
        cur = conn.execute(
            """INSERT INTO deals
               (deal_name, deal_date, asset_class, geography, strategy,
                capital_stack_position, estimated_equity_need, deal_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (deal_name, deal_date, asset_class, geography, strategy,
             capital_stack_position, estimated_equity_need, deal_status),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 4. insert_investor
# ---------------------------------------------------------------------------

def insert_investor(
    db_path: str,
    canonical_name: str,
    aliases: list = None,
    coverage_owner: str = None,
) -> int:
    """Insert an investor and return its id. canonical_name must be unique.
    aliases is stored as a JSON array."""
    if aliases is None:
        aliases = []
    aliases_json = json.dumps(aliases)
    conn = get_connection(db_path)
    try:
        cur = conn.execute(
            """INSERT INTO investors
               (canonical_name, aliases, coverage_owner)
               VALUES (?, ?, ?)""",
            (canonical_name, aliases_json, coverage_owner),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 5. find_investor
# ---------------------------------------------------------------------------

def find_investor(db_path: str, name: str):
    """Find investor by canonical_name or by searching aliases JSON.
    Return dict or None."""
    conn = get_connection(db_path)
    try:
        # Try canonical_name first
        row = conn.execute(
            "SELECT * FROM investors WHERE canonical_name = ?", (name,)
        ).fetchone()
        if row:
            return dict(row)
        # Search aliases
        rows = conn.execute("SELECT * FROM investors").fetchall()
        for row in rows:
            aliases = json.loads(row["aliases"])
            if name in aliases:
                return dict(row)
        return None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 6. insert_interaction
# ---------------------------------------------------------------------------

def insert_interaction(
    db_path: str,
    investor_id: int,
    deal_id: int,
    status: str = None,
    coverage_code: str = None,
    raw_comments: str = None,
    old_comments: str = None,
    pass_reason: str = None,
    date_last_contact: str = None,
    date_om_sent: str = None,
) -> int:
    """Insert an interaction and return its id. UNIQUE(investor_id, deal_id)."""
    conn = get_connection(db_path)
    try:
        cur = conn.execute(
            """INSERT INTO interactions
               (investor_id, deal_id, status, coverage_code,
                raw_comments, old_comments, pass_reason,
                date_last_contact, date_om_sent)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (investor_id, deal_id, status, coverage_code,
             raw_comments, old_comments, pass_reason,
             date_last_contact, date_om_sent),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 7. get_investor_batch
# ---------------------------------------------------------------------------

def get_investor_batch(db_path: str, offset: int, limit: int) -> list:
    """Return list of investor dicts, each with an 'interactions' list.

    Interactions include deal metadata (deal_name, deal_date, asset_class,
    geography, strategy, capital_stack_position).
    Investors ordered by id. Interactions ordered by deal_date DESC.
    """
    conn = get_connection(db_path)
    try:
        investors = conn.execute(
            "SELECT * FROM investors ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()

        result = []
        for inv in investors:
            inv_dict = dict(inv)
            interactions = conn.execute(
                """SELECT i.*, d.deal_name, d.deal_date, d.asset_class,
                          d.geography, d.strategy, d.capital_stack_position
                   FROM interactions i
                   JOIN deals d ON i.deal_id = d.id
                   WHERE i.investor_id = ?
                   ORDER BY d.deal_date DESC""",
                (inv["id"],),
            ).fetchall()
            inv_dict["interactions"] = [dict(r) for r in interactions]
            result.append(inv_dict)
        return result
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 8. merge_investors
# ---------------------------------------------------------------------------

def merge_investors(db_path: str, keep_id: int, merge_id: int) -> None:
    """Merge merge_id investor into keep_id.

    - Move interactions from merge_id to keep_id
    - For duplicate deals, keep the richer data (more non-null/non-empty fields)
    - Add merged investor's canonical_name to keep investor's aliases
    - Delete the merged investor
    """
    conn = get_connection(db_path)
    try:
        # Get the merged investor's name and aliases
        merged = conn.execute(
            "SELECT * FROM investors WHERE id = ?", (merge_id,)
        ).fetchone()
        keep = conn.execute(
            "SELECT * FROM investors WHERE id = ?", (keep_id,)
        ).fetchone()

        if not keep:
            raise ValueError(f"Keep investor {keep_id} not found")
        if not merged:
            raise ValueError(f"Merge investor {merge_id} not found")

        # Get interactions for both
        merge_interactions = conn.execute(
            "SELECT * FROM interactions WHERE investor_id = ?", (merge_id,)
        ).fetchall()
        keep_interactions = conn.execute(
            "SELECT * FROM interactions WHERE investor_id = ?", (keep_id,)
        ).fetchall()

        keep_deal_map = {row["deal_id"]: dict(row) for row in keep_interactions}

        for mi in merge_interactions:
            mi_dict = dict(mi)
            deal_id = mi_dict["deal_id"]

            if deal_id in keep_deal_map:
                # Duplicate deal — keep richer data
                ki = keep_deal_map[deal_id]
                merged_fields = _merge_interaction_fields(ki, mi_dict)
                # Update the keep interaction with merged fields
                conn.execute(
                    """UPDATE interactions SET
                       status=?, coverage_code=?, raw_comments=?,
                       old_comments=?, pass_reason=?,
                       date_last_contact=?, date_om_sent=?
                       WHERE id=?""",
                    (
                        merged_fields["status"],
                        merged_fields["coverage_code"],
                        merged_fields["raw_comments"],
                        merged_fields["old_comments"],
                        merged_fields["pass_reason"],
                        merged_fields["date_last_contact"],
                        merged_fields["date_om_sent"],
                        ki["id"],
                    ),
                )
                # Delete the duplicate from merge_id
                conn.execute(
                    "DELETE FROM interactions WHERE id = ?", (mi_dict["id"],)
                )
            else:
                # No conflict — just reassign
                conn.execute(
                    "UPDATE interactions SET investor_id = ? WHERE id = ?",
                    (keep_id, mi_dict["id"]),
                )

        # Add merged investor's name (and aliases) to keep's aliases
        keep_aliases = json.loads(keep["aliases"])
        merged_aliases = json.loads(merged["aliases"])
        # Add canonical_name and any aliases from the merged investor
        new_aliases = list(keep_aliases)
        if merged["canonical_name"] not in new_aliases:
            new_aliases.append(merged["canonical_name"])
        for a in merged_aliases:
            if a not in new_aliases:
                new_aliases.append(a)

        conn.execute(
            "UPDATE investors SET aliases = ? WHERE id = ?",
            (json.dumps(new_aliases), keep_id),
        )

        # Delete merged investor
        conn.execute("DELETE FROM investors WHERE id = ?", (merge_id,))
        conn.commit()
    finally:
        conn.close()


def _merge_interaction_fields(keep: dict, merge: dict) -> dict:
    """Given two interaction dicts for the same deal, return merged fields
    preferring the richer (more non-empty) record's data."""
    fields = [
        "status", "coverage_code", "raw_comments",
        "old_comments", "pass_reason", "date_last_contact", "date_om_sent",
    ]

    def richness(d):
        return sum(1 for f in fields if d.get(f))

    if richness(merge) > richness(keep):
        primary, secondary = merge, keep
    else:
        primary, secondary = keep, merge

    result = {}
    for f in fields:
        # Use primary value if non-empty, else fall back to secondary
        val = primary.get(f)
        if not val:
            val = secondary.get(f)
        result[f] = val
    return result


# ---------------------------------------------------------------------------
# 9. get_database_stats
# ---------------------------------------------------------------------------

def get_database_stats(db_path: str) -> dict:
    """Return dict with investor_count, deal_count, interaction_count."""
    conn = get_connection(db_path)
    try:
        inv = conn.execute("SELECT COUNT(*) AS c FROM investors").fetchone()["c"]
        deals = conn.execute("SELECT COUNT(*) AS c FROM deals").fetchone()["c"]
        inter = conn.execute("SELECT COUNT(*) AS c FROM interactions").fetchone()["c"]
        return {
            "investor_count": inv,
            "deal_count": deals,
            "interaction_count": inter,
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 10. update_interaction
# ---------------------------------------------------------------------------

_ALLOWED_INTERACTION_UPDATE_FIELDS = {
    "status", "coverage_code", "raw_comments",
    "old_comments", "pass_reason", "date_last_contact", "date_om_sent",
}


def update_interaction(db_path: str, interaction_id: int, **updates) -> None:
    """Update allowed fields on an interaction. Raises ValueError for disallowed fields."""
    if not updates:
        return
    bad_fields = set(updates.keys()) - _ALLOWED_INTERACTION_UPDATE_FIELDS
    if bad_fields:
        raise ValueError(f"Cannot update fields: {bad_fields}")

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [interaction_id]

    conn = get_connection(db_path)
    try:
        cur = conn.execute(
            f"UPDATE interactions SET {set_clause} WHERE id = ?", values
        )
        if cur.rowcount == 0:
            raise ValueError(f"Interaction {interaction_id} not found")
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 11. update_deal_stats
# ---------------------------------------------------------------------------

def update_deal_stats(db_path: str, deal_id: int) -> None:
    """Recalculate total_contacted, pass_count, pass_rate, reviewing_count."""
    conn = get_connection(db_path)
    try:
        total = conn.execute(
            "SELECT COUNT(*) AS c FROM interactions WHERE deal_id = ?",
            (deal_id,),
        ).fetchone()["c"]

        pass_count = conn.execute(
            "SELECT COUNT(*) AS c FROM interactions WHERE deal_id = ? AND status LIKE '%Pass%'",
            (deal_id,),
        ).fetchone()["c"]

        reviewing_count = conn.execute(
            "SELECT COUNT(*) AS c FROM interactions WHERE deal_id = ? AND status LIKE '%Reviewing%'",
            (deal_id,),
        ).fetchone()["c"]

        pass_rate = (pass_count / total) if total > 0 else 0.0

        conn.execute(
            """UPDATE deals SET
               total_contacted = ?, pass_count = ?, pass_rate = ?, reviewing_count = ?
               WHERE id = ?""",
            (total, pass_count, pass_rate, reviewing_count, deal_id),
        )
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 12. get_deal_interactions
# ---------------------------------------------------------------------------

def get_deal_interactions(db_path: str, deal_id: int) -> list:
    """Return interactions for a deal, joined with investor canonical_name."""
    conn = get_connection(db_path)
    try:
        rows = conn.execute(
            """SELECT i.*, inv.canonical_name AS investor_name
               FROM interactions i
               JOIN investors inv ON i.investor_id = inv.id
               WHERE i.deal_id = ?""",
            (deal_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 12a. record_source_file
# ---------------------------------------------------------------------------

def record_source_file(db_path: str, file_path: str, deal_id: int,
                       file_modified: str = None) -> int:
    """Record or update a source file entry. Returns the source_file id.

    file_modified is stored as integer seconds (Unix timestamp string).
    If not provided, reads the file's current mtime from disk.
    """
    now = datetime.datetime.now().isoformat()
    if file_modified is None:
        file_modified = str(int(os.path.getmtime(file_path)))
    conn = get_connection(db_path)
    try:
        existing = conn.execute(
            "SELECT id FROM source_files WHERE file_path = ?", (file_path,)
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE source_files SET deal_id=?, last_imported=?,
                   file_modified=? WHERE id=?""",
                (deal_id, now, file_modified, existing["id"]),
            )
            conn.commit()
            return existing["id"]
        else:
            cur = conn.execute(
                """INSERT INTO source_files
                   (file_path, deal_id, last_imported, file_modified)
                   VALUES (?, ?, ?, ?)""",
                (file_path, deal_id, now, file_modified),
            )
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 12b. check_source_freshness
# ---------------------------------------------------------------------------

def check_source_freshness(db_path: str) -> list:
    """Return list of source files modified since last import.

    Compares file mtime (integer seconds) against stored value.
    """
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM source_files").fetchall()
        stale = []
        for row in rows:
            fp = row["file_path"]
            if not os.path.exists(fp):
                continue
            current_mtime = str(int(os.path.getmtime(fp)))
            if current_mtime != row["file_modified"]:
                stale.append({
                    "file_path": fp,
                    "deal_id": row["deal_id"],
                    "last_imported": row["last_imported"],
                    "stored_modified": row["file_modified"],
                    "current_modified": current_mtime,
                })
        return stale
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _default_db_path() -> str:
    return os.path.join(os.path.expanduser("~"), ".v23", "placement-engine", "placement.db")


def _build_parser() -> argparse.ArgumentParser:
    # Parent parser for --db-path on subcommands (uses SUPPRESS so it only
    # overrides the root parser's value when explicitly provided).
    db_parent = argparse.ArgumentParser(add_help=False)
    db_parent.add_argument(
        "--db-path", default=argparse.SUPPRESS,
        help="Path to SQLite database",
    )

    parser = argparse.ArgumentParser(
        description="V23 Placement Engine DB CLI",
    )
    parser.add_argument(
        "--db-path", default=_default_db_path(),
        help="Path to SQLite database",
    )
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", parents=[db_parent], help="Create / initialize the database")

    # insert-deal
    p = sub.add_parser("insert-deal", parents=[db_parent], help="Insert a deal")
    p.add_argument("--deal-name", required=True)
    p.add_argument("--deal-date")
    p.add_argument("--asset-class")
    p.add_argument("--geography")
    p.add_argument("--strategy")
    p.add_argument("--capital-stack-position")
    p.add_argument("--estimated-equity-need")
    p.add_argument("--deal-status", default="active")

    # insert-investor
    p = sub.add_parser("insert-investor", parents=[db_parent], help="Insert an investor")
    p.add_argument("--canonical-name", required=True)
    p.add_argument("--aliases", nargs="*", default=[])
    p.add_argument("--coverage-owner")

    # insert-interaction
    p = sub.add_parser("insert-interaction", parents=[db_parent], help="Insert an interaction")
    p.add_argument("--investor-id", type=int, required=True)
    p.add_argument("--deal-id", type=int, required=True)
    p.add_argument("--status")
    p.add_argument("--coverage-code")
    p.add_argument("--raw-comments")
    p.add_argument("--old-comments")
    p.add_argument("--pass-reason")
    p.add_argument("--date-last-contact")
    p.add_argument("--date-om-sent")

    # find-investor
    p = sub.add_parser("find-investor", parents=[db_parent], help="Find an investor by name/alias")
    p.add_argument("--name", required=True)

    # get-batch
    p = sub.add_parser("get-batch", parents=[db_parent], help="Get a batch of investors with interactions")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--limit", type=int, default=100)

    # merge
    p = sub.add_parser("merge", parents=[db_parent], help="Merge two investors")
    p.add_argument("--keep-id", type=int, required=True)
    p.add_argument("--merge-id", type=int, required=True)

    # stats
    sub.add_parser("stats", parents=[db_parent], help="Get database statistics")

    # get-deal-interactions
    p = sub.add_parser("get-deal-interactions", parents=[db_parent], help="Get interactions for a deal")
    p.add_argument("--deal-id", type=int, required=True)

    # update-interaction
    p = sub.add_parser("update-interaction", parents=[db_parent], help="Update an interaction")
    p.add_argument("--interaction-id", type=int, required=True)
    p.add_argument("--status")
    p.add_argument("--coverage-code")
    p.add_argument("--raw-comments")
    p.add_argument("--old-comments")
    p.add_argument("--pass-reason")
    p.add_argument("--date-last-contact")
    p.add_argument("--date-om-sent")

    # update-deal-stats
    p = sub.add_parser("update-deal-stats", parents=[db_parent], help="Recalculate deal stats")
    p.add_argument("--deal-id", type=int, required=True)

    # record-source-file
    p = sub.add_parser("record-source-file", parents=[db_parent], help="Record or update a source file entry")
    p.add_argument("--file-path", required=True)
    p.add_argument("--deal-id", type=int, required=True)
    p.add_argument("--file-modified", required=True)

    # check-source-freshness
    sub.add_parser("check-source-freshness", parents=[db_parent], help="Check source files for staleness")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    db_path = args.db_path

    if args.command == "init":
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        create_database(db_path)
        print(json.dumps({"status": "ok"}))

    elif args.command == "insert-deal":
        deal_id = insert_deal(
            db_path, args.deal_name,
            deal_date=args.deal_date,
            asset_class=args.asset_class,
            geography=args.geography,
            strategy=args.strategy,
            capital_stack_position=args.capital_stack_position,
            estimated_equity_need=args.estimated_equity_need,
            deal_status=args.deal_status,
        )
        print(json.dumps({"id": deal_id}))

    elif args.command == "insert-investor":
        inv_id = insert_investor(
            db_path, args.canonical_name,
            aliases=args.aliases if args.aliases else None,
            coverage_owner=args.coverage_owner,
        )
        print(json.dumps({"id": inv_id}))

    elif args.command == "insert-interaction":
        iid = insert_interaction(
            db_path, args.investor_id, args.deal_id,
            status=args.status,
            coverage_code=args.coverage_code,
            raw_comments=args.raw_comments,
            old_comments=args.old_comments,
            pass_reason=args.pass_reason,
            date_last_contact=args.date_last_contact,
            date_om_sent=args.date_om_sent,
        )
        print(json.dumps({"id": iid}))

    elif args.command == "find-investor":
        result = find_investor(db_path, args.name)
        if result is None:
            print(json.dumps(None))
        else:
            print(json.dumps(result))

    elif args.command == "get-batch":
        batch = get_investor_batch(db_path, args.offset, args.limit)
        print(json.dumps(batch))

    elif args.command == "merge":
        merge_investors(db_path, args.keep_id, args.merge_id)
        print(json.dumps({"status": "ok"}))

    elif args.command == "stats":
        stats = get_database_stats(db_path)
        print(json.dumps(stats))

    elif args.command == "get-deal-interactions":
        interactions = get_deal_interactions(db_path, args.deal_id)
        print(json.dumps(interactions))

    elif args.command == "update-interaction":
        updates = {}
        for field in _ALLOWED_INTERACTION_UPDATE_FIELDS:
            val = getattr(args, field.replace("-", "_"), None)
            if val is not None:
                updates[field] = val
        update_interaction(db_path, args.interaction_id, **updates)
        print(json.dumps({"status": "ok"}))

    elif args.command == "update-deal-stats":
        update_deal_stats(db_path, args.deal_id)
        print(json.dumps({"status": "ok"}))

    elif args.command == "record-source-file":
        sf_id = record_source_file(
            db_path, args.file_path, args.deal_id, args.file_modified,
        )
        print(json.dumps({"id": sf_id}))

    elif args.command == "check-source-freshness":
        stale = check_source_freshness(db_path)
        print(json.dumps(stale))


if __name__ == "__main__":
    main()
