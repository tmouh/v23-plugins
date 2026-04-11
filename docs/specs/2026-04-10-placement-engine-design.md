# V23 Placement Engine — Design Specification

**Date:** 2026-04-10
**Status:** Approved
**Type:** Claude Code Skill + Local SQLite Database

---

## Problem

V23 Group runs capital placement processes for commercial real estate deals, sourcing equity and debt partners from a network of 250+ investor groups. For every new deal, the team of 3 manually builds a placement list: researching which investors fit the deal profile, cross-referencing past outreach history, recalling who passed and why, and ranking targets by likelihood of interest.

The institutional knowledge about investor preferences lives in two places:

1. **People's heads** — the primary source. The team knows from experience who does what, who's active, who passed and why.
2. **70+ historical placement list spreadsheets** — scattered across the V23 deal folder system on SharePoint (`V23 Database > 1- Realty > 1- Deals > [Deal Name] > [Placement Folder]`). These are a record of what happened, but the decision of who to approach comes from accumulated experience.

The goal is to externalize and systematize the mental model by mining the historical placement data for patterns that currently live in memory.

---

## Solution Overview

A Claude Code skill backed by a local SQLite database (the "living memory") that:

1. Ingests historical placement lists to build an investor intelligence database
2. Accepts deal descriptions in any format (text, PDF, xlsx)
3. Generates ranked placement lists with match reasoning
4. Exports to xlsx in the team's existing placement list format
5. Updates incrementally as new deal outcomes are imported

Investor contact information never leaves the local machine. Deal parameter extraction uses the Claude API. All matching intelligence is applied at query time by Claude reading raw investor history from the living memory.

---

## Users

3 people on the V23 placement team, identified by coverage codes:

- **HC**
- **MS**
- **SM** (+ occasional **YP**)

Each person owns relationships with specific investors. The coverage code is stored per interaction and pre-populated on generated placement lists.

---

## Living Memory Schema

### Table: `investors`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| canonical_name | TEXT NOT NULL | The canonical investor name (e.g., "Sagard Real Estate") |
| aliases | TEXT | JSON array of known name variations (e.g., ["Sagard/Everwest", "Sagard RE"]) |
| coverage_owner | TEXT | Primary coverage code (HC, MS, SM, YP) |
| contact_name | TEXT | Primary contact name(s) |
| email | TEXT | Contact email |
| phone | TEXT | Contact phone |
| new_contact | TEXT | Secondary contact name |
| new_contact_role | TEXT | Secondary contact role/title |
| new_contact_email | TEXT | Secondary contact email |

### Table: `interactions`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| investor_id | INTEGER FK | References investors.id |
| deal_id | INTEGER FK | References deals.id |
| status | TEXT | Status value: Pass, Reviewing, Reviewing - Pref, Reviewing - GL, Sent, Initial, Hold, Provided Terms, Reviewing - Unlikely, Actively Reviewing, - |
| coverage_code | TEXT | Coverage owner for this specific interaction |
| raw_comments | TEXT | Verbatim Placement Comments from the spreadsheet |
| old_comments | TEXT | Historical notes (Old Comments / Previous / Other Commentary column) |
| date_last_contact | TEXT | Date of last contact (Last / Date - Last column) |
| date_om_sent | TEXT | Date the OM was sent (OM column) |

### Table: `deals`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| deal_name | TEXT NOT NULL | Deal name from the file header |
| deal_date | TEXT | Date from the file header |
| asset_class | TEXT | Office, multifamily, industrial, retail, mixed-use, student housing, IOS, hospitality, etc. |
| geography | TEXT | Market/submarket/state |
| strategy | TEXT | Ground-up, value-add, stabilized, distressed, repositioning |
| capital_stack_position | TEXT | LP equity, co-GP, preferred equity, mezz, debt |
| estimated_equity_need | TEXT | Estimated equity check size |
| deal_status | TEXT | Active, closed, inactive |
| total_contacted | INTEGER | Summary stat: total investors on the list |
| pass_count | INTEGER | Summary stat: number of passes |
| pass_rate | REAL | Summary stat: pass percentage |
| reviewing_count | INTEGER | Summary stat: number still reviewing |

---

## Historical Placement List Formats

Two main formats were identified across the ~70 historical files, plus edge cases:

### Format A (newer — used in 105 N 13th, Hermit Smith, Tarpon Springs, NCA, CCI)

**Two sheets:** Summary view + Detail view

Summary columns: Status, Capital Group, Placement Comments

Detail columns: Row #, Status, Cov., Capital Group, Contact, Email, Contact - Notes, New Contact, New - Role, New - Email, Date - Last, Placement Comments, Old Comments

Some files add deal-specific columns (e.g., Tarpon Springs carries Hermit Smith cross-reference columns: HS Status, HS Date - Last, HS Placement Comments).

NCA adds: Type (A/B/C tier) and Placement (HC/LO/MS coverage codes).

105 N 13th adds: OM (date OM sent), Last (last contact date).

### Format B (older — used in Mira Palmer, Pektor Industrial)

**Multiple sheets:** Summary, Detail, Master/Contact

Columns: Status (numbered 1-5: 1.Actively Reviewing, 2.Reviewing, 3.Reviewing - Unlikely, 4.Next on the list, 5.Pass), Coverage, Capital Provider, Contact Person, Contact Email, Contact Numbers, Date Sent, Placement Comments, Previous / Other Commentary

### Edge Cases

- **Keowee River** (debt/land loan): Single sheet, grouped by status sections (Issued Terms, Interested, Sent, Potential, Passed, Carve Outs). Columns: Company, Contact, Email, Phone, Date, Comments.
- **The Nautilus** (prelim): Transposed layout — investor names as columns, field names as rows. Only 2 rows: Company Name and Feedback.

### Status Values (union across all files)

Pass, Reviewing, Reviewing - Pref, Reviewing - GL, Reviewing - Unlikely, Actively Reviewing (or 1.Actively Reviewing), Sent, Initial, Hold, Provided Terms, Next on the list (or 4.Next on the list), Issued Terms, Interested, Potential, - (blank/not yet contacted)

### Coverage Codes

HC, MS, SM, YP, LO, SL, HC/MS, SM/HC, ? (unknown), - (unassigned)

---

## Bootstrap Process

One-time ingestion of ~70 historical placement lists:

### Step 1: Discovery

Skill uses SharePoint MCP to search for all placement xlsx files under `1- Realty/1- Deals/`. The search identified ~50 files across active and inactive deal folders. A broader search at bootstrap time may surface additional files.

### Step 2: Format Detection

Each file is read via SharePoint MCP. The skill auto-detects which format it follows by checking column headers:

- "Capital Group" present → Format A
- "Capital Provider" present → Format B
- Neither → edge case, handled with format-specific parsing

Column names are mapped to the interaction schema:

| Schema Field | Format A | Format B |
|---|---|---|
| status | Status | Status (strip numeric prefix) |
| coverage_code | Cov. | Coverage |
| investor_name | Capital Group | Capital Provider |
| contact_name | Contact | Contact Person |
| raw_comments | Placement Comments | Placement Comments |
| old_comments | Old Comments | Previous / Other Commentary |
| date_last_contact | Last / Date - Last | Date Sent |
| date_om_sent | OM | (not present) |

### Step 3: Deal Metadata Extraction

Deal name and date are extracted from the header row (e.g., "Deal: 105 N 13 St  09-Apr-26"). Deal attributes (asset class, geography, strategy) are inferred by Claude from:

- The deal folder path (e.g., `Katy Asian Town/V23 - Bridge Debt`)
- Context in the pass reasons and placement comments
- The user confirms or corrects these during the review step

### Step 4: Entity Reconciliation

After all files are processed, the skill surfaces a list of proposed investor merges using fuzzy name matching. Examples:

- "Sagard/Everwest" ↔ "Sagard Real Estate"
- "Koch Real Estate Investments" ↔ "Koch RE"
- "USAA (Affinius Capital)" → rebranded entity

The user confirms or rejects each proposed merge. Confirmed canonical mappings are stored permanently in the `investors.aliases` field.

### Step 5: Review

Before committing to the database, the skill shows summary stats:

- X unique investors identified
- Y total interactions across Z deals
- N proposed entity merges

The user can drill into any investor to see what was captured.

### Step 6: Versioning

For deals with multiple dated versions of the same placement list (e.g., Hermit Smith has 5 versions from Oct-Dec 2025), only the most recent version is imported. The latest file contains the final statuses and comments.

---

## Deal Intake

### Input Methods

1. **Text** — typed in conversation (e.g., "200-unit multifamily value-add in Tampa, $30M equity need")
2. **PDF** — upload an OM or investment memo
3. **Excel** — upload a proforma or deal summary

### Parameter Extraction

Claude reads the input and extracts:

- Asset class (office, multifamily, industrial, retail, mixed-use, student housing, IOS, hospitality, etc.)
- Geography (market, submarket, state)
- Strategy (ground-up, value-add, stabilized, distressed, repositioning)
- Capital stack position (LP equity, co-GP, preferred equity, mezz, debt)
- Estimated equity check size
- Distinguishing features (IOS, opportunity zone, programmatic, etc.)

### Clarifying Questions

If any parameters are missing or ambiguous, Claude asks before proceeding. It does not guess. Example: "I see this is a mixed-use development in Brooklyn — are you placing for LP equity, preferred equity, or both?"

### Confirmation

Claude presents the extracted parameters back to the user for confirmation before running the match:

> Deal: 315 Meserole Street
> Asset class: Office / Mixed-use
> Geography: Brooklyn, NY (Williamsburg)
> Strategy: Value-add / lease-up
> Capital stack: LP equity + preferred equity
> Equity need: ~$15-20M
> Does this look right?

The user confirms, adjusts, or adds context. Then matching runs.

---

## Matching & Ranking

### Process

1. **Pull from Living Memory** — The skill queries the SQLite database and pulls all investor records with their full interaction history.

2. **Batched Processing** — With 600+ investors, Claude processes them in batches of ~50. For each batch, Claude reads the investor's full history (every deal they appeared on, every status, every raw comment) against the current deal parameters and makes a judgment call: strong match, possible match, likely mismatch, or definite mismatch.

3. **Ranking Criteria** — Claude weighs across five dimensions equally, driven by behavioral evidence:
   - **Asset class** — Has this investor done deals with this asset class? Or passed citing asset class as a reason?
   - **Geography** — Have they invested in this geography? Or explicitly said "not our market"?
   - **Check size** — Does the equity check fit what we know about their size range?
   - **Strategy** — Does the strategy match their track record (ground-up vs. value-add vs. stabilized)?
   - **Capital stack** — Are they doing the right position (LP equity vs. pref vs. mezz vs. debt)?

   Additional signals:
   - **Recency** — a pass from 2024 is less predictive than a pass from last month
   - **Structural vs. deal-specific** — "we don't do office" is a hard negative signal; "pricing didn't work on that one" is not
   - **Positive signals** — "Provided Terms," "Actively Reviewing," expressed interest in programmatic deals of this type

4. **Merge & Final Rank** — After all batches are processed, Claude merges the results into a single ranked list. Each batch produces a categorized list (strong match / possible match / likely mismatch / definite mismatch). The merge step combines all "strong match" investors, ranks them relative to each other, then does the same for "possible match," and so on. Definite mismatches are excluded from the output entirely.

### Output in Conversation

The full ranked list is displayed in conversation, grouped by tier:

- **Tier 1 (Strong Match):** Investors with strong behavioral signals supporting fit. Full reasoning for each.
- **Tier 2 (Possible Match):** Investors with mixed or limited signals. Reasoning explains what's known and what's uncertain.
- **Tier 3 (Long Shot):** Investors with weak signals or minor red flags. Included for completeness but flagged as lower probability.

Each investor entry includes:
- Investor name
- Rank within tier
- Match reasoning
- Relevant history flags (e.g., "Passed on 3 similar deals in the last 6 months")
- Warnings

Investors categorized as definite mismatches (hard structural conflicts — e.g., investor explicitly said "we never do office" and this is an office deal) are excluded from the output.

### Export to xlsx

Once the user is satisfied, the skill generates an Excel file in the standard placement list format:

| Column | Content |
|--------|---------|
| Status | Blank (new outreach) |
| Cov. | Pre-populated from database (coverage owner) |
| Capital Group | Investor name |
| Contact | From database |
| Last | Blank |
| OM | Blank |
| Placement Comments | Blank |
| Match Notes | AI's reasoning for this investor's ranking, including specific deal references and quotes from past interactions |

---

## Ongoing Memory Updates

### Trigger

Manual. The user tells the skill to import an updated or new placement list.

### Diff Detection

The skill compares the incoming file against what's already in the database for that deal:

- New investors added to the list since last import
- Status changes (e.g., Reviewing -> Pass)
- New or updated comments/pass reasons
- New contact information

### Entity Matching

New investor names are checked against the canonical name list. Known aliases match automatically. Unknown names trigger a fuzzy match proposal or are created as new investor records.

### Commit

The user reviews the diff summary and confirms. The database updates: new interaction rows are added, existing ones are updated with the latest status and comments.

### No Re-Bootstrap

Each import is incremental. The living memory grows over time as deals close and new placement data comes in.

---

## Constraints

- **Personal contact info stays local** — individual contact names, email addresses, and phone numbers are stored only in the local SQLite database and are never sent to external APIs. Firm/fund names (e.g., "Canyon Partners," "Monomoit") are not sensitive — they are public entities and are sent to Claude as part of the interaction history during matching.
- **Deal parameter extraction uses Claude API** — this is acceptable per user decision
- **At query time**, Claude receives firm names and interaction history (deal names, statuses, raw comments) for matching and reasoning. Personal contact details (individual names, emails, phones) are only inserted into the final xlsx output locally from the SQLite database.
- **Manual imports only** — no automatic SharePoint sync
- **Frequency of use** — a few times a month (steady deal flow)

---

## Data Sources Identified

| Source | Location | Content | Investor Count |
|--------|----------|---------|----------------|
| Historical placement lists (~70 files) | SharePoint: V23 Deals > 1- Realty > 1- Deals > [Deal] > [Placement] | Behavioral data: who was shown what, statuses, pass reasons | 250+ unique investors |
| TRPG Equity List vMain.xlsx | SharePoint: 1- Realty > 3- Database > Contact Lists | Master contact directory, free-text notes | 500-600+ entities |
| Equity Groups Tear Sheets | SharePoint: x- Market Data > Capital Tear Sheets | Structured investor profiles (AUM, check size, geography, asset type, returns) | ~22 firms |

**Primary bootstrap source:** Historical placement lists (Approach 2 — behavioral data over self-reported preferences).

**Supplementary sources:** TRPG Equity List and Tear Sheets can provide contact info and fill gaps for investors that appear in the master list but haven't yet appeared on any placement list. These are imported as investor records without interaction history.
