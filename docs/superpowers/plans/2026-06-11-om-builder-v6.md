# om-builder v6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `v23:om-builder` around the gated artifact pipeline, grounded in an exhaustive multi-dimension Pattern Study of all V23-authored materials, republish so installed = dev, then kick off the Coastal GA bridge-lender OM as the first live run.

**Architecture:** Phase A–B sweep every provenance-confirmed V23 material into on-disk notes (study workspace, resumable). Phase C–D synthesize five dimension reports and validate the voice by adversarial reproduction test. Phase E bakes the validated artifacts + new runbook into the skill. Phase F republishes. Phase G starts the Coastal GA run, which is governed by the new skill's own gated runbook from there.

**Tech Stack:** Claude Code agents (general-purpose + Explore), PowerShell, Python 3.14 (`python-pptx`, `pdfplumber`, stdlib `zipfile`/`xml` for docx), `pdftoppm` (poppler), git.

**Spec:** `docs/superpowers/specs/2026-06-11-om-builder-v6-design.md` (read it first). User context: memory files `project-om-rebuild-context.md` and `feedback-voice-grounding.md` in the Coastal-GA project memory dir.

**Standing rules for every task:**
- Provenance hard rule: positive = `x V23`/`xV23`/`V23 - OM` dirs, deal `OM\` subfolders with V23 naming (`<Deal> - OM - <date>`); negative = `Client Provided`/`Client Files`/broker/data-room folders; ambiguous → log to manifest's AMBIGUOUS section for Theo, exclude meanwhile.
- No recency bias: a pattern needs ≥3 materials spanning years. Note dates on every observation.
- Never anchor to one deal: single-deck idiosyncrasies are logged but excluded from shipped artifacts.
- OneDrive: copy any file that may be open/locked before parsing; if a read returns 0 bytes (cloud placeholder), note it and skip.
- Quotes in notes are evidence; shipped artifacts carry short fragments + file/date citations only.
- Commit after every task with the message given in the task.

**Paths (used throughout):**
- `REPO` = `C:\Users\TheodoreMouhlas\Workspace\Vanadium\x Plugins\v23-plugins`
- `DB` = `C:\Users\TheodoreMouhlas\Vanadium Group LLC\V23 - Database`
- `STUDY` = `REPO\study\om-pattern-study-2026-06`
- `SKILL` = `REPO\plugins\v23\skills\om-builder`

---

## Shared: Reader-agent prompt template (used by Tasks 3–10)

Dispatch one general-purpose agent per slice with this brief (substitute SLICE values):

```
You are a pattern-study reader for Vanadium Realty (V23). Read the V23-AUTHORED materials in your slice and take dense, evidence-cited notes. You are building the raw material for a style/system model — observe, don't judge.

SLICE: <id> — <description>
FILES: <explicit list or glob + exclusion note>
WRITE NOTES TO: <STUDY>\notes\<id>-<name>.md  (create; append sections as you go)
GEOMETRY OUT: for each .pptx you read, run
  python "<SKILL>\scripts\extract-pptx-inventory.py" "<file>" > "<STUDY>\geometry\<id>-<filename>.json"
  (copy locked files to %TEMP% first; if the script errors on a file, note and continue)

EXTRACTION: pptx text via python-pptx; pdf via pdfplumber (fallback: Read tool); docx via python zipfile reading word/document.xml, strip tags.

VERSION CHAINS: when a folder holds >4 dated versions of the same doc, fully read first + ~middle + final, and note what CHANGED across the chain (evolution is signal). List skipped versions.

NOTE FORMAT — one entry per observation, tagged with dimensions:
[VOICE|LAYOUT|STRUCTURE|REGISTER|EXEC-SUMMARY|HEADLINES|KPI-TABLES|NUMBERS|CITATIONS|RISK|SPONSOR|VISUALS|DENSITY|COVER-ADMIN|NEGATIVE-SPACE]
- Observation: <one sentence, deal-agnostic phrasing>
- Evidence: "<verbatim quote or precise layout description>" — <file>, <slide/page>, <doc date>
Multiple tags allowed. Log register metadata per document (equity/debt/pref/JV/teaser/memo/update; deck vs Word doc; date; deal; page count).

Also keep a per-document index at the top of your notes file: file, date, register, pages, 1-line gist, read-depth (full/sampled/skipped+why).

RETURN (final message, ≤300 words): slice coverage stats (files read full/sampled/skipped), 5 strongest cross-document patterns you saw, anything ambiguous-provenance you excluded.
```

---

## Phase A — Study infrastructure

### Task 1: Workspace + gitignore

**Files:** Create `STUDY\` dirs (`notes`, `geometry`, `synthesis`, `validation`), `REPO\.gitignore` (add `study/`), `STUDY\README.md`.

- [ ] **Step 1:** Create directories; write `STUDY\README.md` stating: purpose, the standing rules block from this plan (copy it verbatim), and the note format. Why gitignored: the marketplace path `C:\Users\TheodoreMouhlas\.claude\plugins\marketplaces\v23-plugins` is a clone of this repo — committed study notes (internal deal quotes, bulk) would sync to every team install. Distilled artifacts ship via the skill; raw notes stay machine-local.
- [ ] **Step 2:** Append `study/` to `REPO\.gitignore` (create file if absent).
- [ ] **Step 3:** Verify: `git -C $REPO status -s` shows only `.gitignore` (study/ invisible).
- [ ] **Step 4:** Commit: `chore: gitignore local pattern-study workspace`.

### Task 2: Provenance enumeration → manifest

**Files:** Create `STUDY\00-manifest.md`.

- [ ] **Step 1:** PowerShell enumeration over `DB`: collect all `.pptx/.pdf/.docx` whose path matches positive signals (`\x V23\`, `\xV23\`, `\V23 - OM\`, or a deal `\OM\` folder where filenames match `- OM`), excluding paths matching `Client Provided|Client Files|Data Room|Seller Data`. Separately enumerate triage trees: `DB\4- Marketed Deals`, `DB\x- Deals Archive`, `DB\x- Templates`, plus deal-folder docx that look V23-authored (`*Deal Analysis*`, `*Investor*Memo*`, `*1 Pager*`, `*context*`) — these go to a TRIAGE list, not auto-included.
- [ ] **Step 2:** Write `00-manifest.md` with sections: INCLUDED (table: path, ext, date, assigned slice), TRIAGE (path + why uncertain), AMBIGUOUS-FOR-THEO (provenance undecidable), SKIPPED (locked/0-byte). Assign slices: **A** Obsidian `V23 - OM` (incl. Platform + Krios-format subfolders), **B** 105_N_13 `x V23`, **C** Krios `2. Krios\V23 - OM`, **D** NPV `x V23` (+ Tarpon `xV23`), **E** Pektor All Deals `OM\` trees + Comps-Maps docx, **F** small folders (Alpha Square, Open House, 3605 Church, Alley North, Park City) + whatever TRIAGE items are clearly V23, **G** V23-authored Word memos across deal folders, **H** remaining TRIAGE adjudication notes.
- [ ] **Step 3:** Sanity check: INCLUDED count should be ≈281 ± the deal-`OM\` additions; if wildly off, re-check the filters before proceeding.
- [ ] **Step 4:** No commit (gitignored). Record counts in the task-completion note instead.

---

## Phase B — Reader sweep (Tasks 3–10; parallelizable)

Each task = dispatch one reader agent with the Shared template + slice values; on return, spot-check the notes file (open it, confirm ≥30 tagged observations for big slices, per-doc index present, quotes carry file+date); log coverage stats in `00-manifest.md` under a COVERAGE section. No commits (gitignored).

### Task 3: Slice A — Obsidian V23 - OM (~120 files, heavy version chains)
- [ ] Dispatch reader (template; emphasize version-chain sampling + platform/GTM register tagging). Spot-check notes. Update COVERAGE.

### Task 4: Slice B — 105_N_13 x V23 (~82 files; OM evolution Jan→Apr 2026, vDebt, memos)
- [ ] Dispatch reader (emphasize: equity-vs-debt register contrast on the SAME deal — tag REGISTER heavily; the four memo PDFs are voice gold). Spot-check. Update COVERAGE.

### Task 5: Slice C — Krios V23 - OM (~29 files incl. Ever Leaf finals + teasers)
- [ ] Dispatch reader (tag teaser vs full-OM register differences). Spot-check. Update COVERAGE.

### Task 6: Slice D — NPV x V23 + Tarpon xV23 (~32 files; includes the 6/9–6/10 finals AND 5/26 archives)
- [ ] Dispatch reader (emphasize: note 5/26→6/10 evolution as signal, but tag observations from the final like any other deck — no extra weight). Spot-check. Update COVERAGE.

### Task 7: Slice E — Pektor deals (Wind Gap OM/Pref/JV/BTS 2023–2025 + maps/flyers docx)
- [ ] Dispatch reader (Theo: "perfect voice" — but same evidence rules; tag REGISTER for Pref/JV; Word-doc-era conventions matter). Spot-check. Update COVERAGE.

### Task 8: Slice F — small work-product folders (Alpha Square, Open House, 3605 Church, Alley North, Park City)
- [ ] Dispatch reader. Spot-check. Update COVERAGE.

### Task 9: Slice G — V23-authored Word memos across deal folders (from manifest TRIAGE→clear items)
- [ ] Dispatch reader (deal analyses, investor memos, 1-pagers; docx extraction path). Spot-check. Update COVERAGE.

### Task 10: Slice H — triage adjudication (4- Marketed Deals, x- Deals Archive, x- Templates)
- [ ] Dispatch an Explore agent to classify each TRIAGE tree item per provenance rules; clear V23 items get read (same note format, written to `notes\H-triage.md`); undecidable items land in AMBIGUOUS-FOR-THEO. Spot-check. Update COVERAGE.
- [ ] Surface AMBIGUOUS-FOR-THEO list to Theo in the session (do not block; excluded meanwhile).

---

## Phase C — Synthesis (Tasks 11–15)

Each synthesis task: dispatch one general-purpose agent that reads ALL of `STUDY\notes\*` (+ targeted geometry JSONs / original files for verification), writes `STUDY\synthesis\<dim>.md`; then I review/edit in main context. Each synthesis doc must: state each pattern as a deal-agnostic rule; cite ≥3 materials with years for every kept pattern; carry a DISCARDED section (patterns that failed the ≥3/cross-year bar, with why); separate stable-DNA vs evolving-with-date observations rather than picking the newest.

### Task 11: `synthesis\voice.md` (VOICE, HEADLINES, EXEC-SUMMARY, NEGATIVE-SPACE tags)
- [ ] Dispatch; review; fix citations that don't span years.

### Task 12: `synthesis\layouts.md` (LAYOUT, DENSITY, VISUALS tags + `geometry\*.json` analysis — zone patterns, recurring arrangements, words/slide and KPI-count norms)
- [ ] Dispatch; review.

### Task 13: `synthesis\design.md` (typography/palette/footer/source-line behavior from geometry JSON formatting fields + selective page renders via pdftoppm where needed)
- [ ] Dispatch; review.

### Task 14: `synthesis\registers.md` (REGISTER, STRUCTURE, KPI-TABLES, RISK, SPONSOR tags — how equity/debt/pref/JV/teaser/memo differ; the debt-metrics checklist from 105 vDebt + Wind Gap Pref/JV + lender materials)
- [ ] Dispatch; review.

### Task 15: `synthesis\conventions.md` (NUMBERS, CITATIONS, COVER-ADMIN tags — units, decimals, negatives, footnotes, source lines, disclaimers, contacts)
- [ ] Dispatch; review.

---

## Phase D — Validation (Task 16)

### Task 16: Reproduction test (the "recreate it perfectly" bar)

**Files:** Create `STUDY\validation\reproduction-test.md`.

- [ ] **Step 1:** From synthesis docs only (not original files), write 6 test passages: 2 exec-summary paragraphs, 2 investment-highlight blocks, 1 risk-mitigant entry, 1 asset-overview block — for two HELD-OUT scenarios (a fictional industrial deal + a fictional multifamily deal; nothing from real V23 decks).
- [ ] **Step 2:** Pull 6 real V23 passages of matching types from notes quotes (different deals/years).
- [ ] **Step 3:** Dispatch 3 judge agents, each blind: present shuffled mix of 12 passages, ask "which are V23-authored? justify per passage." Judges get NO synthesis docs.
- [ ] **Step 4:** Score: if judges distinguish generated from real at better than chance (>8/12 correct calls on average), extract their justifications as defects, fix `synthesis\voice.md`, regenerate the failed passage types, re-run with fresh judges. Iterate (max 3 rounds; if still failing, record residual tells and flag to Theo).
- [ ] **Step 5:** Record protocol + rounds + final result in `reproduction-test.md`. Present 2–3 passage pairs to Theo for spot-check in session.

---

## Phase E — Skill artifacts + rewrite (Tasks 17–23; commits resume here)

### Task 17: `voice-model.md` + `anti-ai-ruleset.md`

**Files:** Create `SKILL\voice-model.md`, `SKILL\anti-ai-ruleset.md`. Delete `SKILL\house-voice.md`.

- [ ] **Step 1:** Distill `synthesis\voice.md` (post-validation) into `voice-model.md`: rules with short cited fragments (file+year), register notes (deck vs Word doc), regenerate-note header ("derived from the 2026-06 pattern study; regenerate by re-running the sweep per docs/superpowers/plans/2026-06-11-om-builder-v6.md Phase B–D").
- [ ] **Step 2:** `anti-ai-ruleset.md` = house-voice.md Part 2 verbatim + a new "Observed V23 negative space" section from NEGATIVE-SPACE synthesis findings.
- [ ] **Step 3:** Delete `house-voice.md`. Grep the skill folder for `house-voice` references; update them.
- [ ] **Step 4:** Commit: `feat(om-builder): voice-model + anti-ai ruleset from pattern study (replaces house-voice)`.

### Task 18: `layout-system.md`

**Files:** Create `SKILL\layout-system.md`. Delete `SKILL\layout-repertoire.md`.

- [ ] **Step 1:** Build from `synthesis\layouts.md` + `synthesis\design.md`: observed arrangement catalog (each with ≥3-deck citations), content→layout selection logic (fold in v5.1's selection system where it matched observation; DISCARDED section for what didn't), density norms, variety mandate restated against observed evidence.
- [ ] **Step 2:** Delete `layout-repertoire.md`; grep + fix references.
- [ ] **Step 3:** Commit: `feat(om-builder): observed layout system (replaces layout-repertoire)`.

### Task 19: `design-system.md` + template regen

**Files:** Create `SKILL\design-system.md`. Modify `SKILL\v23-template.pptx` (regenerated). Modify `SKILL\scripts\make-template.py` if its source-deck arg needs updating.

- [ ] **Step 1:** Write `design-system.md` from `synthesis\design.md`: durable DNA vs per-deck choices, exact current values WITH provenance ("stable since <year>" / "current as of <deck, date>").
- [ ] **Step 2:** Regenerate `v23-template.pptx` with `make-template.py` from the seed the synthesis nominated (the deck whose masters best embody the stable DNA — synthesis decides, not recency).
- [ ] **Step 3:** Verify: build a 3-slide smoke deck from the template (title + KPI + prose slide) via `build-deck.py`, render with pdftoppm, eyeball the PNGs against design-system.md.
- [ ] **Step 4:** Commit: `feat(om-builder): design-system + regenerated v23-template`.

### Task 20: `registers-and-coverage.md` + `conventions.md` + `source-standards.md`

**Files:** Create all three in `SKILL\`.

- [ ] **Step 1:** `registers-and-coverage.md` from `synthesis\registers.md` — per-register section/metric checklists (equity, debt, pref, JV, teaser, memo).
- [ ] **Step 2:** `conventions.md` from `synthesis\conventions.md`.
- [ ] **Step 3:** `source-standards.md` — port source tiers / recency / risk-pattern / purposes content from the global CRE rule + conventions memory so the skill has zero cross-project `[[memory]]` dependencies.
- [ ] **Step 4:** Commit: `feat(om-builder): register coverage, conventions, source standards (self-contained)`.

### Task 21: SKILL.md v6 rewrite

**Files:** Rewrite `SKILL\SKILL.md`. Create `SKILL\cip-polish-template.md`. Delete `SKILL\prompt-template.md`.

- [ ] **Step 1:** Rewrite SKILL.md to the §3B runbook: Phase 0 Frame (capital type, deck type, audience, page budget, stop-list, version-echo line printing plugin version) → Phase 1 Extract & Audit (`_data_extract/` + `00-DATA-AUDIT-TRAIL.md` ledger format + self-consistency sweep + `Data needed from <sponsor>.md`) → Phase 2 Research (subagent rules, source-standards.md) → Phase 3 Blueprint (format per NPV's `OM Rebuild - Build Blueprint.md`; PRESERVE/NEVER-REINTRODUCE in revision mode; HARD GATE) → Phase 4 Build (build-deck.py / XML clone; voice-model + layout-system + design-system + conventions govern) → Phase 5 QA (render loop via render-qa.py; numeric verification vs ledger; editorial gate checklist incl. cross-page consistency, M-vs-MM, contradiction sweep, placeholder sweep, parallelism, read-aloud) → Phase 6 Ship (PDF, `x V23\Archive`, TBD summary). Keep v5.1 revision-mode machinery sections. Frontmatter: `name: om-builder`, description only.
- [ ] **Step 2:** `cip-polish-template.md` = slim shape-level punch-list template (target-by-ID + precondition + verbatim text; explicitly optional, post-Phase-5 only).
- [ ] **Step 3:** Delete `prompt-template.md`; grep + fix references. Verify frontmatter rules (folder name match; only name+description).
- [ ] **Step 4:** Commit: `feat(om-builder)!: v6 runbook — gated artifact pipeline, CC-native build`.

### Task 22: `render-qa.py`

**Files:** Create `SKILL\scripts\render-qa.py`.

- [ ] **Step 1:** Script: args `<pptx> <outdir>`; converts pptx→pdf (PowerPoint COM via `powershell -c` Start-Process fallback: instruct user export if COM unavailable; primary path: `soffice` if present else COM), then `pdftoppm -png -r 110`; prints page count + outdir. Keep ~60 lines, stdlib + subprocess only.
- [ ] **Step 2:** Test: run against the Task 19 smoke deck; expect N PNGs where N = slide count; non-zero exit + clear message on failure.
- [ ] **Step 3:** Commit: `feat(om-builder): render-qa script for visual QA loop`.

### Task 23: `build-deck.py` maturation

**Files:** Modify `SKILL\scripts\build-deck.py`.

- [ ] **Step 1:** Read current script; extend to: load `v23-template.pptx`, accept a blueprint-derived JSON slide spec (slide type, headline, prose blocks w/ inline-bold markers, KPI sets, table data, source line), emit deck cloning template layouts; preserve the XML-clone escape hatch for arrangements python-pptx can't express (document it in the script header).
- [ ] **Step 2:** Test: feed a 3-slide JSON spec (write it inline in the test run), build, run `extract-pptx-inventory.py` on output, assert headline texts + source lines present and fonts match design-system values.
- [ ] **Step 3:** Commit: `feat(om-builder): build-deck accepts blueprint slide-spec JSON`.

---

## Phase F — Republish (Tasks 24–25)

### Task 24: Version bump + manifest sync

**Files:** Modify `REPO\plugins\v23\.claude-plugin\plugin.json`, `REPO\.claude-plugin\marketplace.json`.

- [ ] **Step 1:** Set version `6.0.0` in BOTH files (they must match; one invalid/mismatched skill blocks the whole plugin per Theo's skill rules).
- [ ] **Step 2:** Validate every skill in the plugin: each `SKILL.md` frontmatter has `name` == folder name and ONLY `name`+`description` keys (PowerShell loop over `plugins\v23\skills\*\SKILL.md`).
- [ ] **Step 3:** Commit: `release: v23 plugin 6.0.0 — om-builder v6`.

### Task 25: Reinstall + verify installed copy

- [ ] **Step 1:** Update the marketplace clone: `git -C "C:\Users\TheodoreMouhlas\.claude\plugins\marketplaces\v23-plugins" pull` (its remote is the dev repo; if pull fails, report the actual remote and resolve with Theo).
- [ ] **Step 2:** Verify installed `plugin.json` reads 6.0.0 and `om-builder\voice-model.md` exists in the installed path.
- [ ] **Step 3:** Smoke: invoke `/om-builder` availability (or read installed SKILL.md header) and confirm the version-echo line says 6.0.0.

---

## Phase G — Coastal GA kickoff (Task 26)

### Task 26: First live run — Phase 0 Frame

**Files:** Create `DB\1- Realty\1- Deals\Coastal GA Multi Conversion Portfolio\x V23\00-FRAME.md`.

- [ ] **Step 1:** Create the `x V23\` folder. Run skill Phase 0 with the locked decisions: capital type = debt (senior bridge $11,494,200 @ 80% LTC), deck type = two-asset portfolio (NOT platform), audience = bridge lenders, page budget ≤25 (target 20–23), stop-list seeds = the 11 known conflicts from the spec §5 + "never present GIL rezoning as approved" + "always show DSCR".
- [ ] **Step 2:** STOP. Present `00-FRAME.md` to Theo (gate 1 of the new runbook). The OM run continues under the skill's own gated pipeline from here — its artifacts (audit trail, data request, blueprint) are the plan for that work.

---

## Self-review (done at write time)

- Spec coverage: §3A sweep→Tasks 1–10; dimensions→note tags; artifacts→Tasks 17–20; validation→16; §3B runbook→21; scripts→22–23; §4 dispositions→17,18,21 (deletions) + 19 (template) + 20 (memory embedding); §6 plumbing→24–25; §5 first run→26; §9 open items→Task 10 (triage), Task 19 (seed deck), om-builder-help deferred (out of plan, noted).
- Placeholders: none — every step states its concrete action, file, and check.
- Consistency: artifact names match spec (`voice-model.md`, `layout-system.md`, `design-system.md`, `registers-and-coverage.md`, `conventions.md`); note tags in template match synthesis task inputs; study stays gitignored while skill artifacts commit.
