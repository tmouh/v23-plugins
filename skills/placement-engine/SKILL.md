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

**interactions** — One row per investor x deal pair. UNIQUE(investor_id, deal_id).
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| investor_id | INTEGER FK | -> investors.id |
| deal_id | INTEGER FK | -> deals.id |
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
- **Folder path**: e.g., `Katy Asian Town/V23 - Bridge Debt` -> strategy=debt, geography=Katy TX
- **Context in comments**: pass reasons often mention asset class/geography
- **Deal name**: e.g., "105 N 13th" + folder "DL" -> geography=Brooklyn, strategy=development

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
  --deal-name "<deal_name>" --deal-date "<date>" --asset-class "<class>" \
  --geography "<geo>" --strategy "<strategy>" \
  --capital-stack-position "<position>" --estimated-equity-need "<amount>"
```

2. **For each investor row**, check if the investor exists:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" find-investor --name "<investor_name>"
```

3. **If not found**, insert a new investor:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" insert-investor \
  --canonical-name "<canonical_name>" --coverage-owner "<coverage_code>" \
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

> **Proposed merge:** "Sagard/Everwest" -> "Sagard Real Estate" (score: 85/100)
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
   - Reviewed / provided terms on similar asset class -> positive
   - "We don't do [asset class]" -> hard negative
   - No history with this asset class -> neutral (not negative)

2. **Geography fit**
   - Active in the same market/region -> positive
   - "Not our market" / "we focus on [other region]" -> negative
   - National / no geographic restriction -> neutral positive

3. **Check size fit**
   - Past deals with similar equity checks -> positive
   - "Too small" / "too large" -> negative
   - Unknown size range -> neutral

4. **Strategy fit**
   - History of similar strategy deals -> positive
   - "We only do [other strategy]" -> negative
   - Mixed history -> neutral

5. **Capital stack fit**
   - History in same position (equity, pref, mezz, debt) -> positive
   - "We only do [other position]" -> hard negative
   - Unknown -> neutral

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
1. Combine all "strong match" -> **Tier 1** (rank by strength of evidence)
2. Combine all "possible match" -> **Tier 2** (rank by likelihood)
3. Combine all "likely mismatch" -> **Tier 3** (flag as long shots)
4. "Definite mismatch" -> **excluded entirely** (do not show)

### Step 8: Present ranked list

Display in conversation, grouped by tier:

**Tier 1 -- Strong Match** (X investors)
1. **[Investor Name]** — [1-2 sentence reasoning]. [Key history: "Provided terms on [similar deal], active in [geography], [check size] range"]
2. ...

**Tier 2 -- Possible Match** (X investors)
1. **[Investor Name]** — [Reasoning]. [What's known vs. uncertain]
2. ...

**Tier 3 -- Long Shot** (X investors)
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
- **Status changes** (e.g., Reviewing -> Pass)
- **New or updated comments** / pass reasons
- **New contact information**

### Step 4: Apply updates on confirmation

After user confirms:

For **new investors**: insert investor + interaction (same as bootstrap Step 6).

For **updated interactions**:
```bash
python "${SCRIPTS}/db.py" --db-path "$DB_PATH" update-interaction \
  --interaction-id <INTERACTION_ID> --status "<new_status>" \
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
-> Workflow 1. Discover ~70 xlsx files, parse each, insert into DB, reconcile entities, show stats.

**"Build a placement list for a 200-unit multifamily value-add in Tampa, $30M equity need"**
-> Workflow 2. Extract params -> confirm -> batch-process all investors -> present tiered list -> offer export.

**"Import the updated Tarpon Springs placement list"**
-> Workflow 3. Parse file -> diff against existing -> show changes -> apply on confirmation.

**"Who has been active on industrial deals in Texas?"**
-> Ad-hoc query. Get all investors, filter for those with interactions on industrial/TX deals, show their history.

**"How many investors are in the database?"**
-> Quick stat: `python "${SCRIPTS}/db.py" --db-path "$DB_PATH" stats`

**"Export the last placement list to Excel"**
-> Re-export the most recent ranking results to xlsx.

## Troubleshooting

- **Cloud-only files (errno 22 / "Invalid argument")**: The file is not synced locally from OneDrive. Use SharePoint MCP to read it: `mcp__7c83d698-13fd-42a4-9813-685c8f8a4ba7__read_resource`. Or trigger a local sync in OneDrive.
- **Edge case xlsx format (format="edge")**: Non-standard layout. Read the file manually with openpyxl and extract data by hand, presenting findings to the user for validation.
- **Entity reconciliation misses**: If fuzzy matching misses a known alias, manually merge: `python "${SCRIPTS}/db.py" --db-path "$DB_PATH" merge --keep-id X --merge-id Y`
- **UNIQUE constraint error on insert-interaction**: The investor already has an interaction for that deal. Use `update-interaction` instead.
- **Database corruption**: The database uses WAL mode for crash resistance. If corrupted beyond repair, delete `~/.v23/placement-engine/placement.db` and re-run bootstrap.
- **Context too long during batch matching**: Reduce batch size from 50 to 25 investors per batch.
- **Missing deal metadata**: If the deal header doesn't parse cleanly, the user can provide metadata manually during bootstrap.
