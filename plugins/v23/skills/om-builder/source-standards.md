# Source Standards
<!-- Derived from: om-pattern-study-2026-06 + cre-source-tiers.md (global canonical) + user_vanadium_analysis_conventions.md -->
<!-- Regeneration pointer: docs/superpowers/plans/2026-06-11-om-builder-v6.md -->
<!-- Self-contained: no [[memory]] references; no external file dependencies -->

Applies to all V23 deliverables — OMs, IC memos, investor letters, decks, screens.

---

## 1. Source Tiers

### Tier 1 — Primary institutional research / data

CoStar, Green Street, REIS, RCA / MSCI Real Capital Analytics, Newmark Research, JLL Research, CBRE Research, Cushman & Wakefield Research, Colliers Research, NAREIT, NCREIF, INREV / ANREV, Federal Reserve / FRED, BLS, U.S. Census (ACS), BEA, and top-tier manager white papers (Blackstone, Brookfield, Starwood, Carlyle, Ares, KKR, Oaktree — publicly distributed institutional research only).

### Tier 2 — Institutional trade press

PERE / PEI Media, Institutional Real Estate Inc. (IREI), ULI / PwC Emerging Trends, IPE Real Assets, GlobeSt / Real Estate Forum.

### Tier 3 — Academic / specialized

Cornell Baker Program, MIT Center for Real Estate, Wharton Real Estate, peer-reviewed CRE-finance journals (RERI, AREUEA, JRER).

---

## 2. Not Acceptable as a Data or Thesis Source

- Medium / Substack posts (unless a credentialed author with cited institutional affiliation)
- Broker marketing PDFs used as a data or thesis source — broker listings are fine; broker thesis pieces require Tier 1/2 corroboration
- Wikipedia as a primary source
- Generic blog posts, opinion pieces without underlying data
- Vendor-sponsored "studies" with no disclosed methodology
- Anonymous LinkedIn posts, Reddit threads, generic press releases
- Any source that cannot be independently traced to a specific report, edition, and publication date

---

## 3. As-of Dating Discipline

Every market, comp, or financial claim carries an explicit as-of date. A stale comp is worse than a missing comp — it reads as institutional rigor while misleading.

- Format: "Source: CoStar Tampa Bay IOS Submarket Report, Q1 2026" or "Source: NPV sizing model, 3/27/2026."
- Macro and capital-markets references must reflect the current rate environment as of the writing date. When a deal is dated to a moment in the cycle, every cited data point must align to that moment or be flagged explicitly for recency.
- If a number is older than 12 months in a fast-moving sector (industrial, data center, IOS, life science), flag it for refresh before publication.

---

## 4. Claim Auditability (Non-Negotiable for Any Multi-Claim Deliverable)

Every cited claim must be traceable to a specific source and as-of date, and must be auditable after the fact. For any research-backed deliverable, maintain a written audit trail that a reviewer can re-check.

**Audit-trail entry format:**

| Field | What goes here |
|-------|---------------|
| Claim | Exact claim as it appears in the deliverable |
| Value | Numeric or assertion as cited |
| Source | File name / tab / page reference OR URL |
| As-of | Date of the source data |
| Tier | 1 / 2 / 3 |
| Verified | Y / N / TBD |

Every external claim = quoted passage + source (name / URL) + as-of date + tier.
Every internal numeric = value + source file + tab / page reference.
Do not ship a figure that has not been verified against its source. If it cannot be verified, mark "TBD — confirm with sponsor" or "TBD — confirm source" and surface it visibly. Never guess-fill.

---

## 5. Recency Discipline

- Every numeric, comp, market stat, vacancy figure, cap rate, rent comp, or demographic stat carries an as-of date.
- Stale comps are worse than missing comps — date everything or drop it.
- Macro / capital-markets references must reflect the current rate environment, not a prior cycle's.
- Flag any data older than 12 months in a fast-moving sector (industrial, data center, IOS, life science) for refresh before publication.
- If a claim cannot be sourced to a Tier 1/2/3 source with an as-of date, mark it "TBD — confirm source" and surface it. Never fabricate.

---

## 6. Risk-and-Mitigant Pattern (Mandatory)

Every named risk follows: **Risk — Probability — Impact — Mitigant.**

Risks must tie to cash-flow outcomes. If X happens, then NOI Yr N drops by Y%, IRR drops to Z%, mitigant returns return to >= A%.

**Weak (do not use):** "Competition may increase."

**Strong (correct form):** "National IOS aggregators (Catalyst, Zenith, Alterra) move down-market into sub-$10M deals as their core pricing tightens. Probability: moderate over 24 months. Impact: compressed yield-on-cost from 9.5% to approx 8.5% on un-deployed pipeline. Mitigant: NPV's local-sourcing pipeline is contracted via owner-operator relationships; aggregator entry would price-in inflated land basis whereas NPV underwrites cash-flowing in-place."

Listing risks without quantifying or tying to outcomes is an anti-pattern. Every named risk must have probability, impact (tied to IRR or NOI), and mitigant before the deliverable ships.

---

## 7. Analytical Purposes Checklist

Every V23 deliverable must serve these purposes. If any is missing or thin, the deliverable has a blindspot. Research, source, or surface as "TBD — confirm with sponsor" — never fabricate, never skip.

1. **Establish the setting** — macro conditions, submarket fundamentals, sector dynamics, capital markets context as of the writing date.
2. **Define the opportunity** — what dislocation, gap, or angle this deal exploits; why it exists; why it will close.
3. **Position the asset** — what it is in fact, how it works mechanically, what is broken or working, who occupies/uses it.
4. **Argue the thesis** — the argumentative spine that ties setting → opportunity → asset → strategy → execution → return into one defensible claim.
5. **Show the business plan** — concrete, sequenced, sourced, with benchmarked costs and comparable evidence; not generic value-add language.
6. **Vet the sponsor** — track record (full portfolio, not just wins; gross AND net; loss ratios; vintage discipline); AUM; capital partners; principal bios contextualized to the strategy.
7. **Stack the capital** — sources/uses, debt terms, equity terms, fees, carry, waterfall; sponsor earnings if deal underperforms must be visible.
8. **Surface the returns** — IRR + MoIC + cash-on-cash; base AND stress AND downside; sensitivity tables with the actual failure path.
9. **Frame the risks** — every named risk: probability × impact × mitigant; risks tied to cash-flow outcomes; integrated throughout, not buried at end.
10. **Anticipate LP cutting questions** — the eight Braintrust questions must be answerable from the document.

---

## 8. Sponsor-Defensibility Test

Before any claim ships:
- Could the sponsor stand behind this language in front of their LPs without flinching?
- Is the language Vanadium-spin (over-promise) or sponsor-defensible (calibrated)?
- If the sponsor pushed back in review and asked to soften, would softening preserve the thesis? If yes, the original was over-claimed.

Vanadium operates as placement agent — credibility with both the sponsor and the LP is the asset. Over-claims burn sponsor relationships; under-claims burn deal economics. Calibrate.

---

## 9. Never-Fabricate Rule

Never fabricate a stat, comp, citation, URL, or sponsor track-record figure. If a claim cannot be verified against a traceable Tier 1/2/3 source, mark it one of:
- "TBD — confirm with sponsor"
- "TBD — confirm source"

Surface it visibly in the deliverable or audit trail. Do not guess-fill, smooth over, or leave unmarked. A marked gap is always better than an unmarked fabrication.
