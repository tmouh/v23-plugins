# OM Conventions
<!-- Derived from: om-pattern-study-2026-06 synthesis/conventions.md (generated 2026-06-11) -->
<!-- Regeneration pointer: docs/superpowers/plans/2026-06-11-om-builder-v6.md -->

Items are marked OBSERVED (citation) or LEGISLATED (2026-06-11) where the corpus was inconsistent and a rule was imposed to resolve the inconsistency.

---

## 1. Numbers & Units

### 1.1 Dollar-amount notation — Three-Context Rule

LEGISLATED 2026-06-11. The corpus used $mm, $MM, and spelled-out forms inconsistently across contexts. The following rule resolves that and is mandatory going forward:

| Context | Form | Example |
|---------|------|---------|
| Cover ask line (formal) | Spelled out | "$18 Million Joint Venture Investment" |
| Body prose (Word OM and deck narrative) | `$mm` lowercase | "The Sponsor is seeking approximately $14.3mm in preferred equity financing" |
| Stat-box large-format KPI | `$MM` uppercase | "$50MM / LP EQUITY ASK" |
| Financial tables (within rows) | Bare dollar with commas, no M suffix | "$30,208,914" |

Evidence for each form: $mm in Word OM body — Wind Gap Pref OM final (E48, 2025-03-10); $MM in stat box — NPV Florida IOS final (slide 2, 2026-06-09); spelled-out cover — 105 N 13 equity OM cover (2026-04-22); 105 N 13 vDebt cover (2026-03-02).

### 1.2 Two-decimal rule for model-derived returns

OBSERVED (confirmed 2024–2026 across all registers with a live model underlying the numbers). IRR, EM, and YoC from a live model are always shown to two decimal places.

- IRR: `24.06%`, `13.39%`, `24.86%`, `24.99%` — never `24%` or `24.1%`
- Equity Multiple: `2.02x`, `1.74x`, `2.26x` — two decimals, lowercase x, no space
- YoC: `8.19%`, `6.88%`, `7.55%`

Illustrative or scenario returns (not from a live model) may round to whole numbers (e.g., Krios Everleaf: "60% IRR / 2.31x MOIC" in a scenario context). Do not apply two-decimal rule to illustrative figures.

Evidence: 105 N 13 Exec Summary returns table (slide 3, 2026-04-22); Wind Gap Pref final (E48, 2025-03-10); NPV tile slides (2026-06-09).

### 1.3 Multiples format — lowercase x, no space

OBSERVED (confirmed across corpus). One outlier: VHC2 Slice A uses `×` (multiplication symbol) in a single instance — excluded as a pattern (single outlier rule per README).

Rule: `X.XXx` — lowercase `x`, no space between number and suffix. Examples: `2.02x`, `2.87x`, `2.31x`, `2.0x+` (target range with + suffix). Never `2.02 x` or `2.02×`.

Evidence: 105 N 13 deck (2026-04-22); NPV final tiles (2026-06-09); Wind Gap chain (E48 2025-03-10).

### 1.4 Basis points — whole numbers always

OBSERVED. Bps values expressed as whole numbers throughout. `138 basis points`, `204 basis points`, `150 bps` (abbreviated form in stat boxes). Never `138.4 bps`.

Evidence: Wind Gap Pref/JV chain (E48, E52, 2025).

### 1.5 Negatives — parentheses

OBSERVED in user conventions memory; not directly confirmed in primary extraction (sensitivity tables express downside via threshold language rather than negative-sign numbers in the corpus). Rule per user conventions: negatives in parentheses, not minus signs. Example: `($2.1mm)` not `-$2.1mm`.

### 1.6 Range punctuation — hyphen

LEGISLATED 2026-06-11. The corpus confirmed hyphen in body text (Wind Gap Submarket section, E48: "$10/SF - $14/SF range"); en-dash was inferred in study notes but not confirmed in primary extraction (Word XML encoding ambiguity). Until a confirmed en-dash instance is found in primary extraction, use a hyphen for all ranges.

Rule: Hyphen for ranges in all body text, both Word OMs and deck narrative. Example: `$10/SF - $14/SF`, `18–40 slides` (hyphen in this file = house standard). NEVER use an en-dash until positively confirmed from a send-state file.

### 1.7 Unit normalizers by asset class

OBSERVED.

| Asset class | Primary normalizer | Secondary |
|-------------|-------------------|-----------|
| Office / mixed-use | $/GSF | $/NSF |
| Industrial / IOS | $/SF | $/acre |
| Land sale comps | $/SF or $/acre | — |
| Hotel / hospitality | $/key | % margin |
| Multifamily | $/unit | $/SF |
| Data center / powered land | $/SF, $/MW | — |

Evidence: 105 N 13 ("$613/GSF entry"); Wind Gap ("$141/SF basis", "$3.25/SF rent hurdle", "$700k/acre" in land comps); Alley North F-slice ("$353,442/key"); VHC2 Hillwood ("$5,624/SF / $20.2M/MW").

### 1.8 Date formats

OBSERVED.

- Deck covers: spelled-out month + year, no day — "APRIL 2026", "May 2026"
- Source lines and research: abbreviated period — "YE 2025", "Q3 2025", "H2 2025", "Jan 2025"
- File naming: ISO date — YYYY-MM-DD
- "Figures estimated as of [date]" device: institutional/international register only (Ever Leaf vF, April 2026) — NEVER in domestic V23 equity OMs

---

## 2. Citations & Source Lines

### 2.1 Citation formality gradient — register-dependent

Both modes are fully specified. Register determines which to use.

**Mode A — Institutional / international register (R7 platform deck, Ever Leaf, Krios full OM):**
Full citation block with named report + edition + quarter + "Figures estimated as of [month year]" trailer on the source line.

Example (Ever Leaf vF, slide 4, 2026-04-13):
"Sources: JLL EMEA Data Center Report YE 2025; CBRE European Data Centers Q3 2025; Cushman & Wakefield EMEA H2 2025; Newmark 2025 Data Center Site Selection. Figures estimated as of April 2026."

**Mode B — Domestic V23 deck OM (R1, R2, 2026):**
Parenthesized-digit footnotes on the exec summary stat box only. No per-slide source lines in final / send-state versions. No "Figures estimated as of" trailer.

Example (NPV Florida IOS final, slide 2, 2026-06-09):
"(1) Newmark, 2025 | (2) Active Florida pipeline aggregate Total Project Cost per NPV Florida Deal Pipeline"

**Mode C — Domestic Word OM (R3, R4, 2024–2025):**
Named source inline in body prose — not a formatted footnote block. CoStar is the only named third-party database in domestic Word OM market sections.

Example (Wind Gap Pref final E48, 2025-03-10): "Lehigh Valley Economic Summary, CoStar Q12024."

### 2.2 Per-slide source lines — strip at send state

LEGISLATED 2026-06-11. Per-slide source lines with full citations were present in early-draft NPV deck (2026-05-26) and were stripped completely in the 06-01 and 06-09 final send-state versions. This is confirmed observed behavior — citation density decreases as a deck matures toward send state.

Rule: Strip per-slide source lines from domestic equity deck OMs at send state. Retain footnote-only on exec summary stat box (Mode B above). Do not conflate draft citation practice with send-state convention.

### 2.3 Footnote markers

OBSERVED. Parenthesized superscript digits `(1)`, `(2)` are the confirmed marker in deck OMs (NPV final stat box, slide 2, 2026-06-09). Square brackets `[1]`, `[2]` observed in wood-frame strategy deck footnotes (F slice). Asterisks are draft-state placeholder signals only (vDebt 105 N 13 "xxxxx" and "****** months") — never a citation marker style.

Rule: Parenthesized digits `(1)` `(2)` for all outbound OM footnote markers. No asterisks, daggers, or section signs.

### 2.4 Internal-memo source hierarchy (R9)

OBSERVED (G-word-memos.md, PCL/Bridgeport research chain). Structure: national benchmark → state reference → submarket → site-specific. Sponsor-provided assertions explicitly attributed with "according to sponsor" or "in direct conversation, the sponsor told us" — never merged into primary data claims. Tier 1 sources named inline.

---

## 3. Cover, Disclaimer & Contact Conventions

### 3.1 Confidentiality disclaimer — three patterns

**Pattern A — Word OM (Wind Gap, Palmer MF, 2024–2025):** Full multi-paragraph disclaimer as standalone page 2 section headed "CONFIDENTIALITY & DISCLAIMER." 4–6 paragraphs: limited use / no warranty / no reliance / environmental notice / legal-tax counsel / subject to change / copyright line. Closes: "© 2025 Vanadium Realty LLC. All Rights Reserved."

**Pattern B — Deck OM, domestic (105 N 13, 2026):** Full disclaimer on slide 2, single dense text block, 6 paragraphs. Same structure as Pattern A but shorter per paragraph. Closes: "© 2026 Vanadium Realty LLC. All Rights Reserved" (no period).

**Pattern C — Deck OM, institutional/international (Ever Leaf vF, Krios, 2026):** Cover slide carries brief confidentiality badge in 8pt light text: "Qualified Investors Only / Proprietary and Confidential." Full disclaimer assumed in appendix or separate legal document. Co-invest abbreviation (11 slides) carries "PRIVATE & CONFIDENTIAL — FOR DISCUSSION PURPOSES ONLY."

### 3.2 Opening formula — register-determines-construction

OBSERVED (2020–2026, all investor-facing registers). Three constructions, each tied to a register:

- **Advisory / credentials (2020–2022):** "Vanadium Group LLC ('Vanadium') is pleased to present to [Counterparty] our credentials regarding..."
- **Word OM exclusively retained (2024–2025):** "Vanadium Realty LLC ('Vanadium') has been exclusively retained by [Sponsor] to structure and arrange [capital type] financing for [project]."
- **Deck OM exclusively engaged (2026):** "Vanadium Realty ('Agent') has been exclusively engaged by [Sponsor] to source [ask]."

All three are active. Register determines which construction is used.

### 3.3 Defined-terms-in-quotes-and-parens

OBSERVED (universally consistent, 2020–2026, all formats). Format: full legal name first, then ("ShortForm") in quotes inside parens. Short forms used consistently after first reference — never reintroduce the full name. Code-name variant uses ALL-CAPS: `PROJECT "EVER LEAF" ("PEL")`.

Evidence: all slices 2020–2026.

### 3.4 Contact page format — era-dependent

OBSERVED. Format is stable within each era:

**Deck OM (2026, NPV final slide 18):** Named-card grid. Card fields: Name (bold, larger font) / Title / Mobile (M: format) / Email (lowercase + mixed case domain, e.g., hchak@V23Group.com). Vanadium Realty LLC label as section header. No sponsor contacts — V23 only.

**Word OM (2024–2025, Wind Gap E48/E13/E43):** ALL-CAPS name / ALL-CAPS title / M: phone / EMAIL@V23GROUP.COM (all caps domain). Two contacts per column.

Rule: Follow format-era convention — deck OMs use sentence-case name + mixed-case email; Word OMs use ALL CAPS name + ALL CAPS email. Never mix.

---

## 4. File & Version Naming

OBSERVED (confirmed across B, D, E, A slices).

- **Active OM files:** `<Deal> - OM - <YYYY-MM-DD>.pptx` (ISO date). Examples: `105_N_13 - OM - 2026-04-22.pptx`, `NPV-Florida-IOS - OM - 2026-06-09.pptx`.
- **Final PDFs:** Same naming as pptx; PDF export may carry +1 day from conversion (06-09 pptx → 06-10 pdf, NPV chain).
- **Initials suffixes:** `vhc` = Henry Chakardjian; `vTM` = Theodore Mouhlas; `vLiz` = Liz Orlova; `vMike` = Mike Strug or client Mike. Used on in-process circulations only. The send-state file drops all initials suffixes and carries only the ISO date.
- **Archive folder:** Older versions move to `Archive/` subdirectory. Send-state file lives in the root of the `OM/` folder. Confirmed B, D, E, C slices.
- **"vSend" suffix (Word OM chain, Slice E only):** `vSend`, `vSend 2` used just before PDF export for investor distribution. Not confirmed in deck OM chains — treat as Word OM chain convention.

---

## 5. Stat-Box & Exec Summary Conventions

### 5.1 Stat-box content by register

LEGISLATED 2026-06-11. Platform decks NEVER carry blended aggregate IRR in the stat box. This was an explicit correction documented in the NPV Blueprint — the v0 stat box carried a blended 27% IRR and "$39.2M aggregate basis" headline; these were removed in the final per Blueprint prohibition. The per-deal + pipeline form is the canonical platform-era stat-box pattern.

**Equity platform deck stat box (NPV final, slide 2, 2026-06-09):**
- `$50MM / LP EQUITY ASK`
- `20%+ / TARGET GROSS IRR PER DEAL`
- `2.0x+ / TARGET EQUITY MULTIPLE PER DEAL`
- `[Pipeline coverage metric] / ACTIVE [MARKET] PIPELINE COVERAGE`
- `5-YR / TARGET HOLD PER DEAL`

**Debt OM stat box (105 N 13 vDebt, slide 3, VERIFIED):**
- `Debt Returns` header
- `Leverage / 60.00%`
- `Debt Yield / 8.62%`
- `DSCR at Origination / 1.23x`

### 5.2 S&U schema — use the deck schema in Word OMs

LEGISLATED 2026-06-11. The corpus did not fully resolve whether Word OMs always carry $/SF and % columns in their S&U tables (the deck schema). The deck schema ($/SF + % columns alongside dollar total, confirmed in 105 N 13 slide 3) is the more complete and comparable form. Rule: Word OMs use the deck S&U schema — include $/SF (or $/unit) column and % column alongside the dollar total in all S&U tables, regardless of format (deck or Word OM).

### 5.3 Executive Summary word-OM return-metrics phrase structure

OBSERVED (verbatim-stable across E13, E43, E48, E52, E54, E67, E68, 2024–2025):

"The project underwrites to an attractive X.XX% unlevered IRR and X.XXx equity multiple, X.XX% levered IRR and X.XXx equity multiple over a X-year hold, and X.XX% untrended yield on cost resulting in a development spread of XXX basis points."

Do not paraphrase this structure in Word OMs — it is a house formula.

---

## 6. Discarded / Not-A-Convention

Per corpus README bar (pattern needs ≥3 materials spanning years), the following were observed but are NOT conventions:

- `×` (multiplication sign) for equity multiples — single instance (VHC2 Slice A); not a pattern.
- Spaced-caps geographic page header ("W I N D G A P, P E N N S Y L V A N I A") — present in 2024 PDF versions only; replaced by normal caps in 2025 version. Transitional artifact.
- Per-slide source lines with full citations — draft-state artifact in early NPV deck (2026-05-26); stripped before send state. Not a send-state convention.
- German / European monetary units (€) — Krios/Ever Leaf international register only; excluded from domestic OM conventions.
- Blended portfolio IRR as headline metric — explicitly discarded per Blueprint; never use in outbound platform deck.
- "DEAL 1 OF 4" individual deal slide labels — NPV v0 only; replaced by tile format.
- "78%-deployed" pipeline metric and P1/P2/P4 priority-tier language — NPV v0 regressions; never use.

---

## Legislated Items Count: 8

1. Three-context dollar rule ($mm / spelled-out / $MM by context)
2. Two-decimal rule for model-derived returns (from synthesis codification)
3. Lowercase x for multiples (resolves × outlier)
4. Range punctuation: hyphen (not en-dash)
5. Per-slide source lines stripped at send state for domestic decks
6. Platform stat box never carries blended aggregate IRR
7. Word-OM S&U schema: use the deck schema ($/SF + % columns)
8. Blueprint-time risk-register placement decision (registers-and-coverage.md §3, not repeated here)
