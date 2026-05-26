"""
build-deck.py — CC-native NEW-BUILD generator for v23:om-builder.

Generates a Vanadium-grade .pptx directly from a pre-written content spec, by
cloning the house template (assets/v23-template.pptx — inherits the real master,
theme, fonts, color scheme, and the navy footer bar / page numbers) and rendering
the core DATA-DRIVEN layouts deterministically. This is the new-build counterpart
to apply-revision-edits.py: CC owns the file; CIP is reserved for visual polish
and bespoke-visual slides (full-bleed hero, annotated aerial, renderings, image
placement) the JS API can't do well.

COVERAGE (the deterministic core — ~80% of an OM):
  cover, kpi_strip, narrative, table, chart, two_column, section_divider.
NOT COVERED (route to CIP / manual): full-bleed photo heroes, annotated aerials,
maps, renderings, image placement, stacking plans, scatter/quadrant exhibits.
The generator marks any slide whose "layout" it doesn't implement as a labeled
placeholder slide so the deck is complete and CIP knows exactly what to finish.

House style + voice are NOT re-derived here — they live in prompt-template.md
(Step 2 visual spec) and house-voice.md (writing voice). CC must have already
written the content in-voice before calling this; the generator only places it.

Content spec (JSON):
{
  "template": "<path to v23-template.pptx>",   # optional; defaults to ../assets/
  "target": "<out.pptx>",
  "deal_name": "NPV Florida IOS Strategy",      # footer attribution
  "slides": [
    {"layout":"cover","eyebrow":"NORTH PARK VENTURES | MAY 2026",
       "title":"Industrial Outdoor Storage Strategy",
       "subtitle":"Programmatic Equity Partnership Opportunity — Florida",
       "tagline":"$50M Equity Raise | Sponsored by North Park Ventures"},
    {"layout":"kpi_strip","eyebrow":"EXECUTIVE SUMMARY","title":"…","takeaway":"…",
       "kpis":[{"value":"$50M","label":"LP EQUITY ASK"}, ...], "source":"…"},
    {"layout":"narrative","eyebrow":"…","title":"…","takeaway":"…",
       "blocks":[{"lead":"THE OPPORTUNITY","body":"…"}, ...], "source":"…"},
    {"layout":"table","eyebrow":"…","title":"…","takeaway":"…",
       "table":{"header":[...],"rows":[[...],...]}, "source":"…"},
    {"layout":"chart","eyebrow":"…","title":"…","takeaway":"…",
       "chart":{"type":"line","categories":[...],"series":[["IOS",[...]],...]}, "source":"…"},
    {"layout":"two_column","eyebrow":"…","title":"…","takeaway":"…",
       "left":{"head":"…","body":"…"}, "right":{"head":"…","body":"…"}, "source":"…"},
    {"layout":"section_divider","title":"SPONSOR"}
  ]
}

Usage:
  python build-deck.py spec.json
"""

import argparse
import json
import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# ── House style constants (verified from production decks + prompt-template Step 2) ──
FONT = "Garamond"
NAVY = "1F3A5F"
NAVY_DARK = "0F2540"
MIDBLUE = "5B7FA8"
PANEL = "E8EEF6"
BODY = "485269"
MUTED = "9AA3B2"

MARGIN_L = 0.83
USABLE_W = 11.67          # 0.83 .. 12.5
EYEBROW_Y, EYEBROW_H = 0.53, 0.19
TITLE_Y, TITLE_H = 0.75, 0.57
TAKEAWAY_Y, TAKEAWAY_H = 1.33, 0.32
BODY_TOP = 1.94
SOURCE_Y, SOURCE_H = 6.97, 0.17

CHART_TYPES = {
    "line": XL_CHART_TYPE.LINE,
    "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "bar": XL_CHART_TYPE.BAR_CLUSTERED,
    "pie": XL_CHART_TYPE.PIE,
}


def _hex(c):
    return RGBColor.from_string(c)


def _box(slide, x, y, w, h, name=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.text_frame.word_wrap = True
    if name:
        tb.name = name
    return tb


def _set(tb, text, size, color=BODY, bold=False, italic=False, caps=False,
         align=PP_ALIGN.LEFT, font=FONT):
    tf = tb.text_frame
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line.upper() if caps else line
        f = r.font
        f.name = font
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = _hex(color)
    return tb


def _header(slide, s):
    """Eyebrow + title + takeaway — the standard top-of-slide block."""
    if s.get("eyebrow"):
        _set(_box(slide, MARGIN_L, EYEBROW_Y, USABLE_W, EYEBROW_H, "Eyebrow"),
             s["eyebrow"], 9, MUTED, bold=False, caps=True)
    if s.get("title"):
        _set(_box(slide, MARGIN_L, TITLE_Y, USABLE_W, TITLE_H, "Title"),
             s["title"], 24, NAVY, bold=True)
    if s.get("takeaway"):
        _set(_box(slide, MARGIN_L, TAKEAWAY_Y, USABLE_W, TAKEAWAY_H, "Takeaway"),
             s["takeaway"], 13, BODY, italic=True)


def _source(slide, s):
    if s.get("source"):
        _set(_box(slide, MARGIN_L, SOURCE_Y, USABLE_W, SOURCE_H, "Source"),
             s["source"], 8, MUTED, italic=True)


# ── Layout renderers ────────────────────────────────────────────────────────
def render_cover(slide, s):
    # Text-only cover. The hero background image is a CIP/manual add (note it).
    _set(_box(slide, MARGIN_L, 4.69, 7.5, 0.28, "CoverEyebrow"),
         s.get("eyebrow", ""), 11, NAVY, bold=True, caps=True)
    _set(_box(slide, MARGIN_L, 4.95, 7.5, 1.38, "CoverTitle"),
         s.get("title", ""), 30, NAVY, bold=True)
    _set(_box(slide, MARGIN_L, 6.35, 7.5, 0.35, "CoverSubtitle"),
         s.get("subtitle", ""), 14, BODY)
    if s.get("tagline"):
        _set(_box(slide, MARGIN_L, 6.69, 7.5, 0.28, "CoverTagline"),
             s["tagline"], 11, MIDBLUE, bold=True)
    slide.notes_slide.notes_text_frame.text = "[CIP/manual: place full-bleed hero image behind the cover title block.]"


def render_kpi_strip(slide, s):
    _header(slide, s)
    kpis = s.get("kpis", [])
    n = max(len(kpis), 1)
    gap = 0.13
    tile_w = (USABLE_W - (n - 1) * gap) / n
    for i, k in enumerate(kpis):
        x = MARGIN_L + i * (tile_w + gap)
        # value
        _set(_box(slide, x, BODY_TOP + 0.1, tile_w, 0.5, f"KPI_Value_{i+1}"),
             k.get("value", ""), 20, NAVY, bold=True, align=PP_ALIGN.CENTER)
        # label
        _set(_box(slide, x, BODY_TOP + 0.62, tile_w, 0.4, f"KPI_Label_{i+1}"),
             k.get("label", ""), 9, MUTED, caps=True, align=PP_ALIGN.CENTER)
    _source(slide, s)


def render_narrative(slide, s):
    _header(slide, s)
    blocks = s.get("blocks", [])
    y = BODY_TOP
    block_h = min(1.5, (6.6 - BODY_TOP) / max(len(blocks), 1))
    for i, b in enumerate(blocks):
        tb = _box(slide, MARGIN_L, y, USABLE_W, block_h, f"Block_{i+1}")
        tf = tb.text_frame
        p = tf.paragraphs[0]
        if b.get("lead"):
            r = p.add_run(); r.text = b["lead"] + " — "
            r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = _hex(NAVY)
        r2 = p.add_run(); r2.text = b.get("body", "")
        r2.font.name = FONT; r2.font.size = Pt(13); r2.font.color.rgb = _hex(BODY)
        y += block_h
    _source(slide, s)


def render_table(slide, s):
    _header(slide, s)
    t = s.get("table", {})
    header = t.get("header", [])
    rows = t.get("rows", [])
    n_rows = len(rows) + (1 if header else 0)
    n_cols = max(len(header), max((len(r) for r in rows), default=0))
    if n_rows == 0 or n_cols == 0:
        return
    gframe = slide.shapes.add_table(n_rows, n_cols, Inches(MARGIN_L), Inches(BODY_TOP),
                                    Inches(USABLE_W), Inches(0.35 * n_rows))
    tbl = gframe.table
    r0 = 0
    if header:
        for c, htext in enumerate(header):
            cell = tbl.cell(0, c)
            cell.text = str(htext)
            for para in cell.text_frame.paragraphs:
                for run in para.runs:
                    run.font.name = FONT; run.font.size = Pt(11); run.font.bold = True
                    run.font.color.rgb = _hex("FFFFFF")
            cell.fill.solid(); cell.fill.fore_color.rgb = _hex(NAVY)
        r0 = 1
    for ri, row in enumerate(rows):
        for c in range(n_cols):
            cell = tbl.cell(ri + r0, c)
            cell.text = str(row[c]) if c < len(row) else ""
            for para in cell.text_frame.paragraphs:
                for run in para.runs:
                    run.font.name = FONT; run.font.size = Pt(10); run.font.color.rgb = _hex(BODY)
    _source(slide, s)


def render_chart(slide, s):
    _header(slide, s)
    c = s.get("chart", {})
    data = CategoryChartData()
    data.categories = c.get("categories", [])
    for name, vals in c.get("series", []):
        data.add_series(name, tuple(vals))
    ctype = CHART_TYPES.get(c.get("type", "line"), XL_CHART_TYPE.LINE)
    slide.shapes.add_chart(ctype, Inches(MARGIN_L), Inches(BODY_TOP),
                           Inches(USABLE_W), Inches(3.6), data)
    _source(slide, s)


def render_two_column(slide, s):
    _header(slide, s)
    half = (USABLE_W - 0.33) / 2
    for side, x in (("left", MARGIN_L), ("right", MARGIN_L + half + 0.33)):
        col = s.get(side, {})
        if col.get("head"):
            _set(_box(slide, x, BODY_TOP, half, 0.3, f"{side}_head"),
                 col["head"], 13, NAVY, bold=True)
        if col.get("body"):
            _set(_box(slide, x, BODY_TOP + 0.35, half, 4.0, f"{side}_body"),
                 col["body"], 13, BODY)
    _source(slide, s)


def render_section_divider(slide, s):
    _set(_box(slide, MARGIN_L, 3.0, USABLE_W, 1.0, "DividerTitle"),
         s.get("title", ""), 32, NAVY, bold=True, caps=True)


def render_placeholder(slide, s):
    """A slide whose layout the generator doesn't implement — leave a clear,
    labeled placeholder so the deck is complete and CIP knows what to finish."""
    _header(slide, s)
    label = f"[ CIP / MANUAL: {s.get('layout','?')} ]  {s.get('note','')}"
    _set(_box(slide, MARGIN_L, 3.0, USABLE_W, 1.0, "Placeholder"),
         label, 14, MIDBLUE, bold=True, align=PP_ALIGN.CENTER)
    _source(slide, s)


RENDERERS = {
    "cover": render_cover,
    "kpi_strip": render_kpi_strip,
    "narrative": render_narrative,
    "table": render_table,
    "chart": render_chart,
    "two_column": render_two_column,
    "section_divider": render_section_divider,
}

# Layouts the generator does NOT implement → placeholder + flagged for CIP.
CIP_LAYOUTS = {"full_bleed", "aerial", "map", "rendering", "photo_grid",
               "stacking_plan", "scatter", "quadrant", "annotated_aerial"}


def build(spec):
    here = os.path.dirname(os.path.abspath(__file__))
    template = spec.get("template") or os.path.join(here, "..", "assets", "v23-template.pptx")
    template = os.path.abspath(template)
    if not os.path.isfile(template):
        raise SystemExit(f"ERROR: template not found: {template} (run make-template.py first)")
    prs = Presentation(template)
    # find the Blank layout (house pattern: manual shapes on Blank)
    blank = None
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout.name == "Blank":
                blank = layout
                break
    if blank is None:
        blank = prs.slide_masters[0].slide_layouts[-1]

    report = []
    for i, s in enumerate(spec["slides"], 1):
        slide = prs.slides.add_slide(blank)
        lay = s.get("layout", "narrative")
        if lay in RENDERERS:
            RENDERERS[lay](slide, s)
            report.append(f"slide {i}: {lay} (rendered)")
        elif lay in CIP_LAYOUTS:
            render_placeholder(slide, s)
            report.append(f"slide {i}: {lay} -> PLACEHOLDER (route to CIP)")
        else:
            render_placeholder(slide, s)
            report.append(f"slide {i}: UNKNOWN layout '{lay}' -> PLACEHOLDER")
    prs.save(spec["target"])
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate a Vanadium-grade .pptx from a content spec.")
    p.add_argument("spec", help="Path to JSON content spec.")
    args = p.parse_args(argv)
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    report = build(spec)
    print("\n".join(report))
    print(f"\nGenerated {len(report)} slides -> {spec['target']}")
    print("NOTE: structure/text/geometry are deterministic; open the file to judge VISUAL quality.")
    print("Placeholder slides are flagged above — finish those in PowerPoint/CIP.")


if __name__ == "__main__":
    main()
