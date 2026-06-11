# om-builder v6 — Design

**Date:** 2026-06-11 · **Status:** draft for Theo's review · **Scope:** rebuild the `v23:om-builder` skill around the process that actually produced the final NPV OM, then run it on the Coastal GA Multi Conversion Portfolio (bridge-lender OM) as its first live test.

---

## 1. Problem (from the NPV forensics, 2026-06-11)

The final NPV-Florida-IOS OM (6/9–6/10) was not produced by the skill. It was produced by a manual pipeline Theo invented between 6/4 and 6/9 — and the gap between what the skill did and what worked decomposes into four root causes:

1. **Stale plumbing.** The installed plugin is v4.0.0; the dev copy is v5.1.0. Improvements (house-voice, revision engine, build scripts) never reached the running copy. The skill's two foundational memories (`user_the_story_framework`, `user_vanadium_analysis_conventions`) live in the `Workspace-Vanadium-5-20-2026` project's memory folder and never load when running from a deal folder.
2. **One-shot architecture.** The skill generates analysis then hands a composition prompt to Claude-in-PowerPoint. What worked instead was a **gated artifact pipeline**: per-source data extraction → per-claim audit ledger (`00-DATA-AUDIT-TRAIL.md`) → a locked Build Blueprint signed off by stakeholders → in-place pptx build → render-and-inspect QA → an editorial consistency gate. Artifacts on disk, human gates between phases.
3. **Inverted knowledge hierarchy.** Externally-derived distillations were made load-bearing (the story-framework memory cites only third-party sources; house style was hand-frozen into hex codes and coordinates that drifted from the live decks; a hardcoded reference-deck list mixed registers — true OMs alongside a strategic pitch — and was resolved by fuzzy SharePoint search that could land on client-authored files). Meanwhile the actual V23 body of work was consulted by one optional subagent pass, skipped entirely in revision mode.
4. **CIP on the critical path.** Composition-by-paste lost context and required shape-level edit-script babysitting ("CIP types, it does not think" — HANDOFF-Fresh-Chat.md). The NPV endgame abandoned it for direct pptx manipulation.

Defect classes the skill never operationalized, all caught manually: deck-type misidentification (portfolio vs. platform), claim self-consistency ("$5MM minimum" alongside two sub-$5M deals), provenance discipline (projected returns framed as realized; an unverifiable comp shipped), cross-page numeric/style consistency (M vs MM, 25-vs-26 deals, thesis contradictions, leftover placeholders — Henry's 6/9 review).

## 2. Decisions locked with Theo (2026-06-11)

- Coastal GA OM audience = **bridge lenders** (per the 6/1/26 exclusive financing engagement). ≤25 pages, dense; target 20–23.
- **Skill rebuilt first**; the Coastal GA OM is v6's first live run, with Theo gating each artifact.
- **CC-native build** — Claude Code authors the .pptx directly; CIP is off the critical path (optional polish punch-list only).
- **Voice grounding: exhaustive sweep, no curated corpus.** "We have so many examples — you'll learn more the more you look at." No canonical reference list, no quality gatekeeping of a fixed set; the derivation is re-runnable as materials accumulate.
- **No recency bias.** Patterns are weighted by consistency across years (2023 Wind Gap Word-doc OMs count as much as 2026 decks), never by file date. Applies to visual DNA too.
- **Never anchor to any single deal.** "Lightly inspired" is the ceiling for any one deck. No per-run nearest-neighbor reference decks. 105 N 13's debt OM is mined only for which metrics a Vanadium debt OM shows.
- **The Story demoted** from "load-bearing element" to the thesis-and-claims discipline inside the blueprint phase.
- **Provenance hard rule:** "If you can't tell whether Vanadium created it, we probably didn't."

## 3. Architecture

Two halves: **(A) skill-build-time assets** produced by a Pattern Study and regenerable thereafter, and **(B) a per-OM runbook** that is a gated artifact pipeline.

### 3A. The Pattern Study (build-time; re-runnable)

**Enumeration.** Sweep the entire `V23 - Database` for V23-authored materials using provenance rules:
- *Positive signals:* `x V23` / `xV23` / `V23 - OM` directories; deal-folder `OM\` subfolders containing files with the V23 naming pattern (`<Deal> - OM - <date>`); known V23 outputs (investor memos, deal analyses, one-pagers).
- *Negative signals:* `Client Provided`, `Client Files`, broker-OM folders, sponsor data rooms.
- *Ambiguous:* listed for Theo to adjudicate; default exclude.

Census as of 2026-06-11: 10 dedicated work-product folders (~281 files: 151 pptx / 68 pdf / 62 docx) plus deal-folder `OM\` trees — e.g., Pektor Wind Gap alone spans 2023–2025 with straight-OM, Pref-OM, JV-OM, and BTS-memo registers, in both Word and PDF. The sweep also triages `4- Marketed Deals`, `x- Deals Archive`, and `x- Templates` (provenance unknown until inspected).

**Derivation.** Staged subagent fan-out; each agent reads a slice and returns evidence-cited observations (pattern → verbatim quotes → file + date). Synthesis weights each candidate pattern by **cross-time, cross-deal consistency**; single-deck idiosyncrasies are excluded no matter how recent or polished the deck. Quotes serve as evidence in the derivation record, not as copy-this examples.

**Artifacts** (live in the skill folder; each carries a "regenerate by re-running the sweep" note):
- `voice-model.md` — deal-agnostic diction, rhythm, and structural patterns; every pattern cited to ≥3 materials spanning years. Replaces house-voice Part 1. The anti-AI-tell ruleset (current Part 2) is retained unchanged as the backstop — it is external research by design.
- `coverage-checklists.md` — per capital-type register (equity / debt / pref / JV): the sections and metrics a Vanadium OM of that register presents. Derived from the sweep's debt/pref/JV materials (105 N 13 vDebt, Wind Gap Pref and JV OMs, lender-facing files). Checklists, not templates.
- `design-system.md` — the visual DNA that is stable across decks (typography behavior, palette, composition habits, footer/source-line conventions), explicitly separating durable house DNA from per-deck choices. Supersedes the hardcoded style block in prompt-template.md.
- `layout-repertoire.md` — keep the v5.1 content→layout selection system (research-grounded, register-agnostic); validate and extend it against arrangements actually observed in V23 decks during the sweep.

**Validation gate (the "recreate it perfectly" bar).** Reproduction test: generate sample passages/slide copy in the claimed voice for held-out deals; adversarial judge agents attempt to distinguish generated vs. real V23 passages; iterate until judges can't reliably tell, then Theo spot-checks. Results recorded in the study artifact. The voice model does not ship until it passes.

### 3B. Per-OM runbook (phases · artifacts · gates)

| Phase | Work | Artifact | Gate |
|---|---|---|---|
| **0 — Frame** | Capital type (equity/debt/pref/JV), deck type (single-asset/portfolio/platform), audience, page budget, stop-list, new-build vs. revision | `00-FRAME.md` (one page) | **User confirms** |
| **1 — Extract & audit** | CC directly reads every canonical source (model tabs, sponsor decks, appraisals, legal as needed) | `_data_extract/NN-<source>.md` digests + `00-DATA-AUDIT-TRAIL.md` (claim → value → source file/tab/page → as-of → tier → ✅/⚠️/❌/🔢) + claim self-consistency sweep + `Data needed from <sponsor>.md` | **User reviews trail + data request** |
| **2 — Research** | 3–5 parallel subagents, register-scoped single questions, Tier-1/2/3 source rules, as-of dating; findings merge into the audit trail with verification status | updated audit trail | — |
| **3 — Blueprint** | Thesis + load-bearing claims (the Story discipline lives here); slide-by-slide spec where every content block references an audit-trail ID; PRESERVE / NEVER-REINTRODUCE lists in revision mode; special-angle headlines; open items | `OM Build Blueprint - <date>.md` | **User (+Henry) sign-off — nothing is built before this** |
| **4 — Build** | CC-native: seed template → python-pptx + direct XML layout cloning; `voice-model.md` governs every sentence; `design-system.md` + layout selection govern composition | the .pptx + build log | — |
| **5 — QA** | (a) *Visual:* render all slides to PNG, subagent inspection loop (overflow/overlap/contrast/alignment) until clean. (b) *Verification:* every deck numeric ↔ audit trail; criticals ↔ source; research claims re-fetched. (c) *Editorial gate* (codified from Henry's 6/9 review): cross-page numeric consistency, unit style (M vs MM), dash/decimal conventions, thesis-contradiction sweep, placeholder sweep, label/bio parallelism, read-aloud anti-AI pass | QA report (pass/fail per item) | **User reviews deck + QA report** |
| **6 — Ship** | PDF export; archive prior versions per `x V23\Archive` convention; open-TBD summary | final PDF + pptx | — |

**Revision mode** keeps the v5.1 machinery: `extract-pptx-inventory.py` first, stop-list capture, live-pptx-is-source-of-truth, `apply-revision-edits.py` (Path A) for deterministic edits.

**Conflict policy (all phases):** the underwriting model is canonical for deal numerics; appraisals are quoted as third-party support; marketing-deck figures are distrusted until verified. Conflicts are flagged to the sponsor in the data-request doc — never silently fixed, never fabricated.

## 4. Component disposition

| Component (dev v5.1.0) | Disposition |
|---|---|
| `SKILL.md` | Rewrite around §3B; keep v5.1's mode detection, ambiguity surfacing, stop-list, CIP capability notes (for the optional polish path) |
| `house-voice.md` Part 1 (13 deck-tied rules) | Superseded by sweep-derived `voice-model.md` |
| `house-voice.md` Part 2 (anti-AI ruleset) | Keep unchanged; referenced by Phase 5c |
| `layout-repertoire.md` | Keep; validate/extend against the sweep |
| `prompt-template.md` | Retire from critical path; replace with a slim shape-level CIP punch-list template (optional polish only) |
| Hardcoded reference-deck list (SKILL.md Phase 5) | Delete; replaced by Pattern Study provenance rules |
| `extract-pptx-inventory.py`, `apply-revision-edits.py` | Keep |
| `build-deck.py` | Mature into the Phase 4 builder (template seed + layout cloning) |
| *(new)* `render-qa.py` | Render slides to PNG for Phase 5a |
| `v23-template.pptx` | Regenerate via `make-template.py` from `design-system.md` findings (seed deck chosen by the study, not pre-picked) |
| Cross-project `[[memory]]` references | Remove; embed the conventions content (source tiers, recency, risk pattern, purposes) as skill reference files so the skill is self-contained |

## 5. Coastal GA first run (lender OM)

- Create the deal's `x V23\` work folder; all pipeline artifacts land there.
- **Frame:** debt/bridge register, lender audience, ≤25 pages (target 20–23). Expected spine — final structure is decided at the Phase 3 gate, informed by the debt-register coverage checklist, not hardcoded here: exec summary (ask, basis vs. appraisal, DSCR, take-out on one page) → loan request & terms → the conversion arbitrage with audited numbers → market verification → per-asset blocks (asset, scope/budget, timeline, rents vs. comps, pro forma, DSCR/take-out math) → completion story (Altura Source + Summco GC + permits-in-hand policy) → sponsor & guarantor credit → risk framework (probability × impact × mitigant) → compressed comp appendix + SEDA abatement.
- **Known conflicts seeding Phase 1** (found 2026-06-11; verify, then route to `Data needed from Altura`): GIL purchase price $4.65M (deck p.27) vs $4.25M (pro forma); deck's $10.7M GIL exit vs $10.42M NOI÷cap arithmetic; headline YoCs (10.75%/10.90%) not derivable from stated TPC+NOI; p.3 LP-equity figures irreconcilable with the p.15 capital stack; GIL 5% vs WBF 2% credit loss unexplained; GIL pro forma refi value 4% above appraisal as-stabilized; Brunswick rezoning labeled "Approved" with a Nov 2026 vote date; SEDA 30-day acceptance window from 5/6/26 possibly lapsed; no DSCR anywhere in the deck (≈1.40x combined stabilized, calculated); GIL appraisal p.34 carries WBF's unit count (copy-paste error); financing agreement says 7312 & 7412 White Bluff vs deck's 7312 only.

## 6. Plumbing & distribution

- Version **6.0.0**; bump `plugins/v23/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` together; republish/reinstall so the installed copy equals dev (the stale-4.0.0 problem, documented in HANDOFF-Fresh-Chat.md, must not recur — add a version-echo line to the skill's Phase 0 output so a stale install is visible at runtime).
- Frontmatter rules per Theo's global CLAUDE.md: `name:` exactly matches the folder; only `name` and `description` keys; one invalid skill blocks the whole plugin from updating.

## 7. Risks & mitigations

- **Sweep cost/time** (~281+ files): staged fan-out with per-slice digests; provenance filter applied before any reading; resumable (digests persist).
- **Voice overfit / false patterns:** cross-time consistency weighting; ≥3-material citation requirement; adversarial reproduction test; Theo spot-check before the model ships.
- **python-pptx fidelity on complex slides:** the XML clone-and-edit path is the fallback (proven in the NPV endgame); Phase 5a render loop catches breakage.
- **OneDrive locks / cloud-only placeholders:** always work on copies; hydration check before reads (file locks when open in PowerPoint — established rule).
- **25-page ceiling vs. "jampacked":** page budget enforced at the blueprint gate — merge/cut decisions happen on paper, not after slides exist.

## 8. Out of scope

- Teasers, one-pagers, deal-packs (separate skills cover these).
- An equity OM for Coastal GA (revisit if the engagement expands beyond bridge debt).
- Automating the Henry review (human gate by design).

## 9. Open items

1. Sweep-scope triage of `4- Marketed Deals`, `x- Deals Archive`, `x- Templates` (provenance unknown until inspected; ambiguous items go to Theo).
2. Template seed deck — chosen by `design-system.md` findings during the study, deliberately not pre-picked (no recency bias).
3. Whether `om-builder-help` needs a matching update once v6 lands (defer to implementation).
