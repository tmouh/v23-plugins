# V23 OM Design System

Derived from the 2026-06 pattern study. Supersedes the hardcoded style block formerly in prompt-template.md. Regenerate by re-running the sweep per docs/superpowers/plans/2026-06-11-om-builder-v6.md.

---

## 1. Durable DNA

12 confirmed elements. Each carries exact values and a provenance span. Durability threshold: ≥3 materials, ≥2 years, ≥2 deals.

**D-01 — Navy header band**
- Values: fill #1F3A5F, x=0.0 y=0.29 w=13.33 h=0.50 (inches, 13.33×7.50 canvas)
- Stable since: 2026-01-23 (earliest B-chain pptx)
- Observed in: B-105_N_13 all 7 versions (2026-01-23 → 2026-04-22); F-3605-Church-Ave one-pager (2026-05-27, h=0.99 double-height variant but same x=0.0, w=13.33 construct); F-AlphaSquare/Open-House contact slide (2026-05-11, Rectangle at x=0.0 y=0.29 w=13.33 h=0.81)
- Note: The 3605 Church Ave one-pager uses h=0.99 because it omits a separate sub-header band; the navy rectangle at y=0.0, w=13.33 is the same construct, not a deviation.

**D-02 — Left accent-bar stack**
- Values: 8 rectangles at x=−1.23 (off-canvas left bleed), each w=1.02 h=0.69, y-positions: 0.29 / 1.19 / 2.08 / 2.95 / 3.82 / 4.69 / 5.56 / 6.43
- Stable since: 2026-01-23 (earliest B-chain)
- Observed in: B-105_N_13 all 7 versions (2026-01-23 → 2026-04-22); F-AlphaSquare Contact page (same stack, 2026-05-11); D-NPV final (2026-06-09) — template master element, confirmed on every content slide in every B-series version. Absent from F-3605 single-pager, which uses a simplified one-slide master; this confirms it is a content-slide master element, not a cover-only element.

**D-03 — V23 logo, tiny, upper-right**
- Values: picture at x=12.69 y=0.36 w=0.24 h=0.35; bottom-right variant on cover/contact pages: x=12.65 y=6.75 w=0.24 h=0.35
- Stable since: 2026-01-23 (B-series). The 2020 Simple Presentation used a large logo at x=12.21 y=6.26 w=1.12 h=1.24 (bottom-right, ~4.7× the current area); the 2022 Elmhurst pitch book used x=8.69 y=6.17 w=0.84 h=0.93. The current micro-logo at upper-right represents a deliberate tightening confirmed across all 2026 deck families.
- Observed in: B-105_N_13 all versions (2026-01-23 → 2026-04-22); F-3605-Church-Ave (bottom-right variant, 2026-05-27); F-Open-House contact page (x=11.89 y=0.48, 2026-05-11)

**D-04 — Header text: Garamond 20pt bold, white**
- Values: TextBox at x=0.41 y=0.33 w=12.52 h=0.44; Garamond 20pt bold; color scheme:bg1 (#FFFFFF)
- Stable since: 2026-01-23 through 2026-04-22 without any drift
- Observed in: B-105_N_13 all 7 versions (identical coordinates and type spec across all 7); F-AlphaSquare (contact page uses Bell MT 44pt as a deliberate single-slide display departure — see D-08; all other content slides use this spec)

**D-05 — Body text: Garamond 13–15.8pt, dark**
- Values: Garamond; size range 13–15.8pt (Investment Highlights 15.8pt; Exec Summary body 13–14pt; general body 12–14pt); color near-black (exact hex not extracted from plaintext geometry — #000000 or #1A1A1A)
- Stable since: 2024-05 (E-Pektor Word OMs, E13) through 2026-06 (D-NPV final)
- Observed in: B-105_N_13 all versions (2026-01 → 2026-04) — notes confirm "Garamond 15.8pt" (highlights) and "13-14pt" (body); E-Pektor Word OMs (2024-05 through 2025-03) — Garamond confirmed as body font; D-NPV all versions (2026-05 → 2026-06)
- Disagreement flag: Krios V23-dark format (C-01 → C-05, 2026-04-13 → 16) used Georgia headers and Calibri body — a deliberate departure for that format only. See Section 3 for full typography table.

**D-06 — Full-bleed photo cover with text in right-side strip**
- Values: Left half photo at x=0.0 y=0.0 w=6.83 h=7.5; right half address block starting x≈6.83; address text Garamond 44pt bold; city/state 28pt italic; ask line 23pt bold; subtitle lines 20pt; sponsor logos at x≈10.74 y≈6.0 (bottom-right)
- Stable since: At minimum 2020 (H-V23_simple_2020 used a 4-photo grid cover — photo-dominant cover has been standard since then); the split-panel left-photo / right-text configuration solidified by 2026-01-23 (earliest B-chain)
- Observed in: B-105_N_13 all 7 versions (2026-01-23 → 2026-04-22); D-NPV-IOS all versions (2026-05 → 2026-06-09); Krios Everleaf cover (full-bleed background variant, 2026-04-24); F-3605-Church-Ave (compressed one-pager variant)

**D-07 — Off-canvas decorative left rail**
- Values: same 8-bar stack as D-02 (x=−1.23, w=1.02, h=0.69); present on cover AND content slides in B-series; present on content slides in advisory decks
- Note: Listed separately from D-02 to make explicit that this element appears on the cover slide (behind the split-panel photo) and on every content slide — it is a slide-master fixture, not a per-slide insertion. Its presence on the cover is confirmed in B-2026-04-22 geometry.

**D-08 — Contact page: named-card grid, Bell MT header**
- Values: "Contact" header in Bell MT 44pt on full-bleed dark rectangle; 4–5 named-card TextBoxes (name bold + title + mobile + email); V23 logo in standard header position; no headshot photos in D/B-system (B-105N13 contact page has one Muller headshot at x=0.98 y=3.04 w=1.65 h=1.82 — the only confirmed headshot instance)
- Stable since: 2024-05 (E-Pektor Word OMs: "STEPHEN MULLER / MANAGING PRINCIPAL / M: (516) 972-1699 / SMULLER@V23GROUP.COM" format invariant) through 2026-06 (D-NPV final: five V23 contacts only). Personnel update but format is invariant across this entire span.
- Observed in: B-105_N_13-2026-04-22 Slide 39; D-NPV-IOS-FINAL-0609 Slide 18; F-AlphaSquare Slide 7 (2026-05-11); F-OpenHouse Slide 9 (2026-05-11); E-Pektor Word OMs (2024-05 → 2025-03)

**D-09 — Two-slide Exec Summary (narrative + KPI)**
- Values: Slide A = narrative TextBox left panel (x=0.40 y=1.06 w=7.21 h=6.06, Garamond 13–14pt) + dual embedded tables right panel (TABLE 7×6 and TABLE 5×3 or 5×6 at x≈7.5–12.9). Slide B = location/market continuation. Condensed variant (platform decks): one slide with 2×2 named block grid.
- Stable since: 2026-01-23 (B-chain) through 2026-06-09 (D-NPV final). The exact implementation varies (two full slides vs. one condensed slide) but the ES always occupies at least the first non-cover, non-disclaimer slide as a distinct structured section.
- Observed in: B-105_N_13 all versions (2026-01 → 2026-04) — slides 3–4; D-NPV all versions (2026-05 → 2026-06) — condensed one-slide variant with 2×2 block grid; E-Pektor all versions (2024-05 → 2025-03) — slides 3–4

**D-10 — Investment Highlights: bold-label em-dash prose**
- Values: Single TextBox at x=0.41 y=1.04 w=12.52 h≈5.35; structure per bullet: **Bold thesis label** (Garamond bold, 3–5 words) + em-dash separator + plain evidence clause (13–15.8pt, 2 lines); 6–9 highlights per page; no boxes, icons, or bullets — purely typographic. Equity register leads with returns ("Compelling Financials"); debt register leads with coverage ("Existing Debt Service Coverage"); programmatic register leads with market signal ("Compelling Metrics").
- Stable since: 2024-06-19 (E13 Pektor Wind Gap OM) through 2026-06-09 (D-NPV final). Two years, multiple deals, multiple asset classes.
- Observed in: B-105_N_13-2026-04-22 Slide 5; E-WindGap-E48 (2025-03-10); E-WindGap-E43 (2025-02-18); D-NPV-IOS-FINAL-0609 Slide 3

**D-11 — Confidentiality/disclaimer slide (slide 2, full-width header + prose body)**
- Values: Rectangle at x=0.0 y=0.29 w=13.33 h=0.50 (navy fill) + header TextBox "Confidentiality & Conditions" (Garamond 20pt bold) + body TextBox at x=0.41 y=1.03 w=12.52 h=6.18 (full-slide prose). Always Slide 2 in pptx OMs; Pages 1–2 in Word OMs.
- Stable since: 2024-05 (E01 Pektor draft) through 2026-06 (D-NPV final)
- Observed in: B-105_N_13-2026-04-22 Slide 2; D-NPV-IOS-FINAL-0609 Slide 2; C-Obsidian_Krios_Full (2026-04-13) Slide 2; E-WindGap multiple versions (2024–2025)

**D-12 — 13.33" × 7.50" widescreen canvas**
- Values: slide width 13.33", height 7.50" (all V23-authored equity OMs)
- Stable since: H-V23_simple_2020 (2020-10-22) through D-NPV final (2026-06-09). This canvas is confirmed in every V23 pptx in the corpus without exception except the Krios V23-dark (10"×5.62") noted below.
- Observed in: B-105_N_13 all versions; F-3605-Church-Ave; D-NPV all versions; C-Krios-Everleaf (widescreen confirmed); H-V23_simple_2020; H-Obama_V23_2022; H-ELM_PitchBook_2022
- Exception: Krios V23-dark (C-01 → C-05, 2026-04-13 → 16) used 10"×5.62" — a deliberate Sandbrook-style departure, confirmed discarded (see Section 7).

---

## 2. Per-Deck Choices

The following elements vary legitimately by deal, audience, or register. Do not freeze them as rules; do not treat variation here as an error.

- **Color palette (non-navy):** The secondary blue (#C9D4E4, cited as candidate for sub-header band) is not confirmed via XML — only the navy #1F3A5F is directly cited in notes. Per-deck accent colors are a builder decision; do not invent fills without XML verification.
- **Exec Summary implementation:** Two full slides (equity OM) vs. one condensed 2×2 block slide (programmatic/platform deck). Both are valid; selection depends on deal register.
- **Metric vocabulary in tables:** Equity → IRR / EM / YoC / Net Profit. Debt → DSCR / Debt Yield / Leverage. Programmatic → platform metrics. The layout (D-09) is invariant; the column headers are not.
- **Number of Investment Highlights bullets:** 6–9 observed range. 7 is the most common. Cap at 9 before crowding at 13–14pt in the standard TextBox height (h≈5.35).
- **Section dividers:** Explicit numbered dividers (Krios-style: large Georgia number + section title on dark full-slide) appear in long decks (≥25 slides). B-chain (39 slides) uses implicit section transitions (header text change only, no divider slide). Either is correct; the choice depends on whether the deck has a discernible section architecture the reader needs signposted.
- **Source lines on content slides:** B-chain uses them only on market slides with external data (bottom of slide, Garamond 9pt italic). Krios-dark used them on every content slide (Calibri 8–8.5pt). Platform decks (D-NPV v0) used full per-slide citations, later compressed to footnote superscripts. Source-line density is a deal-specific choice; the format decision (footnote vs inline) follows the citation density needed.
- **Cover sponsor logo placement:** x≈10.74 y≈6.0 w=2.06 h=0.85 (bottom-right, B-chain). One-pagers omit sponsor logos. Platform decks may omit them entirely (V23 brand only). Builder strips sponsor logos from the template seed and inserts per-deal.
- **Contact personnel and headshots:** Personnel change per deal team. B-chain has one Muller headshot (x=0.98 y=3.04 w=1.65 h=1.82); NPV final has no headshots (five text-only cards). Headshot inclusion is a per-build decision.
- **Named KPI shapes (NPV-style):** KPI_Bg_N / KPI_Val_N / KPI_Lbl_N are the D-NPV convention; B-chain uses generic Rectangle/TextBox naming. New builds should adopt semantic naming (see Section 6, override list item 6), but this is a template convention, not a visual design element.
- **Eyebrow labels on tile slides:** "RECENT CLOSING / ACTIVE PIPELINE / REALIZED CASE STUDY" are NPV-specific status labels. Other decks use different or no eyebrows. The eyebrow is a per-register typographic element, not a durable DNA element.
- **Sub-header band below navy header:** Observed in some decks as a secondary lighter-blue strip. Color not confirmed via XML. Include only when the design requires a sub-section label below the primary header band.

---

## 3. Typography Table — As Observed

Fonts and sizes derived from pptx XML metadata (extracted by notes agents) and geometry inventories. Where decks disagree, the disagreement and date trajectory are shown explicitly. No values have been averaged or silently resolved.

| Element | Font | Size Range | Color | Weight | Source Decks + Dates |
|---|---|---|---|---|---|
| Slide header / section title | Garamond | 20pt | White (scheme:bg1, #FFFFFF) | Bold | B-105_N_13 all 7 versions (2026-01-23 → 2026-04-22); F-3605-Church-Ave (2026-05-27); F-AlphaSquare/Open-House content slides (2026-05-11) |
| Cover address (deal name) | Garamond | 44pt | White | Bold | B-105_N_13 all versions (2026-01-23 → 2026-04-22) — notes verbatim: "Garamond 44pt bold address" |
| Cover city/state | Garamond | 28pt | White | Italic | B-105_N_13 all versions — notes verbatim: "28pt italic" |
| Cover ask line | Garamond | 23pt | White | Bold | B-105_N_13 all versions — notes verbatim: "23pt bold ask line" |
| Cover subtitle lines | Garamond | 20pt | White | Regular | B-105_N_13 all versions — notes verbatim: "subtitle lines in 20pt" |
| Exec Summary body (left panel) | Garamond | 13–14pt | Dark (near-black) | Regular | B-105_N_13 all versions — notes verbatim: "13-14pt Garamond body"; D-NPV all versions (2026-05 → 2026-06) |
| Investment Highlights bullets | Garamond | 15.8pt | Dark | Regular (body) + Bold (label) | B-105_N_13 all versions — notes verbatim: "Garamond 15.8pt"; E-WindGap-E48 (2025-03-10) |
| General body prose | Garamond | 12–14pt | Dark | Regular | B-series (implied by 13-14pt body note); E-Pektor Word OMs (2024-05 → 2025-03, Garamond confirmed) |
| Contact page header ("Contact") | Bell MT | 44pt | White | Bold (inferred from display weight) | F-AlphaSquare Slide 7 (2026-05-11); F-OpenHouse (2026-05-11) — notes verbatim: "Bell MT 44pt 'Contact' header on full-bleed dark rectangle" |
| Word advisory memo body | Eras Light ITC | 10pt (address block); ~11pt (body) | Black | Light | H-Vanadium Memo Template.docx (2024-03-27); H-Letterhead Template.docx (2020-07-23) — confirmed via w:rFonts XML |
| Word legal/NDA body | Times New Roman | ~11–12pt | Black | Regular | H-NDA-2026.docx; H-Generic-NDA-Final.docx — confirmed: "footer font Times New Roman" |
| Word OM body (Pektor chain) | Garamond | ~12pt (inferred from PDF reads) | Black | Regular | E-Pektor all versions (2024-05 → 2025-03) — confirmed via PDF visual inspection in notes |
| Source / citation lines (B-series market slides) | Garamond or small sans — **unresolved** | ~9pt italic | Dark | Regular | B-105_N_13 market slides (2026-01 → 2026-04) — font class noted but font name not extracted from geometry files. **Confirmed unresolved: see note below.** |
| Source / citation lines (Krios dark) | Calibri | 8–8.5pt | #8FA3B1 (muted steel gray) | Regular | C-Obsidian_Krios_Full (2026-04-13) — notes verbatim: "8-8.5pt Calibri in #8FA3B1" |
| Krios V23-dark section headers | Georgia | 28pt | White | Regular | C-01 through C-05 (2026-04-13 → 2026-04-16) — notes verbatim: "Georgia 28pt" |
| Krios V23-dark body | Calibri | 11–14pt | #E8E8E8 | Regular | C-01 through C-05 (2026-04-13 → 2026-04-16) |
| Krios V23-dark KPI large number | Georgia | ~36–48pt (inferred) | White | Regular | C-Obsidian_Krios_Full — notes: "large Georgia number + Calibri descriptor below" |
| Krios V23-dark eyebrow / breadcrumb | Calibri | 8.5pt | #C9A84C (gold) | Bold | C-01 through C-05 (2026-04-13 → 2026-04-16) |
| Krios V23-dark bio title | Calibri | 10.5pt | #C9A84C (gold) | Italic | C-Obsidian_Krios_Full Slide 15 |
| NPV exec summary blocks (Block_Opportunity etc.) | Garamond | ~11–13pt (inferred) | Dark | Regular + Bold (labels) | D-NPV all versions (2026-05-26 → 2026-06-09) |

**Typography disagreements — explicit with date trajectory:**

1. **Georgia vs. Garamond for headers:** The Krios V23-dark format (C-01 → C-05, 2026-04-13 → 2026-04-16) uses Georgia for all primary display text. Every other 2026 V23 deck uses Garamond. The Krios dark format was replaced within 7 days by the Everleaf format, which itself uses a different system. Neither propagated back into house decks. Date trajectory: Georgia was a 3-day experiment, immediately abandoned. Resolution: Garamond is house standard; Georgia is not.

2. **Calibri vs. Garamond for source lines:** Krios-dark (C-slice) uses Calibri 8–8.5pt for source lines. **RESOLVED 2026-06-11 (template regeneration, per override list item 8):** run-level `rFonts` inspection of the seed deck (105_N_13 - OM - 2026-04-22.pptx) confirms source lines are **Garamond, 11–12pt** (slide 15 "Source: Colliers, Brooklyn Office Market, Q4 2025" = Garamond 11pt; slide 28 "Source: CoStar" = Garamond 12pt). Calibri source lines existed only in the discarded Krios-dark experiment. New builds: Garamond 11pt for source lines.

3. **Bell MT (contact page) vs. Garamond (content slides):** Both appear in the same deck families. The contact page uses Bell MT for the single "Contact" display header; all other content slides use Garamond. This is a deliberate single-element departure for display weight on one specific page, not a system-level conflict.

---

## 4. Word-Document Design Register

### Letterhead / Logo / Address Block

V23 word documents operate in three distinct registers, each with a deliberate font assignment. These are not inconsistencies — they are register markers.

**Advisory-memo register (Eras Light ITC):**
- Font: Eras Light ITC throughout — body, headers, footer. Confirmed via w:rFonts XML ("Every w:rFonts specifies w:ascii='Eras Light ITC'"). Envelope Template uses Eras Medium ITC (slightly bolder weight variant).
- Header: centered Vanadium logo image + two centered paragraphs (909 Third Avenue #1253, New York, NY 10150) in Eras Light ITC 10pt
- Page size: US Letter (12240×15840 DXA); margins: 1" all sides (memo) / 0.5" top (letterhead)
- Body: Eras Light ITC uniform weight — no heading/body font distinction within the document
- Files: Vanadium Memo Template.docx (2024-03-27); Letterhead Template.docx (2020-07-23); Envelope Template.docx
- Era: 2020–present (still active)

**Legal/NDA register (Times New Roman):**
- Font: Times New Roman body — standard legal document convention, confirmed: "footer font Times New Roman"
- Entity name in this register: "Vanadium Realty LLC ('V23')" — legal entity name, not "Vanadium Group"
- Footer: "Page X of 4" (page-number field); US Letter, 1" margins
- Files: NDA-2026.docx; Generic-NDA-Final.docx; Investor NDA
- Era: 2020–present (still active)

**Garamond deck register (pptx OMs):**
- Font: Garamond throughout (headers 20pt bold, body 13–15.8pt) — see Sections 3 and 1/D-04/D-05
- This register governs investor decks (pptx). Eras Light ITC has not been observed in any 2026 pptx deck.
- The Eras-era is the Word-document / correspondence register; Garamond replaced it for the deck era but Eras persists in the document/letterhead layer.
- Inference (flagged as inference, not confirmed fact): Eras Light ITC was the pre-pptx V23 house font; Garamond supplanted it for the deck format while Eras persists in the legacy correspondence layer.

### Register-Based Font Switching — Summary Table

| Register | Font | Era | Confirmed Files |
|---|---|---|---|
| Word advisory memo (letterhead, site memo, envelope) | Eras Light ITC | 2020–present | Vanadium Memo Template.docx; Letterhead Template.docx; Envelope Template.docx |
| Word legal (NDA, engagement agreement) | Times New Roman | 2020–present | NDA-2026.docx; Generic-NDA-Final.docx |
| Word OM body text (Pektor chain) | Garamond | 2024–2025 | Wind Gap OM all versions; Palmer MF OM |
| pptx OM header (content slides) | Garamond 20pt bold | 2026 | B-series; F-series; D-series |
| pptx OM body (content slides) | Garamond 13–15.8pt | 2026 | B-series; F-series; D-series |
| pptx contact page header only | Bell MT 44pt | 2026 | F-AlphaSquare; F-OpenHouse |
| pptx Krios V23-dark format | Georgia (headers) / Calibri (body) | 2026-04-13 → 16 only | C-01 through C-05 (discarded) |

---

## 5. Footer + Source-Line Conventions

### Standard pptx footer treatment (confirmed durable)

- **V23 logo at upper-right, x=12.69 y=0.36 w=0.24 h=0.35**: permanent position on all pptx content slides in the Garamond system. Confirmed across B-series, D-series, F-series (2026). This is the durable footer identity element.
- **No slide page numbers in any pptx OM**: V23 pptx decks do not carry visible slide page numbers. Confirmed by geometry — no field elements found in any pptx inventory across the corpus.
- **No running footer text band on pptx slides**: unlike Word OMs, pptx slides do not carry a bottom text footer. The logo at upper-right is the only persistent footer-zone element.

### Word OM running header (confirmed durable, Word register only)

- Interior pages carry a running location header: "WIND GAP, PENNSYLVANIA" (2025 caps) / "W I N D G A P, P E N N S Y L V A N I A" (spaced-caps 2024 variant, now retired). This is a Word-OM convention only; it does not translate to pptx.
- The spaced-caps variant was used in 2024 PDF releases and replaced by normal caps by March 2025. The spaced-caps treatment was an over-styling, corrected — do not reintroduce it.

### Source-line formats by format family

| Format | Source-line treatment | Font / Size | Position | Source |
|---|---|---|---|---|
| B-series pptx (B-105_N_13) | Appears only on market slides with external data; not on all slides | Garamond ~9pt italic (font unconfirmed — see unresolved flag in Section 3) | y≈6.35–7.07, bottom of slide | B-105_N_13-2026-04-22 market slides |
| D-NPV v0 (2026-05-26) | Full per-slide source lines with full citations | Small (size unconfirmed) | Bottom of each slide | D-NPV-IOS-v0-0526 |
| D-NPV 06-01 and final (2026-06-09) | Footnote superscripts only on exec summary stat box: "(1) Newmark, 2025 \| (2) pipeline note" | Small | Stat box footnote zone | D-NPV-IOS-OM-FINAL-0609 Slide 2 |
| C-Krios-dark (2026-04-13) | Short callouts on every content slide: "Source: Ember, ICIS, Goldman Sachs" | Calibri 8–8.5pt #8FA3B1 | Bottom 0.2" of each slide (y≈4.86–5.05 on 5.62" canvas) | C-Obsidian_Krios_Full |
| C-Krios-Everleaf (2026-04-24) | Long formal source lines with edition/quarter dates: "Sources: JLL EMEA Data Center Report YE 2025; CBRE European Data Centers Q3 2025; Cushman & Wakefield EMEA H2 2025; Newmark 2025. Figures estimated as of April 2026." | Small | Bottom of relevant slides | C-Ever_Leaf_vF |
| E-Pektor Word OMs | No inline footnotes; CoStar named inline; no footnote system | — | Inline | E-Pektor all versions 2024–2025 |

**Direction of source-line evolution:** D-NPV v0 had verbose per-slide source lines; D-NPV final compressed them to stat-box footnotes only. Krios Everleaf used formal long-form; Krios-dark used short callouts. The compression direction (verbose → footnote) is consistent across the two families that evolved across versions. This is directional but not yet durable (one deal family).

### "Vanadium Realty LLC | [deal name]" PDF footer — emerging convention

- **First observed:** D-NPV-final.pdf (2026-06-10) — "Vanadium Realty LLC | North Park Ventures Florida IOS Strategy" on every page of the PDF export.
- **Evidence for treating as an evolution, not a one-off:** (1) It appears on the final/sent version, not a draft. (2) It reflects the "Vanadium Realty LLC" naming convention that replaced "Vanadium Group" across templates starting 2025 (NDA-2026 uses "Vanadium Realty LLC ('V23')"; the 2024 Wind Gap OM still had "VANADIUM GROUP" on the cover; by 2025 the cover dropped the firm name in favor of location identifiers). (3) The agent-and-deal-name format mirrors the Word-OM running-header convention ("WIND GAP, PENNSYLVANIA" header) translated to a pptx PDF footer.
- **Status:** Emerging convention — single confirmed pptx instance. Does not yet meet the ≥3 materials durability bar. Do not treat as invariant, but do not omit from new builds without reason.
- **Decision for new builds:** Include the "Vanadium Realty LLC | [Deal Name]" PDF footer on final PDF exports. Reason: it is the only confirmed instance in the corpus, it is from the most recent final/sent deck (2026-06-10), it aligns with a naming-convention shift that is durable across other document types, and the format is functionally sensible (identifies issuer + deal on every page). Mark it as emerging in any audit trail — but build with it.

---

## 6. Template Seed

### Recommended seed: 105_N_13 - OM - 2026-04-22.pptx

**Stability justification (evidence-based, not recency-based):**

This deck is the terminal version of a 7-version chain spanning 2026-01-23 through 2026-04-22 — three months of iteration converging on a fully stable state. Its master layout (slideLayout7.xml / Blank) and template geometry show zero template drift across 40+ slides and 15+ months of production use. It embodies all 12 durable DNA elements (D-01 through D-12): navy header band at exact coordinates, 8-bar accent stack at exact x=−1.23 y-positions, logo at x=12.69 y=0.36, Garamond system throughout, 13.33×7.50 canvas, split-panel cover, two-slide exec summary, Investment Highlights bold-label structure, confidentiality slide, contact page.

The chain includes both equity and debt OM variants on the same master — proving the master is register-agnostic and can support different metric vocabularies (IRR/EM/YoC vs. DSCR/Debt Yield/Leverage) without structural changes. The D-NPV final (2026-06-09) introduced semantic named shapes (KPI_Bg_N, Block_Opportunity, etc.) that are valuable additions, but the NPV deck is built on the B-series master — it is not a departure. The correct path is to use the B-series seed and overlay the NPV named-shape vocabulary.

**Override list — strip deal content and prepare template:**

1. Replace all deal-specific text on content slides (addresses, metrics, sponsor bios, market data, tenant names) with [PLACEHOLDER] tokens. Do not leave live deal data in the template.

2. Replace the cover photo (left-half full-bleed image, x=0.0 y=0.0 w=6.83 h=7.5) with a placeholder picture frame. Label it [COVER_PHOTO_PLACEHOLDER].

3. Remove sponsor logo(s) at x≈10.74 y≈6.0 from cover slide. Retain V23 logo at x=12.69 y=0.36. Replace sponsor logo zone with [SPONSOR_LOGO_PLACEHOLDER].

4. Reset returns tables (TABLE 7×6, TABLE 5×3, TABLE 5×6 on Exec Summary slide) to empty tables with correct column structure and placeholder headers. Do not leave live financial figures in the template.

5. Replace confidentiality body text on Slide 2 with the canonical text from H-Confidential-Disclaimers-Template.docx, "Presentation Confidential Short" variant. This is the correct confidentiality language for new builds.

6. Add NPV-style semantic shape names to blank content slides: KPI_Bg_1 / KPI_Val_1 / KPI_Lbl_1 (and _2 through _5 for the standard 3–5-box strip); Block_Opportunity / Block_Strategy / Block_Pipeline / Block_Ask (for platform exec summary); Section_Header; Takeaway; Source. The B-series uses generic "Rectangle N" / "TextBox N" naming. Semantic naming enables programmatic editing and should be the standard for all new template builds going forward.

7. Confirm Bell MT is retained as the contact-page "Contact" header font. The corpus evidence (F-AlphaSquare 2026-05-11; F-OpenHouse 2026-05-11) supports Bell MT as the durable contact-page display font. Do not standardize to Garamond for this element; the Bell MT departure is intentional.

8. **Verify and confirm source-line font from pptx XML: DONE 2026-06-11.** Run-level font inspection of the seed deck confirmed source lines are **Garamond 11–12pt** (slide 15: Garamond 11pt; slide 28: Garamond 12pt). Section 3 disagreement #2 is resolved. New builds use Garamond 11pt for source lines. Re-verify only if the seed deck changes.

9. Confirm Garamond (all weights: Regular, Bold, Italic, Bold Italic) and Bell MT are embedded in the template .pptx. Check via File → Info → Inspect Document → Embedded Fonts, or by inspecting ppt/fonts/ in the pptx zip. If either font is missing or not embedded, embed it before publishing the template.

10. Add "Vanadium Realty LLC | [DEAL_NAME_PLACEHOLDER]" as the PDF export footer per Section 5 (emerging convention, single confirmed instance, evidence-based inclusion).

---

## 7. Discarded

Elements that appeared in the corpus and were abandoned, or that were never observed despite appearing in prior repertoire documentation. One-line reasons.

| Item | Source | Reason discarded |
|---|---|---|
| Krios V23-dark format (#0D1B2A background, Georgia/Calibri, 10"×5.62" canvas) | C-01 through C-05 (2026-04-13 → 2026-04-16) | 7-day experiment adapted from Sandbrook Capital's style guide for the Krios co-invest European audience; replaced within days by Everleaf format and never propagated into any V23 house deck; confirmed not V23 DNA |
| Georgia font for headers | C-Krios-dark (2026-04-13 → 16) | Sandbrook-style audience match only; all other 2026 V23 decks use Garamond; 3-day use span |
| Calibri font for body text | C-Krios-dark (2026-04-13 → 16) | Same as Georgia — co-invest format experiment; not house standard |
| "Vanadium Group" on OM cover | E-WindGap E35 (July 2024) | Replaced by location-identifier cover by March 2025 (E49); naming convention shifted to "Vanadium Realty LLC" by 2025–2026 |
| Spaced-caps location header ("W I N D G A P, P E N N S Y L V A N I A") in Word OM PDF | E-WindGap 2024 PDF releases | Replaced by normal caps by March 2025; aesthetic over-styling, corrected |
| "INVESTMENT MEMORANDUM" cover header on Word OMs | E13 (2024-06-19) | Present in mid-chain Word doc; absent from later PDF releases; replaced by location name / deal type header |
| V23 Simple Presentation 2020 master (title at x=0.62 y=0.40, large logo at x=12.21 y=6.26 w=1.12 h=1.24) | H-V23_simple_2020 (2020-10-22); H-Obama_V23_2022 (2022-04-11) | Replaced by Garamond/header-band master by 2026; no header band, no off-canvas accent bars, larger logo — fully superseded |
| Blended-IRR headline on exec summary stat box ("27.0% / BLENDED GROSS IRR") | D-NPV-IOS v0 (2026-05-26) | Explicitly prohibited in NPV Blueprint as a "portfolio-era regression"; removed in 06-01 and final versions |
| "DEAL 1 OF 4" deal labels | D-NPV-IOS v0 (2026-05-26) | Replaced by "CASE STUDY" tile format with status eyebrows in 06-01 and final; the numbered label format was a v0 artifact |
| L17 Stacking plan | layout-repertoire.md (prior) | No stacking-plan geometry observed in any 2024–2026 V23 deck; theoretical entry |
| L19 Comparable sales scatter plot | layout-repertoire.md (prior) | All observed comp-sales slides use map + table; no scatter-plot geometry found |
| L20 Unit-mix split (floor plan + mix table columns) | layout-repertoire.md (prior) | No geometry found; Palmer MF is Word-doc format only; no floor-plan slides in corpus |
| L21 Submarket cycle quadrant | layout-repertoire.md (prior) | No observed example across any deck in the corpus; theoretical |
| L16 Lease rollover cliff chart (WALT visualization) | layout-repertoire.md (prior) | Only lineCharts found on market slides; no cliff-chart geometry; may exist in net-lease deals outside this corpus but not observed here |
| L18 Twin-pillar bar Sources & Uses visualization | layout-repertoire.md (prior) | Capital stack is invariably a TABLE in observed decks (embedded in exec summary right panel); no visual twin-pillar bar geometry found |
| KPI strip description with #E8EEF6 fill + Aptos navy + Arial labels | layout-repertoire.md (prior, L2) | Description uses unconfirmed colors and fonts; Aptos not observed in any V23 deck; replace with observed named-box geometry (KPI_Bg_N / KPI_Val_N / KPI_Lbl_N, confirmed from D-NPV-IOS-FINAL-0609) |
| Disclosures slide (D-NPV v0) | D-NPV-IOS v0 (2026-05-26) | NPV Blueprint marks it conditional: include only if sponsor provides responses; absent from 06-01 and final versions; do not include in template by default |
