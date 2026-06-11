"""
render-qa.py — render every slide of a .pptx to PNG for the visual-QA loop.

Usage:
  python render-qa.py <deck.pptx> <outdir>

Pipeline: pptx -> pdf -> PNGs (pdftoppm -png -r 110). PDF conversion uses
LibreOffice (soffice) when on PATH, else PowerPoint COM via powershell.
If neither is available, export the PDF manually from PowerPoint and re-run
against the PDF directly (a .pdf first arg skips conversion).

Phase 5 visual QA reads the PNGs (overflow, overlap, contrast) — see SKILL.md.
"""

import shutil
import subprocess
import sys
from pathlib import Path

PPT_SAVEAS_PDF = 32  # PowerPoint ppSaveAsPDF

COM_PS = (
    "$pp = New-Object -ComObject PowerPoint.Application; "
    "$pres = $pp.Presentations.Open('{pptx}', $true, $false, $false); "
    "$pres.SaveAs('{pdf}', {fmt}); $pres.Close(); $pp.Quit()"
)


def to_pdf(pptx: Path, pdf: Path) -> None:
    if shutil.which("soffice"):
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf",
             "--outdir", str(pdf.parent), str(pptx)],
            check=True, capture_output=True, text=True)
        produced = pdf.parent / (pptx.stem + ".pdf")
        if produced != pdf:
            produced.replace(pdf)
        return
    ps = COM_PS.format(pptx=str(pptx).replace("'", "''"),
                       pdf=str(pdf).replace("'", "''"), fmt=PPT_SAVEAS_PDF)
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                       capture_output=True, text=True)
    if r.returncode != 0 or not pdf.exists():
        raise SystemExit(
            "PDF conversion failed (no soffice; PowerPoint COM error below).\n"
            f"{r.stderr.strip()}\n"
            "Fallback: open the deck in PowerPoint, File > Save As > PDF, then\n"
            f"re-run: python render-qa.py <that.pdf> {pdf.parent}")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: python render-qa.py <deck.pptx|deck.pdf> <outdir>")
    src, outdir = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if not src.exists():
        raise SystemExit(f"not found: {src}")
    if not shutil.which("pdftoppm"):
        raise SystemExit("pdftoppm not on PATH (install poppler) — cannot render PNGs.")
    outdir.mkdir(parents=True, exist_ok=True)
    pdf = src if src.suffix.lower() == ".pdf" else outdir / (src.stem + ".pdf")
    if src != pdf:
        to_pdf(src, pdf)
    subprocess.run(["pdftoppm", "-png", "-r", "110", str(pdf), str(outdir / "slide")],
                   check=True)
    pages = sorted(outdir.glob("slide-*.png")) or sorted(outdir.glob("slide*.png"))
    if not pages:
        raise SystemExit(f"pdftoppm produced no PNGs in {outdir}")
    print(f"{len(pages)} slide(s) rendered -> {outdir}")


if __name__ == "__main__":
    main()
