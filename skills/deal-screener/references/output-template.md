# Screening Report Template

This is the canonical deliverable shape. Every deal screening produces a report in roughly this structure, scaled to the available information. If a section can't be filled in due to missing data, leave it titled but write "INCOMPLETE — see Questions section #__" and continue.

The report is a **single document**. Output it as Markdown by default. Offer to convert to .docx via the `docx` skill if the user wants something to forward.

## Header

```
DEAL SCREENING — [Property Name]
[City, State] | [Asset Class] | [Submarket if known]
Sponsor: [Name]
Stated Ask: $[Purchase Price] / $[Equity Need] / $[Loan Amount]
V23 Seat: [Equity Placement | Debt Placement | Principal | LP-Side]
Screened: [Date] | Screener: [Claude / V23 Deal Screener]
Recommendation: [Pursue | Pass | Conditional]
```

The header should fit on one screen. Reader knows what the deal is and what we think within 5 seconds.

## 1. Deal Snapshot

One paragraph, max 6 sentences. Cover:
- What the asset is (size, vintage, location)
- What the sponsor is asking for
- The headline financial story (going-in yield, hold period, projected return)
- The one or two factors that make this deal interesting OR concerning at first read

This is the section a busy partner reads in the elevator. Make every sentence earn its place. No marketing language.

## 2. V23 Seat & Engagement

Two to four sentences explaining:
- Which seat we're applying (placement / principal / LP-side / lender)
- Why this seat shapes the analysis (e.g., "as equity placer, the priority question is whether this is placeable to our LP base, not whether we'd buy it ourselves")
- What V23's role would be if we engage (mandate scope, fee structure if known)

## 3. Financial Forensics

The most important section. Subdivide as follows.

### 3a. Headline economics — verified

A small table:

| Metric | OM Stated | Recomputed | Variance | Note |
|---|---|---|---|---|
| Purchase Price | | | | |
| Year 1 NOI | | | | |
| Going-in Cap Rate | | | | |
| Stabilized NOI | | | | |
| Stabilized Cap Rate | | | | |
| Exit Cap Rate | | | | |
| Levered IRR | | | | |
| Equity Multiple | | | | |
| Cash-on-Cash (Avg) | | | | |
| DSCR (Year 1 / Stabilized) | | | | |
| Debt Yield | | | | |
| LTV (Acquisition) | | | | |
| Loan-to-Cost | | | | |

If a metric isn't applicable to the seat (e.g., levered returns when V23 is debt-only), strike it. If a metric isn't disclosed, write "Not disclosed — Q#__".

### 3b. Trailing financial review

Compare T-3 annualized vs. T-12. State what each shows. Flag direction and magnitude. Comment on whether the OM's "Year 1" matches T-12 or is a forward number.

For value-add deals: compare in-place rents to projected post-renovation rents. State the % lift. State the comparable basis (which competing properties are being used as the benchmark, and are they truly comparable).

### 3c. Pro forma stress tests

Rerun the OM's projected returns at:
- **Exit cap = entry cap** (no compression)
- **Exit cap = entry cap + 50bps** (modest expansion, defensible bear case)
- **Rent growth = 50% of OM assumption**
- **Stabilized vacancy at market** (state your market vacancy source)
- **All of the above combined** (the IC stress case)

Report the IRR and equity multiple at each. If the OM doesn't share the model, note that you're estimating directionally and ask for the model.

### 3d. Capital stack and fees

Tabulate:
- Senior debt: amount, rate, term, IO period, amortization, prepayment, recourse
- Mezz / pref: amount, rate, terms
- LP equity: amount, preferred return, return profile
- GP equity: amount, alignment percentage
- Sponsor fees: acquisition, asset management, disposition, financing, refinance, construction management — each as % and absolute $
- Total fee load to LP equity over the hold (in % terms)

Comment on alignment. Standard market is roughly: 1-2% acq fee, 1-1.5% AM fee, 1% disposition. Anything materially above market gets flagged.

### 3e. Source-of-return decomposition (mandatory)

Senior reviewers always know where the return is coming from. Decompose:

- **Operating distributions Y1–Y_hold** as % of equity multiple: __% ($__M)
- **Exit residual to equity** as % of equity multiple: __% ($__M)
- These two should sum to the equity multiple

Apply the threshold rule:
- **Stabilized / credit-leased / core / core-plus:** flag if exit > **60%** of multiple
- **Value-add / opportunistic / development:** flag if exit > **75%** of multiple

If the deal is back-loaded by these thresholds, the screen MUST go heavy on:
- Exit cap defensibility (vs. entry cap, vs. comparable historical exits)
- Terminal NOI defensibility (the FMV / mark-to-market / lease-extension assumptions baked into the year before sale)
- Hold-period sensitivity (what happens if exit slips 12-24 months)
- Buyer pool depth (covered in section 7)

Back-loaded returns mean the entry coupon isn't doing the work — the model is betting on selling at the right cap rate at the right moment. State this explicitly in the screen, not as a hedge but as a fact the reader needs to weigh.

## 4. Market & Competitive Read

Subsections:
- **Submarket fundamentals.** Vacancy, rent growth, supply pipeline, demand drivers — what the OM says vs. what's checkable.
- **Comparable transactions.** What the OM offers as comps, and whether they're truly comparable (vintage, size, condition, basis, financing structure). Cherry-picking flag if applicable.
- **Supply pipeline.** New supply coming on within the asset's competitive set. Often understated in OMs.
- **Demand drivers.** Employment, demographics, traffic counts, etc. — only those material to the asset.

If any of this isn't in the OM (often it's thin), state it and add a question.

## 5. Sponsor Read

- Sponsor name, vehicle, and (if disclosed) prior track record
- Number of comparable deals executed, full-cycle returns where disclosed
- GP team — key principals, years of experience, prior firms
- Conflicts and related-party transactions (broker, manager, GC, lender all owned by sponsor or affiliates? Disclose.)
- Co-GP structure if any
- Any litigation, fund failures, or notable losses if disclosed
- Whether the sponsor has done this asset class / market / business plan before

If V23 is in equity placement seat: comment on whether this sponsor profile is placeable to V23's LP base (institutional / family office / HNW depending on context).

## 6. Capital Stack & Structure (deeper if applicable)

If the deal has structural complexity beyond what fit in 3d, expand here:
- Waterfall — pref, return of capital, splits at each hurdle
- Promote structure — GP catch-up, lookback provisions
- Co-investment rights, ROFO, ROFR
- Refinance plan — when, at what rate, what's the assumed take-out
- Capex / interest reserves — sized adequately?

## 7. Next Buyer Analysis (mandatory)

Every CRE deal has a next buyer. The exit price at the modeled cap is a claim about what someone will pay V23 (or the sponsor) at the end of the hold. Test that claim every time.

Cover four things:

1. **Who buys this asset at exit?** Name 3-5 plausible buyer profiles by category, ideally with named comparable buyers (specific REITs, specific net lease funds, specific family office types, specific defense-thematic operators, etc.). For each, in 2-4 sentences: why would they buy this asset at this price, what's their hurdle, what's their constraint, what's the gating issue?
2. **What's the buyer's underwriting view at exit?** A buyer in year T+hold underwriting this same asset will discount things V23 may not. Lease tail remaining, FMV negotiation risk, capex catch-up needs, market shift since entry. Build the realistic next-buyer underwriting and compare to the OM's exit assumption.
3. **Realistic range of exit prices.** Bear / base / bull, each with the specific assumption that drives it (e.g., "Bull: 6.0% cap on Y9 NOI of $4.3M = $71.8M, requires renewal already exercised at contractual roll. Base: 6.75% cap on Y9 NOI of $4.0M = $59.3M, requires lease tail of 5+ yrs at exit. Bear: 7.5% cap on Y9 NOI of $3.5M = $46.7M, post-FMV walk-down").
4. **What kills the exit?** Top 3 things that, if true at exit, force a price cut or delayed sale. These should map back into the risk register.

If the buyer pool is thin (one specific REIT with a thematic mandate, or one family office with a niche interest), say so plainly. Thin buyer pools mean exit pricing is hostage to a narrow set of decision-makers' appetite at exit.

**Write this section in prose, buyer-class by buyer-class.** Don't bullet-pad. 4-8 sentences per profile is right.

## 8. Risk Register

A ranked list, highest severity first. Each entry:

```
RISK: [One-sentence statement]
Severity: [High / Medium / Low]
Likelihood: [High / Medium / Low]
Mitigant in OM: [Yes / Partial / No — describe]
V23 view: [Brief — what we think the actual risk is]
```

Aim for 5-12 risks. Skip generic risks ("interest rate risk") unless materially asymmetric to this deal. Focus on deal-specific risks.

## 9. Questions for the Sponsor / Broker

The most operationally valuable section. Numbered list. Each question is:
- Specific (references a page or a number)
- Surgical (answers cleanly with a number, document, or short statement)
- Copy-paste-ready (the user can drop this list into an email to the broker as-is)

Group by topic:
- **Financials & assumptions** (Q1-Q__)
- **Property condition & physical** (Q__-Q__)
- **Market & competitive** (Q__-Q__)
- **Sponsor & track record** (Q__-Q__)
- **Capital stack & structure** (Q__-Q__)
- **Other** (Q__-Q__)

Aim for 10-25 questions on a typical screen. More if the OM is thin.

Example question format:
> Q3 (Financials, OM p. 14): The OM cites a 5.4% going-in cap rate on Year 1 NOI of $4.2M. Our recomputation lands at 5.1% on the same NOI ($4.2M / $82M). Please confirm the NOI definition used and reconcile the 30bps gap.

## 10. Information Missing from the OM

A bulleted list of items a senior reviewer would expect but did not find:
- T-3 statements
- Rent roll detail (or full rent roll with tenant names if office/retail/industrial)
- Tenant credit ratings / financials
- Phase I / environmental
- Property condition assessment
- Survey / title
- Tax bill and pending tax appeal status
- Insurance carrier and renewal history
- Prior sale history and seller's basis
- Prior sponsor pitch (if recap or refi)
- Capital stack waterfall detail
- Sponsor track record packet
- Detailed rent comps
- Detailed sale comps
- Supply pipeline data
- ... add any deal-specific items

Each missing item should map to one or more questions in section 8.

## 11. Recommendation

This is the verdict. The screener answers the question: **does this deal make sense?**

One of: **PURSUE | PASS | CONDITIONAL**

Followed by 3-6 sentences covering:
1. The top-line answer.
2. The 2-3 reasons that drive that answer (tied to the analysis above — not new arguments).
3. If conditional, the specific conditions (checkable, not vague — e.g., "if sponsor track record packet shows ≥3 full-cycle deals at >18% net IRR in this asset class, we reconsider," not "subject to further sponsor review").
4. Time-bounded next steps for V23.

A true screener answers the question. The questions in section 9 inform the verdict; they do not replace it. If the deal lacks enough information for a verdict, the verdict is "CONDITIONAL — pending [specific items]," not a punt.

## 12. Proposed Lesson for the Screener (Optional)

Only include if there's a real lesson worth capturing. Format:

```
PROPOSED LESSON:
[One-sentence rule, imperative voice]
Context: [Brief — what triggered this, why it matters]
```

The user decides whether to add this to `references/lessons-learned.md`.

---

## Style notes

- **Length:** Aim for 4-8 single-spaced pages depending on deal complexity. Initial screen of a teaser may be 2 pages; full IC-quality screen may be 12.
- **Tables:** Use them for comparative data, not for everything.
- **Bullets:** Reserved for the question list, missing-info list, and risk register. Body text is prose.
- **No marketing copy.** Strip every "trophy," "irreplaceable," "core-plus opportunity," "value-add story" — translate to observable facts or remove.
- **Page-cite OM references.** "(OM p. 14)" — every quoted number gets a page citation.
- **State your sources for outside data.** "Per CoStar Q3 2026 submarket vacancy of 6.2%" not "submarket is tight."
