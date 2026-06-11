# Registers & Coverage
<!-- Derived from: om-pattern-study-2026-06 synthesis/registers.md (generated 2026-06-11) -->
<!-- Regeneration pointer: docs/superpowers/plans/2026-06-11-om-builder-v6.md -->

---

## 1. Register Taxonomy

Ten registers are observed. Each entry: purpose, audience, observed length range, structural spine (ordered as observed), evidence citations. Thin-evidence registers are flagged.

---

### R1 — Full-Deck OM, Equity (JV / Common)

**Purpose:** LP and JV equity raise for a single asset or programmatic portfolio.
**Audience:** LP investors, JV equity partners, family offices.
**Observed length:** 18–46 slides (NPV final = 18; 105 N 13 final = 39; Krios full OM = 27–46).

**Structural spine (as observed across 105 N 13 / NPV / Krios dark):**
1. Cover — address + deal type + ask on right half; full-bleed photo left
2. Disclaimer — 1–2 pp dense legal block
3. Executive Summary — left narrative paragraph + right dual table (Sources/Uses + Returns KPIs)
4. Investment Highlights — bold-label em-dash prose body; no bullets; no periods at end of entries
5. Asset Overview / Asset Location
6. Project Background / Leasing Activity
7. Market Overview (metro)
8. Submarket Overview — named comps, CAGR, institutional ownership
9. Rent Roll & Comparables
10. Land Sale Comparables (dev deals only)
11. Exit / Sale Comparables
12. Budget
13. Financial Analysis — IRR sensitivity matrix / waterfall
14. Sponsor Background
15. Contact

NPV IOS final (18 slides) compresses this spine into platform-first format: platform thesis slides precede deal tiles; realized case study is a standalone slide; deal tiles are paired IRR+EM lines. Spine logic (exec summary → highlights → market → sponsor → contact) is preserved. Krios V23 dark-format adds numbered section-divider slides but retains same flow.

**Evidence:** B-105n13.md (all versions 2026-01-23 to 2026-04-22); D-npv.md (v0 through final 2026-05-26 to 2026-06-09); C-krios.md (Obsidian_Krios_Full_April2026, 2026-04-13).
**Strength:** Strong — ≥3 deals, multiple versions each.

---

### R2 — Full-Deck OM, Debt (Bridge Loan)

**Purpose:** Bridge loan sourcing for a single asset; lender-facing.
**Audience:** Bridge lenders, debt funds.
**Observed length:** 39 slides (single instance).

**Structural spine:** Identical to R1 except:
- Cover ask line reads "$30 Million Bridge Loan"
- Exec Summary "Project-Level Returns" box → "Debt Returns" box: Leverage / Debt Yield / DSCR at Origination (3 rows)
- Investment Highlights lead bullet: "Existing Debt Service Coverage" (vs. "Compelling Financials" in equity OM)
- No IRR/EM table; no waterfall
- All property, market, and sponsor sections identical to co-dated equity OM

**Evidence:** B-105n13.md vDebt section; VERIFIED against 105_N_13 - OM - 2026-03-02 - vDebt.pptx (Slide 3: "Debt Returns / Leverage 60.00% / Debt Yield 8.62% / DSCR at Origination 1.23x"; Slide 5 Investment Highlights draft placeholder for stabilized DSCR).
**Strength:** SINGLE-INSTANCE EVIDENCE — one deal, one date (2026-03-02). Pattern is clear but not corroborated by a second deal. Confirm against deal needs at blueprint time.

---

### R3 — Word-Doc OM, Pref Equity

**Purpose:** Preferred equity raise for a development deal; lender-investor facing.
**Audience:** Pref equity investors, family offices, HNW.
**Observed length:** 28–29 pages (Word/PDF).

**Structural spine (Pektor Wind Gap, confirmed across 2024–2025):**
1. Cover — INVESTMENT MEMORANDUM / geographic header / capital type subtitle / ask
2. Disclaimer — 2 pp verbatim block
3. Table of Contents — 19 sections
4. Executive Summary — retained-by sentence + S&U table + return metrics paragraph + market thesis paragraph + sponsor narrative
5. Investment Highlights — bold-label em-dash prose (same convention as R1)
6. Asset Overview
7. Asset Location
8. Project Background
9. Approvals / Zoning
10. Lease Abstract — BTS Tenant
11. Market Overview
12. Submarket Overview — named comps + institutional ownership list
13. Rent Roll & Comparables
14. Land Sale Comparables
15. Exit / Sale Comparables
16. Budget
17. Financial Analysis — pref-specific rent-hurdle sensitivity table; NOT project-level IRR matrix
18. Sponsor Background
19. Contact Information

MF version (Palmer) adapts: "Site Overview" replaces "Asset Overview"; "Potential for Additional Development" added; "Leasing Comparables — Case Studies" added between rent roll and land comps. Spine integrity (disclaimer → ToC → ES → Highlights → … → Sponsor → Contact) is invariant.

**Evidence:** E-pektor.md Obs 1–2 (ToC verified E43 2025-02-18 / E48 2025-03-10 / E13 2024-06-19); VERIFIED against Wind Gap Industrial Park - OM - Pref - 2025-03-10.docx.
**Strength:** Strong — ≥3 versions, 2 deals (Wind Gap 2024–2025, Palmer MF 2025).

---

### R4 — Word-Doc OM, JV Equity

**Purpose:** JV/common equity raise for a development deal.
**Audience:** JV equity partners.
**Observed length:** 28 pages.

**Structural spine:** Identical to R3 in every section. Changes by register:
- Cover subtitle: "JOINT VENTURE EQUITY INVESTMENT" (vs. "PREFERRED EQUITY INVESTMENT")
- Disclaimer: "providing common or preferred equity financing" (vs. "providing preferred equity financing")
- Exec Summary return paragraph leads with levered project IRR + EMx + YoC + dev spread (not pref yield)
- Financial Analysis: project-level IRR sensitivity matrix (rows = spec rent; columns = exit cap) replaces pref-tier rent-hurdle table
- Rent-hurdle figure also appears in JV OM as downside-protection device — present in both R3 and R4; the key distinction is that the JV rent hurdle protects all equity, not a pref tranche specifically

**Evidence:** E-pektor.md Obs 3–5; VERIFIED against Wind Gap Industrial Park - OM - JV - 2025-02-10.docx (">29% unlevered IRR / 43% levered IRR / 2.26x EM / 7.55% YoC / dev spread 205 bps") and cross-compared with Pref final.
**Strength:** Adequate — 2 versions (Wind Gap JV 2025-02-10 and 2025-03-24), 1 deal.

---

### R5 — Teaser / 1-Pager

**Purpose:** Initial deal introduction; prompt for a meeting or data-room request.
**Audience:** Cold or semi-warm LP/investor contacts; HNW networks.
**Observed length:** 2–17 slides or 2–3 pages.

Two subtypes:

**R5a — Single-deal 1-pager (2–3 slides/pages):** Full-width header band (address + price/ask); sub-header band (deal type); two-column body (prose exec summary + key-value "AT A GLANCE" table + photos/floor plan); contact strip at bottom. Named shape "AtAGlanceTable" in pptx confirms template status. Examples: Tarpon Springs 1-pager (D-npv.md); 3605 Church Ave (F-small-folders.md).

**R5b — Co-invest / institutional teaser (17 slides; Krios vTeaser):** Cover → Opportunity → Model → Precedent → Team (compressed 3 bios) → Platform → Market → Obsidian's Role → Investment Terms → WHY THIS FITS → urgency coda ("The allocation is finite. / The timing is now."). Financial disclosure section absent. Lead is founder-credential or problem-solution, not market data. WHY THIS FITS slide is single-instance within the teaser subtype — thin evidence for that specific slide.

**Evidence:** D-npv.md (Tarpon 1-pager 2026-02-25); F-small-folders.md (3605 Church Ave 2026-05-27); C-krios.md (Krios_vTeaser 2026-04-23).
**Strength:** Adequate — ≥3 instances, 2 subtypes.

---

### R6 — Co-Investment Abbreviated Pitch

**Purpose:** Introduce a co-investment opportunity to a specific anchor LP; prompt pari-passu participation.
**Audience:** HNW families, family offices, named co-investors.
**Observed length:** 11 slides.

**Structural spine (Krios CoInvest, 2026-04-08):** Cover ("Investing Alongside the Founders of Cloverleaf") → The Opportunity (market + model on one slide) → [deal pages] → Capital structure diagram (stacked boxes, "All investors: pari passu") → Investment Terms. No risk section. No separate market section. Omits proof-point, case study, and WHY THIS FITS slides. Leads with access narrative rather than market thesis.

**Evidence:** C-krios.md, Obsidian_Krios_CoInvestment_April2026 (2026-04-08), Slide 8 capital structure diagram.
**Strength:** SINGLE-INSTANCE EVIDENCE — one file, one deal. Confirm against deal needs at blueprint time.

---

### R7 — Platform Deck / GP Formation Deck

**Purpose:** Present investment platform thesis to institutional LPs or co-sponsors; GP formation / investor recruitment, not a single-deal raise.
**Audience:** Institutional LPs, family offices, co-sponsors, advisory boards.
**Observed length:** 15–77 slides (contracted to 27–30 in final form).

**Structural spine (Obsidian VHC2 final, 2026-05-07):**
1. Cover — platform name / "Platform Overview" subtitle
2. Disclaimer — multi-column legal block
3. Platform Thesis — two-slide sandwich: who we are + three-column THE PLATFORM / THE PLAYBOOK / THE EDGE
4. Comparative Advantage sections — one per advantage; no deal-level returns at portfolio level
5. Sourcing & Portfolio
6. Execution Mode sections (Direct Development / Co-Investment / Value-Add)
7. Market Appendix
8. Contact

No "Investment Terms" section. No LP waterfall. No fund IRR target for the platform. Single-deal reference returns appear only on the co-invest deal slide ("2.75× MOIC / 34.5% IRR"). This is a GP formation register, not an LP offering memorandum. NEVER carry blended aggregate IRR in a platform deck stat box — see §2 Conventions.

**Evidence:** A-obsidian.md (VHC2 2026-05-07 section structure; absent "Investment Terms"; reference returns only on co-invest slide; chain evolution from 9→73→30 slides 2025-11-03 to 2026-05-07).
**Strength:** Adequate — 1 client (Obsidian), multiple versions. Register confirmed; single-client evidence.

---

### R8 — GTM / Strategy Deck

**Purpose:** Operational roadmap; competitive positioning; internal or near-external strategy alignment.
**Audience:** Principals, key advisors, prospective operating partners.
**Observed length:** 15 slides.

**Structural spine (Obsidian GTM v2, 2026-03-27):** Cover KPIs (36 months / 3–5 sites / 200–600 MW / $200M–$1B+ exit target) → Regulatory window thesis → Phase timeline (Q2 2026–2029) → Competitive matrix (named competitors with threat ratings: DIRECT THREAT / HIGH / MEDIUM) → Target profile → Exit thesis. Named competitors appear ONLY in this register — never in platform deck or LP materials.

**Evidence:** A-obsidian.md, Obsidian_BESS_Powered_Land_GTM v2.pptx (2026-03-27), competitive matrix with Cloverleaf/Diode/Hecate/Calibrant.
**Strength:** SINGLE-INSTANCE EVIDENCE — one client. Confirm against deal needs at blueprint time.

---

### R9 — Internal Deal Screen / Investment Analysis Memo

**Purpose:** Internal go/no-go vetting before committing V23 capital or placement capacity to a deal.
**Audience:** V23 principals only.
**Observed length:** 1–5 pages (Word).

**Structural spine (confirmed across ≥6 instances):**
1. Deal at a Glance — 7–12 row key-value table (Site / Sponsor / Program / Total Project Cost / Equity Ask / Levered IRR / Exit Assumption / Status)
2. Deal Structure / Thesis
3. Sponsor Background — explicit verification status; names track-record gaps directly
4. Return Profile / Financial Review — model delta vs. sponsor-presented numbers flagged as active red flag
5. Risk Factors — named risks with one-sentence verdict + downside $ impact quantified
6. SWOT or Stress Test
7. Bottom Line / Recommendation — one-line verdict; attractiveness rating X/10

Voice markers exclusive to this register: "Translation:" device (renaming what sponsor claim actually means); "Internal Work Product" disclaimer; attractiveness rating X/10; direct attribution ("the sponsor told us").

**Evidence:** G-word-memos.md: Blue Harbor JAX (2026-05-17), The Crossing at Santa Fe (2026-05-05), View on Detroit East (2026-04-22), NPV IOS (2026-03-27), 1224 W Randolph (2026-04-03), Solana (2026-03-18).
**Strength:** Strong — ≥6 deals, 2024–2026, multiple asset classes.

---

### R10 — LP Outreach Memo (Email Format)

**Purpose:** Warm-introduction memo sent to a named LP contact for a specific deal; prompt for a call.
**Audience:** Specific named LP (family office, fund, HNW individual).
**Observed length:** 1–3 pages (Word; sent inline in email or as attachment).

**Structure:** First-name salutation → one-sentence context → 4–5 KPI headline bar (Purchase Price / Equity Raise / Projected IRR / Equity Multiple) → Market Overview (brief) → Property → Sponsor → Key Deal Points (numbered bullet list of advantages). No detailed financial analysis. No risk section. Written entirely in sponsor's voice ("Our client has submitted a Letter of Intent").

**Evidence:** G-word-memos.md: Varsity Properties LP Investor Memo (2026-04-03); Piedmont Triad LP Outreach Memo (2026-05-19); IU Bloomington Chickering Memos (2026-02-12 / 2026-02-18).
**Strength:** Adequate — ≥3 deals.

---

### Register Summary Table

| ID | Register | Format | Length | Evidence |
|----|----------|--------|--------|----------|
| R1 | Full Deck OM — Equity | PPTX | 18–46 sl | Strong (≥3 deals) |
| R2 | Full Deck OM — Debt | PPTX | 39 sl | THIN (1 deal, 1 date) |
| R3 | Word OM — Pref Equity | Word/PDF | 28–29 pp | Strong (≥3 versions, 2 deals) |
| R4 | Word OM — JV Equity | Word/PDF | 28 pp | Adequate (2 versions, 1 deal) |
| R5 | Teaser / 1-Pager | PPTX/PDF | 2–17 sl | Adequate (≥3 instances, 2 subtypes) |
| R6 | Co-Invest Abbreviated Pitch | PPTX | 11 sl | THIN (1 file, 1 deal) |
| R7 | Platform / GP Formation Deck | PPTX | 15–77 sl | Adequate (1 client, many versions) |
| R8 | GTM / Strategy Deck | PPTX | 15 sl | THIN (1 client) |
| R9 | Internal Deal Screen Memo | Word | 1–5 pp | Strong (≥6 deals, 2024–2026) |
| R10 | LP Outreach Memo (email) | Word | 1–3 pp | Adequate (≥3 deals) |

---

## 2. Capital-Type Metric Checklists

### 2A — Equity (Levered / JV / Common)

Registers: R1 (deck OMs), R4 (Word JV OM), R7 (platform deck — single-deal reference only).

| Metric | Where observed | Notes |
|--------|---------------|-------|
| Levered IRR (two decimals) | R1 Exec Summary returns table (105 N 13 final: 24.06%); R4 (Wind Gap JV: 37.9%–43.6%); D-slice stat box (20%+ target per deal) | Lead return metric in all equity registers |
| Unlevered IRR (two decimals) | R1 (13.39%); R4 (>29%) | Second in the returns table |
| Equity Multiple, Levered | R1 (2.02x); R4 (2.26x–2.29x); D-slice tiles ("24.99% IRR / 2.31x EM") | Written "X.XXx" — lowercase x, no space |
| Equity Multiple, Unlevered | R1 (1.74x); R4 (1.56x) | Full returns table; omitted from tile/summary format |
| Yield-on-Cost (untrended) | R1 (8.19%); R3/R4 (6.88% / 7.55%); D-slice Skyway ("9.47% PROJ. YIELD ON COST") | Label as "untrended" or "trended" explicitly |
| Development Spread (bps) | R3/R4 (138 bps Pref / 204–205 bps JV, same deal); whole-number bps always | Value-add context: YoC vs. going-in or exit cap spread as appropriate — see adaptation note below |
| Net Profit ($mm) | R1 (105 N 13: "$35.5 million net profit") | Deck body narrative; not a standalone KPI box |
| Stabilized NOI | R1 body (105 N 13: "$4.1mm / Yr 2"); R3/R4 budget and financial analysis sections | Not a headline KPI |
| Exit Value / Exit Cap Rate | R1 ($66.7mm at 6.5% cap, Yr 5 for 105 N 13); R3/R4 exit comps section | Cap rate always stated alongside exit value |
| Basis ($/SF or $/AC) | R1 ($613/GSF entry, $694/GSF TPC, $958/GSF exit); R5 "AT A GLANCE"; R3/R4 ($141/SF pref basis) | Per GSF in urban deals; per AC in land/dev deals |
| Discount to Replacement Cost | R1 ("~31% discount to development cost"); R3/R4 ("70% of terminal value") | Entry risk anchor; phrasing differs by register |
| Capital Stack (% and $/SF) | R1/R2 identical table (LP 36% / GP 4% / Debt 60%); R3/R4 Word OM S&U table | Always dollar-per-SF normalized |

**Per-deal tile format (R1 NPV final):** Metrics compressed to "XX.XX% IRR / X.XXx EM" on a single line. YoC and CoC appear only in body text of live-deal tiles or on the Realized Case Study slide (4–5 KPI boxes).

**Per-register adaptation note — dev spread benchmark:**
- Ground-up dev deals (R3/R4): dev spread = YoC vs. prevailing unlevered exit cap rate (NPV / Wind Gap: 138–205 bps YoC-to-exit-cap spread, 2025–2026).
- Value-add deals (R1, where applicable): dev spread expressed as YoC vs. going-in cap or standalone exit cap spread, whichever the corpus shows — NPV IOS 2026 example: 150 bps YoC-to-standalone-exit-cap spread. State which comparison is being made explicitly in the financial analysis section.

---

### 2B — Debt (Bridge Loan / Construction Loan)

SINGLE-INSTANCE EVIDENCE — one deal (105 N 13, 2026-03-02), one instance. Cross-corroborated in R9 internal screens where DSCR and debt yield appear as screening inputs. No second lender-facing deck OM exists in the corpus.

**REQUIRED metrics — MANDATORY (the single observed debt OM left the last two as draft placeholders; this checklist makes them mandatory so that gap never ships again):**

| Metric | Value (105 N 13) | Status in source | REQUIRED? |
|--------|----------------|-----------------|-----------|
| Leverage / LTV | 60.00% | VERIFIED, Slide 3 | REQUIRED |
| Debt Yield | 8.62% | VERIFIED, Slide 3 | REQUIRED |
| DSCR at Origination | 1.23x | VERIFIED, Slide 3 | REQUIRED |
| **Stabilized DSCR** | placeholder in source ("xxxxx after x months") | DRAFT HOLE in corpus | **REQUIRED — must be filled before ship; never send as placeholder** |
| **Stabilization Period (months)** | placeholder in source ("******* months") | DRAFT HOLE in corpus | **REQUIRED — must be filled before ship; never send as placeholder** |
| Total Loan ($) | $30,208,914 | VERIFIED, Cover + S&U | REQUIRED |
| Total Loan ($/GSF) | $416.85/GSF | VERIFIED, S&U | REQUIRED |

**Inference — items not observed but standard in institutional bridge-loan OMs:** interest reserve amount and months; LTC (loan-to-cost) vs. LTV; debt service constant; exit/payoff thesis (refi vs. sale proceeds); recourse/guaranty status; cash-flow waterfall showing debt service coverage. Their absence in the vDebt OM may reflect draft state, intentional scope, or a lighter-format bridge OM convention. Cannot distinguish from current evidence. Treat as items to confirm at blueprint time.

---

### 2C — Preferred Equity

Registers: R3 (Word OM — Pref); sometimes also present in R1 deck OMs when deal has pref component.

| Metric | Where observed | Notes |
|--------|---------------|-------|
| Pref Ask ($mm) | Cover + Exec Summary opening sentence ("$14.3mm preferred equity financing") | Lead ask metric |
| Pref Basis ($/SF) | Exec Summary return paragraph ("$141/SF") | Pref investor's cost basis per buildable SF |
| Pref Basis as % of Terminal Value | Exec Summary ("70% of terminal value") | Standard downside-framing anchor |
| Development Yield to the Pref | Exec Summary (">7.50% development yield to the preferred equity") | Equivalent of YoC for pref tier |
| Rent Hurdle — Full Principal Repayment | Exec Summary + Investment Highlights ("$3.25/SF" Pref final) | THE primary risk/downside device in the pref register |
| Rent Hurdle — Full Principal + Accrued Interest | Financial Analysis section only ("$5.91/SF" in 2024 version) | Appears in pref OM only |
| Rent Hurdle — Common Equity Catch-Up | Financial Analysis section only ("$7.59/SF" in 2024 version) | Shows buffer before common gets paid; frames pref as protective |
| Levered IRR (post-pref) | Exec Summary table (24.86%) | Lower than JV version (same deal) because reflects post-pref equity returns |
| EMx (post-pref) | Exec Summary table (1.76x) | |
| YoC (untrended) | Exec Summary (6.88%) | |
| Dev Spread (bps) | Exec Summary (138 bps pref vs. 204–205 bps JV, same project) | Spread lower in pref version because pref coupon drag increases effective debt service |

**Pref Financial Analysis section uses a three-tier rent-hurdle sensitivity table** (principal repayment / principal + interest / common catch-up) as the primary risk quantification device. Downside is expressed as "how low can rent go and still recover principal" — not an IRR sensitivity matrix. Distinctive pref-register pattern.

VERIFIED: Wind Gap Industrial Park - OM - Pref - 2025-03-10.docx: "the rent hurdle for the remaining spec building for full principal repayment to the equity is only $3.25/SF" and "24.86% levered IRR and 1.76x equity multiple over a 3-year hold, and 6.88% untrended yield on cost resulting in a development spread of 138 basis points."

---

### 2D — JV / GP (Full-Stack)

Registers: R4 (Word OM — JV), R1 (deck OM full returns table), R7 (platform deck — single-deal reference only).

| Metric | Where observed | Notes |
|--------|---------------|-------|
| Full Levered IRR | R4 (>43.6% first / ~38% final); R1 (24.06%); Krios Everleaf ("18–20% target net IRR") | Lead metric |
| EMx (Full Levered) | R4 (2.26x–2.29x); R1 (2.02x) | Second metric after IRR |
| YoC (untrended) | R4 (7.55%/7.54%); R3/R1 also | Consistent metric across pref/JV registers for same project |
| Dev Spread (bps) | R4 (204–205 bps); R3 (138 bps same project in pref version) | Higher in JV version — pref coupon drag removed |
| Unlevered IRR | R4 (>29%); R1 (13.39%); A-slice Hillwood (23.9%) | Present in every full-return disclosure |
| Unlevered EM | R1 (1.74x); A-slice Hillwood (1.98x) | Appears in full deck OM returns table |
| Promote / Waterfall economics | **NOT shown** in any outbound OM or platform deck in the corpus | Absent from all outbound materials; present only in JV Term Sheet (H-triage.md) as contractual terms |

**Note (H-triage.md JV Term Sheet):** V23's standard JV terms (39% ops cash flow to V23 / 61% to JV Partner; 34% of NAV to V23 at terminal event; Put Option at TCO; Developer Fee = 4.00% of hard + soft costs) are contractual terms — NOT shown in the outbound OM. The outbound OM shows only deal-level project returns, not V23's economics within the JV.

---

## 3. Risk-Framing by Register

**Blueprint-time decision rule: every OM must decide explicitly where the risk register lives (in-deck section, companion memo, or both) before drafting begins. Never silently omit. Document the decision in the blueprint.**

### Internal (R9 — Deal Screen Memos)

Style: Candid, named-verdict, first-person evaluation.

Patterns observed (G-word-memos.md, Blue Harbor JAX 2026-05-17, Crossing at Santa Fe 2026-05-05, View on Detroit East 2026-04-22):
- **Named-verdict risk headers:** Each risk labeled by type with verdict baked in: "Expense Ratio Compression Is the Biggest Bet" — label → specific quantification of downside impact → explicit verdict.
- **Track-record gap:** Named directly and without softening ("Blue Harbor has zero completed automated dry-stack marinas as a sponsor"; "This would be their largest single deal at $53.5M total cap").
- **Model delta flagging:** "The latest internal model is materially better than the marketing package — driven by higher leverage ($28M vs $25.6M debt), higher NOI, and a higher exit valuation. This delta demands scrutiny." Marked explicitly as red flag.
- **SWOT:** Compression device between stress test and recommendation.
- **"Translation:" device:** Converts sponsor claims to plain-language verdicts. Unique to this register.

### Investor-Facing Deck OMs (R1)

Style: Mitigant-paired; risks are named only where simultaneously being neutralized by a deal feature.

Three risk devices observed:
1. **Seller distress framing:** "After a combination of various missteps and prolonged delays" (vDebt / 105 N 13 equity OM, 2026-04-22) — distress named explicitly but immediately framed as the basis for the discount, converting risk into opportunity signal.
2. **Rent hurdle (pref register, R3):** Quantified rent threshold below which investor still recovers principal. "$3.25/SF" for full principal repayment (Pref OM final, VERIFIED). The only quantified downside metric in any investor-facing document in the corpus.
3. **Companion memo quarantine (B-slice pattern):** Risks that cannot be palatably narrated in the deck (office cycle risk, ICAP compliance requirement, valuation uncertainty) are placed in standalone analytical companion memos (Durability Memo, Industrial Usage Memo, Valuation/Comps Memo) that accompany but are separate from the deck. The alt-use underwriting band ($25–35/SF from the Durability Memo) does NOT appear in any deck version. Evidence: B-105n13.md (companion docs 2026-04).

### Platform Deck (R7)

One observed instance (Krios v5 / NPV VHC2 chain, A-obsidian.md) adds a dedicated "Risks & Mitigants" section in the ToC. The earlier Krios vTeaser (17 slides) and R6 co-invest (11 slides) carry no risk section at all. Pattern: risk disclosure escalates with audience formality — teaser (none) → full OM (disclaimer page only) → V5/VHC2 full OM (standalone "Risks & Mitigants" section).

The platform register (R7, VHC2 final NPV 2026) carries an in-deck risk framework following the probability × impact × mitigant structure. This is the only observed case of a structured risk framework in an outbound deck (NPV 2026).

---

## 4. Sponsor Presentation by Register

### Deck OMs (R1 / R7)

- **Bio structure:** 3-sentence format per person: role + credential anchor (former X at Y) + current deal-relevant capability. All six TTC members in Obsidian platform deck follow this exactly, stable Nov 2025 → May 2026 (A-slice).
- **Track-record labeling:** D-slice NPV final labels prior acquisitions "Proj." ("Proj. 40.76% IRR / 3.17x EM") — the only observed instance of explicit realized/projected discipline in a deck OM. Skyway REALIZED CASE STUDY slide also uses "PROJ." prefix because returns not yet realized at deck date (December 2024 deal).
- **Verification-status language:** NOT present in any outbound deck OM. Only R9 (internal memos) carries explicit verification statements. No outbound OM carries a verification disclaimer on sponsor track-record figures.
- **Depth by register:** Full OM (R1): 1–2 dedicated bio slides + proof-point case study. Platform deck (R7): team credential summary slide + external advisory board named. Teaser (R5b): compressed to 3 bios, no full bio paragraphs. Co-invest (R6): 3 bios as access narrative ("investing alongside the founders").

### Word OMs (R3 / R4)

- **Bio structure:** Bold label ("Proven Sponsor Capability") → 2–3 prose sentences. "Sponsorship" collective noun used for sponsor entity throughout (Word OM specific — not used in deck OMs).
- **Proof-point logic:** LogistiCenter Business Park founding narrative is verbatim identical across all Wind Gap versions (2024–2025, Pref and JV registers, confirmed E13/E43/E48/E52) — functions as sponsor origin-story proof point.
- **No verification language** in any investor-facing version.

### Internal (R9)

- Sponsor track record explicitly audited against V23's own knowledge. Verification language is direct: "zero completed automated dry-stack marinas as a sponsor"; "in direct conversation, the sponsor told us."
- Evidence: G-word-memos.md (Blue Harbor JAX 2026-05-17, Crossing at Santa Fe 2026-05-05).

---

## 5. Cross-Register Invariants

These elements appear without exception across every register and deal in the corpus. They are V23's style DNA, not register-specific. See voice-model.md and design-system.md for full treatment.

1. **Retained-by opening formula:** "Vanadium Realty LLC ('Vanadium') has been exclusively retained by [Sponsor] to structure and arrange [capital type] financing for [project]" (Word OMs) / "Vanadium Realty ('Agent') has been exclusively engaged by [Sponsor] to source [ask]" (deck OMs). Present in every investor-facing OM and outreach memo (R1–R4, R10), 2024–2026.

2. **"Sponsorship" collective noun:** Used for sponsor entity actions in Word OMs only ("Sponsorship has been in contract on this site since 2021"). Never used in deck OMs ("Sponsor" only). E-pektor chain 2024–2025.

3. **Bold-label em-dash Investment Highlights bullet:** "**Compelling Financials** — Project-level levered IRR >24.00%..." No period at end of bullet. Confirmed across all R1/R3/R4/R10, 2024–2026.

4. **No external source citations inline in deck OM body:** Statistics stated without inline footnotes in deck body. Some source notes appear in small-print footer positions (Krios/Everleaf register); V23 domestic R1 deck OMs use footnote-only on exec summary stat box, no per-slide lines in final/send-state versions.

5. **Contact page is V23-only:** Sponsor contacts intentionally absent from all outbound decks. Confirmed B-slice blueprint and G-slice contact pages.

6. **V23 logo bottom-right:** Consistent pixel position across all pptx templates (x approx 12.65–12.69, y approx 6.0–6.75). Confirmed across B, C, D, F slices.

7. **Garamond as primary body typeface:** All investor-facing materials (deck and Word OMs). Eras Light ITC in internal memos, letterhead, and templates. Consistent 2020–2026.

8. **Off-slide left accent bar:** 8 rectangles at x=-1.23 in pptx templates. Confirmed B-slice (105 N 13), D-slice (NPV), F-slice (3605 Church Ave).

9. **Dual-panel Executive Summary (deck OMs):** Left narrative paragraph + right dual table (Sources/Uses + Returns KPIs). Confirmed in R1 (105 N 13 all versions) and R2 (vDebt).

10. **Incentive-layer separation from base returns:** Tax abatement, tourism act grant, IPA contract, or regulatory tailwind is always quantified separately from base NOI/IRR and framed as additive/protective, not as primary value driver. Confirmed across F-slice (NTA), B-slice (ICAP), A-slice (IPA contracts), D-slice deal economics.
