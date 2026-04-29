# Lessons Learned

This file accumulates rules, gotchas, and patterns from past deal screenings. **Read this every run before reading the OM.**

Each lesson is one rule. Lessons are added two ways:
1. **The skill proposes them** at the end of a screening when something subtle came up. The user accepts, modifies, or rejects.
2. **The user adds them directly.** When the user says "we missed X on the last deal" or "always check Y," append the rule here.

Lessons are timeless rules, not deal commentary. Strip identifying details when adding (anonymize markets / sponsors only if the user requests; otherwise be specific because specificity helps the model recognize patterns).

## Format

```
### LL-[NNN] — [One-line title]
Rule: [Imperative voice — "Always X," "Check Y before Z," "Never accept Q without R"]
Why: [One or two sentences of context]
Triggered by: [What pattern in an OM should make Claude apply this rule]
Date added: [YYYY-MM-DD]
Source: [User / Skill self-observation / Post-mortem]
```

---

## Active Lessons

### LL-001 — Tax bump-up on acquisition is the most common buried understatement
Rule: Always recompute the post-acquisition property tax bill at the new basis using the local mill rate / assessment ratio, and compare to the OM's projected tax line. Flag any gap >5%.
Why: Most jurisdictions reassess on sale. Sponsors frequently project taxes by trending the seller's tax bill 2-3% per year, ignoring the reassessment. The understatement can be 50-100bps of cap rate.
Triggered by: Any acquisition where pro forma taxes are within 10% of seller's actual tax bill.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-002 — Insurance is materially understated in coastal and high-CAT markets
Rule: For any property in FL, TX, LA, CA, NC, SC coastal counties, or California wildfire zones, ask the broker for current renewal quotes from named carriers. Do not accept seller's premium as Year 1 model input.
Why: Insurance has 2-3x'd in many markets since 2020. Sellers' policies often have prior-period rates locked in that won't be available at renewal. Material to going-in NOI.
Triggered by: Subject property in named coastal county or high-CAT market AND OM models insurance using seller's actual.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-003 — T-3 vs T-12 reveals trajectory; never skip the comparison
Rule: Always annualize the trailing 3 months and compare to T-12. State the direction and magnitude of any divergence in the screening report.
Why: T-3 above T-12 = recent improvement that the seller is annualizing aggressively into Year 1. T-3 below T-12 = recent deterioration being hidden by stronger first half of T-12. Either way, it's signal.
Triggered by: Every screening with at least T-3 disclosed.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-004 — Exit cap = entry cap is the default; compression is a claim that must be defended
Rule: When the pro forma assumes exit cap rate < entry cap rate, treat the compression as a claim requiring evidence. Re-run the IRR at flat-to-+50bps cap expansion and report. Ask the sponsor for the specific market thesis supporting compression.
Why: The natural state of a model is exit cap = entry cap (i.e., neutral cap rate environment). Compression is a directional bet on the market. Most pro formas show 25-50bps of compression with no defensible argument.
Triggered by: Pro forma exit cap < entry cap.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-005 — Seller's basis is checkable; always look
Rule: For every acquisition, check public records (county assessor / recorder) or the OM's prior sale section for what the seller paid, when, and what they invested. A markup >50% over prior trade with no transformative capex is a flag.
Why: Markups against thin or no value-add work surface flips, not real value creation. Even when the markup is justified, knowing the seller's basis informs negotiating posture.
Triggered by: Every acquisition screening.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-006 — The total fee load to LP equity is the alignment question
Rule: Sum acquisition + AM + financing + disposition + construction management + refinance fees. Express as % of LP equity invested over the projected hold. If GP economics from fees alone exceed ~5% of LP equity over the hold, alignment is structurally weak regardless of promote.
Why: Fees are paid regardless of performance. A heavy fee load means the GP makes money even if the LP doesn't. This is the alignment test, not just the promote.
Triggered by: Any equity placement screening, any LP-side advisory screening.
Date added: 2026-04-28
Source: Skill seed lesson

### LL-007 — "Irreplaceable" supports renewal probability, NOT favorable FMV economics
Rule: For single-tenant deals with FMV extension options, the "irreplaceable / cannot be relocated" thesis supports renewal *probability* but does NOT support favorable *economics* at FMV negotiation. A long-term anchor with operational integration has leverage to negotiate sub-market FMV. Default skeptical when underwriting mark-to-market upside on FMV options for single-tenant credit deals.
Why: Long-term tenants with deep operational integration negotiate FMV from a position of strength, not weakness. A recently-executed renewal landing below the cited comp set is direct evidence of the tenant's leverage and a forward indicator of what to expect at the next FMV exercise.
Triggered by: Single-tenant credit-leased deal where the pro forma assumes mark-to-market lift at an FMV option exercise; OR any deal where the in-place rent is materially below cited comps despite a recent renewal.
Date added: 2026-04-29
Source: Skill self-observation (Raytheon Aurora screening)

---

## Adding a new lesson

When the user says "add this as a lesson" or you propose one and they accept:
1. Increment the LL number
2. Use the format above
3. Append to the bottom of "Active Lessons"
4. Confirm with the user: "Added as LL-NNN. Anything else?"

When the user says "remove LL-NNN" or "that lesson was wrong":
1. Move the lesson to a `## Retired Lessons` section at the bottom (don't delete — keeps history)
2. Add a one-line note about why it was retired

When two lessons conflict, raise it: "LL-X and LL-Y appear to conflict on [topic]. Which should take precedence, or should both be revised?"
