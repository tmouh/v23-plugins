# -*- coding: utf-8 -*-
"""
clone-build.py — seed-deck XML-clone builder for v23:om-builder (Phase 4 DEFAULT
method as of v6.1).

Builds a new OM by cloning real slides from a register-matched production seed
deck and editing content surgically at the XML run/cell level. This is the house
method documented in layout-system.md §4B ("clone an existing slide, modify
content, preserve layout and named shape IDs") and validated on the Coastal GA
rebuild (2026-06-11) after the generator-first path shipped a rejected sparse
deck. Structure, run formatting, table styling, and banded constructions are all
INHERITED from the seed — nothing is drawn from primitives.

USAGE
    python clone-build.py <buildspec.py>

The buildspec is a deal-local python file (lives in x V23\\_build\\) defining:

    SEED  = r"...\\x V23\\_build\\seeds\\seed-debt.pptx"   # frozen copy, never a live deck
    OUT   = r"...\\x V23\\<Deal> - OM - v1.pptx"
    WORK  = r"...\\x V23\\_build\\unpacked"                # optional; default: _build\\unpacked next to spec
    PLAN  = [(1, "orig"), (2, "orig"), (3, "orig"), (12, "clone"), ...]
            # target slide order; each entry = (seed_slide_number, "orig"|"clone").
            # First use of a seed slide may be "orig"; every reuse MUST be "clone".
    EDITS = [edit_cover, edit_disclaimer, ...]             # one callable per PLAN entry,
            # signature fn(slide) where slide is a Slide instance (API below).

Content (narratives, tables, photo paths) belongs in the buildspec or a sibling
content module — authored in voice (voice-model.md GP rules) with audit-trail IDs
in comments, exactly like a blueprint content block.

SLIDE API (what an edit function can do)
    s.by_id(shape_id)                  -> shape element (recursive: finds grouped shapes)
    s.tables() / s.pics(skip_logo=True)
    s.text_of(el) / s.expect(el, substr)   # precondition; logs PRECONDITION MISS
    s.set_text(el, paras, sz=None, blank_between=False, expect=None, align=None,
               bullets=True)           # paras: list[str with **bold** spans] or
                                       # list[list[(text, bold[, italic])]]
    s.set_band(shape_id, text, expect=None)   # header-band title; auto-shrinks long titles
    s.set_table(gf, header, rows, col_fracs=None, total_row=None, body_sz=None,
                header_sz=None, row_h=None, width_in=None)
    s.swap_pic(el, img_path)           # new media part + rel; center-crop srcRect
    s.add_textbox_from(tmpl_el, x, y, w, h, paras, sz=None, name=..., color=None,
                       bold=None, align="l")
    s.replace_in_paragraphs(el, [(regex, replacement), ...])  # disclaimer surgery
    s.delete(el) / s.set_xfrm(el, x, y, w, h)
    s.recolor_runs(el, color="1F3A5F", bold=True)

TRAP LIST — every one was hit on the first production run; the library handles
them, listed here so a reader knows WHY the code does what it does:
  1. Seed lead-runs carry underline/strike in rPr -> stripped in every new run.
  2. Seed list paragraphs carry buChar bullets -> set_text(bullets=False) where
     the arrangement is typographic-only (A-06 highlights, A-13 narrative).
  3. Resizing a table does NOT resize its grid -> set_table(width_in=...) recomputes
     tblGrid and the frame extent together; row heights set explicitly (row_h EMU).
  4. graphicFrames use p:xfrm, not a:xfrm -> set_xfrm checks both.
  5. p:pic uses p:blipFill, not a:blipFill -> swap_pic checks both.
  6. Shapes can live inside p:grpSp groups -> shape search is recursive.
  7. Added media needs a [Content_Types].xml Default for its extension or the
     package will not open (PowerPoint COM error 0x80CB8002).
  8. Seed contact-card emails carry hyperlink rPr -> rebuild card text to kill
     the underline (set_text with the card's name-run as template does this).
  9. OneDrive marks unpacked files read-only -> rmtree uses an onerror chmod handler.
 10. CONFIDENTIALITY: deleted seed slides leave their media/charts/embeddings as
     orphan parts INSIDE the package (another deal's photos shipped to a lender).
     repack() runs a reachability prune over ppt/media, ppt/charts, ppt/embeddings,
     ppt/notesSlides before zipping. Never disable it.

After building: render with render-qa.py, verify with verify-deck.py (Phase 5b),
then the editorial checklist (Phase 5c). The build is deterministic — rerunning
the spec reproduces the deck from the frozen seed.
"""
import copy
import importlib.util
import os
import re
import shutil
import struct
import sys
import zipfile

from lxml import etree

LOG = []

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
R_EMBED = "{%s}embed" % NS["r"]
R_ID = "{%s}id" % NS["r"]
EMU = 914400


def q(tag):
    pre, local = tag.split(":")
    return "{%s}%s" % (NS[pre], local)


def inches(v):
    return str(int(round(v * EMU)))


def load(path):
    return etree.parse(path)


def save(tree, path):
    tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)


# ---------------------------------------------------------------- image dims
def img_size(path):
    """Pure-python PNG/JPEG dimension reader (no PIL dependency)."""
    with open(path, "rb") as f:
        head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24])
            return w, h
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                b0 = f.read(1)
                if not b0:
                    break
                if b0 != b"\xff":
                    continue
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                m = marker[0]
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h
                if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                    continue
                (seg,) = struct.unpack(">H", f.read(2))
                f.seek(seg - 2, 1)
    raise ValueError("cannot read image size: " + path)


# ---------------------------------------------------------------- package ops
class Pkg:
    def __init__(self, seed, work, out):
        self.seed, self.work, self.out = seed, work, out
        if os.path.isdir(work):
            def _force(fn, path, _exc):     # trap 9: OneDrive read-only locks
                os.chmod(path, 0o777)
                fn(path)
            shutil.rmtree(work, onerror=_force)
        with zipfile.ZipFile(seed) as z:
            z.extractall(work)
        self.media_n = 900
        self.rel_n = 900

    def path(self, rel):
        return os.path.join(self.work, rel.replace("/", os.sep))

    def apply_plan(self, plan):
        """plan: list of (seed_slide_number, 'orig'|'clone') in TARGET order.
        Returns slide file basenames in target order."""
        pres = load(self.path("ppt/presentation.xml"))
        prels = load(self.path("ppt/_rels/presentation.xml.rels"))
        rels_root = prels.getroot()
        rid2tgt = {e.get("Id"): e.get("Target") for e in rels_root}
        sldlst = pres.getroot().find(q("p:sldIdLst"))
        order_rids = [s.get(R_ID) for s in sldlst]
        seed_files = [rid2tgt[r] for r in order_rids]

        used_orig = set()
        next_new = 100
        targets = []
        for seed_no, mode in plan:
            src = seed_files[seed_no - 1]
            if mode == "orig" and seed_no not in used_orig:
                used_orig.add(seed_no)
                targets.append(src)
            else:
                next_new += 1
                new = "slides/slide%d.xml" % next_new
                shutil.copyfile(self.path("ppt/" + src), self.path("ppt/" + new))
                src_rels = self.path("ppt/slides/_rels/%s.rels" % os.path.basename(src))
                new_rels = self.path("ppt/slides/_rels/slide%d.xml.rels" % next_new)
                shutil.copyfile(src_rels, new_rels)
                self._strip_notes_rel(new_rels)
                targets.append(new)
                LOG.append("clone: %s -> %s" % (src, new))

        keep = set(targets)
        for f in seed_files:
            if f in keep:
                continue
            rels_f = self.path("ppt/slides/_rels/%s.rels" % os.path.basename(f))
            if os.path.isfile(rels_f):
                t = load(rels_f)
                for e in t.getroot():
                    if e.get("Type", "").endswith("/notesSlide"):
                        notes = os.path.normpath(
                            os.path.join("ppt/slides", e.get("Target"))
                        ).replace(os.sep, "/")
                        for pth in (notes, notes.replace("notesSlides/", "notesSlides/_rels/") + ".rels"):
                            fp = self.path(pth)
                            if os.path.isfile(fp):
                                os.remove(fp)
                        self._drop_override("/" + notes)
                os.remove(rels_f)
            os.remove(self.path("ppt/" + f))
            self._drop_override("/ppt/" + f)

        for e in list(rels_root):
            if e.get("Type", "").endswith("/slide"):
                rels_root.remove(e)
        new_rids = []
        for i, t in enumerate(targets, 1):
            rid = "rIdSl%d" % i
            etree.SubElement(
                rels_root, q("rel:Relationship"), Id=rid,
                Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide",
                Target=t)
            new_rids.append(rid)
        for s in list(sldlst):
            sldlst.remove(s)
        for i, rid in enumerate(new_rids):
            e = etree.SubElement(sldlst, q("p:sldId"), id=str(300 + i))
            e.set(R_ID, rid)
        for t in targets:
            self._ensure_override(
                "/ppt/" + t,
                "application/vnd.openxmlformats-officedocument.presentationml.slide+xml")
        save(pres, self.path("ppt/presentation.xml"))
        save(prels, self.path("ppt/_rels/presentation.xml.rels"))
        return [os.path.basename(t) for t in targets]

    def _strip_notes_rel(self, rels_path):
        t = load(rels_path)
        root = t.getroot()
        for e in list(root):
            if e.get("Type", "").endswith("/notesSlide"):
                root.remove(e)
        save(t, rels_path)

    def _ct(self):
        return load(self.path("[Content_Types].xml"))

    def _ensure_override(self, partname, ctype):
        t = self._ct()
        root = t.getroot()
        for e in root:
            if e.tag == q("ct:Override") and e.get("PartName") == partname:
                return
        etree.SubElement(root, q("ct:Override"), PartName=partname, ContentType=ctype)
        save(t, self.path("[Content_Types].xml"))

    def _ensure_default(self, ext, ctype):   # trap 7
        t = self._ct()
        root = t.getroot()
        for e in root:
            if e.tag == q("ct:Default") and e.get("Extension", "").lower() == ext:
                return
        etree.SubElement(root, q("ct:Default"), Extension=ext, ContentType=ctype)
        save(t, self.path("[Content_Types].xml"))

    def _drop_override(self, partname):
        t = self._ct()
        root = t.getroot()
        for e in list(root):
            if e.tag == q("ct:Override") and e.get("PartName") == partname:
                root.remove(e)
        save(t, self.path("[Content_Types].xml"))

    def add_media(self, img_path):
        self.media_n += 1
        ext = os.path.splitext(img_path)[1].lower().lstrip(".")
        self._ensure_default(ext, "image/png" if ext == "png" else "image/jpeg")
        name = "media/imageCB_%d.%s" % (self.media_n, ext)
        shutil.copyfile(img_path, self.path("ppt/" + name))
        return "../" + name

    def prune_unreferenced(self):
        """Trap 10 — reachability sweep from the package root; delete orphan
        parts under ppt/media, ppt/charts, ppt/embeddings, ppt/notesSlides.
        The seed's unused media is another deal's content; it must not ship."""
        reached = set()
        queue = []
        root_rels = self.path("_rels/.rels")
        if os.path.isfile(root_rels):
            for e in load(root_rels).getroot():
                if e.get("TargetMode") == "External":
                    continue
                queue.append(e.get("Target").lstrip("/"))
        while queue:
            part = os.path.normpath(queue.pop()).replace(os.sep, "/")
            if part in reached:
                continue
            reached.add(part)
            d, n = os.path.split(part)
            rels = "%s/_rels/%s.rels" % (d, n) if d else "_rels/%s.rels" % n
            rp = self.path(rels)
            if not os.path.isfile(rp):
                continue
            reached.add(rels)
            for e in load(rp).getroot():
                if e.get("TargetMode") == "External":
                    continue
                queue.append(os.path.normpath(
                    os.path.join(d, e.get("Target"))).replace(os.sep, "/"))
        removed = 0
        for sub in ("ppt/media", "ppt/charts", "ppt/embeddings", "ppt/notesSlides"):
            base = self.path(sub)
            if not os.path.isdir(base):
                continue
            for f in os.listdir(base):
                full = os.path.join(base, f)
                if not os.path.isfile(full):
                    continue
                rel = "%s/%s" % (sub, f)
                if rel not in reached:
                    os.remove(full)
                    self._drop_override("/" + rel)
                    rl = self.path("%s/_rels/%s.rels" % (sub, f))
                    if os.path.isfile(rl):
                        os.remove(rl)
                    removed += 1
        LOG.append("pruned %d unreferenced parts" % removed)

    def repack(self):
        self.prune_unreferenced()
        if os.path.isfile(self.out):
            os.remove(self.out)
        with zipfile.ZipFile(self.out, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _dirs, files in os.walk(self.work):
                for f in files:
                    full = os.path.join(root, f)
                    arc = os.path.relpath(full, self.work).replace(os.sep, "/")
                    z.write(full, arc)


# ---------------------------------------------------------------- slide edits
class Slide:
    def __init__(self, pkg, fname):
        self.pkg = pkg
        self.fname = fname
        self.fpath = pkg.path("ppt/slides/" + fname)
        self.rpath = pkg.path("ppt/slides/_rels/" + fname + ".rels")
        self.tree = load(self.fpath)
        self.spTree = self.tree.getroot().find(q("p:cSld")).find(q("p:spTree"))

    def save(self):
        save(self.tree, self.fpath)

    def shapes(self):
        for tag in ("p:sp", "p:pic", "p:graphicFrame"):   # trap 6: recursive
            for el in self.spTree.iter(q(tag)):
                yield el

    def by_id(self, sid):
        for el in self.shapes():
            nv = el.find(".//" + q("p:cNvPr"))
            if nv is not None and nv.get("id") == str(sid):
                return el
        raise KeyError("shape id %s not in %s" % (sid, self.fname))

    def tables(self):
        return [el for el in self.shapes() if el.tag == q("p:graphicFrame")
                and el.find(".//" + q("a:tbl")) is not None]

    def pics(self, skip_logo=True):
        out = []
        for el in self.shapes():
            if el.tag != q("p:pic"):
                continue
            off = el.find(".//" + q("a:off"))
            if skip_logo and off is not None and abs(int(off.get("x")) - int(12.69 * EMU)) < 50000:
                continue   # V23 logo at x=12.69 stays
            out.append(el)
        return out

    def text_of(self, el):
        return " ".join(t.text or "" for t in el.iter(q("a:t")))

    def expect(self, el, substr):
        cur = self.text_of(el)
        if substr.lower() not in cur.lower():
            LOG.append("PRECONDITION MISS in %s: wanted '%s', found '%s'"
                       % (self.fname, substr[:40], cur[:80]))
            return False
        return True

    def delete(self, el):
        el.getparent().remove(el)

    def set_xfrm(self, el, x=None, y=None, w=None, h=None):
        xfrm = el.find(".//" + q("a:xfrm"))
        if xfrm is None:
            xfrm = el.find(".//" + q("p:xfrm"))   # trap 4: graphicFrame
        if xfrm is None:
            return
        off, ext = xfrm.find(q("a:off")), xfrm.find(q("a:ext"))
        if x is not None:
            off.set("x", inches(x))
        if y is not None:
            off.set("y", inches(y))
        if w is not None:
            ext.set("cx", inches(w))
        if h is not None:
            ext.set("cy", inches(h))

    # -- text -------------------------------------------------------------
    @staticmethod
    def _runs_from(text):
        parts = re.split(r"\*\*(.+?)\*\*", text)
        return [(t, i % 2 == 1) for i, t in enumerate(parts) if t]

    def _mk_run(self, rpr_tmpl, text, bold=None, italic=None, sz=None):
        r = etree.Element(q("a:r"))
        rpr = copy.deepcopy(rpr_tmpl) if rpr_tmpl is not None else etree.Element(q("a:rPr"))
        rpr.set("lang", "en-US")
        rpr.attrib.pop("u", None)        # trap 1: inherited underline
        rpr.attrib.pop("strike", None)
        for hl in rpr.findall(q("a:hlinkClick")):   # trap 8: hyperlink rPr
            rpr.remove(hl)
        if bold is not None:
            rpr.set("b", "1" if bold else "0")
        if italic is not None:
            rpr.set("i", "1" if italic else "0")
        if sz is not None:
            rpr.set("sz", str(sz))
        r.append(rpr)
        t = etree.SubElement(r, q("a:t"))
        t.text = text
        return r

    def replace_in_paragraphs(self, el, replacements):
        """Regex-replace within each paragraph's joined text; matched paragraphs
        are rebuilt as a single run carrying the paragraph's first rPr. Use for
        disclaimer surgery (prior-deal names, addresses)."""
        tx = el.find(q("p:txBody"))
        if tx is None:
            tx = el.find(".//" + q("a:txBody"))
        for p in tx.findall(q("a:p")):
            joined = "".join(t.text or "" for t in p.iter(q("a:t")))
            new = joined
            for pat, rep in replacements:
                new = re.sub(pat, rep, new)
            if new == joined:
                continue
            rpr = None
            for r in p.iter(q("a:rPr")):
                rpr = r
                break
            for child in list(p):
                if child.tag != q("a:pPr"):
                    p.remove(child)
            p.append(self._mk_run(rpr, new))
            LOG.append("para replace in %s: ...%s..." % (self.fname, new[:60]))

    def set_text(self, el, paras, sz=None, blank_between=False, expect=None,
                 align=None, bullets=True):
        if expect and not self.expect(el, expect):
            return
        tx = el.find(q("p:txBody"))
        if tx is None:
            tx = el.find(".//" + q("a:txBody"))
        ps = tx.findall(q("a:p"))
        ppr_tmpl = ps[0].find(q("a:pPr")) if ps else None
        rpr_tmpl = None
        for r in tx.iter(q("a:rPr")):
            rpr_tmpl = r
            break
        for p in ps:
            tx.remove(p)
        first = True
        for para in paras:
            if blank_between and not first:
                bp = etree.SubElement(tx, q("a:p"))
                if ppr_tmpl is not None:
                    bp.insert(0, copy.deepcopy(ppr_tmpl))
            first = False
            p = etree.SubElement(tx, q("a:p"))
            if ppr_tmpl is not None:
                p.insert(0, copy.deepcopy(ppr_tmpl))
            if align is not None or not bullets:
                ppr = p.find(q("a:pPr"))
                if ppr is None:
                    ppr = etree.Element(q("a:pPr"))
                    p.insert(0, ppr)
                if align is not None:
                    ppr.set("algn", align)
                if not bullets:                      # trap 2: buChar bullets
                    for bu in ("a:buChar", "a:buAutoNum"):
                        for e in ppr.findall(q(bu)):
                            ppr.remove(e)
                    ppr.attrib.pop("indent", None)
                    ppr.attrib.pop("marL", None)
                    if ppr.find(q("a:buNone")) is None:
                        ppr.append(etree.Element(q("a:buNone")))
            specs = self._runs_from(para) if isinstance(para, str) else para
            for spec in specs:
                txt, bold = spec[0], spec[1]
                italic = spec[2] if len(spec) > 2 else None
                p.append(self._mk_run(rpr_tmpl, txt, bold=bold, italic=italic, sz=sz))

    def set_band(self, sid, text, expect=None):
        """Header-band title (eyebrow | action title). Auto-shrinks long titles
        so the assertive-sentence grammar fits the 12.52\" band textbox."""
        el = self.by_id(sid)
        sz = 2000 if len(text) <= 78 else (1800 if len(text) <= 95 else 1600)
        self.set_text(el, [text], sz=sz, expect=expect)

    def recolor_runs(self, el, color=None, bold=None):
        for rpr in el.iter(q("a:rPr")):
            if bold is not None:
                rpr.set("b", "1" if bold else "0")
            if color is not None:
                for f in rpr.findall(q("a:solidFill")):
                    rpr.remove(f)
                fill = etree.Element(q("a:solidFill"))
                etree.SubElement(fill, q("a:srgbClr"), val=color)
                rpr.insert(0, fill)

    # -- tables -----------------------------------------------------------
    def set_table(self, gf, header, rows, col_fracs=None, total_row=None,
                  body_sz=None, header_sz=None, row_h=None, width_in=None):
        """Rebuild a seed table from its own row templates: header style from
        row 0, body style from row 1, total style from the last row. All cells
        rebuilt 1x1 (merge attrs dropped). trap 3: width_in recomputes tblGrid
        AND the frame extent together; set row_h (EMU) when row count changes."""
        tbl = gf.find(".//" + q("a:tbl"))
        grid = tbl.find(q("a:tblGrid"))
        old_cols = grid.findall(q("a:gridCol"))
        total_w = sum(int(c.get("w")) for c in old_cols)
        if width_in is not None:
            total_w = int(width_in * EMU)
            self.set_xfrm(gf, w=width_in)
        trs = tbl.findall(q("a:tr"))
        tr_head, tr_body = trs[0], (trs[1] if len(trs) > 1 else trs[0])
        tr_total = trs[-1]

        def cell_tmpl(tr, idx):
            tcs = tr.findall(q("a:tc"))
            return tcs[min(idx, len(tcs) - 1)]

        def mk_tc(tmpl_tc, text, sz):
            tc = etree.Element(q("a:tc"))
            txb = etree.SubElement(tc, q("a:txBody"))
            src_body = tmpl_tc.find(q("a:txBody"))
            bodyPr = src_body.find(q("a:bodyPr")) if src_body is not None else None
            txb.append(copy.deepcopy(bodyPr) if bodyPr is not None else etree.Element(q("a:bodyPr")))
            txb.append(etree.Element(q("a:lstStyle")))
            p = etree.SubElement(txb, q("a:p"))
            src_p = src_body.find(q("a:p")) if src_body is not None else None
            src_ppr = src_p.find(q("a:pPr")) if src_p is not None else None
            if src_ppr is not None:
                p.append(copy.deepcopy(src_ppr))
            rpr = None
            if src_body is not None:
                for r in src_body.iter(q("a:rPr")):
                    rpr = r
                    break
            for txt, bold in Slide._runs_from(str(text)) or [("", False)]:
                p.append(self._mk_run(rpr, txt, bold=(bold or None), sz=sz))
            tcPr = tmpl_tc.find(q("a:tcPr"))
            tc.append(copy.deepcopy(tcPr) if tcPr is not None else etree.Element(q("a:tcPr")))
            return tc

        n_cols = len(header)
        fr = col_fracs or [1.0 / n_cols] * n_cols
        s = sum(fr)
        for c in list(grid):
            grid.remove(c)
        for f in fr:
            etree.SubElement(grid, q("a:gridCol"), w=str(int(total_w * f / s)))
        for tr in trs:
            tbl.remove(tr)

        def add_row(tmpl_tr, cells, sz):
            tr = etree.Element(q("a:tr"), h=str(row_h or int(tmpl_tr.get("h", "370000"))))
            for i, val in enumerate(cells):
                tr.append(mk_tc(cell_tmpl(tmpl_tr, i), val, sz))
            tbl.append(tr)

        add_row(tr_head, header, header_sz)
        for rdata in rows:
            add_row(tr_body, list(rdata) + [""] * (n_cols - len(rdata)), body_sz)
        if total_row:
            add_row(tr_total, total_row, body_sz)

    # -- pictures ---------------------------------------------------------
    def swap_pic(self, el, img_path):
        target = self.pkg.add_media(img_path)
        rels = load(self.rpath)
        rroot = rels.getroot()
        self.pkg.rel_n += 1
        rid = "rIdCB_%d" % self.pkg.rel_n
        etree.SubElement(
            rroot, q("rel:Relationship"), Id=rid,
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            Target=target)
        save(rels, self.rpath)
        blip = el.find(".//" + q("a:blip"))
        blip.set(R_EMBED, rid)
        xfrm = el.find(".//" + q("a:xfrm"))
        if xfrm is None:
            xfrm = el.find(".//" + q("p:xfrm"))
        ext = xfrm.find(q("a:ext"))
        fw, fh = int(ext.get("cx")), int(ext.get("cy"))
        iw, ih = img_size(img_path)
        fa, ia = fw / fh, iw / ih
        fill = el.find(".//" + q("p:blipFill"))     # trap 5
        if fill is None:
            fill = el.find(".//" + q("a:blipFill"))
        for sr in fill.findall(q("a:srcRect")):
            fill.remove(sr)
        if abs(ia - fa) / fa > 0.03:
            sr = etree.Element(q("a:srcRect"))
            if ia > fa:
                cut = int((1 - fa / ia) / 2 * 100000)
                sr.set("l", str(cut)); sr.set("r", str(cut))
            else:
                cut = int((1 - ia / fa) / 2 * 100000)
                sr.set("t", str(cut)); sr.set("b", str(cut))
            blip.addnext(sr)
        LOG.append("pic swap in %s -> %s" % (self.fname, os.path.basename(img_path)))

    def add_textbox_from(self, tmpl_el, x, y, w, h, paras, sz=None, name="CBBox",
                         color=None, bold=None, align="l"):
        el = copy.deepcopy(tmpl_el)
        ids = [int(nv.get("id")) for nv in self.spTree.iter(q("p:cNvPr"))]
        nv = el.find(".//" + q("p:cNvPr"))
        nv.set("id", str(max(ids) + 1))
        nv.set("name", name)
        self.spTree.append(el)
        self.set_xfrm(el, x, y, w, h)
        self.set_text(el, paras, sz=sz, align=align)
        if color is not None or bold is not None:
            self.recolor_runs(el, color=color, bold=bold)
        return el


# ---------------------------------------------------------------- runner
def run_buildspec(spec_path):
    spec_path = os.path.abspath(spec_path)
    spec_dir = os.path.dirname(spec_path)
    sys.path.insert(0, spec_dir)
    spec = importlib.util.spec_from_file_location("buildspec", spec_path)
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)

    work = getattr(bs, "WORK", os.path.join(spec_dir, "unpacked"))
    plan, edits = bs.PLAN, bs.EDITS
    if len(plan) != len(edits):
        raise SystemExit("ERROR: PLAN has %d entries but EDITS has %d"
                         % (len(plan), len(edits)))
    pkg = Pkg(bs.SEED, work, bs.OUT)
    files = pkg.apply_plan(plan)
    for i, (fname, fn) in enumerate(zip(files, edits), 1):
        sl = Slide(pkg, fname)
        fn(sl)
        sl.save()
        LOG.append("slide %02d <- %s : %s OK" % (i, fname, fn.__name__))
    pkg.repack()
    LOG.append("OUTPUT: " + bs.OUT)
    print("\n".join(LOG))
    misses = [l for l in LOG if "PRECONDITION MISS" in l]
    if misses:
        print("\n%d PRECONDITION MISS(ES) — those edits were SKIPPED; "
              "fix the expect strings and rerun." % len(misses))


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        raise SystemExit(__doc__.split("USAGE")[1].split("\n\n")[0])
    run_buildspec(args[0])


if __name__ == "__main__":
    main()
