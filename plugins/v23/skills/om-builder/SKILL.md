---
name: om-builder
description: "Build or revise a Vanadium-grade CRE Offering Memorandum using a gated artifact pipeline. Claude Code authors the .pptx directly via build-deck.py seeded from v23-template.pptx; CIP is optional post-QA polish only. Triggers: build/create/generate an OM, refresh/revise an existing OM, deal folders under \\1- Realty\\1- Deals\\. Asset-class agnostic. All capital types: equity, debt, pref, JV. Pipeline: Phase 0 Frame → Phase 1 Extract & Audit → Phase 2 Research → Phase 3 Blueprint → Phase 4 CC-native pptx build → Phase 5 QA (visual + verification + editorial) → Phase 6 Ship. Human gates after Phases 0, 1, 3, and 5."
---

# om-builder v6.0.0

**Version echo — print this line at the start of every run:**
`om-builder v6.0.0 — if this does not match the installed plugin version, your install is stale (see om-builder-help).`

---

## Working folder convention

All pipeline artifacts live in `<deal-folder>\x V23\`. Create it if absent. Before overwriting any existing artifact, move the prior version to `<deal-folder>\x V23\Archive\`.

---

## Mode detection (new-build vs. revision)

Run this before Phase 0.

1. Glob `<deal-folder>` and `<deal-folder>\x V23\` for `*.pptx` files.
2. Zero `.pptx` found → **new-build mode**.
3. One or more `.pptx` found:
   - User said "build from scratch" / "rebuild" / "fresh deck" → ask: "I see [N] existing .pptx files. Build from scratch (new-build) or revise the existing deck (revision)?" Wait for answer.
   - Otherwise → **revision mode**; target = the file confirmed as live by the user. Ask if more than one exists.
4. Never switch modes silently mid-run. If the detected mode appears wrong partway through, stop and re-detect with the user.
5. State the detected mode and target file (if revision) explicitly before Phase 0.

---

## Phase 0 — Frame

**Artifact:** `x V23\00-FRAME.md` (one page)

Capture:
- **Capital type:** equity / debt / pref / JV
- **Deck type:** single-asset / portfolio / platform — state WHY (the NPV portfolio-vs-platform miss cost a full rebuild; deck type determines exec-summary recipe, stat-box vocabulary, and register coverage checklist)
- **Audience:** specific LP / lender / family office / institutional
- **Page budget:** stated ceiling (e.g., ≤25 pages) and target (e.g., 20–23)
- **Stop-list seeds:** any explicit "don't / never / remove / kill" directives the user has provided; extract add-list and modify-list as well; flag hidden meta-directives (see v5.1 stop-list mechanic below)
- **Mode:** new-build or revision, as detected above
- **Version echo line** (repeat in this artifact): `om-builder v6.0.0`

**Stop-list mechanics (port from v5.1):** Read every user directive line by line. Extract three columns: Add-list / Modify-list / Stop-list. Every output block and every slide must be re-checked against all three before shipping. Pattern-match: "don't be too specific about what's under contract" is a meta-directive to strip dated status language across the whole deck, not just one phrase.

**GATE: user confirms 00-FRAME.md before anything is read deeply.**

---

## Phase 1 — Extract & Audit

**Artifacts:**
- `x V23\_data_extract\NN-<source>.md` — one digest per canonical source (CC reads every source directly: model tabs, sponsor deck, appraisals, legal where referenced)
- `x V23\00-DATA-AUDIT-TRAIL.md` — the persistent ledger
- `x V23\Data needed from <sponsor> - <date>.md` — data request doc

### Direct reads (CC's own context)

CC opens and reads directly (never subagent-summarized):
- Sizing model — Investment Summary tab is canonical for deal numerics; Pro Forma, Rent Roll, Waterfall, Comps tabs for supporting detail
- Sponsor OM / exec summary / decks — extract narrative, asset story, business plan, sponsor-provided market commentary
- Appraisals — extract as-stabilized value, cap rate, methodology; use as third-party support, NOT as the canonical deal numeric
- V23 work product — deal analysis docx, 1-pagers, outreach memos already done on this deal
- Prior OM (revision mode only) — the live `.pptx` extracted via inventory first (see Revision Mode section)

### Audit trail entry format

Every claim goes into `00-DATA-AUDIT-TRAIL.md` in this format:

| Claim | Value | Source file / tab / page | As-of date | Tier | Status |
|-------|-------|--------------------------|------------|------|--------|
| … | … | … | … | 1/2/3 | ✅ verified / ⚠️ conflicted / ❌ unverifiable / 🔢 sponsor-canonical |

Source tiers per `source-standards.md`. `🔢 sponsor-canonical` = figures from the underwriting model that are not independently verifiable but are the sponsor's numbers of record.

### Conflict policy (non-negotiable)

The underwriting model is canonical for deal numerics. Appraisals are quoted as third-party support. Marketing-deck figures are distrusted until verified against the model. When two sources cite the same metric with different values:
1. Identify the conflict explicitly: metric, value A + source A + date A, value B + source B + date B.
2. Use the most recent source as canonical. Date is the tiebreaker.
3. Flag the conflict in `00-DATA-AUDIT-TRAIL.md` with status ⚠️ and route to `Data needed from <sponsor>`.
4. Never silently average, hedge, or fudge. Never fabricate. See `source-standards.md`.

### Claim self-consistency sweep

After extracting all sources, run a cross-check: do any claims in the sponsor deck contradict each other or contradict the model? Common classes:
- "$X minimum" alongside deals smaller than X (the "$5MM minimum / $4.29M deal" class from NPV)
- Headline returns not derivable from stated TPC + NOI
- Capital-stack figures that don't sum across slides
- Status labels (e.g., "Approved") contradicted by dates in the same document

Flag every inconsistency in `00-DATA-AUDIT-TRAIL.md` as ⚠️ and route to the data request doc.

### Data request doc

Create `x V23\Data needed from <sponsor> - <date>.md`. List every ⚠️ conflict and ❌ unverifiable item as a numbered question. This is what gets sent to the sponsor; it is never silently assumed away.

**GATE: user reviews 00-DATA-AUDIT-TRAIL.md and the data request doc before Phase 2.**

---

## Phase 2 — Research

No gate after this phase.

Dispatch 3–5 parallel subagents, each scoped to ONE specific research question identified from the Phase 1 gaps. The question must name the exact submarket, metric, as-of period, and preferred source tier. "Submarket fundamentals" is not a question; "Brunswick, GA multifamily vacancy and asking rents for workforce units, as of Q1 2026, from CoStar or Newmark" is.

Source rules: per `source-standards.md` §1–3 (tiers, as-of dating, never-fabricate). Each subagent must return: quoted passage + source name/URL + as-of date + tier + confidence flag.

Findings merge into `00-DATA-AUDIT-TRAIL.md` with verification status. Any finding that cannot be re-verified against its source before Phase 5 gets status ⚠️ and is flagged in the QA report.

Dispatch all subagents in a single message (parallel execution). Wait for all before continuing.

---

## Phase 3 — Blueprint

**Artifact:** `x V23\OM Build Blueprint - <date>.md`

Blueprint contents:

1. **Thesis** — one defensible sentence. The entire deck argues this. (The Story discipline lives here, not as a separate framework.)
2. **Load-bearing claims** — 3–5 claims that must be true for the thesis to hold; each must trace to an audit-trail ID.
3. **Register and deck type** — confirmed from 00-FRAME.md; cross-check against `registers-and-coverage.md` coverage checklist for the deal's capital type (equity / debt / pref / JV). Confirm all required metrics are sourced or flagged.
4. **Slide-by-slide spec** — for every slide: eyebrow / action title / layout key / content blocks / audit-trail IDs for every number. Action titles are assertive sentences ("Brunswick workforce vacancy sits 4.1% — 180bps below metro average"), not topic labels ("Market Overview"). No content block that lacks an audit-trail ID ships to build.
5. **Page budget enforcement** — merge/cut decisions happen here, on paper. If the slide count exceeds the 00-FRAME.md ceiling, cuts happen in the blueprint, not after slides are built.
6. **Special-angle headlines** — any slides with non-standard framing noted and justified.
7. **Risk register placement** — explicit decision: in-deck section, companion memo, or both. Must be stated. (Per `registers-and-coverage.md` §3.)
8. **(Revision mode) PRESERVE list** — slides, shapes, and text blocks to leave unchanged.
9. **(Revision mode) NEVER-REINTRODUCE list** — phrases, framings, and numbers explicitly killed by the stop-list that must not reappear.
10. **Open items** — every ⚠️/❌ audit-trail item still unresolved at blueprint time.

**HARD GATE: user (+Henry) sign-off required. Nothing is built before this gate clears.**

---

## Phase 4 — Build (CC-native)

No gate after this phase.

**Steps:**
1. Seed `assets\v23-template.pptx` — do not modify the original; work on a copy at `x V23\<deal>-v1.pptx` (new-build) or `x V23\<deal>-vN.pptx` (revision).
2. Serialize the blueprint slide spec as the JSON input to `scripts\build-deck.py`. Run:
   ```
   python "<skill-dir>/scripts/build-deck.py" spec.json
   ```
3. For arrangements that python-pptx cannot express cleanly, use the direct XML layout-cloning escape hatch: clone the slide XML from the template, edit content in-place. Do not invent new masters; clone existing slides and modify.
4. **Voice:** every authored sentence governed by `voice-model.md` (GP rules §1 outrank all other rules) + `anti-ai-ruleset.md` (run the read-aloud pass over every authored text block before including it in the spec).
5. **Layout:** selection governed by `layout-system.md` (structural-first: canonical sequence → arrangement mapping overrides intent-based selection for canonical slide positions).
6. **Visual and numeric style:** `design-system.md` + `conventions.md` govern all number formatting, typography, footer conventions, and stat-box vocabulary.
7. **Build log:** record every slide — layout key used, notable decisions, any XML-clone escapes taken.

---

## Phase 5 — QA

Three sub-gates in order. All three must pass before the deck goes to the user.

### 5a — Visual QA

Run `scripts\render-qa.py` to render every slide to PNG. Then run a subagent inspection loop over every PNG — check for: text overflow, shape overlap, contrast failures, misalignment, off-canvas elements, font-default leak (Aptos/Calibri bleedthrough), broken tables. Fix any issue and re-render the affected slide. Loop until clean.

### 5b — Verification QA

Re-check every deck numeric against `00-DATA-AUDIT-TRAIL.md`. Every figure in a KPI box, table, chart, or prose block must have a ✅ verified entry in the ledger. For criticals (ask size, key return metrics, cap stack), re-check directly to the source file/tab/page. For research claims, re-fetch the cited URL and confirm the passage still reads as cited. Any figure without a ✅ entry gets replaced with `TBD — confirm with sponsor` before the deck ships.

### 5c — Editorial QA (codified from Henry's 2026-06-09 NPV review)

Work through this checklist; record pass/fail per item in the QA report:

- [ ] **Cross-page numeric consistency** — pick 5–10 key figures (ask, total cap, equity, debt, key return metric); verify they are identical across every prose block, KPI, table, and chart in the deck (the 25-vs-26-deals class)
- [ ] **Unit style** — M vs. MM per `conventions.md` Three-Context Rule: `$mm` in prose, `$MM` in stat boxes, spelled out on covers
- [ ] **Dash / decimal conventions** — per `conventions.md`: two decimals on model-derived returns; lowercase `x` for multiples; parentheses for negatives; hyphen for ranges
- [ ] **Thesis-contradiction sweep** — no slide content contradicts the deck's stated thesis or discipline (no "blended IRR" in a platform deck; no aggregate basis where deal-by-deal is the thesis)
- [ ] **Placeholder sweep** — zero `[PLACEHOLDER]`, `TBD`, `xxxxx`, `******` tokens remain unless explicitly reviewed and surfaced as open items
- [ ] **Label/bio parallelism** — all sponsor bio blocks and contact cards follow the same structural pattern; no one bio is formatted differently
- [ ] **Read-aloud anti-AI pass** — read every slide's authored text aloud; flag and fix any sentence that sounds metronomic, content-free, or AI-voiced per `anti-ai-ruleset.md`

Produce a QA report at `x V23\QA Report - <date>.md`: pass/fail per item, fix actions taken, remaining open items.

**GATE: user reviews the deck + QA report.**

---

## Phase 6 — Ship

No gate.

1. Export PDF. Footer: "Vanadium Realty LLC | <Deal Name>" on every page per `design-system.md` §5.
2. Name the PDF per `conventions.md` §4: `<Deal> - OM - <YYYY-MM-DD>.pdf`.
3. Move prior `.pptx` and `.pdf` versions to `x V23\Archive\`.
4. Produce `x V23\Open Items - <date>.md`: list every ⚠️ and ❌ item in `00-DATA-AUDIT-TRAIL.md` still unresolved, every `TBD — confirm with sponsor` placeholder, and any editorial open items from the QA report.
5. Report to user: final file paths (pptx + pdf), QA report path, open-items path.

---

## Revision mode

### Extract the live .pptx first (mandatory)

```
python "<skill-dir>/scripts/extract-pptx-inventory.py" "<path-to-canonical.pptx>"
```

Outputs to `<filename>-extracted\`: `inventory.txt` (slide + shape + position + text preview), `inventory-fulltext.txt` (adds run-level formatting, table cell grids, chart series). The live `.pptx` is the source of truth, period. Earlier PDF exports of the deck are stale by definition.

Read both inventory files. Build a working table: `slide N → title → [shape id, name, current text, position, formatting]`. Every edit must reference a real shape ID from this inventory with the current text quoted as a precondition.

### Stop-list capture

Phase 0's stop-list mechanics (mandatory in revision mode): extract Add / Modify / Stop lists from every user directive. Every edit-script action must be re-checked against the stop list. The PRESERVE and NEVER-REINTRODUCE lists go into the Phase 3 blueprint.

### Path A — deterministic edits (default)

Author a JSON edit spec per `apply-revision-edits.py`'s op schema (`set_text`, `set_rich_text`, `set_cell`, `set_chart_series`, `delete_slide`). Each op carries slide (1-based), shape_id, `expect` precondition (current-text substring), and new content verbatim. Run:

```
python "<skill-dir>/scripts/apply-revision-edits.py" edits.json
```

The engine copies source → target (never edits the original), verifies each precondition before editing, preserves run formatting, and prints PASS/SKIP/ERROR per op. A SKIP on a precondition mismatch is surfaced to the user; it is not silently ignored.

After running, re-run `extract-pptx-inventory.py` on the output to confirm edits landed and stop-list phrases are gone.

### Path B — CIP edit script (visual/judgment edits only)

Reserve for edits that genuinely require the live app: repositioning shapes visually, image/logo placement, anything requiring visual judgment CC cannot make from XML. Produce a shape-level edit script (see v5.1's `CIP-Edit-Script.md` format for the preflight / global rules / per-action / post-edit-checklist structure). Save to `x V23\CIP-Edit-Script.md`. Do NOT paste the full script into the conversation — reference the file path.

### Render-QA loop after revision

Run `scripts\render-qa.py` on the revised `.pptx` after Path A or Path B. Run Phase 5c editorial checks. Confirm stop-list phrases are absent.

---

## Optional CIP polish (post-Phase-5 only)

Off the critical path. Invoke only after the deck has passed Phase 5 QA. CIP executes a bounded shape-level visual punch-list — it does not author or recompose. See `cip-polish-template.md` for the template and per-item format.

---

## Conflict policy and never-fabricate

Per `source-standards.md`:
- Never fabricate a stat, comp, citation, URL, or return figure.
- If a claim cannot be verified, mark `TBD — confirm with sponsor` or `TBD — confirm source`; surface it in the open-items summary; never guess-fill.
- Every cited claim: quoted passage + source name/URL/tab/page + as-of date + tier.
- Stale comps are worse than missing comps. Date everything or drop it.

---

## Updating this skill

1. `SKILL.md` — runbook changes (this file)
2. `voice-model.md` — voice rules (re-runnable from the pattern study)
3. `anti-ai-ruleset.md` — anti-AI backstop
4. `layout-system.md` — arrangement catalog and selection logic
5. `design-system.md` — visual DNA
6. `registers-and-coverage.md` — register taxonomy and metric checklists
7. `conventions.md` — numbers, units, citations, naming
8. `source-standards.md` — source tiers, audit-trail format, risk-mitigant pattern
9. `scripts\build-deck.py` — new-build generator
10. `scripts\render-qa.py` — PNG renderer for Phase 5a
11. `scripts\extract-pptx-inventory.py` — inventory extractor
12. `scripts\apply-revision-edits.py` — revision engine (Path A)
13. `scripts\make-template.py` + `assets\v23-template.pptx` — regenerate template if design system changes
14. `cip-polish-template.md` — optional CIP polish punch-list
15. Bump version in `.claude-plugin\plugin.json` AND `.claude-plugin\marketplace.json` together; republish so installed copy equals dev
