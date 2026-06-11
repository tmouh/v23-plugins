_Derived from the 2026-06 pattern study (geometry extraction across V23 production decks 2020–2026). Supersedes layout-repertoire.md. Regenerate by re-running the sweep per docs/superpowers/plans/2026-06-11-om-builder-v6.md._

---

# LAYOUT SYSTEM

## 1. SELECTION LOGIC (THE LOAD-BEARING RULE)

Layout selection is **primarily structural**: a slide's position and role in the register's canonical sequence determines its arrangement. Every V23 production deck — across registers, dates, and deal types — assigns its canonical slide positions to fixed arrangements. The sequence→arrangement mapping below is the decision rule.

**Intent-based selection is demoted to tiebreak only.** The old repertoire's four-stage intent-classification procedure (recover intent from action title → map to layout family) applies exclusively to non-canonical or custom slides that fall outside the register's canonical sequence. For any slide whose position matches a canonical slot, the structural mapping overrides intent-based reasoning.

### 1A. Canonical Sequence → Arrangement Mapping (Deck-OM Register)

| Slide # | Canonical role | Arrangement | Notes |
|---|---|---|---|
| 1 | Cover | A-01 Full-bleed photo cover (split-panel) | Invariant in Garamond system |
| 2 | Confidentiality / Disclaimer | A-02 Header-band + full-slide prose | Always slide 2; mandatory |
| 3 (equity OM / debt OM) | Executive Summary | A-03 Dual-panel: left narrative + right tables | B/E-chain; right-panel metric vocabulary shifts by register (equity → IRR/EM/YoC; debt → DSCR/Debt Yield/Leverage) |
| 3 (platform / programmatic OM) | Executive Summary | A-04 2×2 four-block grid + stat strip | D/C-chain; blocks: Opportunity / Strategy / Pipeline / Ask |
| Next non-cover, non-disclaimer (all registers) | Investment Highlights | A-06 Bold-lead label-rail | Invariant; register changes only the lead bullet topic |
| First geographic slide | Asset Location | A-09 Map-dominant | Standard position; varies in deck order |
| Asset photography slide | Photos | A-10 2×2 photo grid | Standard |
| All narrative content slides | Project Background / Business Plan / Market / Submarket | A-13 Header-band narrative prose | Invariant body arrangement |
| All data/comparison slides | Rent roll / Comps / Financials | A-12 Table-dominant | Invariant |
| Sponsor track record section | Case study tiles | A-14 Sponsor tile cards | Consistent across B/D/H |
| Second-to-last or last | Contact | A-17 Named-card grid | Invariant |
| All content slides (shell) | Any | A-08 Header-band shell | The master template underlying every content slide |

**Tiebreak (non-canonical slides only):** When a slide falls outside the canonical sequence, select arrangement by communicative intent using the content-type mapping in Section 2. Never apply intent-based selection to a canonical slot.

---

## 2. OBSERVED ARRANGEMENT CATALOG

### 2A. CORE Arrangements (≥3 decks, ≥2 years)

---

#### A-01 — FULL-BLEED PHOTO COVER (split-panel variant)

**Zone description:** Left half: full-bleed photo [x=0.0 y=0.0 w=6.83 h=7.5]. Right half: address text Garamond 44pt bold at x≈6.83 y≈1.36; ask-line text 23pt bold at y≈3.49; sponsor logos at x≈10.74 y≈6.0 (bottom right). Off-canvas accent bars at x=−1.23 (8 bars, template fixture). V23 logo at x=12.69 y=0.36 w=0.24 h=0.35. Canvas: 13.33×7.5".

**Content:** Deal OM cover — single-asset or programmatic platform.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.1); B-105_N_13-OM-2026-01-23 (sl.1); D-NPV-IOS-OM-FINAL-0609 (sl.1); F-3605-Church-Ave (sl.1, compressed one-pager variant: full-width header bar h=0.99 rather than split-panel).

---

#### A-02 — CONFIDENTIALITY / DISCLAIMER PAGE

**Zone description:** Full-width header band [x=0.0 y=0.29 w=13.33 h=0.50, navy fill]. Header text: TextBox [x=0.41 y=0.33 w=12.52 h=0.44], Garamond 20pt bold white, "Confidentiality & Conditions." Body: single large TextBox [x=0.41 y=1.03 w=12.52 h=6.18] — full-slide disclaimer prose. V23 logo at standard position.

**Content:** Mandatory legal/confidentiality page. Always slide 2 in pptx OMs.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.2); C-Obsidian_Krios_Full_April2026 (sl.2, 2026-04-13); D-NPV-IOS-OM-FINAL-0609 (sl.2); E-WindGap (pages 1–2, Word OM, 2024–2025).

---

#### A-03 — EXECUTIVE SUMMARY: DUAL-PANEL (left narrative + right dual-table)

**Zone description:** Full-width header band + header text. Left panel: narrative TextBox [x=0.40 y=1.06 w≈7.21 h≈6.06], Garamond 13–14pt, 700–900 characters / ~115–145 words. Right panel: dual embedded tables — Uses/Sources capital stack (TABLE 5×3 or 5×6) stacked above returns KPI table (TABLE 5×3 or 7×6); x≈7.5–12.9, y=1.06–7.50.

**Content:** Exec Summary — narrative left, numbers right. Always slide 3 in B-chain equity and debt OMs. Right-panel metric vocabulary shifts by register (equity → IRR/EM/YoC/Net Profit; debt → DSCR/Debt Yield/Leverage).

**Citations:** B-105_N_13-OM-2026-04-22 (sl.3); B-105_N_13-OM-2026-02-17 (sl.3); B-105_N_13-OM-vDebt-2026-03-02 (sl.3); D-NPV-IOS-v0-0526 (sl.2).

---

#### A-04 — EXECUTIVE SUMMARY: 2×2 FOUR-BLOCK GRID + STAT STRIP

**Zone description:** Full-width header band + header text + stat box strip below header (3–5 KPI boxes, y≈1.5–2.4). Four named content blocks in 2×2 arrangement below stat strip: Block_Opportunity [x=0.83 y=2.47 w=5.69 h≈1.3]; Block_Strategy [x=6.81 y=2.47 w=5.69 h≈1.3]; Block_Pipeline [x=0.83 y=4.04 w=5.69 h≈1.5]; Block_Ask [x=6.81 y=4.04 w=5.69 h≈1.5]. Each block opens with ALL-CAPS em-dash label ("WHY NOW — [one sentence]").

**Content:** Platform or programmatic deck executive summary. Carries the "why now + thesis + pipeline + ask" quad.

**Citations:** D-NPV-IOS-OM-0601 (sl.2, 2026-06-01); D-NPV-IOS-OM-FINAL-0609 (sl.2); C-Krios_v4 (sl.4, 2×3 grid variant, 2026-04-20).

---

#### A-06 — INVESTMENT HIGHLIGHTS: BOLD-LEAD LABEL-RAIL

**Zone description:** Full-width header band + header text. Single full-width TextBox [x=0.41 y=1.04 w=12.52 h≈5.35]: stacked vertical blocks separated by pipe "|" delimiters (pptx) or double-newline (Word). Each block: **Bold thesis label** (Garamond bold, 3–5 words) + em-dash + plain evidence clause (Garamond 13–15.8pt, 2 lines). No boxes, icons, or bullets — purely typographic. 6–9 highlights per page.

**Content:** Investment Highlights. Most consistent single slide pattern in the V23 corpus. Lead bullet topic changes by register: equity → returns ("Compelling Financials"); debt → coverage ("Existing Debt Service Coverage"); programmatic → market signal ("Compelling Metrics").

**Citations:** B-105_N_13-OM-2026-04-22 (sl.5); E-WindGap-E48 (2025-03-10); E-WindGap-E43 (2025-02-18); D-NPV-IOS-OM-FINAL-0609 (sl.3).

---

#### A-07 — KPI STRIP WITH NAMED BACKGROUND RECTS (stat-box system)

**Zone description (D/NPV named-box variant):** Stat strip at y≈1.5–2.4 (below header, above content blocks). Named shapes: KPI_Bg_N [w=2.64 h=0.97]; KPI_Val_N [w=2.78 h=0.44, large number 26–36pt]; KPI_Lbl_N [w=2.78 h=0.28, ALL-CAPS caption]. 3–5 boxes per strip on exec summary; 8 boxes on dedicated investment criteria slide (D-NPV final sl.16). Case study bottom strip: 4 boxes at y≈6.23, each w=2.83, at x=0.83/3.78/6.72/9.67.

**Zone description (B/105N13 variant):** Right-panel capital-stack tables (TABLE 5×3 and 5×6) embedded in exec summary — same stat-display function, tabular realization rather than named boxes.

**Content:** Transaction snapshot KPIs, returns metrics, platform-level deal parameters.

**Citations:** D-NPV-IOS-OM-FINAL-0609 (sl.2 stat strip; sl.12 case-study KPI boxes); D-NPV-IOS-OM-0601 (sl.2); C-Obsidian_Krios_Full_April2026 (sl.5, 3-column stat blocks [w=3.88 h=1.05 each]).

---

#### A-08 — HEADER-BAND CONTENT PAGE (standard body slide shell)

**Zone description:** Off-canvas accent bars: 8 rectangles [x=−1.23 w=1.02 h=0.69] stacked at y=0.29/1.19/2.08/2.95/3.82/4.69/5.56/6.43 — permanent template fixture on ALL content slides in Garamond system. Full-width header band: Rectangle [x=0.0 y=0.29 w=13.33 h=0.50, navy #1F3A5F fill]. Header text: TextBox [x=0.41 y=0.33 w=12.52 h=0.44], Garamond 20pt bold white. V23 logo: [x=12.69 y=0.36 w=0.24 h=0.35]. Content area begins y≈1.03–1.06.

**Stability:** Zero template drift confirmed from 2026-01-23 through 2026-04-22 (15 months, 40+ slides). This is the shell that all other arrangements inhabit in the Garamond system.

**Content:** Any content slide — the underlying master.

**Citations:** B-105_N_13-OM-2026-01-23 through 2026-04-22 (all content slides); D-NPV-IOS-v0-0526 through D-NPV-IOS-OM-FINAL-0609 (all content slides).

---

#### A-09 — ASSET LOCATION: MAP-DOMINANT

**Zone description:** Header band + header text. Map image fills primary zone [x≈0.87–1.98 y≈1.05 w≈7.63–9.38 h≈5.92–6.17]. Right 25–30%: legend or narrative text — numbered callout labels or geographic context bullets. Numbered oval/circle pins on map. Caption below at y≈7.0–7.1.

**Content:** Geographic asset positioning — locator map, neighborhood map, annotated amenities map, submarket map.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.6, 19, 23); D-NPV-IOS-OM-FINAL-0609 (sl.8 "Why Central Florida"); E-WindGap "Asset Location" section (2024–2025).

---

#### A-10 — PHOTO GRID: 2×2 WITH CAPTION BARS

**Zone description:** Header band + header text. 4 photos in 2×2 arrangement [each ≈4.49w × 2.87h], filling content zone y=1.13–7.11. Left column x≈1.73; right column x≈6.78; row 1 y≈1.13; row 2 y≈4.24. Caption bars: narrow Rectangle [h=0.29] directly below each photo with 1–2 word label.

**Variant — 1×2 (right side):** Two photos at x≈8.09–9.41 stacked (y≈1.08 and y≈4.28–4.39).

**Content:** Asset photography — interior/exterior views, sponsor track-record case studies.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.8); H-V23_simple_2020 (sl.1, 4-photo cover grid, 2020-10-22); H-ELM_PitchBook_2022 (sl.7–12, 2022-06-15).

---

#### A-11 — NEIGHBORHOOD AMENITIES: LABELED 2-COLUMN GRID

**Zone description:** Header band + header text. Two columns: left [x=0.40 y=1.0]; right [x=6.83 y=1.0]. Within each column: 4 vertical stacks — numbered Rectangle label [w=0.34 h=0.32] + name Rectangle [w=1.98 h=0.32] + body TextBox [w≈2.30 h≈0.92–1.12]. Photos embedded: 2×2 pairs within left column zone [w=1.73 h=1.28] at x=2.84 and x=4.69. 8 amenity entries per slide (4 per column).

**Content:** Neighborhood amenities/context — parks, hospitality, retail, wellness.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.22–23); B-105_N_13-OM-2026-02-17 (equivalent slides).

---

#### A-12 — TABLE-DOMINANT (comps, financials, rent roll)

**Zone description:** Header band + header text + optional one-line action sub-header (y≈0.84–0.98). Primary table fills content zone: observed sizes 2×4, 4×5, 5×2, 6×2, 6×3, 7×2, 7×6, 8×6, 8×7, 11×8. Source line at y≈5.78–7.07 (italic, 8pt). Some comp slides embed photo right-side [x≈9.4–9.44 y≈1.23–4.73].

**Multi-table variant:** 2–3 tables per slide (TABLE 8×6, TABLE 14×7, TABLE 11×6, TABLE 26×5 on same slide — confirmed H-Obama-2022 UW slides).

**Practical limit:** 7 columns max on 13.33" canvas before column labels wrap. Dense comps typically 6–8 rows + 1 header.

**Content:** Rent roll, comparable leases, comparable sales, operating financials, returns table, budget.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.24–28); E-WindGap Financial Analysis section (2024–2025); H-Obama_V23_2022 (sl.2–4, 2022-04-11).

---

#### A-13 — NARRATIVE PROSE BODY (dense single-column)

**Zone description:** Header band + header text. Single large TextBox [x=0.41 y≈1.06–1.15 w=12.52 h≈5.84–6.12]. Garamond 13–14pt. Pipe "|" or double-newline separates logical sections within the box. Bold inline for key numerics and proper nouns. Optional right-side supplemental picture [x≈8.0–9.44] where text needs visual proof.

**Content:** Project Background, Business Plan, Submarket overview narrative, Exec Summary continuation, In-Place Tenancy narrative.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.9, 12); E-WindGap-E48 (all narrative sections, 2025-03-10); D-NPV-IOS-OM-FINAL-0609 (sl.8–9).

---

#### A-14 — SPONSOR TRACK RECORD TILES (2+1 case-study cards)

**Zone description:** Header band + header text + optional sponsor bio block at top [x=0.41 y=0.94]. Two equal-width case study columns: left [x≈3.09–3.11], right [x≈6.91–6.95], each w≈3.31. Per column: photo [w=3.31 h=2.21 at y=1.37] + name Rectangle [h=0.37 at y=3.72] + location TextBox [h=0.44 at y=3.97] + stats TABLE [3×2 or 6×2] + body narrative TextBox [w=3.31 h≈1.19 at y≈5.91]. Some slides have 3 tiles (additional left column).

**Content:** Sponsor track record case studies, prior deal exhibits.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.36–37); D-NPV-IOS-OM-FINAL-0609 (sl.11); H-ELM_PitchBook_2022 (sl.7–12, 2022-06-15).

---

#### A-15 — 3-UP TILE ROW WITH STATUS EYEBROWS

**Zone description:** Header band + 3-tier header block (section title y=0.53; slide title y=0.75; lead sentence y=1.20). Three tile columns: left [x≈0.97], center [x≈4.92], right [x≈8.99]. Per tile, vertical stack: eyebrow TextBox [h=0.17 at y≈4.50, ALL-CAPS, no box — purely typographic] → address TextBox [h=0.29–0.47 at y≈4.78] → metric line "XX.XX% IRR / X.XXx EM" [h=0.29 at y≈5.33] → body description [h=0.83–1.01]. Eyebrow labels: "RECENT CLOSING," "ACTIVE PIPELINE," "INDUSTRIAL ADJACENT."

**Variant:** 2-up tile row for fewer deals (eyebrow behavior identical).

**Content:** Multi-deal tile slides — realized, recent, or active deals with status classification. Platform / programmatic register.

**Citations:** D-NPV-IOS-OM-FINAL-0609 (sl.13 "RECENT FLORIDA EXECUTIONS"; sl.15 "LIVE DEPLOYABLE DEALS"); D-NPV-IOS-OM-0601 (deal-tile slides).

---

#### A-16 — REALIZED CASE STUDY (eyebrow header + bottom KPI strip)

**Zone description:** Header band + section-level eyebrow as header text (e.g., "REALIZED CASE STUDY | 3161 SKYWAY CIRCLE, MELBOURNE, FL (DEC 2024)"). Body: narrative TextBox left 55–60% [y=1.0–5.5] + right photo. Bottom KPI strip: 4 horizontal boxes at y≈6.23, each w=2.83 at x=0.83/3.78/6.72/9.67. Each box: large value (20–26pt) + small-caps label (8–10pt) below. Labels: "PROJ. GROSS IRR / PROJ. EQUITY MULTIPLE / PROJ. YIELD ON COST / YR 1 CAPITAL RETURNED (REFI)."

**Content:** Single deal case study or sponsor track-record proof-point.

**Citations:** D-NPV-IOS-OM-FINAL-0609 (sl.12); B-105_N_13-OM-2026-04-22 (sl.13).

---

#### A-17 — CONTACT PAGE (named-card grid)

**Zone description:** Header band + "Contact" header text (Bell MT 44pt bold white on dark band — confirmed F-slice). 2×2 or 2×3 grid of named-card TextBoxes, each card: Name (bold) + Title (italic) + Mobile + email. Typical: 5 contacts — three at y≈2.31, two at y≈4.22 (or Stephen Muller centered at y=3.30). No headshot photos in B/D system.

**Geometry (B-2026-04-22 sl.39):** Henry Chakardjian [x=6.2 y=2.31]; Mike Strug [x=9.37 y=2.31]; Liz Orlova [x=6.2 y=4.22]; Theodore Mouhlas [x=9.37 y=4.22]; Stephen Muller [x=3.04 y=3.30]. Photo id=15 [x=0.98 y=3.04 w=1.65 h=1.82] = Muller headshot.

**Content:** Deal contact page — Vanadium-only contacts.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.39); D-NPV-IOS-OM-FINAL-0609 (sl.18); F-AlphaSquare Rapid Depreciation (sl.7, 2026-05-11); F-OpenHouse Rapid Depreciation (sl.9, 2026-05-11).

---

#### A-18 — SECTION DIVIDER (numbered or named, dark-fill)

**Zone description (Krios-dark explicit, 10×5.62" canvas):** Full-slide dark fill #0D1B2A + left accent stripe [x=0.0 w=0.25 h=5.62]. Horizontal rule at y≈2.20, w=9.75. Large number Georgia 72pt bold gold [x=0.50 y=1.30 w=2.0 h=1.10]. Section title Georgia 28pt below rule [x=0.50 y=2.35 w=9.0 h=0.70]. Sub-descriptor Calibri 14pt gold italic [x=0.50 y=3.10 w=7.0 h=0.45].

**Zone description (B-chain implicit):** No explicit divider slide; sections transition via new header-band title only.

**Zone description (VHC2/Obsidian):** Section title slides with three-column arrangement (rectangle titles at x≈0.58/3.58/6.58).

**Content:** Major section transitions. Optional; required in full OMs ≥25 slides. Many V23 decks skip explicit dividers entirely (B-chain uses header-band title change only).

**Citations:** C-Obsidian_Krios_Full_April2026 (sl.4/8/11/16, 2026-04-13); A-Platform-Deck-VHC2 (sl.3/7/11/14); B-105_N_13 (implicit only — no explicit divider slides).

---

#### A-21 — SIDEBAR + DOMINANT MAP/VISUAL (35/65 split)

**Zone description:** Left sidebar [x≈0.41–0.56 y≈1.06–1.22 w≈5.11–5.38 h≈4.89–6.00] — prose narrative or bullet list. Right dominant [x≈5.98–8.21 y≈1.19–1.23 w≈4.50–6.24 h≈2.43–5.30] — photo, map, or rendering. Optional second image stacked below right image at y≈4.23–4.39.

**Content:** In-place tenancy narrative + lease charts, adjacent development descriptions, sponsor track record with proof images.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.10, 20, 21); D-NPV-IOS-OM-FINAL-0609 (multiple slides); E-WindGap (multiple).

---

#### A-22 — HALF-AND-HALF (image left + narrative right, true 50/50)

**Zone description:** Left photo [x=0.0–1.73 y=0.0–1.08 w≈6.83 h≈7.50, full-height left half]. Right narrative [x≈8.09–8.56 y≈1.08–1.38 w≈4.50–4.61 h≈2.79–2.91, top]; second image below at y≈4.23–4.39.

**Content:** Cover (left photo + right text), asset overview (photo + data), exec summary continuation (context photo + market narrative).

**Citations:** B-105_N_13-OM-2026-04-22 (sl.4); C-Ever_Leaf_vF (sl.2, splash/headshot trio, 2026-04-24); A-Platform-Deck-VHC2 (sl.1, 2026-05-07).

---

#### A-24 — CHART-DOMINANT WITH SUPPLEMENTAL NARRATIVE

**Zone description:** Header band + header text + brief lead paragraph (y≈1.03–1.85). Chart (lineChart or TABLE) fills middle-to-lower zone. Source line at y≈6.35–7.07 (italic, 8pt). Optional supplemental text blocks below chart.

**Content:** NOI build, vacancy trend, returns trajectory, market charts.

**Citations:** B-105_N_13-OM-2026-04-22 (sl.16, lineChart + dense text; sl.17, lineChart + TABLE 7×2); D-NPV-IOS-OM-FINAL-0609 (sl.8 "Why Central Florida"); H-Obama_V23_2022 (market charts).

---

#### A-25 — SIMPLE PRESENTATION MASTER (pre-Garamond era, 2020–2022)

**Zone description:** Same 13.33×7.5" canvas. Title placeholder [x=0.62 y=0.40 w=11.50 h=0.46]. Logo large [x=12.12–12.21 y=5.87–6.26 w=1.12 h=1.24], bottom-right. NO header-band rectangle. NO off-canvas accent bars. Font system not Garamond (earlier system — Times New Roman / Arial per template files).

**Content:** All content slides from 2020–2022 V23 decks. The predecessor system to the current Garamond master.

**Citations:** H-V23_simple_2020 (all slides, 2020-10-22); H-Obama_V23_2022 (all slides, 2022-04-11); H-ELM_PitchBook_2022 (all slides, 2022-06-15).

**Note:** Transition from Simple Presentation to Garamond system occurred 2022–2026. Not deprecated for historical context; do not use as template seed for new OMs.

---

### 2B. SECONDARY Arrangements (2 decks — real pattern, not yet generalized; do not codify until third confirmation)

#### A-05 — EXEC SUMMARY: FIVE-ROW LABEL-RAIL CARD

**Zone (10×5.62" canvas):** Section breadcrumb + short accent rule. Five horizontally banded rows: background Rectangle + 0.06"-wide gold left-accent bar + two TextBoxes (left: 2.0"-wide gold-colored label; right: 6.65"-wide body). Row heights ≈0.80", stacked y=1.22–5.50. Labels: "The market gap / The model / The proof point / The platform / The access."

**Citations:** C-Obsidian_Krios_Full_April2026 (sl.3, 2026-04-13) — single deck only.

---

#### A-19 — THREE-COLUMN EQUAL-WIDTH TILE (platform/thesis overview)

**Zone:** Three equal-width rectangles across slide [each w≈2.83" on 13.33" canvas]. Col 1: x=0.58; Col 2: x=3.58; Col 3: x=6.58. Each col: label bar [y=1.17 h=0.31] + body below. Semantic named shapes (Col1Body/Col2Body/Col3Body in VHC2).

**Citations:** A-Platform-Deck-VHC2 (sl.5, 8, 10, 22, 2026-05-07); C-Krios_v4 (sl.4, 2026-04-20). Absent from all 2025 and earlier materials; emerged May 2026.

---

#### A-20 — AT-A-GLANCE FACT TABLE (key-value property facts)

**Zone:** Named TABLE shape [e.g., F: id=27 name='AtAGlanceTable' TABLE 15×2; id=9 TABLE 6×2]. Label-value rows: Asking Price / $/SF / Size / Lot / Zoning / Building Class / BBL. Positioned mid-slide alongside building description and floor-plan image.

**Citations:** F-3605ChurchAve-One-Pager (sl.1, 2026-05-27); D-Tarpon-1pg-0224 (sl.1, 2026-02-25).

---

#### A-23 — COMPACT ONE-PAGER / TEASER (2-slide format)

**Zone:** Slide 1: full-width header bar [h≈0.69] with deal type + address bold-white left + price bold-white right; sub-header band below [h≈0.25] all-caps 9pt; then fact table + property photos + feature bullets. Slide 2 (if present): floor plan or site plan with building label overlays (rounded-corner rectangles: "Building A | 46,800 SF").

**Citations:** F-3605ChurchAve-One-Pager (sl.1–2, 2026-05-27); D-Tarpon-1pg-0224 (sl.1–3, 2026-02-25); C-Krios-CoInvest-11-slide (2026-04-08).

---

## 3. DENSITY NORMS BY REGISTER

### 3A. Words per slide (observed ranges — not targets)

| Slide type | Register | Observed range | Notes |
|---|---|---|---|
| Cover | Full OM | 15–35 words | Address + ask + subtitle only |
| Confidentiality / disclaimer | Full OM | 350–500 words | Dense prose, one TextBox |
| Exec Summary narrative panel | Full OM | 100–180 words | 700–900 chars / ~115–145 words in B-chain left panel |
| Investment Highlights | Full OM | 200–350 words | 6–9 bullets × ~30–40 words each |
| Project Background / Business Plan | Full OM | 150–280 words | Narrative prose body |
| In-place tenancy / Business Plan | Full OM | 150–250 words | Narrative + brief table annotations |
| Market Overview (metro) | Full OM | 120–220 words | 2–3 prose blocks + embedded table headers |
| Submarket Overview | Full OM | 150–300 words | Two full prose columns |
| Comparable leases / sales | Full OM | 60–120 words | Table dominant; 1–2 intro sentences |
| Financial / budget table | Full OM | 30–80 words | Table dominant; notes below |
| Map / location | Full OM | 20–60 words | Caption + legend labels |
| Photo grid | Full OM | 10–30 words | Caption labels only |
| Sponsor Track Record | Full OM | 120–250 words | Bio paragraph + case studies |
| Contact | Full OM | 40–80 words | 5 contacts × name/title/mobile/email |
| Section Divider | Full OM | 10–25 words | Number + title + sub-descriptor only |
| Teaser one-pager | Teaser | 120–200 words | Dense but compressed |
| 3-up tile slide | Platform | 80–150 words | 3 tiles × 30–50 words |
| Exec Summary 4-block | Platform | 150–250 words | 4 blocks × 40–60 words |

**Full OM median:** ~120–160 words per content slide (excluding disclaimer, table-dominant, and map slides). Decks of 38–40 slides typically carry 3,000–5,000 total words in slide bodies.

### 3B. KPI counts per strip (observed)

| System | KPI count | Box dimensions | Source |
|---|---|---|---|
| D-NPV-IOS named-box (exec summary stat strip) | 3–5 per strip | KPI_Bg: 2.64w × 0.97h | D-NPV-IOS-OM-FINAL sl.2 |
| D-NPV-IOS investment criteria slide | 8 boxes | same dimensions | D-NPV-IOS-OM-FINAL sl.16 |
| D-NPV-IOS case study bottom strip | 4 boxes | each w=2.83 at y≈6.23 | D-NPV-IOS-OM-FINAL sl.12 |
| B-105N13 exec summary right panel | 3–4 rows × 1–2 col tables | TABLE 5×3 or 5×6 | B-2026-04-22 sl.3 |
| C-Krios-dark 3-col stat blocks | 3 blocks per slide | each w=3.88 h=1.05 | C-Krios-Full sl.5 |

**Typical range:** 3–5 on exec summary; 4 on single-deal case study bottom strip; up to 8 on dedicated investment criteria slide.

### 3C. Bullets per Investment Highlights page (observed)

| Version | Register | Bullet count | Format |
|---|---|---|---|
| B-105N13 final 2026-04-22 | Equity full OM | 7 | Bold label + em-dash + 2-line body |
| E-WindGap pref OM 2025-03-10 | Pref equity full OM | 8 | Same structure |
| E-WindGap JV OM 2025-03-24 | JV equity full OM | 7–8 | Same structure |
| D-NPV-IOS final 2026-06-09 | Programmatic platform | 6 | Category-label + parenthetical metric |
| B-105N13 vDebt 2026-03-02 | Debt OM | 7 | Lead bullet changes to debt metric |

**Observed range:** 6–9. Practical ceiling at Garamond 13–14pt in TextBox h≈5.35 is ~9.

### 3D. Exec panel character range

Left-panel prose body in A-03 dual-panel: **700–900 characters / ~115–145 words** at Garamond 13–14pt in TextBox [w=7.21 h=6.06]. Confirmed from B-chain geometry.

### 3E. Table row/column ranges (observed)

| Table type | Rows × Columns | Source |
|---|---|---|
| Capital stack (S&U) | 5×3 to 7×6 | B-105N13 sl.3 |
| Returns summary | 3×4 to 5×6 | B-105N13 sl.3; E-WindGap |
| Comp leases | 5×7 to 8×7 | B-105N13 sl.25–27 |
| Comp sales | 2×7 to 11×8 | B-105N13 sl.28–30 |
| Office vacancy | 11×8 | B-105N13 sl.28 |
| Asset overview | 6×2 | B-105N13 sl.7 |
| Sponsor track record stats | 3×2 | B-105N13 sl.36–37 |
| 1-pager fact table | 15×2 | F-3605ChurchAve sl.1 |
| Pipeline | 11×5 | C-Krios sl.17 |

**Practical limit:** 7 columns max on 13.33" canvas before column labels wrap. Dense comps typically 6–8 data rows + 1 header.

---

## 4. COMPOSITION BEHAVIORS

### 4A. Zone-pattern variety practice

V23 production decks vary zone patterns deliberately — the comp section of B-105N13 (sl.24–27, same arrangement 4× in a row) is the one documented case of layout monotony and the only zone-pattern violation in the corpus. The track-record tile series (sl.35–38) uses deliberate parallel repetition as evidence structure, which is intentional.

**Rules derived from observation:**
- Never the same body layout on two consecutive content slides, except in deliberate parallel series (comps, case study tiles, amenity grids) where repetition IS the evidence structure.
- Maximum 2 identical arrangements in any 4-slide window outside a declared parallel series.
- Open each major section with a higher-contrast "statement" layout (map-dominant, full-bleed photo, or chart-dominant), then move to working layouts (narrative prose, table).
- Aim for ≥7 distinct arrangements across a full OM deck (38–40 slides).

**For non-canonical slides where intent-based selection applies:** use the content-type → arrangement mapping in the tiebreak table (below) to select the arrangement that matches the slide's primary communicative intent.

| Intent | Arrangement | Action-title cue |
|---|---|---|
| Geographic positioning | A-09 Map-dominant | "located in", "submarket", "within N miles" |
| Multiple photos | A-10 Photo grid | Photography, amenities visuals |
| Data comparison / structured lookup | A-12 Table-dominant | Rent roll, comps, financials |
| Prose narrative | A-13 Narrative prose | Business plan, project background |
| Profile / credibility | A-14 Tile cards | Track record, sponsor case studies |
| Multi-deal status | A-15 3-up tile eyebrows | Pipeline, realized deals |
| Single case study | A-16 Case study + KPI strip | Realized deal proof-point |
| Quantitative trend | A-24 Chart-dominant | NOI build, vacancy trend |
| Narrative + dominant visual | A-21 Sidebar 35/65 | In-place tenancy, adjacent development |
| Asset overview (photo + text) | A-22 Half-and-half | Cover continuation, asset overview |

### 4B. New-slide practice (clone pattern)

V23's confirmed production method: **clone an existing slide from the deck, modify content, preserve layout and named shape IDs**. Never invent a new master layout from scratch for a production deck.

From B-chain notes: "version chain grows by cloning an existing slide and modifying content — the layout and named shape IDs are inherited." Confirmed: all 39 slides in B-2026-04-22 use the same slideLayout7.xml (Blank) master with identical 8 accent rectangles at x=−1.23.

Semantic named shapes from D-NPV final that should be preserved on any new slide: `Block_Opportunity`, `Block_Strategy`, `Block_Pipeline`, `Block_Ask`, `KPI_Bg_N`, `KPI_Val_N`, `KPI_Lbl_N`, `CoverTitleBlock`, `Takeaway`, `Section_Header`, `Source`.

### 4C. Footer and source-line positions

**V23 logo (content slides):** x=12.69 y=0.36 w=0.24 h=0.35 — upper-right, permanent on all pptx content slides in Garamond system.

**No slide page numbers:** V23 pptx OMs carry no visible page numbers (confirmed by geometry — no field elements in any pptx inventory).

**Source lines (market slides only):** B-chain places source lines at y≈6.35–7.07, Garamond 9pt italic, only on market slides with external data (e.g., "Source: JLL Research, 'New York Office Market,' Q4 2025"). Not present on every slide.

**Krios-style per-slide source lines:** C-series uses Calibri 8–8.5pt #8FA3B1 at bottom 0.2" of every content slide. This is a Krios-specific convention, not the Garamond system standard.

**Confidentiality footer variants (confirmed in corpus):**
- "PRIVATE & CONFIDENTIAL — FOR DISCUSSION PURPOSES ONLY" (Calibri 9pt #8FA3B1, C-Krios-dark)
- "ALL INFORMATION HEREIN PRIVATE & CONFIDENTIAL | VANADIUM GROUP" (right-aligned caps, F-AlleyNorth)
- "Qualified Investors Only / Proprietary and Confidential" (8pt, C-Everleaf cover)

**PDF footer (emerging, single confirmed instance):** "Vanadium Realty LLC | [Deal Name]" on every page in D-NPV-final.pdf (2026-06-10) — consistent with Word-OM running-header convention; not yet ≥3-deck durable.

---

## 5. DISCARDED ITEMS

The following layouts from the old `layout-repertoire.md` are discarded — either never observed in production decks or directly contradicted by geometry evidence. Do not apply them to new OMs.

| Old repertoire item | Reason discarded |
|---|---|
| **L2 KPI Strip — #E8EEF6 fill + Aptos navy + Arial labels** | Color and font claims unconfirmed by any geometry or notes. Observed system uses named rectangles (KPI_Bg_N) with no confirmed fill color; Garamond system decks do not use Aptos or Arial. Description was written from design theory, not observed material. Replace with A-07 observed geometry. |
| **L3 Half-and-half — pixel coordinates (x=60–470 / x=490–900)** | Coordinates reference an obsolete 960pt-wide canvas spec. Actual canvas is 13.33" × 7.5" with photo at x=0.0 w=6.83 (left) and narrative starting x≈6.83–8.09. Superseded by A-22 observed geometry. |
| **L14 KPI overlay band on hero photo (interior slide)** | No interior "KPI overlay band on hero photo" slide confirmed in any V23 OM. GTM cover has cover-KPI treatment; no interior equivalent found. Retain as a theoretically valid construction, but do not treat as a default or confirmed V23 pattern. |
| **L16 Lease rollover cliff chart** | No WALT cliff-chart geometry found in any corpus deck. B-chain uses lineCharts for leasing trends (sl.16–17), not cliff-chart visualization. May exist for net-lease deals not in scope. |
| **L17 Stacking plan (vertical floor diagram)** | No stacking-plan slides in 2024–2026 corpus. Theoretically valid for office/mixed-use; no observed example. |
| **L18 Sources & Uses twin-pillar bars** | Capital stack is ALWAYS shown as an embedded TABLE in observed decks (TABLE 5×3 and 5×6 in exec summary right panel). No visual twin-pillar bar geometry found. Tabular S&U is the actual V23 convention. Twin-pillar description is aspirational, not observed. |
| **L19 Comparable sales scatter plot (cap rate vs $/SF)** | All observed comp sales use map + table. No scatter plot geometry in any deck. |
| **L20 Unit-mix split (floor plan + table columns)** | No observed geometry. Palmer MF OM is a Word document only; no floor-plan + mix-table pptx slide found. |
| **L21 Submarket cycle quadrant** | No observed example in any corpus deck. Theoretical. |
| **L23 NOI bridge / waterfall column chart** | Not observed in any geometry. Theoretical. |
| **L24 Renovation before-and-after split** | Not observed in any geometry. Theoretical. |
| **L25 Twin-table financial (net-lease)** | No net-lease deals in corpus. Not observed. |
| **C-Krios 10×5.62" dark format** | Sandbrook Capital audience-match for European co-invest; not V23 house template. Superseded within 7 days by Everleaf format; never propagated to other V23 decks. |
| **A-19 Three-column equal-width tile** | Single deck (A-VHC2, 2026-05-07); absent from all 2025 and earlier materials. Moved to SECONDARY pending third-deck confirmation. |
| **"WHY THIS FITS" urgency coda / scarcity close** | C-Krios teaser only; single-register European family-office teaser. No V23 full OM uses this. |
| **Blended-IRR headline on exec summary stat box** | Explicitly prohibited in NPV Blueprint as "portfolio-era regression." Removed from D-NPV final. |
| **"DEAL 1 OF 4" position labels** | Replaced by status eyebrow system (A-15) in NPV final. Discarded. |
| **Four-stage intent-classification as primary selection method** | Observation confirms layout is structurally determined for canonical slide positions. Intent classification now applies only as a tiebreak for non-canonical slides. |
