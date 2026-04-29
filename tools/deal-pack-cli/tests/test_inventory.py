from pathlib import Path

from deal_pack.inventory import scan_folder


def test_scan_empty_folder(tmp_path: Path):
    items = scan_folder(tmp_path)
    assert items == []


def test_scan_recursive(tmp_path: Path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "rent_roll.csv").write_text("unit,tenant\n101,X\n")
    (tmp_path / "photo.jpg").write_bytes(b"\xff\xd8\xff\xd9")
    items = scan_folder(tmp_path)
    paths = {Path(i["source_path"]).name for i in items}
    assert paths == {"rent_roll.csv", "photo.jpg"}


def test_preview_text_for_csv(tmp_path: Path):
    f = tmp_path / "rent_roll.csv"
    f.write_text("unit,tenant,sqft\n101,Acme,5000\n102,Beta,3000\n")
    items = scan_folder(tmp_path)
    preview = items[0]["preview"]
    assert "unit" in preview and "tenant" in preview
    assert "Acme" in preview


def test_preview_image_has_metadata(tmp_path: Path):
    # Create a tiny valid PNG via Pillow
    from PIL import Image
    p = tmp_path / "site.png"
    Image.new("RGB", (10, 10), color="white").save(p)
    items = scan_folder(tmp_path)
    preview = items[0]["preview"]
    assert "image" in preview.lower() or "png" in preview.lower() or "10x10" in preview


def test_preview_truncated(tmp_path: Path):
    long_text = "line " * 5000
    f = tmp_path / "big.txt"
    f.write_text(long_text)
    items = scan_folder(tmp_path)
    assert len(items[0]["preview"]) <= 4000


def test_source_path_is_absolute(tmp_path: Path):
    (tmp_path / "x.csv").write_text("a,b\n1,2\n")
    items = scan_folder(tmp_path)
    assert Path(items[0]["source_path"]).is_absolute()


def test_zip_is_auto_extracted(tmp_path: Path):
    import zipfile
    zf_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("inside/rent_roll.csv", "unit,tenant\n101,Acme\n")
    items = scan_folder(tmp_path)
    paths = {Path(i["source_path"]).name for i in items}
    assert "rent_roll.csv" in paths


def test_zip_file_excluded_from_inventory(tmp_path: Path):
    """The .zip itself must not appear in inventory — only its extracted contents."""
    import zipfile
    zf_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("inside/rent_roll.csv", "unit,tenant\n101,Acme\n")
    items = scan_folder(tmp_path)
    paths = {Path(i["source_path"]).name for i in items}
    assert "bundle.zip" not in paths


def test_nested_zip_is_extracted(tmp_path: Path):
    """A zip inside a zip must still have its contents inventoried."""
    import io
    import zipfile

    # Build an inner zip in memory
    inner_buf = io.BytesIO()
    with zipfile.ZipFile(inner_buf, "w") as inner:
        inner.writestr("t12.csv", "category,total\nrevenue,1000\n")
    inner_bytes = inner_buf.getvalue()

    # Outer zip contains the inner zip
    outer_path = tmp_path / "outer.zip"
    with zipfile.ZipFile(outer_path, "w") as outer:
        outer.writestr("financials/inner.zip", inner_bytes)

    items = scan_folder(tmp_path)
    paths = {Path(i["source_path"]).name for i in items}
    assert "t12.csv" in paths


def test_zip_slip_is_rejected(tmp_path: Path):
    """A zip containing a '../' escape path must raise rather than silently extract."""
    import zipfile
    zf_path = tmp_path / "evil.zip"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("../escaped.txt", "should never land outside")

    import pytest
    with pytest.raises(ValueError, match="Zip slip"):
        scan_folder(tmp_path)


def test_partial_extraction_retry(tmp_path: Path):
    """If an <name>__extracted folder is missing, a new scan re-extracts cleanly.

    We simulate a 'partial crash' scenario by deleting the __extracted folder
    after a successful run and re-running — contents should come back."""
    import shutil
    import zipfile

    zf_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(zf_path, "w") as zf:
        zf.writestr("rent_roll.csv", "unit,tenant\n101,Acme\n")

    # First scan: extracts and inventories
    scan_folder(tmp_path)
    extracted = tmp_path / "bundle__extracted"
    assert extracted.exists()

    # Simulate prior crash by removing extracted folder
    shutil.rmtree(extracted)

    # Re-run: should re-extract and inventory again
    items = scan_folder(tmp_path)
    paths = {Path(i["source_path"]).name for i in items}
    assert "rent_roll.csv" in paths
