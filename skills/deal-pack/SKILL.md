---
name: deal-pack
description: |
  Ingest a folder of commercial real-estate due-diligence materials (rent roll,
  T-12, leases, photos, appraisal, seller OM, etc.) and produce a clean,
  canonical "deal pack" folder (facts.md, financials.xlsx, leases/, images/,
  sources/, pack-manifest.json). The pack is the source of truth that
  Claude-in-PowerPoint consumes to build the OM live. Use when the user says
  "deal pack", "normalize DD", "ingest materials", or provides a folder of
  client due-diligence files.
---

# v23-deal-pack

## When to use
When V23 receives client DD materials for a new deal and needs them normalized
into a clean working set before building the OM.

## Runbook

You will orchestrate the pipeline. All arithmetic is delegated to the
`deal_pack.cli` Python CLI. Never compute numbers yourself; always call the CLI.

**CLI I/O contract (applies to every command below):**
- Every `deal_pack.cli` command emits JSON to stdout on success.
- Commands that emit *data* (`inventory`, `rent-roll-summary`, `t12-summary`,
  `derived`) — redirect stdout to a file: `... > "<working>/foo.json"`.
- Commands that emit *status markers* (`write-financials` → `{"wrote": path}`,
  `copy-sources` → `{"copied": true}`, `write-facts-sidecar` → `{"wrote": sidecar_path}`,
  `check-facts-edited` → `{"edited": true|false}`) — capture stdout and
  `json.loads` it to confirm success and read the wrote-path.
- `copy-sources` additionally writes per-file warnings to **stderr** (lines
  prefixed `warning: `). Collect those into your manifest `warnings` list; they
  are informational, not failures.

### Step 0 — Resolve arguments

- `input_path` — absolute path to client materials folder.
- `name` — default: last segment of `input_path`.
- `out` — default: `C:\Users\TheodoreMouhlas\Documents\Claude\deal-packs\<name>\`.
- If `out` exists and `force` is not true, STOP and tell the user to pass `force: true`
  or choose a different `out`.

Create a working directory at `<out>/.v23-working/` and do all writes there.
Promote to `<out>/` only on success.

### Step 1 — Inventory + preview

Run:
```
python -m deal_pack.cli inventory "<input_path>" > "<working>/inventory.json"
```
This returns a JSON list of `{source_path, preview}` entries.

### Step 2 — Classify each file (LLM work — you)

For each inventory entry, read the filename and preview and classify it as one of:
`rent_roll, t12, lease, appraisal, seller_om, photo, plan, esa_pca, market_study, zoning, other`.

Produce a classifications JSON:
```json
[
  {
    "source_path": "...",
    "classified_as": "rent_roll",
    "classification_confidence": "high|medium|low",
    "preview": "..."
  }
]
```

Save this to `<out>/.v23-working/classifications.json`.

Rules:
- **Content beats filename.** A file named `rent_roll_july.pdf` whose preview is
  clearly a lease gets classified as `lease`.
- If ambiguous, use confidence `low` and pick the most likely class. Files with
  low confidence also land in the `sources/unclassified/` bucket (handled by the
  CLI `copy-sources` command).
- Files you cannot make any sense of → classified_as: `other`, confidence: `low`.

### Step 3 — Extract canonical rent roll (LLM work — you)

For each file classified as `rent_roll`:
1. Read its contents (use pdfplumber / openpyxl tools available to you, or the
   `anthropic-skills:xlsx` / `anthropic-skills:pdf` skills).
2. Produce a canonical CSV with these columns (exact header):
   `unit,tenant,sqft,lease_start,lease_end,base_rent_annual,base_rent_psf,recoveries,options,security_deposit,notes`
   - `lease_start` and `lease_end` in ISO format (YYYY-MM-DD) or blank.
   - `base_rent_annual` is a plain number (no commas, no $).
   - `tenant` blank for vacant units; add "vacant" to `notes`.
   - Preserve lease-specific details (percentage rent, step-ups, free rent) in `notes`.
3. Save to `<out>/.v23-working/rent_roll.csv`.
4. If the rent-roll layout defeats you, also save a raw dump as
   `<out>/.v23-working/raw_rent_roll.csv` — the writer will put this in a
   low-confidence tab of `financials.xlsx`.

If multiple rent rolls exist, pick the most recent (by filename date or preview)
for the primary `rent_roll.csv`. Save others to
`rent_roll__<slug>.csv` with a note in the manifest.

### Step 4 — Compute rent-roll summary (CLI)

```
python -m deal_pack.cli rent-roll-summary "<working>/rent_roll.csv" --reference-date <today-YYYY-MM-DD> > "<working>/rent_roll_summary.json"
```

### Step 5 — Extract canonical T-12 (LLM work — you)

For each file classified as `t12`:
1. Read the file.
2. Map each line item to one of: `revenue / base_rent`, `revenue / recoveries`,
   `revenue / other_income`, `revenue / less_vacancy`, `controllable_opex / <sub>`,
   `non_controllable_opex / <sub>`, `below_line / <sub>`.
3. Produce a canonical CSV with columns: `category,subcategory,line_item,total`.
   Use only the trailing-12-month total per row; the xlsx writer does not need
   the monthly breakdown for summary math.
4. Save to `<out>/.v23-working/t12.csv`. If layout defeats you, also save
   `raw_t12.csv`.

### Step 6 — Compute T-12 summary (CLI)

Use `total_sqft` from the rent-roll summary you produced in Step 4. Read that
JSON and extract `total_sqft`.

```
python -m deal_pack.cli t12-summary "<working>/t12.csv" --total-sqft <n> > "<working>/t12_summary.json"
```

### Step 7 — Compute derived metrics (CLI)

```
python -m deal_pack.cli derived "<working>/rent_roll_summary.json" "<working>/t12_summary.json" > "<working>/derived.json"
```

If an ask price is provided in the input materials or by the user, pass `--ask-price <n>`.

### Step 8 — Write financials.xlsx (CLI)

```
python -m deal_pack.cli write-financials \
  --out "<working>/financials.xlsx" \
  --rent-roll-csv "<working>/rent_roll.csv" \
  --rent-roll-summary "<working>/rent_roll_summary.json" \
  --t12-csv "<working>/t12.csv" \
  --t12-summary "<working>/t12_summary.json" \
  --derived "<working>/derived.json"
```

Add `--raw-rent-roll-csv` / `--raw-t12-csv` if you produced raw dumps.

Parse stdout as JSON; confirm the `wrote` path matches `<working>/financials.xlsx`.

### Step 9 — Abstract leases (LLM work — you)

For each file classified as `lease`:
1. Read the lease.
2. Produce a markdown abstract at `<working>/leases/<tenant-slug>-<suite>.md` with
   these fields (use blanks for missing):
   - **Tenant** / **Suite** / **SqFt**
   - **Commencement** / **Expiration**
   - **Base rent schedule** (steps, in a table)
   - **Renewal options**
   - **Recovery structure** (NNN / gross / modified gross / other)
   - **Free rent / abatements**
   - **Security deposit** / **Guarantor**
   - **Use clause / exclusivity**
   - **Notable provisions** (key risks, unusual terms)
   - **Source:** `<original filename>` (page refs if helpful)

### Step 10 — Index photos (LLM work — you)

For each file classified as `photo`:
1. Copy to `<working>/images/<descriptive-slug>.<ext>`.
2. Use vision to write a 1–2 sentence caption and classify as one of:
   `exterior`, `interior`, `aerial`, `site_plan`, `rendering`.
3. Save `<working>/images/captions.json` mapping filename → `{caption, category}`.

### Step 11 — Extract narrative facts (LLM work — you)

Read all files classified as `seller_om`, `appraisal`, `zoning`, and any
`market_study`. Produce `<working>/facts.md` covering (skip sections with no
source):
- Property overview: name, address, asset type, year built/renovated, total sqft/units
- Zoning and current use
- Location & submarket context (short)
- Ownership history (if derivable)
- Sponsor background (if provided in materials)
- Investment thesis hints from the seller OM (frame as "seller's claim", not V23 thesis)
- Notable items (upside, deferred maintenance, tenant risk, lease expiries cluster, etc.)

Every section ends with: `_Source: <filename>_`.

Also record the current hash as a sidecar for re-run protection:
```
python -m deal_pack.cli write-facts-sidecar "<working>/facts.md"
```

Parse stdout as JSON; the `wrote` field gives the sidecar path.

### Step 12 — Copy originals with predictable names

```
python -m deal_pack.cli copy-sources "<working>/classifications.json" --pack-root "<working>"
```

Parse stdout as JSON (`{"copied": true}`). Any `warning: ...` lines on stderr
should be appended to the manifest `warnings` list before Step 13.

### Step 13 — Write the manifest

Assemble a manifest JSON at `<working>/manifest-in.json`:
```json
{
  "deal_name": "<name>",
  "generated_at": "<ISO-8601 now>",
  "skill_version": "0.1.0",
  "input_root": "<input_path>",
  "files": [ /* one entry per classified file, with pack_destination + status */ ],
  "arithmetic_checks": [ /* log of LLM-vs-Python reconciliations, Python wins */ ],
  "warnings": [ /* human-readable strings */ ]
}
```

Then pipe it into the CLI via stdin (the `write-manifest` command reads the
manifest JSON from stdin — there is no positional path argument):
```
python -m deal_pack.cli write-manifest --out "<working>/pack-manifest.json" < "<working>/manifest-in.json"
```

This redirection works in both bash (Git Bash / WSL) and Windows cmd/PowerShell.
Parse stdout as JSON; confirm `wrote` matches `<working>/pack-manifest.json`.

### Step 14 — Preserve user edits on re-run, then promote

If `<out>/facts.md` already exists, run:
```
python -m deal_pack.cli check-facts-edited "<out>/facts.md"
```

Parse stdout as JSON. If `payload["edited"]` is `true`, rename the regenerated
file to `facts.generated.md` (do not overwrite the user's copy). If `false`,
the regenerated `facts.md` may replace the existing one.

Then atomically promote the working tree to `<out>/`:
- Move each generated artifact from `<out>/.v23-working/` to `<out>/`.
- Remove `<out>/.v23-working/` on success.

### Step 15 — Report

Print a summary to the user:
```
Pack ready: <out>

Files processed: N
Flagged (low confidence): M
Warnings: K

Open PowerPoint and tell Claude-in-PowerPoint:
  "Build the OM for <name> using the deal pack at <out>. Read facts.md for
   narrative, financials.xlsx for numbers, leases/ for tenant detail, and
   images/captions.json to pick photos for each slide. Do not invent numbers."

Flagged items to review before building:
  - <list>
```

## Safety rules

- **Never compute a number yourself.** All arithmetic must come from the CLI
  summary commands. If the LLM extraction of a rent roll contains "total
  base rent: $1,234,000", ignore that number — the CLI's computed total is
  authoritative.
- **Never write outside `<out>/`.** Never write into the V23 database folder.
- **Never skip the sidecar.** Step 11 always ends with `write-facts-sidecar`.
- **Never overwrite a user-edited `facts.md`.**
- On any error, leave `<out>/.v23-working/` in place for debugging.
- If any CLI invocation emits `{"error": "..."}` on stdout with exit code 1, STOP and report the error to the user verbatim. Do not retry.
