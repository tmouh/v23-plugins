---
name: om-builder
description: "Build or revise a Vanadium-grade commercial real estate Offering Memorandum by front-loading all analytical work in Claude Code (deep folder reads + parallel research subagents + The Story synthesis), then handing Claude in PowerPoint either a composition-only prompt (new build) or a shape-level edit script (revision). Triggers: build/create/generate an OM, refresh/revise an existing OM, point at a SharePoint-synced deal folder under \\1- Realty\\1- Deals\\. Asset-class agnostic. The user pastes one block into Claude in PowerPoint, which executes visually."
---

# v23-om-builder

## Overview

Building an institutional CRE OM has two distinct phases:
1. **Analysis** — read the deal, research the gaps, construct The Story, write the prose
2. **Production** — turn that content into a finished, designed .pptx

**The governing principle (one rule for both modes): Claude Code ("CC") owns the file. It writes the content AND produces the .pptx deterministically. Claude in PowerPoint ("CIP") is reserved for the narrow residue that genuinely needs the live app — visual judgment, image/logo placement, and bespoke-visual slides the PowerPoint JS API can't render well.** This is grounded in the CIP capability research (see "CIP capability profile" below): the JS API is fast and reliable for text/tables/charts/geometry on an existing file, but slow, quota-bound, and weak at composing from scratch.

Two operating modes, same principle:

- **New-build mode** — CC writes the content in-voice, then runs `scripts/build-deck.py` to generate the deck from the house template (`assets/v23-template.pptx`): native text, KPI strips, tables, charts, and the core layouts, with the navy footer/theme inherited. Bespoke-visual slides become labeled placeholders. CC hands CIP a short **polish prompt** (fill placeholders, place images, visual QA) — not a build-from-scratch prompt.
- **Revision mode** — CC applies deterministic edits directly to a copy of the live deck via `scripts/apply-revision-edits.py` (Path A); CIP only handles live/visual-judgment edits via a shape-level edit script (Path B).

The mode is determined automatically in Phase 0. **Do not skip Phase 0.**

**Why this architecture:**
- The PowerPoint JS API is weakest exactly where decks need polish (charts ~70%, images preview-only, precise geometry); CC writing the .pptx via python-pptx is precise, fast, reproducible, and quota-free.
- CIP is slow and quota-expensive (≈30% of a Pro session for a ≤10-slide build); minimizing CIP turns is the dominant design constraint.
- Subagent isolation in CC keeps raw file reads + research out of the synthesis context window.
- CIP has no memory across turns; everything CC hands it is self-contained.

The skill is **asset-class agnostic**. It does not hardcode section names (Multifamily ≠ IOS ≠ Office). Instead it enforces analytical *purposes* that any institutional OM must serve, and lets the deal's substance determine the spine. Writing voice is codified in `house-voice.md`; layout selection in `layout-repertoire.md`. See `[[user-the-story-framework]]` and `[[user-vanadium-analysis-conventions]]` for the analytical framework CC applies.

## When to use

**New-build mode triggers:**
- User says "build the OM" / "create an OM" / "generate offering memorandum"
- User points at a deal folder containing sponsor materials + a sizing model but no prior live deck

**Revision mode triggers:**
- User says "refresh / revise / update the OM" / "rework the deck" / "fix the [list of things]"
- A `.pptx` file exists in the deal folder (or a `\x V23\` subfolder)
- User pastes a list of "kill this / change this / don't do this" directives against an existing deck

Do NOT use for:
- One-pagers, teasers, or sales flyers (different artifact)
- Re-styling an existing deck without re-doing analysis (use a different prompt)
- Building decks directly in Claude Code (CIP does the visual work)

## Hybrid architecture (read this before running)

**CC reads DIRECTLY in its own context** (precision required, no summarization tolerance):
- **The live `.pptx` if one exists** — extract XML; in revision mode this is the source of truth, period
- All sponsor materials in the deal folder — OMs, exec summaries, sizing models (every relevant tab), lease flyers, photo packets
- Any prior version of the OM being refreshed (V01, V02, etc.) — read fully so the new version improves on it
- V23 internal work product — deal-analysis docx, investor-outreach docx, V23 1-pagers, internal memos
- Tracker/pipeline files referenced by the user

**Subagents handle, in isolated context** (digest IS the natural output):
- **Reference DNA subagent** *(new-build mode only — skip in revision mode)* — one Explore agent reads 5–8 prior Vanadium production OMs/decks, returns layout/voice/structural observations as a digest
- **3–5 Research subagents** — general-purpose agents in parallel, each scoped to ONE research question, return cited findings with quoted passages + URLs + as-of dates

**CC synthesizes** with access to both raw direct-read data AND subagent digests, writes The Story + content (composition mode) OR per-shape actions (revision mode), then runs a **verification gate** that re-reads canonical sources for every critical numeric/quote AND surfaces source-of-truth conflicts before shipping, writing a persistent **audit ledger** (every figure → source → as-of date → verified). Before research, CC builds a **coverage manifest** that flags what the deal is missing against the OM Coverage Checklist — holes are surfaced, not silently plugged.

### 🔥 CIP context-loss is a load-bearing constraint

CIP does **not** retain reliably across turns. A 50-action composition prompt pasted into CIP will leak context within a few back-and-forth exchanges. Implications:

- For revisions, **always** deliver a shape-level edit script (each action self-contained with shape ID + current text precondition + new text verbatim). Never tell CIP "use the content I wrote earlier."
- For new builds, every section in the composition prompt should also be self-contained: full prose verbatim, full KPI values, full source lines — no internal cross-references like "as defined above."
- If the user pastes mid-conversation and CIP says "I don't have that prompt in front of me," that's the symptom; the fix is making each action atomic from inception.

## CIP capability profile & division of labor

CIP runs as a task-pane Office add-in driving the live `.pptx` through the **PowerPoint JavaScript API (Office.js)**. The API surface — not the model's intelligence — is the binding constraint. The model is current-generation and strong (selectable Opus 4.7 / Opus 4.6 / Sonnet 4.6 as of 2026-05); the bottleneck is what the API can physically do, plus per-turn tool-use caps and quota cost. **CIP is slow and quota-expensive** (independent testing: ~10 min + ~30% of a Pro session to draft a ≤10-slide deck; a single font tweak ≈ 18% of session usage). The governing design principle: **pre-compute everything in CC; minimize CIP turns; let CIP do only what the API does reliably.**

### What CIP is GOOD at — offload TO it
| Capability | Why it's reliable |
|---|---|
| Replace/edit text in existing shapes & placeholders | `TextRange.text` settable; surgical sub-range edits via `getSubstring`. Its single strongest area. |
| Write slide copy (titles, bullets, captions, notes) | Pure text; model strength |
| Run-level text formatting (font family, pt size, `#RRGGBB`, bold/italic/underline) | `ShapeFont` on `TextRange` — fully supported |
| Create native tables + fill cell text | `addTable` + Table/Cell APIs; table formatting supported |
| Generate new slides on a specified master + layout | `slides.add({slideMasterId, layoutId})`, `applyLayout` |
| Reorder / delete / duplicate slides | `Slide.moveTo(index)`, `delete()` |
| Read the current deck (shape IDs, names, positions, text, master/layout) | Full read surface — this is what the inventory helper leverages |
| Geometric / flow-chart shapes + connectors at SUPPLIED coordinates | `addGeometricShape`, `addLine` |
| Slide background, theme color scheme, alt text | Supported (API 1.10) |

### What CIP is BAD at or CAN'T do — do BEFORE, in CC
| Limitation | Reason | What CC does instead |
|---|---|---|
| **Insert raster images / logos / photos** | `addPicture` is **preview-only**, not in a stable requirement set; testers report it "cannot generate images." | Prefer pre-placed template image placeholders; flag image insertion as "verify in your build"; never assume URL/Graph-URI insertion works |
| **Create charts with precise data/series/axis/colors** | **No `addChart` exists**; charts are injected via OOXML and land ~60–70% right | CC computes exact series (the inventory helper extracts them); deliver a clean data table and either (a) let CIP draft a native chart for HUMAN REVIEW, or (b) place the data as a **native table** (reliable) |
| **Pixel-precise geometry / "match the grid exactly"** | Geometry IS settable, but the model picks coordinates poorly | CC supplies **exact left/top/width/height in points** |
| **Brand/template fidelity unattended** | ~85% compliance; testers saw it introduce template errors | Hand exact values targeted at existing placeholders; require human review pass |
| **Long multi-step sequences in one turn** | Per-turn tool-use cap halts long jobs ("reached its tool-use limit for this turn") | Batch per slide / small slide-group; expect to re-prompt |
| **Holding a long spec across turns / restart** | History is local IndexedDB, not persistent, auto-compacted | Re-deliver a self-contained block each session; never reference "earlier" content |
| **Cheap iterative micro-tweaks** | Each action is slow + quota-heavy | Batch all formatting into the initial instruction |
| **SmartArt; animations; transitions; media/video** | No API surface | Out of scope — build diagrams as grouped shapes/tables; no motion |
| **"Seeing" the rendered slide to self-correct** | Unconfirmed whether CIP feeds rendered images to the model | Don't rely on CIP catching its own visual errors; CC specifies precisely |

### The division of labor (both modes)

**CC fully pre-computes and hands over:** all final, proofed text as exact strings; all numbers, table matrices, and chart data as finished values; the exact target for each edit (slide + shape name/ID, preferring existing placeholders); exact geometry in points and exact font specs for any new shape; the layout decision (which master + layout each new slide uses, chosen via the `layout-repertoire.md` selection procedure); and a deterministic, ordered slide plan.

**CIP executes only:** insert N slides on specified layouts; reorder/delete; drop pre-written text into named targets; build native tables from supplied matrices; apply specified run-level formatting and theme/background; optionally draft native charts from a clean data table *with explicit human-review expectation*; add geometric/flow shapes at supplied coordinates.

**Keep out of CIP entirely:** precise charts, SmartArt, image/logo placement at scale, animations/transitions/media, any "make it pixel-perfect to brand" guarantee.

### Optimal delivery format for CIP

- **Batch, don't dribble — but bound each batch.** One structured instruction per logical unit (per slide or small slide-group), not 30 atomic one-word edits. Tool-use caps and quota both punish many tiny turns.
- **Target by placeholder NAME, fall back to slide index.** Meaningful, stable shape names are the most robust target for a natural-language agent. Avoid identifying a shape by geometry. (CC names new shapes meaningfully and references them by name.)
- **Give exact values; phrase as imperative execution.** "Set the text of placeholder `KPI_Value_1` to: '20%+'." Not "make a KPI about returns." Open prompts trigger CIP's slow, lower-fidelity compose mode.
- **Charts:** deliver a clean labeled data table + one-line chart spec; accept a draft and plan a human pass, OR place as a native table when precision matters.
- **Images:** treat as a template concern, not a CIP runtime task; verify insertion empirically in the target build.
- **Re-deliver context every session** — assume nothing persists across a restart.

### Architecture note (implemented)

Because the PowerPoint JS API is weakest exactly where decks need polish (charts, images, precise layout), CC builds the `.pptx` directly with python-pptx in BOTH modes, and CIP is used only for in-app polish — which is what CIP is good at. New-build = `scripts/build-deck.py` (generate from the house template); revision = `scripts/apply-revision-edits.py` (edit a copy). The generator covers the core data-driven layouts (cover, KPI strip, narrative, table, chart, two-column, section divider) and emits labeled placeholders for bespoke-visual slides (full-bleed hero, aerial, map, rendering, photo grid, stacking plan, scatter, quadrant) so CIP knows exactly what to finish. **CC can verify structure/text/geometry/colors but cannot render the slide — visual quality is confirmed by the user opening the file.**

### Empirical-verification flags (re-confirm on the target machine)

These are inferred from docs + independent testing as of 2026-05; verify in the user's actual build and tell the user if behavior differs: (1) image insertion mechanism and whether the SharePoint/Graph connector path works; (2) whether CIP "sees" rendered slides; (3) how large a pasted instruction block survives before auto-compaction; (4) whether CIP resolves "the shape named X" reliably via natural language.

## Runbook

### Phase 0 — Detect mode (revision vs new build)

Before doing anything else, determine the operating mode.

**Mode detection algorithm:**

1. Glob the deal folder and any `\x V23\` subfolder for `*.pptx` files.
2. If **zero** `.pptx` files exist → **new-build mode**. Proceed to Phase 1 with new-build runbook.
3. If **one or more** `.pptx` files exist:
   - If user message explicitly says "build a new OM from scratch" / "rebuild" / "fresh deck" → ask: "I see [N] existing .pptx files in the folder. Do you want me to ignore them and build from scratch (new-build mode), or revise the existing deck (revision mode)?" Wait for answer.
   - Otherwise → **revision mode**. Proceed to Phase 1 with revision-mode rules.

**Mode-specific deliverables:**

| | New-build mode | Revision mode |
|---|---|---|
| **Phase 5 Reference DNA** | Optional (codified in `house-voice.md` + `layout-repertoire.md`) | Skip — the existing deck IS the reference |
| **Phase 7 synthesis output** | A `build-deck.py` JSON content spec (text in-voice + layout keys) | Per-shape actions referencing the live deck's shape IDs |
| **Phase 9 delivery** | CC runs `build-deck.py` → finished `.pptx`; then a short CIP **polish prompt** for placeholders + images | Path A: CC runs `apply-revision-edits.py` → finished `.pptx`. Path B: CIP edit script (live/judgment edits) |
| **Phase 10 output** | Generated `\x V23\<deal>-v1.pptx` + polish prompt | Path A: revised `.pptx`. Path B: `<deal>-CIP-Edit-Script.md` |

State the detected mode explicitly to the user at the start of Phase 1. Do not silently switch modes mid-run.

### Phase 1 — Resolve the deal folder + surface ambiguities

Ask the user for the deal folder path if not given. Path typically looks like:
`C:\Users\<user>\Vanadium Group LLC\V23 - Database\1- Realty\1- Deals\<Deal Folder>`

**Validate the folder:**
- Folder exists locally (SharePoint sync) and contains source files
- Identify deal asset class from folder name + a quick scan of file titles (Industrial / IOS / Multifamily / Office / Hospitality / Mixed-Use / Data Center / Land / Retail / Senior Housing / Student Housing / etc.) — this informs research scoping later

**Surface ambiguities — ASK if any exist, do not guess:**

1. **Multiple .pptx files** — if more than one `.pptx` exists across the deal folder and any subfolder, list them with last-modified dates and ASK: "I see these PowerPoint files: [...]. Which is the live file I should work against?" Do not assume "the one with v2 in the name is newer" — file naming is unreliable.

2. **Multiple pipeline / tracker files** — if more than one tracker xlsx/PDF exists (e.g., `Pipeline-Redacted.pdf` AND `Pipeline-AddressDeleted.xlsx`), ASK which is canonical OR confirm whether they are the same dataset in different formats.

3. **Tracker-vs-folder naming mismatch** — see `[[project-npv-ios-deal-naming]]` for the canonical pattern. The tracker may use a different label than the folder. Resolve by ask + returns + folder substance, not by city-string match. If unresolved, ASK.

4. **Sponsor identity ambiguity** — if the deal folder contains multiple sponsor OMs from different firms (rare, but happens during sponsor changes), confirm which sponsor is the current counterparty.

5. **Version uncertainty for any source PDF** — sponsor OMs often have a `v01`, `v02`, `-final`, `-DRAFT` suffix. If multiple versions exist, use the most recent + flag the others as "may contain prior-state assumptions."

If validation fails or an ambiguity cannot be resolved, stop and tell the user what's wrong. Do not proceed.

### Phase 1.5 — Capture user directives + build the stop list

**This is non-optional whenever the user has provided notes or directives** (revisions always; new builds when the user has fed feedback against a prior OM).

Read the user's prompt + any attached notes line by line. Extract:

**A. Add-list** — every explicit "add / include / show / put in" directive
**B. Modify-list** — every "change X to Y / reframe / retitle / replace" directive
**C. Stop-list** — every "don't / remove / kill / not this / less of / never / strip / stop saying" directive

Write these out as three columns in your working notes. Every output section, KPI, prose block, and slide must be re-checked against ALL THREE lists before it ships. The stop list is the most important: it captures what the user has specifically said they do NOT want, and those exclusions are easy to violate by accident.

**Pattern-match: the stop list often contains hidden meta-directives.** "Don't be too specific about what's under contract" means more than "remove the words 'under contract'" — it means strip dated status language across every slide. "Basis through each one like its a portfolio, don't care" means remove per-deal $/AC entry-basis figures from prose. Surface the meta-rule explicitly in your notes.

If the user has NOT provided directives (true new-build with no feedback), skip the stop list and proceed.

### Phase 2 — Enumerate folder + classify files

Enumerate every file. Classify into:

- **Canonical numerics** — sizing models, underwriting xlsx (Investment Summary, Pro Forma, Rent Roll, Waterfall, Comps tabs)
- **Sponsor narrative** — sponsor-provided OMs, exec summaries, decks, lease flyers, pitch materials
- **V23 work product** — deal analysis docx, investor outreach docx, prior V23 OMs/1-pagers, internal memos, placement lists
- **Pipeline / tracker** — deal pipeline xlsx/PDF, naming maps
- **Visual assets** — photos, renderings, floor plans, aerial shots, site maps (CIP will open these directly for image placement)
- **Admin / legal** — agency agreements, contracts (read for terms ONLY if the OM references them; otherwise skip)
- **Live deck (revision mode only)** — the `.pptx` file confirmed in Phase 1 as canonical

### Phase 3 — CC reads canonical files DIRECTLY

#### Source-of-truth hierarchy

**Revision mode:**
1. **The live `.pptx`** is canonical for everything currently in the deck — slide structure, shape positions, current text, layout names. Extract its XML first (see below). Earlier PDF exports of the deck are stale by definition.
2. Sponsor materials (OMs, sizing models) are canonical for facts about the deal (numerics, asset details, sponsor track record).
3. V23 work product (deal analysis docx, 1-pagers) is canonical for V23's analytical voice and conclusions.

**New-build mode:**
1. Sponsor materials + V23 work product as in revision-mode #2 and #3.
2. Any prior OM `.pptx` (if a refresh, even a partial one) — read fully so the new version improves on it.

#### Revision mode — extract the .pptx XML FIRST

This step is mandatory in revision mode and replaces "read the prior PDF as if it were current." The PDF is stale; the .pptx is live.

Run the helper script in this skill folder:

```
python "<skill-dir>/scripts/extract-pptx-inventory.py" "<path-to-canonical.pptx>"
```

Outputs land in a sibling folder `<filename>-extracted/`:
- `ppt/slides/slideN.xml` — raw slide XML, one per slide
- `inventory.txt` — preview inventory (every slide, every shape's id/name/position/text up to 200 chars; flags `[TABLE rxc]` and `[CHART type]`)
- `inventory-fulltext.txt` — full inventory; additionally includes, per shape:
  - **Run-level formatting** — font family, pt size, hex color, bold/italic for every text run (so CC can specify exact formatting for NEW shapes instead of telling CIP to "match the style")
  - **Table cells** — the full row × column cell-text grid for every native table (so CC can author precise cell edits)
  - **Chart series** — chart type + each series' name, categories, and values from the cached data (so CC can author precise chart-data edits)

Read both inventory files. Build a working table: `slide N → title → [shape id, name, current text, position, formatting]` for every shape, plus the table/chart data where present. **Every edit-script "Action N.M" you author must reference a real shape ID from this inventory, with the current text quoted so CIP can verify before changing it.** For table/chart edits, reference the specific cell (row/col) or series; for new shapes, supply exact font + geometry from the formatting CC observed on sibling shapes.

If the helper script fails or Python is unavailable, unzip the .pptx manually (`unzip -o file.pptx -d extracted/`) and parse the slide XMLs directly — `<p:cNvPr id="N" name="...">` for shape identifiers, `<p:txBody>` for current text, `<p:spPr>/<a:xfrm>` for position.

#### Both modes — direct reads in CC's context

CC opens, in its own context:
- Every sizing model — Investment Summary tab is canonical for cost basis, cap stack, IRR, MoIC, NOI trajectory. Pro Forma, Rent Roll, Waterfall, Comps tabs for supporting detail.
- Every sponsor OM PDF — extract narrative voice, asset story, business plan, in-place leasing context, sponsor-provided market commentary
- Every V23 work product — V23 has already analyzed this deal internally; mirror that voice and conclusions; the V23 1-pager (if it exists) is the closest model for what Vanadium says about this deal
- The previous OM (if a refresh): in revision mode, the live `.pptx` XML inventory; in new-build refresh, the prior PDF if no .pptx exists

CC extracts and structures (in working notes):
- Every numeric needed for the deck, with source path and tab/page reference
- The sponsor's existing thesis and where it's strong vs. thin
- V23's internal point of view on this deal (which is what we'll mirror, not the sponsor's)
- Gaps — what's missing from the folder that an institutional LP would demand
- **(Revision mode)** Per-slide cross-walk: for each slide in the inventory, map user's directives (add/modify/stop lists from Phase 1.5) to specific shapes that need changing

### Phase 3.5 — Build the Coverage Manifest (flag the holes BEFORE filling them)

Now that CC has read the folder, diff what the deal actually HAS against what an institutional OM MUST cover. The goal is to **flag holes, not silently plug them.**

1. Take the enumerated **OM Coverage Checklist** (see the reference section of that name below).
2. For each required item, mark a status from the Phase 2/3 reads:
   - **Have** — a source in the folder fully supports it (name the file + tab/page).
   - **Partial** — some support exists but it's thin, stale, or unsourced.
   - **Missing** — nothing in the folder supports it.
3. For every Partial/Missing item, tag a **fill-route**:
   - **Research-fillable** — external market / sponsor-public data a Phase 6 subagent can source (submarket fundamentals, comps, sponsor public record, capital-markets context).
   - **Client-only** — only the sponsor/client can provide it (rent roll, T-12, sizing model, proprietary business-plan detail, asset photos). Research cannot manufacture these.
   - **Synthesis** — CC produces it from inputs already present (The Story, risk register, LP-question pre-empt).
4. **Save the manifest** to `<deal-folder>\x V23\<deal>-OM-Coverage-Manifest.md` as a table: `Required item | Status | Source-or-gap | Fill-route`. Create the `\x V23\` subfolder if needed.
5. **Surface it to the user NOW, front-and-center** — this is warn-only, it does NOT halt the run. Present two short lists: "I will research these" (research-fillable gaps) and "Only the sponsor/client can supply these — request them" (client-only gaps).

**Warn-only behavior:** never block. Proceed to build, but every client-only Missing item becomes a literal `TBD — confirm with sponsor` placeholder in the content (never a guessed value). The manifest feeds Phase 4 (research-fillable gaps become research questions), Phase 8 (verify no Missing item got silently filled with an unsourced number), and Phase 10 (the front-facing open-items list).

**Revision mode:** Phase 3.5 is optional but recommended — run it against the existing deck's coverage so directives that delete/retitle slides don't accidentally strip a required section. If you skip it, say so.

### Phase 4 — Identify research scopes (this is where the work pays off)

Based on the folder read, identify 3–5 *specific* research questions that, if answered, complete The Story. Examples (the actual list depends on the deal):

- **Sponsor track record** — prior fund/deal exits, AUM, capital partners, principal bios, any publicly known disputes or lawsuits
- **Submarket fundamentals** — vacancy, asking rents, supply pipeline, recent absorption, cap rate trends in the EXACT submarket, with as-of dates Q[current quarter]
- **Sector macro** — asset-class-specific demand drivers, structural supply/demand picture, recent institutional capital flows, named precedent transactions
- **Comparable transactions** — recent sales and lease comps in submarket; cap rates, $/SF, $/AC, $/door; institutional-quality comps not just MLS listings
- **Tenant credit / use-case validation** — for occupied properties: tenant financials, industry health; for value-add: prospective tenant universe and absorption likelihood
- **Capital markets context** — current debt market for this asset class, recent loan terms, agency vs. CMBS vs. life co. activity, rate environment as of writing

**Scope rule:** be specific. "Submarket fundamentals" is a category, not a research question. The actual question is "Tampa Bay industrial outdoor storage submarket vacancy rate and asking $/AC for sub-10 acre yards, as of Q1 2026, from CoStar / Green Street / Newmark Research." That precision is what makes the subagent return useful instead of generic.

**Adapt scope to asset class.** IOS research ≠ office research. For IOS: trailer storage demand, port traffic, e-commerce logistics, infill scarcity. For office: tenant absorption by industry, sublease overhang, return-to-office data. Etc.

**Revision mode tightening:** in revision mode, the prior deck has already cited certain sources. Only dispatch research to (a) fill gaps the prior deck left, (b) refresh stale figures (>6 months old or marked Q[prior quarter]), or (c) verify claims the user has specifically flagged in directives. Don't re-run the entire research sweep if the prior deck's research is still defensible.

### Phase 5 — Dispatch Reference DNA subagent  (NEW-BUILD MODE — NOW OPTIONAL)

**In revision mode: SKIP entirely.** The existing deck IS the reference.

**In new-build mode: usually SKIP — the DNA is already codified.** `house-voice.md` (writing voice, 13 rules with verbatim examples) and `layout-repertoire.md` (layout selection system + 25 layouts) were extracted from the canonical reference decks (105 N 13th, Obsidian, Ever Leaf, Krios) and now stand in for the Reference DNA digest. Run this subagent ONLY when: (a) the deal is an asset class with no codified precedent and you suspect a layout/voice pattern the files miss, or (b) you have reason to think the codified files are stale. Otherwise apply `house-voice.md` + `layout-repertoire.md` directly and move to Phase 6.

**If you do run it:** dispatch ONE Explore-type subagent with a comprehensive scope of 5–8 prior Vanadium production OMs/decks. The subagent reads each, returns observations grouped by:

- **Layout DNA** — specific arrangements that recur or that diverge from defaults; cite slide context
- **Voice DNA** — phrasing patterns, idea-block rhythm, bold-inline patterns, opening sentences
- **Structural DNA** — section sequencing, depth ratios across sections, where the Story spine lives in each deck
- **Source-line DNA** — how citations are formatted, what counts as primary vs. secondary
- **Anti-AI cues honored** — what the references conspicuously DON'T do

Return format: one paragraph per reference + a final synthesis paragraph naming the 5–7 patterns the new OM should inherit and the 2–3 patterns to deliberately vary against.

Reference set should include (resolve URIs via SharePoint search):
- 105_N_13 — OM — most recent (canonical Vanadium house style, single-asset)
- TheExchange — most recent (recent production, single-asset)
- Krios v5 (programmatic platform OM)
- Obsidian Platform Deck VHC2 (programmatic platform, most recent)
- Obsidian Powered Land Platform (programmatic, earlier)
- Obsidian Ever Leaf (Ever Leaf platform)
- Hillwood Presentation (strategic platform deck)
- (Optionally one more, asset-class-matched if available)

### Phase 6 — Dispatch 3–5 Research subagents in parallel

For each research question identified in Phase 4, dispatch a general-purpose subagent. Each subagent receives:

- **The single research question** — narrowly scoped, asset-class-specific, with as-of date specified
- **Acceptable source tiers** (from `[[user-vanadium-analysis-conventions]]`):
  - Tier 1: CoStar, Green Street, REIS, RCA/MSCI, Newmark/JLL/CBRE/Cushman Research, NAREIT, NCREIF, FRED/BLS/Census
  - Tier 2: PERE/IREI, ULI/PwC Emerging Trends, IPE Real Assets
  - Tier 3: Cornell/MIT/Wharton CRE programs, peer-reviewed journals
  - NOT acceptable: Medium/Substack posts (unless credentialed author), broker marketing PDFs as data sources, Wikipedia primary, anonymous social, vendor "studies" without methodology
- **Required return format:**
  - Each claim must include: quoted passage + source URL + as-of date
  - Flag uncertainties explicitly (saw-but-couldn't-verify)
  - Order findings from most-cited/most-confident to least
  - End with a one-sentence synthesis of what this research means for The Story

Dispatch the subagents in a SINGLE message with multiple Agent tool calls (parallel execution). Wait for all to return.

### Phase 7 — Synthesize

#### New-build mode (Phase 7-NB)

**7a — Build The Story (one paragraph, the load-bearing thesis).** Apply `[[user-the-story-framework]]`. The Story is one defensible sentence — the thesis the entire deck argues — followed by a paragraph naming the 3–5 load-bearing claims that have to be true for the thesis to hold. Every section the OM will have must trace back to this.

**7b — Sequence the narrative spine.** Per The Story framework, the institutional consensus is: Setting → Strategy/Business Plan → Asset → Sponsor → Returns/Cap Stack/Risk → Executive Summary written last but positioned first. Adapt this to the deal's substance. Platform raises differ from single-asset acquisitions.

**7c — Identify section purposes (NOT names).** From `[[user-vanadium-analysis-conventions]]`, the deliverable must accomplish: establish setting, define opportunity, position asset, tell The Story, show business plan, vet sponsor, stack capital, surface returns, frame risks, anticipate LP cutting questions. Map each onto specific sections appropriate to this deal's substance. Do not force a generic section list.

**7d — Write content per slide, in-voice, as a `build-deck.py` content spec.** The output of Phase 7-NB is a JSON content spec (the input to `scripts/build-deck.py`), not a CIP composition prompt. For each slide author:
- **Action title** — the one-sentence takeaway, written FIRST (it drives layout selection). A topic label ("Market Overview") is not an action title; "Central Florida IOS vacancy sits 400 bps below the national average" is. The deck's action titles read in sequence should tell the whole story (horizontal logic).
- **Layout** — chosen via the `layout-repertoire.md` **four-stage selection procedure**: confirm one idea per slide → recover communicative INTENT from the action-title grammar → map intent → layout family → place per reading-flow. Then pick the matching `build-deck.py` layout key (`cover`, `kpi_strip`, `narrative`, `table`, `chart`, `two_column`, `section_divider`). If the slide is bespoke-visual (full-bleed hero, aerial, map, rendering, photo grid, stacking plan, scatter, quadrant), use that layout key — the generator emits a labeled placeholder and CIP finishes it. Enforce the variety rules (no two consecutive content slides share an arrangement; ≥ 7 distinct arrangements).
- **Content fields per the layout's schema** — eyebrow, title, takeaway, and then `kpis` / `blocks` / `table` / `chart` / `left`+`right` as the layout requires; every value final, exact, and in-voice. Plus the `source` line (citation + as-of date).
- **Visual references** — for bespoke-visual slides, the Graph URIs CIP will place, passed in the slide's `note` field.

**Voice is mandatory and codified.** Apply `house-voice.md` — both the 13 house-voice rules (conclusion-first openings; vary rhythm; numbers/deltas/benchmarks instead of adjectives; name every actor with pedigree; state the bear case then neutralize it; prove with precedent; recurring one-line thesis; surgical bolding; quarantine legal hedging) AND the anti-AI-tell ruleset (kill the negation antithesis; demand a number/name/date per claim; purge the AI vocabulary; restore "is"; vary sentence length; one em-dash per slide; cut restating summaries; ban CRE puffery; read it aloud). Run the anti-AI pass over every slide's text before it goes in the spec. Also apply `[[user-vanadium-analysis-conventions]]`: risks framed probability × impact × mitigation; cross-document numeric consistency; institutional source tiers only.

#### Revision mode (Phase 7-R)

In revision mode, you are NOT writing section-level prose. You are writing **per-shape actions** against the live deck's inventory. For each slide that needs changes:

**7R-a — Identify which shapes change.** For each user directive (from Phase 1.5 add/modify/stop lists), map to specific shape IDs from the Phase 3 inventory. A directive may touch one shape on one slide ("retitle slide 4") or many ("kill the 27% blended IRR framing wherever it appears").

**7R-b — Author each action.** Each action has four parts:
1. **Action number** (e.g., "Action 2.3") — sequential by slide
2. **Shape identifier** — shape ID + name + current text (the precondition CIP will verify)
3. **Physical action** — select-all-and-delete + type new text + apply formatting (or: delete shape entirely, insert new shape, resize, etc.)
4. **New content VERBATIM** — every word, including bold markers, superscript markers, em-dashes, paragraph breaks. Any NEW prose (not a verbatim lift from a source) must pass `house-voice.md` — the voice rules and the anti-AI-tell pass — before it goes in the action/spec.

**7R-c — Handle structural changes carefully.**
- **Inserting a new slide:** specify the master layout name (from inventory), position (between which existing slides), and provide complete shape-by-shape content. After insertion, downstream slide numbers shift — account for it in references and post-edit checklist.
- **Deleting a slide:** specify the slide's title (precondition) for CIP to verify before deleting. Migrate any content from that slide that should be preserved elsewhere BEFORE the deletion action.
- **Resizing or repositioning:** state current geometry (from inventory) and target geometry explicitly in inches.

**7R-d — Write the preflight + global rules + post-edit checklist.**
- **Preflight:** CIP verifies the slide count + title list matches expected before doing any edits.
- **Global rules:** preserve font/size/color unless action says otherwise; preserve shape geometry unless action says otherwise; superscript handling; em-dash typing; stop list reminders (don't ever type the killed phrases).
- **Post-edit checklist:** binary pass/fail items CIP reports back after every edit completes — including specific stop-list items as verifiable assertions.

### Phase 8 — Verification gate (mandatory before shipping)

Before assembling the prompt/script for CIP, CC re-reads canonical sources for every critical numeric/quote:

- **Every numeric in any KPI, table, chart, or prose block** is re-checked against the sizing model Investment Summary tab (canonical) or the cited tab
- **Every quoted passage** from sponsor or V23 materials is re-checked against the source file
- **Every research finding** that survives into the final OM is re-fetched from the cited URL (the actual passage, not just the citation) so we know it still says what the subagent said it said
- **Cross-document consistency** — cross-check 5–10 key figures across the prose: PP, total cap, equity ask, debt, IRR, EM, NOI Yr 1, NOI Yr 5, exit value, exit cap rate
- **(Revision mode) Stop-list compliance** — search the proposed edit script for every phrase in the Phase 1.5 stop list. If any survives, fix or surface
- **(Revision mode) Shape inventory consistency** — every "Action N.M" references a shape ID that exists in the inventory with current text matching the action's precondition

**Write the audit ledger.** Record the verification as a persistent artifact — `<deal-folder>\x V23\<deal>-OM-Audit-Ledger.md` — one row per critical claim: `Claim/figure | Value | Source (file+tab/page or URL) | As-of date | Tier | Verified (Y/N)`. This is the reviewable trail for every number and quote in the deck; surface its path in Phase 10. A figure that is not in the ledger as Verified=Y must not ship (mark it `TBD` instead).

#### Source-of-truth conflict resolution

When two internal sources cite the same metric with DIFFERENT values (e.g., Skyway Exec Summary 26.77% IRR vs. Frontage Park OM case study 32.82% IRR — same deal, different points in time):

1. **Identify the conflict explicitly** — capture: metric, value A + source A + date A, value B + source B + date B.
2. **Pick the most recent source** as canonical for the new OM. Date is the tiebreaker.
3. **Flag the conflict in the "Data Conflicts" appendix** of the user-facing output. Format: "Skyway IRR — used 32.82% (Frontage Park OM case study, March 2026, post-close updated). Earlier figure 26.77% (Skyway Exec Summary, September 2024, pre-close underwriting). If you want the pre-close version restored, update Action X."
4. **Never silently average, hedge, or fudge.** Pick one, cite it, surface the alternative.

If anything fails verification (number doesn't match, quote drifted, URL rotted): fix it before shipping. If a research finding can't be re-verified: replace with a verifiable equivalent or mark "TBD — confirm with sponsor."

### Phase 9 — Assemble the output for CIP

#### New-build mode (Phase 9-NB) — CC generates the file, then a polish prompt

**Step 1 — CC generates the deck.** Serialize the Phase 7-NB content as a `build-deck.py` JSON spec (`template` = `assets/v23-template.pptx`, `target` = `\x V23\<deal>-v1.pptx`, `deal_name` for footer attribution, `slides` array). Run:

```
python "<skill-dir>/scripts/build-deck.py" spec.json
```

This produces a near-finished `.pptx` with the house theme/master/footer inherited, native KPI strips/tables/charts, and labeled placeholders for bespoke-visual slides. Then run `extract-pptx-inventory.py` on the output to verify slide count, text, and that charts/tables landed. **Tell the user to open it to judge visual quality — CC cannot render.**

**Step 2 — assemble the CIP POLISH prompt** (not a build-from-scratch prompt). Read `prompt-template.md` (now a polish prompt) and substitute:

| Placeholder | What to substitute |
|---|---|
| `{{DEAL_DISPLAY_NAME}}` | Tracker label (e.g., "NPV Florida IOS Strategy") |
| `{{GENERATED_FILE}}` | Path to the CC-generated `.pptx` from Step 1 |
| `{{PLACEHOLDER_SLIDES}}` | The list of placeholder slides build-deck.py flagged (slide #, layout key, the `note`), each with the Graph URI(s) of the visual asset to place |
| `{{VISUAL_ASSETS_BLOCK}}` | Graph URIs for the images/aerials/renderings CIP must place |

(Visual QA is already covered by the template's Step 6/7 checklist — no per-deal checklist injection needed.)

CIP's job is now narrow: open the CC-generated file, fill the flagged placeholder slides (place images/build the bespoke visual), and run visual QA. It does NOT compose the deck. Use the full connector name **"Microsoft 365 SharePoint/Graph search MCP connector"** for image retrieval (CIP doesn't recognize "365 MCP").

The polish prompt carries the **anti-AI ruleset (`house-voice.md` Part 2)** and **Operational Rules (Office.js)** as cross-cutting constraints, but most text is already in-voice from CC — CIP should not rewrite it.

#### Revision mode (Phase 9-R) — choose a delivery path FIRST

Revision mode has two delivery paths. **Default to Path A** (CC applies edits directly); use Path B (CIP edit script) only for the edits Path A can't handle well.

**Why CC-direct is the default:** the PowerPoint JS API that CIP drives is slow, quota-expensive, per-turn-capped, and weak at charts/images/geometry. CC applying edits through python-pptx is fast, free, deterministic, preserves run formatting, and produces a finished file — empirically verified (text/table/chart edits round-trip as valid .pptx). The only hard constraint: CC must work on a **copy**, never the file the user has open (file lock) — which also satisfies "never touch the original."

**Path A — CC applies edits directly (DEFAULT; deterministic edits).**
Use for the deterministic majority: text/number replacements, table-cell edits, chart-data edits, slide deletes. CC builds a JSON edit spec and runs the engine:

```
python "<skill-dir>/scripts/apply-revision-edits.py" edits.json
```

The engine (`scripts/apply-revision-edits.py`):
- Copies `source` → `target` first (never edits the original in place).
- Targets every shape by `shape_id` (same IDs the inventory emits).
- Verifies a precondition (`expect` = current-text substring) before each edit; on mismatch it SKIPS that edit, prints the actual current text, and exits non-zero — it does not guess.
- Preserves run formatting (font, size, color, bold, italic) on text/cell edits.
- Ops: `set_text`, `set_rich_text` (inline-bold segments), `set_cell`, `set_chart_series`, `delete_slide` (with `expect_title` precondition).
- Prints a PASS/SKIP/ERROR report.

The JSON edit spec is what CC authors in Phase 7-R instead of (or alongside) the markdown action list. Each op carries slide (1-based), shape_id, the `expect` precondition, and the new content verbatim. Output: a finished revised `.pptx` saved to `\x V23\<deal>-vN.pptx` (a NEW file — never the original, never the open file). After running, re-run `extract-pptx-inventory.py` on the output to verify the edits landed and the stop-list phrases are gone.

**Path B — CIP edit script (for live / visual-judgment edits only).**
Reserve for edits that genuinely need the live app: resizing/repositioning shapes "until it looks right," image/logo placement, anything requiring visual judgment CC can't make blind, or when the user explicitly wants changes applied interactively in their open session. Also the fallback if python-pptx can't cleanly express an edit (e.g., complex inline formatting the `set_rich_text` op doesn't cover). Assemble a shape-level edit script with this structure (a worked example lives in `\x V23\CIP-Edit-Script.md` from prior runs; mirror its shape):

```
═══ CIP EDIT SCRIPT — paste into Claude in PowerPoint ═══

How to use:
1. Open the canonical .pptx file: <full filename>
2. Open Claude in PowerPoint (right-hand pane)
3. Copy everything between the COPY markers below
4. Paste into Claude in PowerPoint
5. CIP executes every action in order

━━━━ COPY FROM HERE ━━━━

# PRE-FLIGHT — DO THIS FIRST, DO NOT SKIP
[slide count + title list, both expected; CIP halts if mismatch]

# GLOBAL RULES — APPLY TO EVERY ACTION
[font preservation; shape geometry preservation; superscript handling;
 em-dash typing; stop-list of phrases CIP must never type;
 reporting cadence (e.g., one line per slide completed); save cadence]

# SLIDE N — <SLIDE TITLE>
**Action N.1** — Shape **id X** (current text: "<verbatim precondition>")
- Select all text. Delete. Type:
  <verbatim new text>

[... every action, every slide ...]

# POST-EDIT CHECKLIST — REPORT BACK
- [ ] Total slide count is <N>
- [ ] No instance of "<stop-list phrase 1>" appears anywhere
- [ ] No instance of "<stop-list phrase 2>" appears anywhere
- [ ] [other binary pass/fail items]
- [ ] File saved as <full filename> (do NOT overwrite a different version)

━━━━ END COPY ━━━━

# NOTES TO USER (NOT FOR CIP)
[Source-of-truth conflicts flagged in Phase 8 — listed here with each one's
 chosen value + alternative + how to switch]
[Open questions / unresolved ambiguities]
[Things deliberately NOT changed and why]
```

Save the edit script to `<deal-folder>\x V23\CIP-Edit-Script.md` (create the subfolder if it doesn't exist). The `\x V23\` convention keeps V23-authored revision artifacts segregated from sponsor materials.

### Phase 10 — Print to user

#### New-build mode

Print, in this order:
1. **The generated file path** (`\x V23\<deal>-v1.pptx`) + the build-deck.py per-slide report (rendered vs placeholder).
2. **Verification**: slide count + that charts/tables/KPIs landed (from the inventory re-extraction). State plainly: "Open it to judge visual quality — I can't render."
3. **The list of placeholder slides** CIP must finish (slide #, what to place).
4. **The CIP polish prompt**, paste-ready:

```
═══ READY: open the generated deck in PowerPoint, then paste this into Claude in PowerPoint ═══

How to use:
1. Open the CC-generated file: <generated .pptx path>
2. Open Claude in PowerPoint (right-hand pane)
3. Copy everything between the COPY markers below
4. Paste into Claude in PowerPoint — it will fill the flagged placeholder slides, place images, and run visual QA. It will NOT recompose the deck.

━━━━ COPY FROM HERE ━━━━

<the filled polish prompt — prompt-template.md with placeholders substituted>

━━━━ END COPY ━━━━
```

5. **Coverage & Open Items** — the path to `\x V23\<deal>-OM-Coverage-Manifest.md` plus a short front-facing summary: what's covered, what's `TBD`/client-needed, and what was researched to fill a gap.
6. **Audit ledger** — the path to `\x V23\<deal>-OM-Audit-Ledger.md` (every figure → source → as-of date → verified).
7. The **Data Conflicts appendix** if Phase 8 found any.
8. ⚠ Any visual-asset Graph URI that couldn't be resolved (look up manually before pasting).

#### Revision mode

**Path A (CC-direct, default):**
- Run the engine, then print its PASS/SKIP/ERROR report.
- The path to the finished revised file (`<deal-folder>\x V23\<deal>-vN.pptx`).
- Confirmation that you re-ran `extract-pptx-inventory.py` on the output and the edits landed + stop-list phrases are gone (PASS/FAIL per phrase).
- **The Data Conflicts appendix** from Phase 8.
- **Audit ledger** path (`\x V23\<deal>-OM-Audit-Ledger.md`) for figures changed or added; plus the coverage-manifest path if Phase 3.5 was run.
- Any edits routed to Path B (and why), plus any unresolved questions.
- If any edit SKIPPED on a precondition mismatch, surface it — do not silently ship a partial revision.

**Path B (CIP edit script, when used):**
- The path to the saved edit script (`<deal-folder>\x V23\CIP-Edit-Script.md`).
- A tight summary of slide-by-slide actions (counts only, not the full prose).
- **The Data Conflicts appendix** from Phase 8.
- The stop-list compliance status (PASS/FAIL per phrase).
- Any unresolved questions for the user.
- Do NOT paste the full edit script into the conversation — it's long. Reference the file path.

## OM Coverage Checklist

The asset-class-agnostic set of analytical purposes an institutional OM must serve. Phase 3.5 diffs the deal folder against this list; Phase 7 maps each onto deal-appropriate sections (do NOT treat these as literal slide titles). An item may be marked **N/A** in the manifest only with a one-line justification.

1. **The Story / Investment Thesis** — the one-sentence thesis + the 3–5 load-bearing claims it rests on. *Fill-route: synthesis.*
2. **Executive Summary** — deal-at-a-glance: asset, location, ask, headline returns. *Synthesis from the sizing model.*
3. **Setting — Market & Submarket** — vacancy, asking rents, supply pipeline, absorption, cap-rate trend in the EXACT submarket, as-of dated. *Research-fillable.*
4. **The Opportunity / Business Plan** — what we do to create value and on what timeline. *Sponsor OM + V23 analysis (client-only if absent).*
5. **The Asset** — physical/operational description, location context, photos/aerials/renderings. *Client-only for proprietary visuals.*
6. **Sponsor / Operator** — track record, AUM, prior exits, principal bios, capital partners, any public disputes. *Research-fillable (public) + client-only (proprietary).*
7. **Financials — Sources & Uses** — total capitalization, equity ask, debt amount + terms, the full cap stack. *Client-only (sizing model).*
8. **Returns** — IRR, equity multiple / MoIC, NOI trajectory, exit value + exit cap rate, hold period. *Client-only (sizing model).*
9. **Comparables** — sale comps + lease/rent comps with $/SF, $/AC, or $/door and cap rates, as-of dated. *Research-fillable (+ V23 comp DB).*
10. **Risk Register** — each material risk framed as probability × impact × mitigation. *Synthesis.*
11. **LP Cutting-Questions** — pre-empt the hardest diligence questions an institutional LP will ask. *Synthesis.*

Emphasis and depth vary by asset class — see "Asset-class adaptation guidance." Items 7–8 are the load-bearing client-only inputs: if no sizing model is present, the manifest flags them Missing/client-only and the deck builds with `TBD — confirm with sponsor` rather than invented numbers.

## Source-quality bar

Acceptable sources for any cited claim in the OM:

- **Tier 1 — primary institutional research:** CoStar, Green Street, REIS, RCA/MSCI Real Capital Analytics, Newmark Research, JLL Research, CBRE Research, Cushman & Wakefield Research, Colliers Research, NAREIT, NCREIF, INREV/ANREV, Federal Reserve/FRED, BLS, Census ACS, BEA, Top-tier shop white papers (Blackstone, Brookfield, Starwood, Carlyle, Ares, KKR, Oaktree)
- **Tier 2 — institutional trade pubs:** PERE/PEI Media, Institutional Real Estate Inc., ULI/PwC Emerging Trends, IPE Real Assets, GlobeSt Real Estate Forum
- **Tier 3 — academic/specialized:** Cornell Baker Program, MIT Center for Real Estate, Wharton Real Estate, peer-reviewed CRE finance journals

**NOT acceptable:** Medium/Substack posts (unless credentialed author with institutional affiliation), broker marketing PDFs as data sources (their listings are fine; their thesis pieces require Tier 1/2 corroboration), Wikipedia citations as primary sources, generic blog posts, opinion pieces without data, vendor-sponsored "studies" without methodology, anonymous social media, Reddit, generic press releases.

Every cited claim must include an as-of date. Stale comps are worse than missing comps.

**This standard is also codified globally** at `~/.claude/rules/cre-source-tiers.md` (applies to all of this user's CRE research, not just OMs). The skill keeps its own copy here because the plugin must carry the standard to teammates who don't have that local rule — keep the two consistent.

## Subagent dispatch rules

1. **Reference DNA subagent uses the Explore agent type** (read-only, fast pattern recognition across many files). Skip in revision mode.
2. **Research subagents use the general-purpose agent type** (web access + synthesis).
3. **Dispatch parallel research agents in a SINGLE message with multiple Agent tool calls** for concurrent execution.
4. **Each research subagent must receive a single, narrowly-scoped research question** — not a category. "What is the Q1 2026 Tampa Bay IOS vacancy rate per CoStar / Green Street?" not "Submarket research."
5. **Required return format is structured** — claim + quoted passage + URL + as-of date + confidence flag.
6. **Cap research budget per agent at ~5 minutes** but allow deep dives where the source quality is high. Total skill runtime 10–30 minutes is acceptable.
7. **Revision-mode parallel reads.** When CC needs to read multiple long source files (sponsor OM sections, prior pipeline PDF, V23 deal analysis docx), dispatch general-purpose subagents in parallel — one file per subagent — rather than reading sequentially in CC's main context. Returns are structured dumps that CC then synthesizes.

## Verification gate procedure

After Phase 7 synthesis, before Phase 9 assembly:

1. **Numerics audit** — for every numeric in the pre-written content (or in every edit-script "type this" block), identify its source path + tab/page. Re-open and verify. Record each in the persistent audit ledger (`\x V23\<deal>-OM-Audit-Ledger.md`): claim → value → source → as-of date → tier → verified Y/N.
2. **Cross-document audit** — pick 5–10 key figures (PP, equity ask, debt, IRR, EM, etc.) and verify they're identical across every prose block, KPI, table, and chart in the output.
3. **Quote audit** — every quoted passage attributed to sponsor materials or V23 work product is re-read against the source file.
4. **Research audit** — for each research finding cited in the OM, re-fetch the source URL via WebFetch and verify the passage still appears as cited.
5. **Source-quality audit** — every citation belongs to a Tier 1/2/3 source per the bar above. Any Medium/blog/Wikipedia citation is dropped or replaced.
6. **Conflict audit** — for every load-bearing numeric, ask: "does any other source in this folder cite a different value?" If yes, apply the conflict-resolution procedure in Phase 8.
7. **(Revision mode) Stop-list audit** — grep the edit script for every phrase in the Phase 1.5 stop list. Each must return zero matches.
8. **(Revision mode) Inventory audit** — every action's shape ID + current-text precondition matches the inventory.

If anything fails, fix before assembly.

## Asset-class adaptation guidance

The skill is class-agnostic but expects CC to adapt research scoping and section emphasis to the asset class:

- **Industrial / IOS:** trailer/container demand, port volumes, e-commerce logistics, infill scarcity, drayage corridors, BTS vs. spec
- **Office:** tenant absorption by industry, sublease overhang, return-to-office, conversion optionality, sublet markets
- **Multifamily:** rent growth, supply pipeline, absorption, vintage discount, workforce vs. luxury, regulatory environment
- **Hospitality:** RevPAR/ADR/occupancy, STR comp set, brand vs. independent, F&B and events drivers
- **Data center / powered land:** power capacity, grid interconnection queue, hyperscaler demand, latency to fiber, ESG and water constraints
- **Retail:** trade area demos, anchor credit, co-tenancy, sales/SF, ground-floor vs. mall
- **Senior / Student Housing:** demographic tailwinds, university or hospital catchment, regulatory licensing, operator quality
- **Land / Mixed-use:** entitlement status, infrastructure timing, phasing economics, public incentives
- **Hospitality / Marina / Specialty:** asset-class-specific operating metrics

This list is suggestive, not exhaustive. CC chooses scopes based on what the deal needs.

## Safety rules

- Never fabricate a Graph URI, a numeric, a market stat, or a research finding. If anything can't be verified, mark "TBD — confirm with sponsor" or "TBD — confirm source" and surface to the user at the end.
- Never substitute a numeric into output content that hasn't been verified in Phase 8.
- Never use the MCP shorthand "365 MCP" in the prompt for CIP — always use the full name "Microsoft 365 SharePoint/Graph search MCP connector."
- Never let subagent returns ship without re-verifying their citations against the actual source URL.
- Never assume tracker naming matches folder naming — see `[[project-npv-ios-deal-naming]]` for the canonical example; map by ask + returns, not by city string.
- Never assume the "newest-looking" file (by name suffix like v2, v3, final, FINAL2) is actually the live one. Ask. Modification timestamps can lie if SharePoint sync wrote stale local copies; the user is the only authority on which file is live.
- Never silently switch operating mode mid-run. If Phase 0 detected new-build and partway through CC realizes a `.pptx` is present, stop and re-detect mode with the user.
- Never write generic value-add language ("compelling," "strong," "robust") without substituting specifics; never list risks without probability × impact × mitigation.
- Never tell CIP "use the content I wrote earlier" or "reference the prior section." CIP doesn't reliably retain across turns; every action must be self-contained.
- Never silently average, hedge, or fudge conflicting source values. Pick the most recent, cite, surface alternatives.
- Always run the Phase 3.5 coverage manifest and surface gaps to the user — flag holes, never silently plug them. Client-only Missing items ship as `TBD — confirm with sponsor`, never as a guessed value.
- Always write the Phase 8 audit ledger; never ship a figure that isn't in it as Verified=Y.
- Preserve the LAYOUT VARIETY MANDATE (new-build mode); never let two consecutive content slides share the same zone pattern; aim for ≥ 7 distinct arrangements across the deck.
- (Revision mode) Never overwrite the original file the user has marked as the live version. If revision mode is detected against `<filename>.pptx` and the user says "use v2 only," the edit script targets v2; the original stays untouched. The edit script's preflight + post-edit checklist must explicitly name the target file.

## Mode reference (quick glance)

| Concern | New-build mode | Revision mode |
|---|---|---|
| Trigger | "build / create / generate the OM" | "refresh / revise / update / rework the OM" |
| Detection | No `.pptx` in folder | `.pptx` exists in folder or `\x V23\` |
| Phase 0 output | "Mode: new-build" | "Mode: revision; target = <filename>" |
| Phase 1 ambiguity asks | Asset class, sponsor identity, deal folder | All of NB + which .pptx is live, which pipeline is canonical |
| Phase 1.5 | Optional (only if user provided feedback) | Mandatory — stop list is load-bearing |
| Phase 3 .pptx extraction | Skip | Required (run `scripts/extract-pptx-inventory.py`) |
| Phase 3.5 coverage manifest | Build + save (`<deal>-OM-Coverage-Manifest.md`); warn-only, never halts | Optional (check existing deck's coverage) |
| Phase 5 Reference DNA | Optional (DNA codified in `house-voice.md` + `layout-repertoire.md`) | Skip |
| Phase 7 output | `build-deck.py` JSON content spec (text in-voice + layout keys) | Per-shape actions with IDs + verbatim text |
| Phase 8 verification adds | Conflict resolution + anti-AI pass (`house-voice.md`) | Conflict resolution + stop-list audit + inventory audit + anti-AI pass on new prose |
| Phase 8 audit ledger | Saved (`<deal>-OM-Audit-Ledger.md`) | Saved (figures changed/added) |
| Phase 9 delivery | CC runs `build-deck.py` → finished `.pptx`; then short CIP polish prompt | **Path A (default):** CC runs `apply-revision-edits.py` → finished `.pptx`. **Path B:** CIP edit script |
| Phase 10 to user | Generated file path + verification + polish prompt + Data Conflicts | Path A: engine report + revised-file path + verification. Path B: edit-script path. Both: Data Conflicts + stop-list status |
| Typical CIP behavior | Polishes a CC-generated deck: fill placeholders, place images, visual QA | Path A: CIP not used. Path B: CIP executes select/delete/type/format/save |

## Updating this skill

If you need to refine the architecture or add capabilities:

1. Edit `SKILL.md` (this file) — runbook changes
2. Edit `house-voice.md` — the writing voice + anti-AI-tell ruleset (applies to all authored prose, both modes)
3. Edit `layout-repertoire.md` — layout selection system + catalog
4. Edit `prompt-template.md` — the CIP POLISH prompt (new-build: fill placeholders + place images + visual QA)
5. Edit `scripts/extract-pptx-inventory.py` — shape inventory (reads charts/tables/run-formatting)
6. Edit `scripts/apply-revision-edits.py` — revision engine (Path A): set_text/rich_text/cell/chart_series/geometry, insert_slide, delete_slide
7. Edit `scripts/build-deck.py` — new-build generator (core layouts from the house template)
8. Edit `scripts/make-template.py` + `assets/v23-template.pptx` — regenerate the house template if the master/theme changes
9. Edit `~/.claude/rules/cre-source-tiers.md` — the GLOBAL CRE source-tier + claim-auditability standard (this user's machine); keep it consistent with the `Source-quality bar` + `OM Coverage Checklist` sections here
5. Update memories if framework knowledge improves (`[[user-the-story-framework]]`, `[[user-vanadium-analysis-conventions]]`)
6. Bump version in `.claude-plugin/plugin.json` AND `.claude-plugin/marketplace.json`
7. Commit so clients pick up the change

## Related memories (CC reads these as part of running the skill)

- `[[user-the-story-framework]]` — The Story / argumentative narrative spine; institutional research-backed
- `[[user-vanadium-analysis-conventions]]` — voice, source bar, recency, risk-mitigant pattern, sponsor-defensibility, purpose-based section framing
- `[[feedback-search-breadth]]` — search/research discipline
- `[[project-npv-ios-deal-naming]]` — example of tracker-vs-folder naming reconciliation
