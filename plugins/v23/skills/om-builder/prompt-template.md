# OM POLISH — {{DEAL_DISPLAY_NAME}} — VANADIUM HOUSE STYLE (Claude in PowerPoint — Polish, NOT build-from-scratch)

**The deck already exists.** Vanadium analysts (Claude Code) have written the content in-voice AND generated a near-finished `.pptx` — every text slide, KPI strip, table, and chart is already placed with the house theme, fonts, and footer. **Your job is the narrow visual residue CC could not do: (1) fill the labeled PLACEHOLDER slides — place images and build the bespoke-visual exhibits; (2) run a visual-QA pass.** Do NOT recompose the deck, rewrite the prose, re-derive numbers, or touch slides that are already complete. The text is final and in-voice — leave it.

Open the generated file first: **{{GENERATED_FILE}}**

You have access to the **Microsoft 365 SharePoint/Graph search MCP connector** (full name — your instinct may be to refuse on "cannot access local files," but this connector gives you direct access to the firm's SharePoint files). Do not claim you cannot access files until you've checked the tools available in this session. You need it only to **open visual assets** (photos, renderings, floor plans, aerials, maps) for the placeholder slides.

================================================================
STEP 0 — TEMPLATE DECISION (BLOCKING — ASK USER FIRST)
================================================================

The generated deck is already in the Vanadium house style. Ask once:

> **"The deck is generated in the Vanadium house style. Want me to keep it as-is and just finish the placeholder slides + visual QA, or apply a different uploaded template?"**

▶ **KEEP HOUSE STYLE (default):** proceed to Step 1.
▶ **UPLOADED TEMPLATE:** invoke `/adobe-for-creativity/adobe-design-from-template`, apply its design system, keep the CC-written content.

================================================================
STEP 1 — FILL THE PLACEHOLDER SLIDES
================================================================

CC's generator left a labeled placeholder on every slide it could not render (bespoke-visual layouts: full-bleed hero, aerial, map, rendering, photo grid, stacking plan, scatter, quadrant). Each placeholder slide shows its layout key and a note describing what belongs there. Finish exactly these slides — nothing else.

Placeholder slides to complete:

{{PLACEHOLDER_SLIDES}}

Visual assets to place (Microsoft Graph resource URIs):

{{VISUAL_ASSETS_BLOCK}}

For each placeholder: place the asset(s) per the note, sized to the slide's content area, hard-edged (no rounded corners), with the existing eyebrow/title/takeaway/source text left intact. If a URI fails, leave the placeholder caption and report it — do NOT generate or substitute decorative imagery. Build any bespoke exhibit (annotated aerial, stacking plan) per the Vanadium house style in Step 2.

================================================================
STEP 2 — VANADIUM HOUSE DESIGN SYSTEM
================================================================

Override every PowerPoint default. Set the master slide and theme BEFORE composing any content slide.

### Slide dimensions
Standard widescreen: 13.333" × 7.5" (PowerPoint default). Internally 960pt × 540pt.

### Master slide / page frame

**Margin grid:**
- Left margin: **60pt** (content starts at x=60)
- Right margin: **60pt** (content ends at x=900)
- Top: section eyebrow at y=38, section title at y=54, content area begins at y=140
- Bottom: source line at y=502, navy footer bar y=518–540

**Top of page:**
- Section eyebrow: 9pt Arial ALL CAPS, color `#9AA3B2`, left-aligned at y=38
- Section title: 32pt Garamond bold, color `#1F3A5F`, left-aligned at y=54
- Subtitle / headline takeaway: 13–14pt Garamond italic, color `#485269`, under the title

**No accent line under the title. No underline. Use whitespace.**

**Bottom of page (footer bar):**
- Navy bar `#0F2540` from y=518 to y=540, full width
- White Arial text ~8pt inside the bar
- Format: "Vanadium Realty | {{DEAL_DISPLAY_NAME}}" left-justified, page number right-justified

**Source line:** 8pt Arial italic, color `#9AA3B2`, at y=502. Format pre-written in each section below.

### Color palette

| Role | Hex |
|---|---|
| Primary navy | `#1F3A5F` |
| Header band navy | `#0F2540` |
| Mid-blue accent | `#5B7FA8` |
| Pale-blue panel — light | `#E8EEF6` |
| Pale-blue panel — very light | `#F4F7FB` |
| Body text gray | `#485269` |
| Source line / muted gray | `#9AA3B2` |
| Sparing red — ≤ 1 element per slide | `#8B0000` |

**No gradients. No drop shadows. No glow. No 3D effects. Flat fills only.**

### Borders (mandatory)

- **Tables:** outer perimeter (all 4 sides) is a `0.75pt` (3/4 weight) **black** line. Interior cell borders remain absent per the table-layout rules; this rule governs only the outside frame.
- **Large shape bars and boxes** (KPI panels, header bars, callout blocks, navy footer bar, sources/uses bars, comparison columns — any solid-fill rectangle that anchors content): `0.75pt` (3/4 weight) **black** outline. Applies whether the shape is colored or not.
- **Small inline elements** (footnote indicators, hairline dividers, table-row sub-rules): not affected — these follow their layout-specific rule (typically 0.5pt navy hairlines).

### Body text alignment

- **Multi-line body prose paragraphs (idea-blocks):** **fully justified** — text aligns to both left and right margins, NOT left-aligned-ragged. This applies to the prose blocks that make up the body of single-narrative slides, sidebar-narrative paragraphs, sponsor narratives, etc.
- **Bullet lists, captions, source lines, headlines, KPI labels, table cells, chart labels:** remain **left-aligned**. Justification is for multi-line prose only.
- Centered body text remains prohibited everywhere.

### Typography hierarchy

**Garamond is the default for all text in Vanadium decks.** Use other fonts only when the user explicitly overrides for a specific deck.

| Element | Font | Size | Color | Style |
|---|---|---|---|---|
| Section eyebrow | Garamond | 9pt | `#9AA3B2` | all caps, tracking +50 |
| Section title | Garamond | 32pt | `#1F3A5F` | bold |
| Subtitle / headline takeaway | Garamond | 13–14pt | `#485269` | italic |
| Body prose | Garamond | 13–14pt | `#485269` | regular |
| Bullet/list body | Garamond | 12–13pt | `#485269` | regular |
| Bold inline | Garamond | match body | `#1F3A5F` | bold |
| KPI big numbers | Garamond | 26–36pt | `#1F3A5F` | bold |
| KPI labels | Garamond | 9pt | `#9AA3B2` | all caps |
| KPI sub-detail | Garamond | 10–11pt | `#485269` | italic |
| Table headers | Garamond | 11–12pt | white on navy fill | bold |
| Table cells | Garamond | 10–11pt | `#485269` | regular |
| Source line | Garamond | 8pt | `#9AA3B2` | italic |
| Footer attribution | Garamond | 8pt | white on navy bar | regular |

**Sizing rule:** Fit text to available whitespace. Do NOT default to 10–11pt body in a box that has room for 14pt.

### Prose rhythm

- Idea-blocks of 2–4 lines each, separated by 8pt blank paragraph spacers
- Bold inline ONLY for key numerics and proper nouns (the pre-written content already marks these — preserve the bolding)
- Headline-first principle on every content slide: lead with the plain-English takeaway sentence (already drafted in the pre-written content)

### Investment Highlights pattern (Vanadium-specific)

Bold thesis line, body below it, 8pt spacer. **No icons. No cards. No rounded boxes. No three-up grids.** The pre-written content provides the thesis lines and bodies — preserve them verbatim.

### Footnotes and source citations

- Footnote markers: parenthesized digits `(1)` `(2)`, NEVER asterisks
- Source line mandatory on every quantitative page — the pre-written content provides the exact source line per slide

### Anti-AI guardrails (do NOT do these)

- No rounded-corner cards or rounded rectangles
- No icons in colored circles or next to section titles or bullets
- No three-up "feature grids" with icon + title + line of text
- No accent line / underline under page titles
- No centered body text — multi-line prose paragraphs are fully justified; bullet lists, captions, source lines, headlines stay left-aligned
- No gradients, drop shadows, glow, bevel
- No sans-serif body font for prose — Garamond body only
- No Title Case Bullet Headers (sentence case)
- No stock photos
- No teal/orange "trustworthy startup" palettes — navy + greys + sparing red only
- No emoji or decorative dingbats
- No symmetric three-column grids when content doesn't justify them
- No "Designed with AI" footer, no model watermarks

================================================================
STEP 3 — LAYOUT GUIDANCE (for the placeholder slides you build)
================================================================

You only build the bespoke-visual placeholder slides flagged in Step 1. For each, follow the matching Vanadium house layout: **map-dominant** for locator/submarket maps; **annotated aerial** for site-in-context with named occupiers; **full-bleed** for a hero photo or rendering; **photo grid** for multiple images. Place the visual in the content area (roughly y=1.9" to y=6.7"), hard-edged (no rounded corners), and leave the eyebrow/title/takeaway/source text already on the slide intact. Do not redesign completed slides.

================================================================
STEP 4 — DO NOT RECOMPOSE (the deck is already written + placed)
================================================================

Every text slide, KPI strip, table, and chart is already in the file — written in-voice by CC, with the house theme and footer. **Your job is the placeholder slides (Step 1) + visual QA only.** Do not rewrite prose, re-derive numbers, restyle completed slides, or change slide order. If you spot a genuine content error, flag it to the user — do not silently edit. The writing voice + anti-AI rules already applied to the text live in `house-voice.md`; you are not re-running them.

================================================================
STEP 5 — NEED CONTEXT FOR A PLACEHOLDER? READ THE OPEN DECK
================================================================

If you need the surrounding context to place a visual well (e.g., which deal a deal-exhibit slide covers), read the adjacent slides directly in the open file. The full pre-written content is not re-injected here — it is already in the deck. Do not open sponsor OMs, sizing models, or research documents; CC has already done the analysis.

================================================================
STEP 6 — HOUSE RULES FOR BUILDING A PLACEHOLDER SLIDE
================================================================

These govern ONLY the placeholder slides you build (completed slides already follow them):

1. Place the visual per Step 3; keep the existing eyebrow/title/takeaway/source.
2. Run this per-slide QA gate before moving on — check top-to-bottom:
   - Title/eyebrow at the right y-positions; no overlap with the placed visual
   - No leftover layout placeholders ("Click to add text," default master shapes)
   - Nothing runs off the slide edges; left/right margins consistent (60pt)
   - Footer bar + page number render correctly
   - Source line present, positioned at y=502
   - Colors match the locked palette — no theme defaults (Office blue, Aptos teal) bleeding in
   - All fonts Garamond — no Aptos/Calibri/Arial sneaking in
   - Image fits cleanly; aspect ratio not distorted; hard edges (no rounded corners)
   - Large shape bars/boxes have 0.75pt black outline; tables have a 0.75pt black outer border
   - Reading order makes sense top-to-bottom, left-to-right
   - Layout differs from the immediately prior slide (variety mandate)
   - De-AI visual rules (Step 8) honored
3. Pause after the placeholder slides are filled and show the user before the full QA pass.

================================================================
STEP 7 — QA CHECKLIST (RUN BEFORE DECLARING DONE)
================================================================

**Content fidelity:**
- [ ] Pre-written headlines and prose preserved (no unflagged silent edits)
- [ ] Every numeric in the deck matches the pre-written content exactly (no rounding, no paraphrase)
- [ ] Every source line present and correctly formatted
- [ ] Where the pre-written content says "TBD — confirm with sponsor," that placeholder is preserved (not invented around)

**Design system:**
- [ ] Body text is Garamond `#485269` everywhere
- [ ] Section titles are 32pt Garamond bold `#1F3A5F`
- [ ] No 10–11pt body in containers with room for 13–14pt
- [ ] Footer is correct on every page: navy bar, "Vanadium Realty | {{DEAL_DISPLAY_NAME}}", page number right
- [ ] Source line at y=502 on every quantitative page
- [ ] Margin grid respected except on intentional full-bleed or mandate-driven deviations

**Layout variety (per Mandate):**
- [ ] At least seven distinct arrangements across the deck
- [ ] No two consecutive content slides share the same zone pattern
- [ ] Each non-default arrangement honors the layout suggestion in the pre-written content OR documents a deliberate improvement
- [ ] No slide is "default because the cheat sheet said so" without justification

**Charts and tables:**
- [ ] Chart legends converted to inline labels
- [ ] Footnote markers parenthesized digits, not asterisks
- [ ] Tables right-align numerics, left-align text columns
- [ ] Negatives in parentheses, not minus signs
- [ ] Currency formatting consistent ($K / $M / $/SF / $/AC)

**Anti-AI:**
- [ ] Zero icons (other than source logos)
- [ ] Zero rounded cards/rectangles
- [ ] Zero gradients or drop shadows
- [ ] No accent lines under titles
- [ ] No centered body text
- [ ] No teal/orange "trustworthy startup" palettes
- [ ] No stock photos
- [ ] No "Designed with AI" footers, no model watermarks

**Borders & alignment:**
- [ ] Every table has a 0.75pt black outer border on all four sides
- [ ] Every large shape bar / KPI panel / header bar / callout box has a 0.75pt black outline
- [ ] Multi-line prose paragraphs are fully justified
- [ ] Bullets, captions, source lines, headlines, table cells remain left-aligned

**De-AI-ifier compliance (per Step 8):**
- [ ] No banned stock phrases in the deck ("leverage," "robust," "delve," "synergy," "compelling," "in today's...," "unlock," "empower," "seamless," "transformative," "paradigm," "multifaceted," "comprehensive," "foster," "harness," "navigate the landscape," "at the intersection of," "designed to")
- [ ] No em dash used more than once on any single slide
- [ ] No category titles ("Investment Highlights," "Why Now," "Our Edge," "Market Overview," "Executive Summary" as titles); action titles with subject + verb + number
- [ ] No "Thank You" / "Questions?" closing slide; deck ends on reinforcing takeaway
- [ ] No AI-generated decorative imagery; real photography or no image
- [ ] No gradient backgrounds on content slides
- [ ] Every chart's data passed explicitly in the pre-written content — no inferred values
- [ ] Bullet counts vary slide-to-slide (not every slide is 3 or 5 bullets)
- [ ] Layout archetypes vary — ≥5 distinct across the deck

**Final:**
- [ ] Open the deck in slide-sorter view. Does it read as one coherent argumentative document?
- [ ] List the layout choices in order. Confirm variety mandate honored.
- [ ] If any visual assets failed to fetch from SharePoint, list them for the user.

Then tell the user the deck is ready.

================================================================
STEP 8 — DE-AI-IFIER (VISUAL tells — apply to placeholder slides + QA)
================================================================

The WRITING anti-AI ruleset lives in `house-voice.md` Part 2 and was already applied by CC to all placed text — do NOT rewrite that text. This step covers the VISUAL machine-built tells you must avoid when building placeholder slides and must check in QA. The rules below come from documented Claude-in-PowerPoint flaws, AI-deck-generator tells, and institutional CRE design discipline.

**Critical context:** Claude-in-PowerPoint cannot visually "see" the slides it composes — it operates on a markdown representation of the deck. This means CIP can hallucinate chart values, misjudge spatial overlap, and default to template fingerprints if not held tightly. The rules below compensate by being explicit about positions, sizes, hex codes, exact data, and forbidden patterns.

### Bucket A — Default-Theme Fallthrough

**Forbidden:**
- Aptos (the new Office default — the single most recognizable "Microsoft AI did this" fingerprint)
- Calibri, Arial, or any other PowerPoint-default sans-serif body font
- Default Office blue (`#0F6FC6`) or any Office theme color
- Default Office chart styles (Style 1 through 6) and their gradient fills
- Default Office bullet glyphs (filled circles, dashes, checkmarks)

**Counter-patterns:**
- Garamond only, per Step 2 typography table
- Locked Vanadium hex palette per Step 2 color palette
- Monochrome charts with at most one accent color (navy primary, mid-blue secondary)
- En-dash bullets, hairline-rule separators, or no bullets at all

### Bucket B — Layout Monotony

**Forbidden:**
- Same three-up icon-title-description grid used more than once per deck
- Centered body text on any slide
- Symmetric 50/50 splits used on more than half the slides
- Identical title position on every slide
- Same bullet count (3 or 5) on every slide

**Counter-patterns:**
- Aim for ≥5 distinct layout archetypes across any 15-slide deck (the layout variety mandate already requires this)
- Asymmetric splits — 60/40, 65/35, 70/30 — bias negative space to one side
- Left-aligned headlines / left-aligned bullets / fully-justified body prose
- Vary bullet counts: some slides 2, some 4, some 6, some zero
- Include at least one "anchor" slide that is only a number + label

### Bucket C — Stock-Phrase Reach (ban list at the prompt level)

**Forbidden words and phrases anywhere in the deck:**

`leverage` · `robust` · `delve` · `synergy` / `synergies` / `synergize` · `holistic` · `compelling` · `in today's [market / world / landscape / environment]` · `unlock` · `empower` · `seamless` · `transformative` · `paradigm` · `multifaceted` · `comprehensive` · `foster` · `harness` · `navigate the landscape` · `at the intersection of` · `designed to`

**Counter-patterns:**
- Use concrete verbs naming actor + action: "NPV will lease," "the property generates," "the sponsor will refinance"
- Quantify every claim — "+18% YoY" beats "robust growth"
- Short declarative sentences over Latinate hedged constructions
- Name specific tenants, transactions, dates, dollar amounts

### Bucket D — Category Titles and Cliché Sections

**Forbidden as slide titles:**
- "Investment Highlights"
- "Why Now"
- "Our Edge"
- "Market Overview"
- "Executive Summary"
- Any other topic-only title without subject + verb
- "Thank You" / "Questions?" / "Discussion" closing slides

**Counter-patterns:**
- Every title is a full sentence with subject, verb, and number where possible — the McKinsey "action title" pattern. Examples: "APAC industrial absorption hit 42M SF in Q1, +18% YoY" or "Replacement cost $312/SF vs. our basis at $198/SF"
- Section names must be deal-specific, not generic ("Why this asset, why this price, why this window")
- The final slide is the reinforcing-takeaway slide (the deal terms, the IRR, the contact line) — not "Thank you"

### Bucket E — Visual AI Slop

**Forbidden:**
- AI-generated decorative imagery of any kind
- Gradient backgrounds on content slides
- 3D shapes, glow effects, bevel, drop shadows on any element
- Rounded-corner cards used as decorative containers
- Stock-photo handshakes, city skylines, "diverse-team-around-a-table"
- Emoji bullets or decorative dingbats
- **More than one em dash on any single slide.** The em dash is the single most-cited AI punctuation tell (NPR, Rolling Stone, multiple humanizer detectors converge on this). Where you would use a second em dash, switch to a comma, a colon, or two short sentences.

**Counter-patterns:**
- Real property photography only (aerials, drone shots, building exteriors, interior photos)
- Flat color blocks for fills
- 2D charts with one accent color
- Hairline-bordered rectangles for any structural container
- Site plans, floor plates, market maps over abstract imagery
- Sparing punctuation — one em dash max per slide

### Bucket F — Provenance and Numerical Discipline

**Forbidden:**
- Any chart value not explicitly provided in the pre-written content (CIP will hallucinate plausible-looking figures if left to infer)
- Unsourced data points
- Round-looking numbers that read as pre-fabricated ($10M, $50M, 10%, 25%) when the actuals have decimals
- "Industry-leading" / "best-in-class" / "top-performing" without citation
- Date-less stats (every numeric needs an as-of date)

**Counter-patterns:**
- Every chart's data table arrives explicitly in the pre-written content — pull values verbatim
- Source line on every data slide naming issuer + report + as-of date
- Use actual reported figures with the decimals they came with ($9.4M, 11.3%, 47.2%)
- Cite issuer for every market claim
- If a number is unverifiable, mark "TBD — confirm with sponsor" and preserve verbatim

================================================================
STEP 9 — OPERATIONAL RULES (CIP / Office.js context)
================================================================

These rules govern how CIP interacts with its execution environment. Read them once and apply throughout.

1. **Refresh MCP connections before declaring Microsoft unavailable.** If Microsoft 365 / SharePoint MCP appears disconnected, run the MCP refresh first. Do not tell the user "I cannot access SharePoint" without verifying the connection state.

2. **Ignore non-Microsoft MCPs for this deck.** Visual asset retrieval depends on the Microsoft 365 SharePoint/Graph MCP only. Box, Notion, HubSpot, Linear, Atlassian, Asana, monday, Intercom, Canva, Figma, and other connectors are not relevant — do not surface their status as a blocker.

3. **Target shapes by ID + a current-text precondition; treat names as a secondary confirmation only.** Resolve each edit's target by the numeric/GUID shape ID supplied in the pre-written content, and before changing it, verify the shape's CURRENT text matches what the instruction expects — if it doesn't, stop and report rather than editing the wrong shape. Do NOT rely on default master placeholder names (locale-dependent: "Title 1" → "Titel 1" in German PowerPoint). Custom names the content assigns (e.g., "Block_Opportunity") are stable and fine as a confirmation, but the ID + current-text precondition is the authority.

4. **Escape `&` as `&amp;` in any text or XML you write.** Office Open XML requires entity-encoded ampersands. Unescaped `&` in shape text or XML payloads will corrupt the slide.

5. **Acknowledge the markdown-representation limitation.** CIP works on a markdown abstraction of the deck, not on a pixel-accurate visual model. To compensate:
   - Use the explicit position coordinates (x, y, w, h in points) given in the pre-written content rather than relying on inferred placement
   - Use exact hex codes from the locked palette rather than inferred color names
   - Use the exact data tables provided rather than asking CIP to generate plausible figures
   - Trust the per-slide QA gate (Step 6 item 4) to catch overlap, margins, and font-default leak

6. **Edit shapes in place. Never delete-and-rebuild a slide.** Re-creating the slide loses position state, manual color overrides, and any QA-validated work already done. Modify existing shapes via their IDs.

7. **Re-check shape IDs after each `edit_slide_xml` call.** Office.js shape IDs can shift after structural edits. Always re-list shapes before the next edit.

8. **Work in bounded batches; minimize turns.** The add-in is slow and has a per-turn tool-use cap that will halt long sequences ("reached its tool-use limit for this turn"). Compose ONE slide (or a small slide-group) per batch, run that slide's QA gate, then continue. If you hit the tool-use limit mid-job, resume from the next slide — do not restart the deck. Do not make many tiny single-edit turns (each is slow and quota-expensive); fold all of a slide's text + formatting into one batch.

9. **Execute, don't re-compose, where exact values are given.** The pre-written content supplies final strings, hex codes, point coordinates, and data tables. Apply them verbatim. Do not paraphrase pre-written prose, re-derive numbers, or "improve" supplied values — open-ended composing is slower, lower-fidelity, and burns quota.

10. **Charts: build from the supplied data table, then expect a human pass.** Native chart rendering through the add-in is imprecise (series/axis/colors land ~60–70% right). Build the chart from the exact data table provided, apply the monochrome navy/mid-blue spec, and flag it for human review. If the pre-written content marks a data exhibit "place as native table," do that instead — a native table is the most reliable precise data-visual the add-in can place.

11. **Images: place into the provided placeholder; if insertion fails, leave the caption and flag it.** Raster-image insertion is not guaranteed in every build. Attempt the placement at the specified location; if it fails, leave the labeled placeholder caption from the pre-written content in place and report which assets could not be inserted — do NOT generate or substitute decorative imagery, and do not silently skip.

12. **Re-deliver context, don't assume memory.** Your chat history does not persist across a PowerPoint restart and long conversations auto-compact. Everything needed to execute is in THIS prompt block — never rely on "what we discussed earlier."

---

Begin by asking the template-decision question in Step 0. Wait for the user's answer. Then proceed.
