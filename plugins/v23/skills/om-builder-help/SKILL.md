---
name: om-builder-help
description: "Use when the user asks for help with the om-builder workflow - phrases like 'om-builder help', 'omcreator help', 'om creator help', 'how does the OM builder work', 'what does the OM builder need', 'om-builder prereqs', 'om-builder setup', 'what do I need to build an OM', 'om-builder docs', or any meta question about prerequisites, caveats, troubleshooting, or extending the OM-creation pipeline. Returns a comprehensive guide covering the v6 gated artifact pipeline, prerequisites, the phase-by-phase flow with human gates, the build and revision scripts, the QA loop, optional Claude-in-PowerPoint polish, known caveats and limitations, troubleshooting, and how to update or extend."
---

# v23-om-builder-help

When the user invokes help on the om-builder workflow, present the guide below. Keep it intact — the user wants the full reference, not a summary.

---

# Vanadium OM Builder v6 — Help & Reference

## What is the OM Builder?

`v23:om-builder` builds or revises a Vanadium-grade commercial real estate Offering Memorandum **end-to-end inside Claude Code** using a gated artifact pipeline. Claude Code (CC) reads the deal folder directly, extracts and audits every number into a persistent ledger, researches gaps with parallel subagents, writes a slide-by-slide blueprint, and authors the `.pptx` itself via `scripts/build-deck.py`, seeded from the house template (`assets/v23-template.pptx`).

**Claude in PowerPoint (CIP) is no longer the build engine.** The v4/v5 "pasteable prompt" architecture is retired — there is no prompt to paste, and the old `prompt-template.md` / `layout-repertoire.md` files no longer exist. CIP's only remaining roles are optional and bounded: post-QA visual polish (cover photos, logo placement, annotated aerials) and Path-B revision edits that genuinely require visual judgment.

The house style and voice are no longer inferred from a single reference deck. They are codified in eight reference docs derived from the 2026-06 pattern study across V23 production materials 2020–2026 (see "Reference docs and scripts" below).

The pipeline is asset-class agnostic and covers all capital types (equity, debt, pref, JV). Human gates sit after Phases 0, 1, 3, and 5 — nothing is built before the blueprint gate clears.

## How to invoke

In Claude Code, say one of these (or natural variants):
- "Build the OM for [deal name or folder]"
- "Create an OM for [deal]"
- "Revise / refresh the OM for [deal]"
- Point at a deal folder under `\1- Realty\1- Deals\`

For help (this guide): "om-builder help", "omcreator help", "how does the OM builder work", "what does the OM builder need".

## Version check

The runbook prints a version echo at the start of every run:

> `om-builder v6.0.0 — if this does not match the installed plugin version, your install is stale (see om-builder-help).`

If the echoed version doesn't match the installed plugin version, the installed marketplace copy is stale — see Troubleshooting.

## Prerequisites

### Required

1. **V23 plugin ≥ 6.0.0** in Claude Code. Earlier versions run the retired CIP-prompt flow.
2. **Deal folder synced locally** (typically `C:\Users\<you>\Vanadium Group LLC\V23 - Database\1- Realty\1- Deals\<Deal Folder>`). CC reads every source file directly — online-only folders won't work.
3. **Source files in the deal folder.** At minimum the sizing/underwriting model (the Investment Summary tab is canonical for deal numerics). Quality improves with: sponsor OM / exec summary / decks, appraisals, prior V23 work product, photos and renderings. Revision mode additionally requires the live `.pptx`.
4. **Python 3 with `python-pptx`** — used by `build-deck.py`, `apply-revision-edits.py`, and `make-template.py`. (`extract-pptx-inventory.py` and `render-qa.py` are stdlib-only.)
5. **A render path for Phase 5a visual QA:** `pdftoppm` (poppler) on PATH is required; pptx→PDF conversion uses LibreOffice (`soffice`) if on PATH, else desktop PowerPoint via COM. Fallback: export the PDF manually from PowerPoint and pass the `.pdf` to `render-qa.py` directly.

### Optional

6. **Claude in PowerPoint** — only for optional post-QA polish or Path-B revision edits. Not needed for a standard build.
7. **Microsoft 365 MCP** — only if CIP punch-list items reference SharePoint/Graph image URIs. The core pipeline reads files from the local synced folder and does not use Graph.

## Working folder convention

All pipeline artifacts live in `<deal-folder>\x V23\` (created if absent). Before any existing artifact is overwritten, the prior version moves to `<deal-folder>\x V23\Archive\`.

## The pipeline at a glance

Before Phase 0, the skill runs **mode detection**: it globs the deal folder for `.pptx` files. Zero found → new-build. One or more → revision mode targeting the file the user confirms as live. It never switches modes silently mid-run, and states the detected mode (and target file) before starting.

| Phase | Name | Key artifact(s) in `x V23\` | Gate |
|---|---|---|---|
| 0 | Frame | `00-FRAME.md` | User confirms before anything is read deeply |
| 1 | Extract & Audit | `_data_extract\NN-<source>.md` digests, `00-DATA-AUDIT-TRAIL.md`, `Data needed from <sponsor> - <date>.md` | User reviews audit trail + data request doc |
| 2 | Research | findings merged into the audit trail | none |
| 3 | Blueprint | `OM Build Blueprint - <date>.md` | **HARD GATE — user (+Henry) sign-off; nothing is built before this clears** |
| 4 | Build (CC-native) | `<deal>-vN.pptx` + build log | none |
| 5 | QA | rendered slide PNGs, `QA Report - <date>.md` | User reviews deck + QA report |
| 6 | Ship | PDF, `Open Items - <date>.md` | none |

### Phase 0 — Frame

One page capturing: capital type (equity/debt/pref/JV), deck type (single-asset / portfolio / platform — with the WHY, since deck type drives the exec-summary recipe, stat-box vocabulary, and coverage checklist), audience, page budget (ceiling + target), and stop-list seeds. **Stop-list mechanics:** every user directive is parsed into three columns — Add-list / Modify-list / Stop-list — and every output block is re-checked against all three before shipping. Meta-directives are pattern-matched (e.g., "don't be too specific about what's under contract" means strip dated status language deck-wide, not just one phrase).

### Phase 1 — Extract & Audit

CC opens and reads every canonical source directly (never subagent-summarized): the model (Investment Summary tab canonical; Pro Forma / Rent Roll / Waterfall / Comps tabs for detail), sponsor OM and decks, appraisals (third-party support, never the canonical deal numeric), prior V23 work product, and — in revision mode — the live `.pptx` via inventory extraction.

Every claim lands in `00-DATA-AUDIT-TRAIL.md`: claim, value, source file/tab/page, as-of date, tier, and status (✅ verified / ⚠️ conflicted / ❌ unverifiable / 🔢 sponsor-canonical). **Conflict policy:** the underwriting model is canonical for deal numerics; when sources disagree, the most recent wins, the conflict is flagged ⚠️, and it routes to the data request doc — never silently averaged or fudged. A **self-consistency sweep** then hunts contradictions within and across sources (headline returns not derivable from TPC + NOI, capital stacks that don't sum, status labels contradicted by dates). Every ⚠️/❌ becomes a numbered question in `Data needed from <sponsor> - <date>.md`.

### Phase 2 — Research

3–5 parallel subagents, each scoped to ONE specific question naming the exact submarket, metric, as-of period, and preferred source tier ("Brunswick, GA multifamily vacancy and asking rents for workforce units, as of Q1 2026, from CoStar or Newmark" — not "submarket fundamentals"). Each returns quoted passage + source + as-of date + tier + confidence, merged into the audit trail per `source-standards.md`.

### Phase 3 — Blueprint (the hard gate)

The blueprint is where all composition decisions happen, on paper: a one-sentence thesis the whole deck argues; 3–5 load-bearing claims each traced to an audit-trail ID; register/deck-type cross-check against the `registers-and-coverage.md` coverage checklist; a slide-by-slide spec (eyebrow / action title / layout key / content blocks / audit-trail IDs — action titles are assertive sentences, not topic labels); page-budget enforcement (cuts happen here, not after slides are built); risk-register placement decision; and in revision mode, PRESERVE and NEVER-REINTRODUCE lists. No content block ships to build without an audit-trail ID. **Nothing is built before the user (+Henry) signs off.**

### Phase 4 — Build (CC-native)

The template is never modified — work happens on a copy at `x V23\<deal>-vN.pptx`. The blueprint slide spec is serialized as JSON and run through `python build-deck.py spec.json`. For arrangements python-pptx can't express cleanly, the escape hatch is direct XML layout-cloning from the template (clone and modify; never invent new masters). Every authored sentence is governed by `voice-model.md` (GP rules outrank everything) + `anti-ai-ruleset.md` (read-aloud pass); layout selection by `layout-system.md` (structural-first); number formatting, typography, and footers by `design-system.md` + `conventions.md`. A build log records every slide's layout key and any XML escapes taken.

### Phase 5 — QA (three sub-gates, in order)

- **5a Visual:** `render-qa.py` renders every slide to PNG; a subagent inspection loop checks overflow, overlap, contrast, misalignment, off-canvas elements, font-default leak (Aptos/Calibri bleedthrough), and broken tables. Fix → re-render → loop until clean.
- **5b Verification:** every deck numeric is re-checked against the audit trail. Criticals (ask size, key returns, cap stack) re-check directly to the source file/tab/page; research claims re-fetch the cited URL. Any figure without a ✅ entry is replaced with "TBD — confirm with sponsor" before shipping.
- **5c Editorial** (codified from Henry's 2026-06-09 NPV review): cross-page numeric consistency on 5–10 key figures; unit style per the `conventions.md` Three-Context Rule ($mm in prose, $MM in stat boxes, spelled out on covers); dash/decimal conventions; thesis-contradiction sweep; placeholder sweep; label/bio parallelism; read-aloud anti-AI pass.

Results land in `QA Report - <date>.md` with pass/fail per item.

### Phase 6 — Ship

Export the PDF with the "Vanadium Realty LLC | <Deal Name>" footer on every page; name it `<Deal> - OM - <YYYY-MM-DD>.pdf` per `conventions.md`; archive prior versions; write `Open Items - <date>.md` listing every unresolved ⚠️/❌ item and TBD placeholder; report final paths.

## Revision mode

1. **Inventory first (mandatory):** `python extract-pptx-inventory.py <canonical.pptx>` writes `inventory.txt` and `inventory-fulltext.txt` into `<filename>-extracted\`. The live `.pptx` is the source of truth — earlier PDF exports are stale by definition. Every edit must reference a real shape ID with current text quoted as a precondition.
2. **Stop-list capture** (Phase 0 mechanics, mandatory here): PRESERVE and NEVER-REINTRODUCE lists go into the blueprint.
3. **Path A — deterministic edits (default):** author a JSON edit spec for `apply-revision-edits.py` (ops: `set_text`, `set_rich_text`, `set_cell`, `set_chart_series`, `delete_slide`; each op carries slide number, shape_id, an `expect` precondition, and the new content verbatim). The engine copies source → target (never edits the original), verifies each precondition, preserves run formatting, and prints PASS/SKIP/ERROR per op. SKIPs are surfaced, never silently ignored. Re-run the inventory afterward to confirm edits landed and stop-list phrases are gone.
4. **Path B — CIP edit script (visual/judgment edits only):** for repositioning shapes visually, image/logo placement, or anything requiring visual judgment CC can't make from XML. The shape-level script is saved to `x V23\CIP-Edit-Script.md` and referenced by path, not pasted into the conversation.
5. **Render-QA loop** after either path, plus the Phase 5c editorial checks.

## Optional CIP polish (post-Phase-5 only)

Off the critical path, invoked only after the deck passes QA. CIP executes a bounded shape-level punch-list per `cip-polish-template.md` — typically swapping photo placeholders for real images, placing logos, annotating aerials. Every item carries a precondition and a skip rule; CIP does not author, recompose, rewrite prose, or re-derive numbers. Key operational caveats from the template: embed Garamond and Bell MT in the `.pptx` before CIP touches it (unembedded fonts silently substitute to Calibri off-Windows); check z-order after image insertion; escape `&` as `&amp;` in any XML; re-list shapes after structural edits; batch actions per item.

## Reference docs and scripts

All live in `<plugin>/skills/om-builder/`.

| File | Governs |
|---|---|
| `voice-model.md` | Writing voice: 5 generation-priority (GP) rules that outrank everything (every claim block carries a computed downside anchor; underwrite below the validated comp and show both numbers; odd-precision anchored numbers; withhold/leave asymmetry; a defensive numeric in every block) plus 11 corpus-validated voice rules |
| `anti-ai-ruleset.md` | Final-pass anti-AI-tell checklist run over every authored block (kill negation antithesis, number/name/date in every claim, banned-vocabulary purge, read-aloud pass) |
| `layout-system.md` | Arrangement catalog + structural-first selection: the canonical sequence → arrangement mapping decides layouts for canonical slide positions; intent-based selection is a tiebreak for non-canonical slides only. Supersedes the old `layout-repertoire.md` |
| `design-system.md` | Visual DNA: 12 durable elements with exact values (navy #1F3A5F header band, Garamond type ramp, off-canvas accent-bar stack, logo positions). Supersedes the style block formerly hardcoded in `prompt-template.md` |
| `registers-and-coverage.md` | 10-register taxonomy with structural spines, required-metric coverage checklists per capital type, and risk-register placement rules |
| `conventions.md` | Numbers, units, citations, naming: Three-Context Rule for dollar amounts, two-decimal rule for model-derived returns, lowercase-x multiples, whole-number bps, parentheses negatives, file naming |
| `source-standards.md` | Source tiers (1–3), as-of dating discipline, audit-trail format, never-fabricate policy |
| `cip-polish-template.md` | Optional post-QA CIP punch-list template with per-item format and Office.js caveats |

| Script | Role |
|---|---|
| `scripts/build-deck.py` | Phase 4 new-build generator: JSON slide spec → `.pptx` cloned from `assets/v23-template.pptx`. Deterministic layouts: cover, kpi_strip, narrative, table, chart, two_column, section_divider (~80% of an OM). Any other layout value becomes a labeled placeholder slide for CIP/manual finish |
| `scripts/render-qa.py` | Phase 5a renderer: deck → PDF → per-slide PNGs (usage: `python render-qa.py <deck> <outdir>`; accepts a `.pdf` directly to skip conversion) |
| `scripts/extract-pptx-inventory.py` | Revision-mode inventory: slide/shape/position/text preview, plus run-level formatting, table cell grids, and chart series in the fulltext variant |
| `scripts/apply-revision-edits.py` | Path-A revision engine: precondition-checked JSON edit ops with PASS/SKIP/ERROR reporting |
| `scripts/make-template.py` | Regenerates `assets/v23-template.pptx` when the design system changes |

## Known caveats and limitations

- **`build-deck.py` covers the deterministic ~80%.** Full-bleed photo heroes, annotated aerials, maps, renderings, image placement, stacking plans, and scatter/quadrant exhibits are not generated — they ship as labeled placeholder slides routed to CIP polish or manual finish. A deck with many bespoke visuals will have a longer punch-list.
- **Phase 5a needs a local render path.** No poppler = no PNGs; no LibreOffice/PowerPoint = manual PDF export fallback. Visual QA is mandatory, so install the tooling once.
- **The model is canonical; everything else is support.** Appraisal values are quoted as third-party support, and marketing-deck figures are distrusted until verified. Date is the tiebreaker on conflicts. If the model is stale, refresh it before running — the pipeline dates everything but can't generate numbers the model doesn't have.
- **Never-fabricate is enforced, by design.** Unverifiable figures ship as "TBD — confirm with sponsor" and appear in the open-items doc rather than being guessed. Expect TBDs when source material is thin.
- **Revision mode trusts only the live `.pptx`.** PDF exports of the deck are stale by definition; every edit requires a shape-ID precondition from a fresh inventory.
- **Stop-lists are sticky.** Phrases killed by a stop-list go on the NEVER-REINTRODUCE list and are re-checked at QA — but only if they were captured at Phase 0/revision intake. State "don't/never/remove/kill" directives explicitly.
- **Font embedding matters only when CIP touches the file.** Embed Garamond and Bell MT before any CIP polish session, or fonts may silently substitute on non-Windows machines.
- **The version echo is the staleness tripwire.** If the echoed version doesn't match the installed plugin version, stop and update before building.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skill doesn't appear, or version echo doesn't match the installed plugin | Installed marketplace copy is stale | `git pull` in `~\.claude\plugins\marketplaces\v23-plugins`; restart Claude Code |
| `ModuleNotFoundError: No module named 'pptx'` | `python-pptx` not installed | `pip install python-pptx` |
| `render-qa.py`: "pdftoppm not on PATH" | poppler missing | Install poppler and add it to PATH |
| `render-qa.py`: PDF conversion failed | No `soffice`; PowerPoint COM failed | Open the deck in PowerPoint, Save As PDF, re-run `render-qa.py` with the `.pdf` as the first argument |
| Rendered slides show Aptos/Calibri instead of Garamond | Font-default leak (a Phase 5a check) | Fix the slide spec or cloned XML; re-render the affected slide |
| `apply-revision-edits.py` prints SKIP on an op | `expect` precondition mismatch — the deck changed since the inventory | Re-run `extract-pptx-inventory.py`, update the op's expect text, re-run |
| Numbers differ across slides | Phase 5c cross-page consistency check failed or skipped | Verify 5–10 key figures against the audit trail; fix every instance |
| A figure has no audit-trail entry at 5b | Claim never extracted/verified in Phase 1–2 | Replace with "TBD — confirm with sponsor"; add to the data request doc |
| Deck exceeds the page budget | Cuts weren't made in the blueprint | Return to Phase 3, merge/cut on paper, re-gate, rebuild affected slides |
| CIP improvised or edited the wrong shape during polish | Punch-list item lacked a precondition or skip rule | Use the `cip-polish-template.md` item format; re-deliver the full block (CIP has no cross-turn memory) |
| Prose sounds AI-generated | Voice rules not applied at build | Run the `anti-ai-ruleset.md` read-aloud pass; rewrite per `voice-model.md` GP rules |

## Updating or extending the skill

Development copy: `C:\Users\TheodoreMouhlas\Workspace\Vanadium\x Plugins\v23-plugins\plugins\v23\skills\om-builder\` (and `om-builder-help\` for this guide). Installed copy: `C:\Users\TheodoreMouhlas\.claude\plugins\marketplaces\v23-plugins\...` — edit the dev repo, never the installed copy directly.

What to edit:

1. **Runbook / phase logic** → `om-builder/SKILL.md`
2. **Voice rules** → `voice-model.md`; **anti-AI backstop** → `anti-ai-ruleset.md`
3. **Layouts** → `layout-system.md`; **visual DNA** → `design-system.md` (then regenerate the template via `make-template.py` if values changed)
4. **Registers / coverage checklists** → `registers-and-coverage.md`
5. **Number/unit/naming conventions** → `conventions.md`; **source rules** → `source-standards.md`
6. **Build/revision behavior** → the scripts under `scripts/`
7. **CIP polish format** → `cip-polish-template.md`
8. **This guide** → `om-builder-help/SKILL.md`

Then publish:

1. **Bump the version in BOTH** `plugins/v23/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` — they must match. Patch for fixes/doc tweaks, minor for new behavior, major for breaking changes.
2. **Frontmatter rules (hard requirement):** every SKILL.md keeps exactly two frontmatter keys — `name` (must equal the folder name) and `description`. Any other key, or a name/folder mismatch, silently fails validation and **blocks the entire plugin from updating on clients** with no surfaced error.
3. **Commit and push** to the plugin repo, then `git pull` in the installed marketplace folder so the installed copy equals dev. Verify with the version echo on the next run.

## Related skills

- **`v23:deal-pack`** — normalize raw DD materials into a canonical pack first if the deal folder is a mess.
- **`v23:deal-screener`** — pressure-test the draft OM with a senior CRE eye after Phase 5.
- **`v23:comp-search`** — pull sale/lease comps to feed the comp slides and the audit trail.
- **`v23:placement-engine`** — generate the investor placement list once the OM ships.

## When NOT to use the om-builder

- **Non-OM artifacts** (IC memos, broker pitches, LP updates, teasers/one-pagers) → different document type; `v23:deal-screener` output or a one-off is closer.
- **Pure data extraction or folder cleanup** → `v23:deal-pack`.
- **Changing the house style itself** → edit `design-system.md` / `make-template.py` and bump the plugin version; don't fight the pipeline deal-by-deal.

## The bottom line

The om-builder v6 is a **gated artifact pipeline that owns the OM end-to-end in Claude Code**: frame → extract & audit → research → blueprint (hard gate) → CC-native build → three-stage QA → ship. Every number traces to an audit-trail entry; every sentence passes the voice and anti-AI rules; every layout comes from the codified system. CIP is a bounded finishing tool, not the builder.

If something feels off on a real run, the answer is to refine the relevant artifact doc or script and bump the plugin version — not to abandon the pipeline. The skill exists to compound lessons across deals.
