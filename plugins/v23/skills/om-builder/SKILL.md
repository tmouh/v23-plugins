---
name: om-builder
description: "Build a Vanadium-grade commercial real estate Offering Memorandum by front-loading all analytical work in Claude Code (deep folder reads + parallel research subagents + The Story synthesis), then handing Claude in PowerPoint a composition-only prompt with pre-written slide content. Triggers: build/create/generate an OM, refresh an existing OM, point at a SharePoint-synced deal folder under \\1- Realty\\1- Deals\\. Asset-class agnostic. The user pastes one block into Claude in PowerPoint, which composes visually using Vanadium house style + the layout variety mandate."
---

# v23-om-builder

## Overview

Building an institutional CRE OM has two distinct phases:
1. **Analysis** — read the deal, research the gaps, construct The Story, write the prose
2. **Composition** — translate that content into a designed deck

This skill puts **all of Phase 1 inside Claude Code** ("CC") and hands **Phase 2 to Claude in PowerPoint** ("CIP") as a composition-only prompt. CIP no longer reads sponsor OMs, runs underwriting checks, or does research — it receives pre-written headlines, prose blocks, bullets, KPI values, table data, and source lines, then composes them visually using Vanadium house style + the LAYOUT VARIETY MANDATE.

**Why this architecture:**
- CIP's context budget is tight on long deals; pre-digesting in CC eliminates rework
- Subagent isolation in CC means raw file reads + research stay out of the synthesis context window
- The user's workflow is unchanged: plug CC into a folder, run the skill, copy/paste into CIP

The skill is **asset-class agnostic**. It does not hardcode section names (Multifamily ≠ IOS ≠ Office). Instead it enforces analytical *purposes* that any institutional OM must serve, and lets the deal's substance determine the spine. See `[[user-the-story-framework]]` and `[[user-vanadium-analysis-conventions]]` for the framework CC applies.

## When to use

- User says "build the OM" / "create an OM" / "generate offering memorandum" / "refresh the OM"
- User points at a SharePoint-synced deal folder under `\1- Realty\1- Deals\<deal>`
- The deal has at minimum: sponsor materials (OM/exec summary) + a sizing model (or equivalent underwriting)

Do NOT use for:
- One-pagers, teasers, or sales flyers (different artifact)
- Re-styling an existing deck without re-doing analysis (use a different prompt)
- Building decks directly in Claude Code (CIP does the visual work)

## Hybrid architecture (read this before running)

**CC reads DIRECTLY in its own context** (precision required, no summarization tolerance):
- All sponsor materials in the deal folder — OMs, exec summaries, sizing models (every relevant tab), lease flyers, photo packets
- Any prior version of the OM being refreshed (V01, V02, etc.)
- V23 internal work product — deal-analysis docx, investor-outreach docx, V23 1-pagers, internal memos
- Tracker/pipeline files referenced by the user

**Subagents handle, in isolated context** (digest IS the natural output):
- **Reference DNA subagent** — one Explore agent reads 5–8 prior Vanadium production OMs/decks, returns layout/voice/structural observations as a digest
- **3–5 Research subagents** — general-purpose agents in parallel, each scoped to ONE research question, return cited findings with quoted passages + URLs + as-of dates

**CC synthesizes** with access to both raw direct-read data AND subagent digests, writes The Story + pre-written slide content, then runs a **verification gate** that re-reads canonical sources for every critical numeric/quote before shipping.

## Runbook

### Phase 1 — Resolve the deal folder

Ask the user for the deal folder path if not given. Path typically looks like:
`C:\Users\<user>\Vanadium Group LLC\V23 - Database\1- Realty\1- Deals\<Deal Folder>`

Validate:
- Folder exists locally (SharePoint sync) and contains source files
- Identify deal asset class from folder name + a quick scan of file titles (Industrial / IOS / Multifamily / Office / Hospitality / Mixed-Use / Data Center / Land / Retail / Senior Housing / Student Housing / etc.) — this informs research scoping later
- Note whether this is a refresh (prior OM exists in folder) or new build

If validation fails, stop and tell the user what's wrong. Do not proceed.

### Phase 2 — Enumerate folder + classify files

Enumerate every file. Classify into:

- **Canonical numerics** — sizing models, underwriting xlsx (Investment Summary, Pro Forma, Rent Roll, Waterfall, Comps tabs)
- **Sponsor narrative** — sponsor-provided OMs, exec summaries, decks, lease flyers, pitch materials
- **V23 work product** — deal analysis docx, investor outreach docx, prior V23 OMs/1-pagers, internal memos, placement lists
- **Pipeline / tracker** — deal pipeline xlsx/PDF, naming maps
- **Visual assets** — photos, renderings, floor plans, aerial shots, site maps (CIP will open these directly for image placement)
- **Admin / legal** — agency agreements, contracts (read for terms ONLY if the OM references them; otherwise skip)

### Phase 3 — CC reads canonical files DIRECTLY

CC opens, in its own context:
- Every sizing model — Investment Summary tab is canonical for cost basis, cap stack, IRR, MoIC, NOI trajectory. Pro Forma, Rent Roll, Waterfall, Comps tabs for supporting detail.
- Every sponsor OM PDF — extract narrative voice, asset story, business plan, in-place leasing context, sponsor-provided market commentary
- Every V23 work product — V23 has already analyzed this deal internally; mirror that voice and conclusions; the V23 1-pager (if it exists) is the closest model for what Vanadium says about this deal
- The previous OM (if a refresh) — read fully so the new version improves on it rather than duplicates it

CC extracts and structures (in working notes):
- Every numeric needed for the deck, with source path and tab/page reference
- The sponsor's existing thesis and where it's strong vs. thin
- V23's internal point of view on this deal (which is what we'll mirror, not the sponsor's)
- Gaps — what's missing from the folder that an institutional LP would demand

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

### Phase 5 — Dispatch Reference DNA subagent

Dispatch ONE Explore-type subagent with a comprehensive scope of 5–8 prior Vanadium production OMs/decks. The subagent reads each, returns observations grouped by:

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

### Phase 7 — Synthesize: build The Story + write pre-written slide content

In CC's main context, with access to both the direct-read deal materials AND the subagent digests:

**7a — Build The Story (one paragraph, the load-bearing thesis).** Apply `[[user-the-story-framework]]`. The Story is one defensible sentence — the thesis the entire deck argues — followed by a paragraph naming the 3–5 load-bearing claims that have to be true for the thesis to hold. Every section the OM will have must trace back to this.

**7b — Sequence the narrative spine.** Per The Story framework, the institutional consensus is: Setting → Strategy/Business Plan → Asset → Sponsor → Returns/Cap Stack/Risk → Executive Summary written last but positioned first. Adapt this to the deal's substance. Platform raises differ from single-asset acquisitions.

**7c — Identify section purposes (NOT names).** From `[[user-vanadium-analysis-conventions]]`, the deliverable must accomplish: establish setting, define opportunity, position asset, tell The Story, show business plan, vet sponsor, stack capital, surface returns, frame risks, anticipate LP cutting questions. Map each onto specific sections appropriate to this deal's substance. Do not force a generic section list.

**7d — Write the pre-written content per section.** For each section:
- **Headline** — plain-English takeaway sentence (not category label)
- **Prose blocks** — 2–4 idea-blocks of 2–4 lines each, with bold inline for key numerics and proper nouns
- **Bullets** (where parallel-list applies — Investment Highlights especially): bold thesis line + body
- **KPI values** — numerics with units, label, sub-detail, source line
- **Table data** — rows, columns, exact values, sources
- **Chart data** — series, x-axis, y-axis, exact values, source
- **Visual references** — Graph URIs for images/floor plans/aerials CIP should place
- **Layout suggestion** — describe the SPECIFIC arrangement in plain English per the LAYOUT VARIETY MANDATE (not "Layout 3"); note which reference deck inspired it; if it's a non-default arrangement, give a one-sentence rationale
- **Source line** — formatted citation with as-of date

Voice rules from `[[user-vanadium-analysis-conventions]]` apply throughout: argumentative essay tone; risks framed with probability × impact × mitigation; sponsor-defensible language; cross-document numeric consistency; institutional source tiers only.

### Phase 8 — Verification gate (mandatory before shipping)

Before assembling the prompt for CIP, CC re-reads canonical sources for every critical numeric/quote:

- **Every numeric in any KPI, table, chart, or prose block** is re-checked against the sizing model Investment Summary tab (canonical) or the cited tab
- **Every quoted passage** from sponsor or V23 materials is re-checked against the source file
- **Every research finding** that survives into the final OM is re-fetched from the cited URL (the actual passage, not just the citation) so we know it still says what the subagent said it said
- **Cross-document consistency** — cross-check 5–10 key figures across the prose: PP, total cap, equity ask, debt, IRR, EM, NOI Yr 1, NOI Yr 5, exit value, exit cap rate

If anything fails verification: fix it before shipping. If a research finding can't be re-verified (URL changed, link rotted): replace with a verifiable equivalent or mark "TBD — confirm with sponsor."

### Phase 9 — Assemble the composition-only prompt for CIP

Read `prompt-template.md` and `layout-repertoire.md`. Substitute:

| Placeholder | What to substitute |
|---|---|
| `{{DEAL_DISPLAY_NAME}}` | Tracker label preferred (e.g., "NPV Florida IOS Strategy") — used in footer attribution |
| `{{DEAL_FOLDER_DISPLAY}}` | Folder name as it appears under `\1- Realty\1- Deals\` (for context only) |
| `{{THE_STORY}}` | The one-paragraph Story from Phase 7a, including the load-bearing claims |
| `{{VISUAL_ASSETS_BLOCK}}` | Graph URIs for image/floor-plan/aerial files only — CIP opens these for placement, NOT for analysis |
| `{{SECTIONS_BLOCK}}` | All pre-written section content from Phase 7d, in order, with headlines, prose, KPIs, tables, chart data, visual refs, layout suggestions, source lines |
| `{{LAYOUT_REPERTOIRE}}` | Full contents of `layout-repertoire.md` inserted verbatim |
| `{{HOUSE_STYLE_BLOCK}}` | Vanadium house style spec — embedded inline in the prompt-template; do not externalize |

DO NOT substitute the canonical source files into the prompt as "open these and analyze." CC has already analyzed them. CIP receives content, not raw inputs.

DO substitute visual-asset URIs — CIP needs to open photo/rendering/floor-plan files to place them in the deck. Use the full connector name **"Microsoft 365 SharePoint/Graph search MCP connector"** in the prompt (CIP doesn't recognize "365 MCP" shorthand).

### Phase 10 — Print to user

Output structure:

```
═══ READY: paste this into Claude in PowerPoint ═══

How to use:
1. Open PowerPoint with the deal materials nearby (for any visuals CIP needs to fetch)
2. Open Claude in PowerPoint (right-hand pane)
3. Copy everything between the COPY markers below
4. Paste into Claude in PowerPoint
5. CIP will set the master slide + theme, then begin composing section by section using the pre-written content
6. CIP will pause after the cover + exec summary for your review

━━━━ COPY FROM HERE ━━━━

<the filled prompt — prompt-template.md with all placeholders substituted>

━━━━ END COPY ━━━━
```

If any visual-asset URI couldn't be resolved, list above the COPY block:

```
⚠ Could not resolve Graph URIs for these visual assets. Look them up manually before pasting:
  - <filename>
```

Optionally, save a backup of the assembled prompt to a file in the user's working directory for reproducibility.

## Source-quality bar

Acceptable sources for any cited claim in the OM:

- **Tier 1 — primary institutional research:** CoStar, Green Street, REIS, RCA/MSCI Real Capital Analytics, Newmark Research, JLL Research, CBRE Research, Cushman & Wakefield Research, Colliers Research, NAREIT, NCREIF, INREV/ANREV, Federal Reserve/FRED, BLS, Census ACS, BEA, Top-tier shop white papers (Blackstone, Brookfield, Starwood, Carlyle, Ares, KKR, Oaktree)
- **Tier 2 — institutional trade pubs:** PERE/PEI Media, Institutional Real Estate Inc., ULI/PwC Emerging Trends, IPE Real Assets, GlobeSt Real Estate Forum
- **Tier 3 — academic/specialized:** Cornell Baker Program, MIT Center for Real Estate, Wharton Real Estate, peer-reviewed CRE finance journals

**NOT acceptable:** Medium/Substack posts (unless credentialed author with institutional affiliation), broker marketing PDFs as data sources (their listings are fine; their thesis pieces require Tier 1/2 corroboration), Wikipedia citations as primary sources, generic blog posts, opinion pieces without data, vendor-sponsored "studies" without methodology, anonymous social media, Reddit, generic press releases.

Every cited claim must include an as-of date. Stale comps are worse than missing comps.

## Subagent dispatch rules

1. **Reference DNA subagent uses the Explore agent type** (read-only, fast pattern recognition across many files).
2. **Research subagents use the general-purpose agent type** (web access + synthesis).
3. **Dispatch parallel research agents in a SINGLE message with multiple Agent tool calls** for concurrent execution.
4. **Each research subagent must receive a single, narrowly-scoped research question** — not a category. "What is the Q1 2026 Tampa Bay IOS vacancy rate per CoStar / Green Street?" not "Submarket research."
5. **Required return format is structured** — claim + quoted passage + URL + as-of date + confidence flag.
6. **Cap research budget per agent at ~5 minutes** but allow deep dives where the source quality is high. Total skill runtime 10–30 minutes is acceptable.

## Verification gate procedure

After Phase 7 synthesis, before Phase 9 assembly:

1. **Numerics audit** — for every numeric in the pre-written content, identify its source path + tab/page. Re-open and verify. Track in a simple ledger (claim → source → verified Y/N).
2. **Cross-document audit** — pick 5–10 key figures (PP, equity ask, debt, IRR, EM, etc.) and verify they're identical across every prose block, KPI, table, and chart in the pre-written content.
3. **Quote audit** — every quoted passage attributed to sponsor materials or V23 work product is re-read against the source file.
4. **Research audit** — for each research finding cited in the OM, re-fetch the source URL via WebFetch and verify the passage still appears as cited.
5. **Source-quality audit** — every citation belongs to a Tier 1/2/3 source per the bar above. Any Medium/blog/Wikipedia citation is dropped or replaced.

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
- Never substitute a numeric into pre-written content that hasn't been verified in Phase 8.
- Never use the MCP shorthand "365 MCP" in the prompt for CIP — always use the full name "Microsoft 365 SharePoint/Graph search MCP connector."
- Never let subagent returns ship without re-verifying their citations against the actual source URL.
- Never assume tracker naming matches folder naming — see `[[project-npv-ios-deal-naming]]` for the canonical example; map by ask + returns, not by city string.
- Never write generic value-add language ("compelling," "strong," "robust") without substituting specifics; never list risks without probability × impact × mitigation.
- Preserve the LAYOUT VARIETY MANDATE; never let two consecutive content slides share the same zone pattern; aim for ≥ 7 distinct arrangements across the deck.

## Updating this skill

If you need to refine the architecture or add capabilities:

1. Edit `SKILL.md` (this file) — runbook changes
2. Edit `prompt-template.md` — what gets handed to CIP
3. Edit `layout-repertoire.md` — layout catalog + mandate
4. Update memories if framework knowledge improves (`[[user-the-story-framework]]`, `[[user-vanadium-analysis-conventions]]`)
5. Bump version in `.claude-plugin/plugin.json` AND `.claude-plugin/marketplace.json`
6. Commit so clients pick up the change

## Related memories (CC reads these as part of running the skill)

- `[[user-the-story-framework]]` — The Story / argumentative narrative spine; institutional research-backed
- `[[user-vanadium-analysis-conventions]]` — voice, source bar, recency, risk-mitigant pattern, sponsor-defensibility, purpose-based section framing
- `[[feedback-search-breadth]]` — search/research discipline
- `[[project-npv-ios-deal-naming]]` — example of tracker-vs-folder naming reconciliation
