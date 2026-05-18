Pick the layout whose content type matches the slide's purpose. Default to the simpler layout when in doubt — a single-narrative slide is always safer than an over-designed one. Split slides freely if content fights for space; merge when ideas span thin slides.

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

**Why:** Mayer's coherence — narrative without visual chrome lets the prose carry weight. Spatial-contiguity preserved by keeping bolded numerics inline with their context.

**DO:**
- Make each idea-block a complete thought
- Bold the numbers that support the thesis
- Use 13-14pt body, not 11pt — there's room

**DON'T:**
- Wrap prose in cards or boxes
- Add icons before each idea-block
- Use bullets for narrative prose (bullets are for parallel lists, not stories)

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
  - Top label: 9pt Arial all caps `#9AA3B2` (e.g., "GOING-IN CAP RATE")
  - Big number: 26-36pt Aptos navy `#1F3A5F` bold (e.g., "9.0%")
  - Sub-detail (optional): 10-11pt Arial italic gray `#485269` (e.g., "Yr 1 NOI / $65M PP")
- Below the strip: optional narrative explaining context, full-width 13-14pt Garamond

**Why:** Dual coding — big numerics with minimal label gives one mental anchor per metric. Gestalt proximity groups label+number+detail visually.

**DO:**
- Equal column widths and equal gaps
- Center all three elements within each column

**DON'T:**
- Use rounded corners on the panels
- Add icons above the labels
- Mix column widths

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

**Why:** Mayer's spatial contiguity (d=1.10) — visual and supporting text sit next to each other. Cuts split-attention cost.

**DO:**
- Keep image rectangular, hard edges (no rounded corners)
- Caption directly under image, italic gray
- Right zone narrative scans the image's content — the two zones reinforce one idea

**DON'T:**
- Wrap the image in a rounded frame
- Add icons in the right zone
- Make the two zones tell different stories

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

**Why:** Tufte data-ink — photos ARE the content; chrome around them is wasted ink.

**DO:**
- Crop photos to consistent aspect ratio
- Equal cell sizes

**DON'T:**
- Round photo corners
- Float captions in separate boxes
- Mix photo aspect ratios within the grid

────────────────────────────────────────────────────────────────
LAYOUT 5 — MAP-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** Asset Location, Neighborhood Map, Adjacent Developments map. Content is geographic positioning where location IS the message.

**Structure:**
- Map fills ~70% of content area (x=60 to x=700, y=140 to y=490)
- Right zone (x=720 to x=900, y=140 to y=490): legend, pin descriptions, or context narrative
- Numbered pins ON the map, labeled inline next to each pin OR in the right legend with matching numbers
- Caption italic 8pt below map ("Source: Google Maps, V23 markup" or similar)

**Why:** Mayer's spatial contiguity (the strongest effect in the literature, d=1.10) — annotations on the map are far more memorable than annotations across the slide from the map.

**DO:**
- Annotate ON the map where possible
- Number-match pins to legend entries when legend is unavoidable
- Show actual scale and orientation

**DON'T:**
- Float labels in slide corners
- Use icons for pins; numbered circles or chevrons are clearer
- Crop so tight the reader can't orient

────────────────────────────────────────────────────────────────
LAYOUT 6 — TABLE-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** Rent Roll, Comparable Sales, Comparable Leases, Operating Financials (5-year build), Returns Summary detail. Content is structured data that needs to be scanned and compared.

**Structure:**
- Headline takeaway at top (Garamond 13-14pt italic, y=120)
- Table fills the rest: x=60 to x=900, y=160 to y=490
- Table style:
  - Hairline top and bottom rules (0.75pt navy)
  - Header row: navy fill `#1F3A5F`, white Aptos 11-12pt bold
  - Thin rule under header row (0.5pt)
  - No vertical lines, no interior horizontal lines (or very subtle 5% navy alternating shading for dense rows)
- Column alignment:
  - First column (identifier): left-aligned
  - Numeric columns: right-aligned
  - Date / unit columns: center-aligned
- Source line italic 8pt at y=502

**Why:** Tufte data-ink — the table IS the content. Erase every gridline, border, or decoration that doesn't help the reader.

**DO:**
- Right-align all numerics
- Use parens for negatives (8.5)
- Abbreviate currency: $63M, $114/SF
- Keep column count to 5-7 (the sweet spot)

**DON'T:**
- Vertical lines between columns
- Color-code rows by category (sort by the relevant metric instead)
- Use icons in cells
- Wrap headers across multiple lines unless necessary

────────────────────────────────────────────────────────────────
LAYOUT 7 — CHART-DOMINANT
────────────────────────────────────────────────────────────────

**Use when:** NOI Build, Vacancy Trend, Returns Trajectory, Cash Flow waterfall. Content is a single chart that tells a quantitative story.

**Structure:**
- Headline takeaway at top
- Chart fills ~70% of slide: x=60 to x=900, y=160 to y=420
- Source line italic 8pt directly under the chart at y=440
- Optional brief narrative below chart: 1-2 lines, y=460-490

**Why:** Picture Superiority — a well-built chart conveys a relationship prose can't. Mayer spatial-contiguity — labels on the data points, not in a legend.

**DO:**
- Label bars/lines directly (e.g., "$5.83M" on the Year 1 bar)
- Flat fills, navy primary `#1F3A5F`, mid-blue secondary `#5B7FA8`
- Horizontal-only gridlines if any, light gray, sparingly
- Show source

**DON'T:**
- Legend across the slide from the chart
- 3D effects, gradients, drop shadows, chart borders
- Bevel or glow on data series

────────────────────────────────────────────────────────────────
LAYOUT 8 — TWO-COLUMN COMPARISON
────────────────────────────────────────────────────────────────

**Use when:** Base case vs. Stress case, Asset vs. Comp, Before vs. After. Content is a side-by-side comparison.

**Structure:**
- Two equal columns: x=60 to x=470 and x=490 to x=900, y=140 to y=490
- Each column has a header bar (navy fill, white Aptos 12-14pt bold, ~25pt tall)
- Below header: structured content (table, KPI list, prose paragraph) — same structure in both columns
- Equal alignment of comparable elements across columns

**Why:** Gestalt proximity + similarity — readers compare matched rows when the two sides have identical structure.

**DO:**
- Identical row structures in both columns (rent on row 1 in left = rent on row 1 in right)
- Highlight the delta with bold or with the sparing red on the "worse" side

**DON'T:**
- Different row counts across columns
- Different fonts or sizes across columns
- Stack the two as full-width sections (defeats the comparison)

────────────────────────────────────────────────────────────────
LAYOUT 9 — INVESTMENT HIGHLIGHTS (bullet list with bold headers)
────────────────────────────────────────────────────────────────

**Use when:** Investment Highlights slide ONLY. This is a specific Vanadium pattern — NOT a card grid.

**Structure:**
- Headline takeaway at top
- 4-7 highlight blocks stacked vertically
- Each block:
  - **Bold Garamond navy** thesis statement (one line) — e.g., "**Basis is the deal.**"
  - Body text below it: 13pt Garamond `#485269`, 2 lines explaining the thesis with bolded numerics
  - 8-10pt spacer to next block

**Why:** The bold-then-body rhythm makes the thesis scannable in 10 seconds (read just the bolds) and supportable in 30 seconds (read the bodies). Mayer signaling.

**DO:**
- Bold only the thesis statement line, not the whole block
- Sentence case in the thesis statement
- Keep each body to 2 lines max

**DON'T:**
- Card grids
- Icons before each highlight
- Numbered highlights
- Same opening word ("Strong," "Robust," "Compelling") on every highlight — vary

────────────────────────────────────────────────────────────────
LAYOUT 10 — FULL-BLEED VISUAL (rendering or floor plan)
────────────────────────────────────────────────────────────────

**Use when:** Building renderings, floor plans, large architectural diagrams. Content is one large visual that needs to dominate.

**Structure:**
- Visual fills nearly the full slide: x=0 to x=960, y=80 to y=502 (extends past the standard margin)
- Minimal overlay: section eyebrow at y=38, section title at y=54 (visible against the visual, or with a small white overlay box if needed for legibility)
- Caption italic 8pt at y=502
- Footer bar unchanged

**Why:** Some content demands full visual real estate. A building rendering should not be shrunk to fit a 60pt margin.

**DO:**
- Note the deviation from the margin grid explicitly in your section depth plan
- Ensure caption is legible against the visual (white background bar if needed)
- Preserve the footer bar

**DON'T:**
- Force a rendering into a half-and-half layout when it deserves the full slide
- Crop the rendering to fit a non-standard aspect

────────────────────────────────────────────────────────────────
LAYOUT 11 — SECTION DIVIDER
────────────────────────────────────────────────────────────────

**Use when:** Major section transitions (e.g., between "Asset" and "Market," or "Market" and "Financials"). Optional — only if the deck is long enough to warrant breaks.

**Structure:**
- Mostly empty slide
- Section name in large Garamond ALL CAPS or small caps, navy `#1F3A5F`, centered both axes (or left-aligned at x=60, y=270)
- Thin horizontal rule below the section name, navy, ~200pt wide
- Footer bar unchanged
- No subtitle, no narrative

**Why:** Breathing room. Signals chapter change without burning content density.

**DO:**
- Use sparingly — only when content volume justifies
- Keep all dividers visually identical (same position, same size, same treatment)

**DON'T:**
- Stock photos behind the section name
- Gradient backgrounds
- Icons next to the section name

────────────────────────────────────────────────────────────────
LAYOUT 12 — HYBRID: NARRATIVE + EMBEDDED CHART
────────────────────────────────────────────────────────────────

**Use when:** Operating Financials, Returns Summary. Content needs both a story-prose explanation AND a quantitative anchor chart.

**Structure:**
- Top half (y=140 to y=300): narrative prose (Garamond 13-14pt, 2-3 idea-blocks)
- Bottom half (y=320 to y=480): chart spanning x=60 to x=900
- Source line italic 8pt at y=495 under the chart

**Why:** Tells the story AND shows the data on one page. Mayer coherence (narrative carries the takeaway), Tufte data-ink (chart shows the underlying numbers).

**DO:**
- Keep prose tight — this isn't the place for 4 idea-blocks
- Label chart data directly

**DON'T:**
- Make the chart smaller than ~150pt tall (illegible)
- Run prose past y=300 (it'll crowd the chart)

────────────────────────────────────────────────────────────────
LAYOUT-SELECTION CHEAT SHEET
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
| Big visual (rendering, floor plan) | Layout 10 — Full-bleed |
| Major section break | Layout 11 — Divider |
| Prose + supporting chart | Layout 12 — Hybrid |

When proposing the section depth plan in Step 6 of the build prompt, name the layout per slide. Document any deviation from the default in the cheat sheet with a one-sentence rationale.
