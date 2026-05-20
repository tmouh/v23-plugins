════════════════════════════════════════════════════════════════
LAYOUT VARIETY MANDATE (READ FIRST — OVERRIDES THE 12-LAYOUT CATALOG BELOW)
════════════════════════════════════════════════════════════════

The twelve layouts below are a starting library, not a ceiling. Treat every slide as a fresh design problem and invent the arrangement the information actually demands. Translate, rotate, resize, re-weight, invert, or hybridize any canonical layout, and reach for arrangements that aren't in the catalog at all:

- a tall portrait photo on the right two-fifths beside three stacked stat blocks left-aligned in the remaining three-fifths
- a horizontal photo strip across the top third with a four-column rent-roll table beneath
- a centered 40pt headline number flanked by two narrow vertical prose columns on either side
- a quadrant grid where each cell mixes one stat, one one-line caption, and one micro-chart
- a building elevation drawn as a tall column with floor-by-floor stacking-plan blocks fanning out to its right
- prose at top in a 2-1-3 weighted three-column rhythm above a half-height chart
- a single big number anchored hard to the right edge while supporting prose left-aligned eats the remaining two-thirds
- a navy header bar that runs only halfway across to make space for a chart bleeding into the title row
- a five-pin annotated map at 60% width with a vertical stack of comp cards filling the other 40%

**Aim for at least seven distinct arrangements across the deck. Never let two consecutive content slides share the same zone pattern.**

When the pre-written content (from Claude Code) suggests a layout in plain English ("large left photo, narrow right stat column, bottom caption strip"), use it as the starting point but improve where a smarter arrangement reads faster, hits harder, or sits more elegantly on the page.

Before composing each slide, ask: is there a smarter arrangement than the default that lets this particular set of facts read faster, hit harder, or sit more elegantly on the page? If yes, build the smarter one and document the deviation in one sentence at the end of the section.

Repetition of layout is the single biggest tell that a deck was machine-built. Thoughtful, content-weighted variety — every slide earning its own composition — is the single biggest signal of editorial care.

The layout choice for any given slide should be a direct reflection of the type of information that slide is conveying. The pre-written content provides the data; you provide the arrangement.

════════════════════════════════════════════════════════════════
THE 12 CANONICAL LAYOUTS (Starting Library)
════════════════════════════════════════════════════════════════

Pick or adapt the layout whose content type matches the slide's purpose. Default to the simpler arrangement when in doubt — a single-narrative slide is always safer than an over-designed one. Split slides freely if content fights for space; merge when ideas span thin slides. Hybridize freely per the MANDATE above.

────────────────────────────────────────────────────────────────
LAYOUT 1 — SINGLE-NARRATIVE (text-heavy)
────────────────────────────────────────────────────────────────

**Use when:** Executive Summary, Project Background, Business Plan narrative, Sponsor Background. Content is prose-driven — telling a story about the deal.

**Structure:**
- Full-width content area: x=60 to x=900, y=140 to y=480
- 2-4 idea-blocks of Garamond 13-14pt prose, each 2-4 lines
- 8pt blank paragraph spacer between idea-blocks
- Bold inline for key numerics and proper nouns only
- Optional: small KPI strip at the bottom (y=420-470) with 3-4 supporting stats — anchors the prose with concrete numbers

**DO:** make each idea-block a complete thought; bold the numbers that support the thesis; use 13-14pt body, not 11pt.

**DON'T:** wrap prose in cards or boxes; add icons before each idea-block; use bullets for narrative prose.

────────────────────────────────────────────────────────────────
LAYOUT 2 — KPI STRIP (stats-driven)
────────────────────────────────────────────────────────────────

**Use when:** Transaction Snapshot, Returns Summary, Asset Overview header. Content is a small set of key metrics that need to read instantly.

**Structure:**
- KPI strip occupies y=180 to y=320 (or y=140 to y=280 if no headline takeaway above)
- 3-5 equal-width columns from x=60 to x=900
- Column width = (840 − (N−1)×gap) / N, where gap = 12pt for 4-col, 8pt for 5-col
- Each column = pale-blue panel `#E8EEF6` fill, no border, no rounded corners
- Per column, three stacked elements (centered horizontally):
  - Top label: 9pt Arial all caps `#9AA3B2`
  - Big number: 26-36pt Aptos navy `#1F3A5F` bold
  - Sub-detail (optional): 10-11pt Arial italic gray `#485269`
- Below the strip: optional narrative explaining context, full-width 13-14pt Garamond

**DO:** equal column widths and equal gaps; center all three elements within each column.

**DON'T:** rounded corners on the panels; icons above the labels; mixed column widths.

────────────────────────────────────────────────────────────────
LAYOUT 3 — HALF-AND-HALF (image + text)
────────────────────────────────────────────────────────────────

**Use when:** Asset Overview, Adjacent Developments, Sponsor Track Record case study, Submarket Residential Overview. Content needs one strong visual anchor and parallel narrative.

**Structure:**
- Two zones at 50/50 split with a 20pt gutter:
  - Left zone (x=60 to x=470, y=140 to y=490): image, rendering, or chart
  - Right zone (x=490 to x=900, y=140 to y=490): narrative prose or stat list
- Image fills its zone or maintains aspect ratio centered; caption italic 8pt directly below image
- Right zone: 13-14pt Garamond prose; may include a small vertical KPI mini-strip (2-3 inline stats)

**DO:** keep image rectangular, hard edges (no rounded corners); caption directly under image; right zone narrative scans the image's content.

**DON'T:** wrap the image in a rounded frame; add icons in the right zone; make the two zones tell different stories.

────────────────────────────────────────────────────────────────
LAYOUT 4 — PHOTO GRID
────────────────────────────────────────────────────────────────

**Use when:** Asset Overview — Photos, Neighborhood Amenities, Sponsor Track Record (multiple prior deals). Content is multiple visual elements with brief captions.

**Structure (pick by photo count):**
- 4 photos: 2×2, each ~410pt wide × 175pt tall
- 6 photos: 3×2, each ~270pt wide × 175pt tall
- 9 photos: 3×3, each ~270pt wide × 115pt tall
- Equal cell size and equal gutters (10-12pt)
- Each cell: hard-edge rectangle, photo fills cell
- Caption italic 8pt directly under each photo, inside the grid

**DO:** crop photos to consistent aspect ratio; equal cell sizes.

**DON'T:** round photo corners; float captions in separate boxes; mix photo aspect ratios within the grid.

────────────────────────────────────────────────────────────────
LAYOUT 5 — MAP-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** Asset Location, Neighborhood Map, Adjacent Developments map. Content is geographic positioning where location IS the message.

**Structure:**
- Map fills ~70% of content area (x=60 to x=700, y=140 to y=490)
- Right zone (x=720 to x=900, y=140 to y=490): legend, pin descriptions, or context narrative
- Numbered pins ON the map, labeled inline next to each pin OR in the right legend with matching numbers
- Caption italic 8pt below map ("Source: Google Maps, V23 markup" or similar)

**DO:** annotate ON the map where possible; number-match pins to legend; show actual scale and orientation.

**DON'T:** float labels in slide corners; use icons for pins (numbered circles or chevrons are clearer); crop so tight the reader can't orient.

────────────────────────────────────────────────────────────────
LAYOUT 6 — TABLE-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** Rent Roll, Comparable Sales, Comparable Leases, Operating Financials, Returns Summary detail. Content is structured data that needs to be scanned and compared.

**Structure:**
- Headline takeaway at top (Garamond 13-14pt italic, y=120)
- Table fills the rest: x=60 to x=900, y=160 to y=490
- Hairline top and bottom rules (0.75pt navy)
- Header row: navy fill `#1F3A5F`, white Aptos 11-12pt bold
- Thin rule under header row (0.5pt)
- No vertical lines, no interior horizontal lines (or very subtle 5% navy alternating shading for dense rows)
- First column (identifier): left-aligned
- Numeric columns: right-aligned
- Date / unit columns: center-aligned
- Source line italic 8pt at y=502

**DO:** right-align all numerics; use parens for negatives; abbreviate currency; keep column count to 5-7.

**DON'T:** vertical lines between columns; color-code rows by category; use icons in cells; wrap headers across multiple lines unless necessary.

────────────────────────────────────────────────────────────────
LAYOUT 7 — CHART-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** NOI Build, Vacancy Trend, Returns Trajectory, Cash Flow waterfall. Content is a single chart that tells a quantitative story.

**Structure:**
- Headline takeaway at top
- Chart fills ~70% of slide: x=60 to x=900, y=160 to y=420
- Source line italic 8pt directly under the chart at y=440
- Optional brief narrative below chart: 1-2 lines, y=460-490

**DO:** label bars/lines directly; flat fills, navy primary `#1F3A5F`, mid-blue secondary `#5B7FA8`; horizontal-only gridlines sparingly.

**DON'T:** legend across the slide from the chart; 3D effects, gradients, drop shadows, chart borders; bevel or glow on data series.

────────────────────────────────────────────────────────────────
LAYOUT 8 — TWO-COLUMN COMPARISON
────────────────────────────────────────────────────────────────

**Use when:** Base case vs. Stress case, Asset vs. Comp, Before vs. After. Content is a side-by-side comparison.

**Structure:**
- Two equal columns: x=60 to x=470 and x=490 to x=900, y=140 to y=490
- Each column has a header bar (navy fill, white Aptos 12-14pt bold, ~25pt tall)
- Below header: structured content (table, KPI list, prose paragraph) — same structure in both columns
- Equal alignment of comparable elements across columns

**DO:** identical row structures in both columns; highlight the delta with bold or sparing red on the worse side.

**DON'T:** different row counts across columns; different fonts or sizes; stack the two as full-width sections.

────────────────────────────────────────────────────────────────
LAYOUT 9 — INVESTMENT HIGHLIGHTS (bullet list with bold headers)
────────────────────────────────────────────────────────────────

**Use when:** Investment Highlights slide ONLY. This is a specific Vanadium pattern — NOT a card grid.

**Structure:**
- Headline takeaway at top
- 4-7 highlight blocks stacked vertically
- Each block:
  - **Bold Garamond navy** thesis statement (one line)
  - Body text below it: 13pt Garamond `#485269`, 2 lines explaining the thesis with bolded numerics
  - 8-10pt spacer to next block

**DO:** bold only the thesis statement line, not the whole block; sentence case in the thesis statement; keep each body to 2 lines max.

**DON'T:** card grids; icons before each highlight; numbered highlights; same opening word ("Strong," "Robust," "Compelling") on every highlight.

────────────────────────────────────────────────────────────────
LAYOUT 10 — FULL-BLEED VISUAL (rendering, floor plan, aerial)
────────────────────────────────────────────────────────────────

**Use when:** Building renderings, floor plans, large architectural diagrams, drone-shot aerials. Content is one large visual that needs to dominate.

**Structure:**
- Visual fills nearly the full slide: x=0 to x=960, y=80 to y=502 (extends past the standard margin)
- Minimal overlay: section eyebrow at y=38, section title at y=54 (visible against the visual, or with a small white overlay box if needed for legibility)
- Caption italic 8pt at y=502
- Footer bar unchanged

────────────────────────────────────────────────────────────────
LAYOUT 11 — SECTION DIVIDER
────────────────────────────────────────────────────────────────

**Use when:** Major section transitions. Optional — only if the deck is long enough to warrant breaks.

**Structure:**
- Mostly empty slide
- Section name in large Garamond ALL CAPS or small caps, navy `#1F3A5F`, centered both axes (or left-aligned at x=60, y=270)
- Thin horizontal rule below the section name, navy, ~200pt wide
- Footer bar unchanged
- No subtitle, no narrative

────────────────────────────────────────────────────────────────
LAYOUT 12 — HYBRID: NARRATIVE + EMBEDDED CHART
────────────────────────────────────────────────────────────────

**Use when:** Operating Financials, Returns Summary. Content needs both story-prose AND a quantitative anchor chart.

**Structure:**
- Top half (y=140 to y=300): narrative prose (Garamond 13-14pt, 2-3 idea-blocks)
- Bottom half (y=320 to y=480): chart spanning x=60 to x=900
- Source line italic 8pt at y=495 under the chart

────────────────────────────────────────────────────────────────
DEFAULT MAPPING (STARTING POINT — DEVIATE PER THE MANDATE ABOVE)
────────────────────────────────────────────────────────────────

| Content type | Default layout |
|---|---|
| Story prose | Layout 1 — Single-narrative |
| Small set of key metrics | Layout 2 — KPI strip |
| One visual + parallel story | Layout 3 — Half-and-half |
| Multiple photos | Layout 4 — Photo grid |
| Geographic positioning | Layout 5 — Map-dominant |
| Rent roll, comps, financials | Layout 6 — Table |
| Single chart story | Layout 7 — Chart |
| Side-by-side scenarios | Layout 8 — Comparison |
| Investment thesis bullets | Layout 9 — Highlights (specific pattern) |
| Big visual (rendering, floor plan, aerial) | Layout 10 — Full-bleed |
| Major section break | Layout 11 — Divider |
| Prose + supporting chart | Layout 12 — Hybrid |

This mapping is a starting point only. The MANDATE above governs final composition — every slide deserves a composition that reflects its specific content, not a checkbox match against this table.
