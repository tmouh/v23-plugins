"""
extract-pptx-inventory.py — Shape inventory extractor for v23:om-builder revision mode.

A .pptx is a ZIP archive of XML files; each slide lives at ppt/slides/slideN.xml.
This script unzips a target .pptx into a working folder and emits a structured
inventory of every slide: slide number, layout name, every shape's ID, name,
position (in inches), placeholder type, picture/chart/table tag, and current
text content (with paragraph breaks preserved).

CC runs this in Phase 3 of the om-builder runbook when revision mode is active.
The output is the source of truth for the shape-level edit script CC will hand
to CIP — every "Action N.M" instruction references a shape ID emitted here.

Usage:
    python extract-pptx-inventory.py <path-to-pptx> [--extract-dir DIR] [--out FILE]

    Example:
        python extract-pptx-inventory.py "...\\NPV-Florida-IOS - v2.pptx"

Outputs:
    <extract-dir>/                       — unzipped .pptx contents
    <extract-dir>/inventory.txt          — preview inventory (text snippets up to 200 chars)
    <extract-dir>/inventory-fulltext.txt — full inventory (complete shape text)

The two files differ only in how much text per shape is shown. The preview is
optimized for fast human scanning; the full-text version is the version CC
should reference when authoring "current text" preconditions in the edit script.

Encoding: outputs are UTF-8. The script writes to files rather than stdout
because cp1252 (Windows default console encoding) cannot encode em-dashes,
en-dashes, and superscript characters that frequently appear in V23 decks.
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}

EMU_PER_INCH = 914400.0


def emu_to_in(v):
    try:
        return round(int(v) / EMU_PER_INCH, 2)
    except (TypeError, ValueError):
        return None


def get_text(elt):
    """Join all <a:t> descendants, preserving paragraph breaks as newlines."""
    if elt is None:
        return ""
    pieces = []
    for para in elt.findall(".//a:p", NS):
        line = "".join(t.text or "" for t in para.findall(".//a:t", NS))
        pieces.append(line)
    return "\n".join(p for p in pieces if p.strip() != "")


def _font_color(rPr):
    """Pull a hex color from <a:solidFill><a:srgbClr val=...> on a run-properties element."""
    if rPr is None:
        return None
    srgb = rPr.find("a:solidFill/a:srgbClr", NS)
    if srgb is not None:
        return "#" + srgb.attrib.get("val", "")
    scheme = rPr.find("a:solidFill/a:schemeClr", NS)
    if scheme is not None:
        return "scheme:" + scheme.attrib.get("val", "")
    return None


def get_runs(txBody):
    """Return run-level formatting for every run in a txBody.

    Each run: {text, font, size_pt, bold, italic, color}. Sizes are points
    (the XML stores 1/100 pt in the sz attribute). Returns [] if no runs.
    This is what lets CC author edit-script actions that specify exact
    formatting for new shapes instead of telling CIP to "match the style."
    """
    if txBody is None:
        return []
    runs = []
    for r in txBody.findall(".//a:r", NS):
        t = r.find("a:t", NS)
        text = t.text if (t is not None and t.text) else ""
        rPr = r.find("a:rPr", NS)
        info = {"text": text}
        if rPr is not None:
            sz = rPr.attrib.get("sz")
            info["size_pt"] = round(int(sz) / 100, 1) if sz else None
            info["bold"] = rPr.attrib.get("b") == "1"
            info["italic"] = rPr.attrib.get("i") == "1"
            latin = rPr.find("a:latin", NS)
            info["font"] = latin.attrib.get("typeface") if latin is not None else None
            info["color"] = _font_color(rPr)
        runs.append(info)
    return runs


def table_info(graphic_frame):
    """Extract a table's cell grid from a graphicFrame containing <a:tbl>.

    Returns {rows: [[cell_text, ...], ...], n_rows, n_cols} or None if the
    frame isn't a table.
    """
    tbl = graphic_frame.find(".//a:tbl", NS)
    if tbl is None:
        return None
    rows = []
    for tr in tbl.findall("a:tr", NS):
        cells = []
        for tc in tr.findall("a:tc", NS):
            txBody = tc.find("a:txBody", NS)
            cells.append(get_text(txBody))
        rows.append(cells)
    n_cols = max((len(r) for r in rows), default=0)
    return {"rows": rows, "n_rows": len(rows), "n_cols": n_cols}


def chart_info(graphic_frame, slide_rels, charts_dir):
    """If the graphicFrame references a chart, follow the slide rels to the
    chartN.xml and extract series (name, categories, values) from the cache.

    Returns {chart_type, series: [{name, categories, values}, ...]} or None.
    """
    chart_ref = graphic_frame.find(".//c:chart", NS)
    if chart_ref is None:
        return None
    rid = chart_ref.attrib.get("{%s}id" % NS["r"])
    if not rid or not slide_rels:
        return {"chart_type": "unknown", "series": [], "note": "chart present; rels unresolved"}
    target = slide_rels.get(rid)
    if not target:
        return {"chart_type": "unknown", "series": [], "note": "chart rel id not found"}
    chart_path = os.path.normpath(os.path.join(charts_dir, os.path.basename(target)))
    if not os.path.exists(chart_path):
        return {"chart_type": "unknown", "series": [], "note": f"chart file missing: {os.path.basename(target)}"}
    tree = ET.parse(chart_path)
    root = tree.getroot()
    plot = root.find(".//c:plotArea", NS)
    chart_type = "unknown"
    if plot is not None:
        for child in plot:
            tag = child.tag.split("}")[-1]
            if tag.endswith("Chart"):
                chart_type = tag
                break
    series = []
    for ser in root.findall(".//c:ser", NS):
        name_el = ser.find("c:tx//c:v", NS)
        name = name_el.text if name_el is not None else None
        cats = [v.text for v in ser.findall("c:cat//c:pt/c:v", NS)]
        vals = [v.text for v in ser.findall("c:val//c:pt/c:v", NS)]
        series.append({"name": name, "categories": cats, "values": vals})
    return {"chart_type": chart_type, "series": series}


def read_slide_rels(slides_dir, slide_n):
    """Return {rId: target} for a slide's relationships (used to resolve charts)."""
    rels_path = os.path.join(slides_dir, "_rels", f"slide{slide_n}.xml.rels")
    out = {}
    if not os.path.exists(rels_path):
        return out
    tree = ET.parse(rels_path)
    for rel in tree.getroot():
        out[rel.attrib.get("Id")] = rel.attrib.get("Target", "")
    return out


def get_layout_for_slide(slides_dir, slide_n):
    rels_path = os.path.join(slides_dir, "_rels", f"slide{slide_n}.xml.rels")
    if not os.path.exists(rels_path):
        return None
    tree = ET.parse(rels_path)
    for rel in tree.getroot():
        target = rel.attrib.get("Target", "")
        if "slideLayout" in target:
            return os.path.basename(target)
    return None


def get_layout_name(layouts_dir, layout_file):
    if not layout_file:
        return None
    p = os.path.join(layouts_dir, layout_file)
    if not os.path.exists(p):
        return None
    tree = ET.parse(p)
    cSld = tree.getroot().find(".//p:cSld", NS)
    return cSld.attrib.get("name") if cSld is not None else None


def _first_present(*candidates):
    """Return the first non-None element from candidates (replaces `a or b or c` pattern, which Python 3.14+ deprecates for Element)."""
    for c in candidates:
        if c is not None:
            return c
    return None


def shape_info(sp_elt, slide_rels=None, charts_dir=None):
    """Extract id, name, placeholder type, position, text, run formatting,
    table cells, and chart series from a shape-like element."""
    nv = _first_present(
        sp_elt.find(".//p:nvSpPr", NS),
        sp_elt.find(".//p:nvPicPr", NS),
        sp_elt.find(".//p:nvGraphicFramePr", NS),
    )
    if nv is None:
        return None
    cnv = nv.find(".//p:cNvPr", NS)
    sid = cnv.attrib.get("id") if cnv is not None else "?"
    sname = cnv.attrib.get("name") if cnv is not None else "?"
    ph = _first_present(nv.find(".//p:nvSpPr/p:nvPr/p:ph", NS), nv.find(".//p:nvPr/p:ph", NS))
    ph_type = ph.attrib.get("type") if ph is not None else None
    ph_idx = ph.attrib.get("idx") if ph is not None else None
    xfrm = _first_present(sp_elt.find(".//p:spPr/a:xfrm", NS), sp_elt.find(".//p:grpSpPr/a:xfrm", NS))
    pos = {}
    if xfrm is not None:
        off = xfrm.find("a:off", NS)
        ext = xfrm.find("a:ext", NS)
        if off is not None:
            pos["x_in"] = emu_to_in(off.attrib.get("x"))
            pos["y_in"] = emu_to_in(off.attrib.get("y"))
        if ext is not None:
            pos["w_in"] = emu_to_in(ext.attrib.get("cx"))
            pos["h_in"] = emu_to_in(ext.attrib.get("cy"))
    tx = sp_elt.find(".//p:txBody", NS)
    text = get_text(tx) if tx is not None else ""
    runs = get_runs(tx) if tx is not None else []
    has_pic = sp_elt.find(".//p:blipFill", NS) is not None
    table = chart = None
    if sp_elt.tag.split("}")[-1] == "graphicFrame":
        table = table_info(sp_elt)
        if table is None:
            chart = chart_info(sp_elt, slide_rels, charts_dir)
    return {
        "id": sid,
        "name": sname,
        "ph_type": ph_type,
        "ph_idx": ph_idx,
        "pos": pos,
        "text": text,
        "runs": runs,
        "table": table,
        "chart": chart,
        "is_picture": has_pic,
        "tag": sp_elt.tag.split("}")[-1],
    }


def iter_shapes(spTree):
    """Yield each shape-like element (sp, pic, graphicFrame, grpSp recursively)."""
    for child in spTree:
        tag = child.tag.split("}")[-1]
        if tag in ("sp", "pic", "graphicFrame"):
            yield child
        elif tag == "grpSp":
            yield from iter_shapes(child)


def parse_slide(slides_dir, layouts_dir, charts_dir, slide_n):
    path = os.path.join(slides_dir, f"slide{slide_n}.xml")
    tree = ET.parse(path)
    root = tree.getroot()
    spTree = root.find(".//p:cSld/p:spTree", NS)
    slide_rels = read_slide_rels(slides_dir, slide_n)
    shapes = []
    if spTree is not None:
        for sp in iter_shapes(spTree):
            info = shape_info(sp, slide_rels=slide_rels, charts_dir=charts_dir)
            if info:
                shapes.append(info)
    layout_file = get_layout_for_slide(slides_dir, slide_n)
    layout_name = get_layout_name(layouts_dir, layout_file)
    return {
        "slide": slide_n,
        "layout_file": layout_file,
        "layout_name": layout_name,
        "shapes": shapes,
    }


def extract_pptx(pptx_path, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(pptx_path, "r") as z:
        z.extractall(extract_dir)


def _fmt_runs(runs):
    """Compact one-line-per-run formatting summary for the full inventory."""
    out = []
    for r in runs:
        if not (r.get("text") or "").strip():
            continue
        bits = []
        if r.get("font"):
            bits.append(r["font"])
        if r.get("size_pt"):
            bits.append(f"{r['size_pt']}pt")
        if r.get("color"):
            bits.append(r["color"])
        if r.get("bold"):
            bits.append("bold")
        if r.get("italic"):
            bits.append("italic")
        style = ", ".join(bits) if bits else "(inherits)"
        txt = (r["text"] or "")[:60]
        out.append(f"            run: \"{txt}\"  [{style}]")
    return out


def build_inventory(extract_dir, preview_path, full_path):
    slides_dir = os.path.join(extract_dir, "ppt", "slides")
    layouts_dir = os.path.join(extract_dir, "ppt", "slideLayouts")
    charts_dir = os.path.join(extract_dir, "ppt", "charts")
    if not os.path.isdir(slides_dir):
        raise SystemExit(f"ERROR: Expected slides dir at {slides_dir}; extraction failed?")
    slide_files = sorted(
        [f for f in os.listdir(slides_dir) if f.startswith("slide") and f.endswith(".xml")],
        key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
    )
    with open(preview_path, "w", encoding="utf-8") as preview, open(full_path, "w", encoding="utf-8") as full:
        header = f"# Shape inventory for {os.path.basename(extract_dir)}  ({len(slide_files)} slides)\n"
        note = "# full-text file additionally includes run-level formatting, table cells, and chart series.\n"
        preview.write(header + "\n")
        full.write(header + note + "\n")
        for fname in slide_files:
            n = int(re.search(r"slide(\d+)", fname).group(1))
            info = parse_slide(slides_dir, layouts_dir, charts_dir, n)
            block = f"\n=== SLIDE {info['slide']}  layout: {info['layout_name']} ({info['layout_file']}) ===\n"
            preview.write(block)
            full.write(block)
            for s in info["shapes"]:
                pos = s.get("pos") or {}
                pos_s = f"[x={pos.get('x_in')} y={pos.get('y_in')} w={pos.get('w_in')} h={pos.get('h_in')}]"
                ph_s = f"  ph={s['ph_type'] or ''}" if s.get("ph_type") else ""
                pic_s = "  [PICTURE]" if s.get("is_picture") else ""
                kind = ""
                if s.get("table"):
                    kind = f"  [TABLE {s['table']['n_rows']}x{s['table']['n_cols']}]"
                elif s.get("chart"):
                    kind = f"  [CHART {s['chart'].get('chart_type')}]"
                line = f"  id={s['id']:>4}  tag={s['tag']:<14} name={s['name']!r}  {pos_s}{ph_s}{pic_s}{kind}\n"
                preview.write(line)
                full.write(line)
                text = s.get("text") or ""
                if text:
                    preview_text = text.replace("\n", " | ")
                    if len(preview_text) > 200:
                        preview_text = preview_text[:200] + " ..."
                    preview.write(f"        TEXT: {preview_text}\n")
                    full.write(f"        FULL: {text.replace(chr(10), ' | ')}\n")
                # full inventory only: run formatting, table cells, chart series
                if s.get("runs"):
                    run_lines = _fmt_runs(s["runs"])
                    if run_lines:
                        full.write("        FORMATTING:\n")
                        for rl in run_lines:
                            full.write(rl + "\n")
                if s.get("table"):
                    full.write("        TABLE CELLS:\n")
                    for ri, row in enumerate(s["table"]["rows"]):
                        cells = " | ".join((c or "").replace("\n", " ") for c in row)
                        full.write(f"            row {ri}: {cells}\n")
                if s.get("chart"):
                    ch = s["chart"]
                    full.write(f"        CHART ({ch.get('chart_type')}):\n")
                    if ch.get("note"):
                        full.write(f"            note: {ch['note']}\n")
                    for se in ch.get("series", []):
                        full.write(f"            series {se.get('name')!r}: "
                                   f"cats={se.get('categories')} vals={se.get('values')}\n")
    return preview_path, full_path


def main(argv=None):
    p = argparse.ArgumentParser(description="Extract .pptx shape inventory for V23 om-builder revision mode.")
    p.add_argument("pptx", help="Path to the .pptx file (use the LIVE/CANONICAL file when multiple versions exist).")
    p.add_argument("--extract-dir", default=None, help="Working directory for extracted XML (default: sibling folder named '<stem>-extracted').")
    p.add_argument("--out", default=None, help="Optional explicit path for the preview inventory file.")
    args = p.parse_args(argv)
    pptx_path = os.path.abspath(args.pptx)
    if not os.path.isfile(pptx_path):
        raise SystemExit(f"ERROR: Not a file: {pptx_path}")
    stem = os.path.splitext(os.path.basename(pptx_path))[0]
    extract_dir = args.extract_dir or os.path.join(os.path.dirname(pptx_path), f"{stem}-extracted")
    preview_path = args.out or os.path.join(extract_dir, "inventory.txt")
    full_path = os.path.join(extract_dir, "inventory-fulltext.txt")
    extract_pptx(pptx_path, extract_dir)
    build_inventory(extract_dir, preview_path, full_path)
    print(f"Extracted to: {extract_dir}")
    print(f"Preview inventory: {preview_path}")
    print(f"Full-text inventory: {full_path}")


if __name__ == "__main__":
    main()
