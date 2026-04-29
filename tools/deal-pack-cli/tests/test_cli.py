import json
import subprocess
import sys
from pathlib import Path


def _run(*args: str, cwd: Path | None = None, input: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "deal_pack.cli", *args],
        capture_output=True, text=True, cwd=cwd, input=input,
    )


def test_cli_inventory(tmp_path: Path):
    (tmp_path / "rent.csv").write_text("unit,tenant\n101,Acme\n")
    result = _run("inventory", str(tmp_path))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert len(data) == 1
    entry = data[0]
    # Pin the full InventoryEntry contract, not just source_path: the preview
    # field is load-bearing for downstream classification and must be present.
    assert Path(entry["source_path"]).name == "rent.csv"
    assert "preview" in entry
    assert "unit,tenant" in entry["preview"]


def test_cli_rent_roll_summary(fixtures_dir: Path):
    csv_path = fixtures_dir / "rent_rolls" / "office_standard.csv"
    result = _run("rent-roll-summary", str(csv_path), "--reference-date", "2025-01-01")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["total_sqft"] == 12000
    assert summary["occupied_sqft"] == 12000


def test_cli_t12_summary(fixtures_dir: Path):
    csv_path = fixtures_dir / "t12s" / "standard_office.csv"
    result = _run("t12-summary", str(csv_path), "--total-sqft", "100000")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["noi"] == "620000"
    assert summary["opex_per_sqft"] == "3.30"


def test_cli_derived(tmp_path: Path, fixtures_dir: Path):
    rr_path = fixtures_dir / "rent_rolls" / "office_standard.csv"
    t12_path = fixtures_dir / "t12s" / "standard_office.csv"

    rr_summary = _run("rent-roll-summary", str(rr_path),
                      "--reference-date", "2025-01-01").stdout
    t12_summary = _run("t12-summary", str(t12_path),
                       "--total-sqft", "100000").stdout

    rr_file = tmp_path / "rr.json"; rr_file.write_text(rr_summary)
    t12_file = tmp_path / "t12.json"; t12_file.write_text(t12_summary)

    # Without --ask-price: implied_cap_rate_at_ask must be None
    result = _run("derived", str(rr_file), str(t12_file))
    assert result.returncode == 0, result.stderr
    derived = json.loads(result.stdout)
    # T12 fixture: EGI=950000, NOI=620000, opex=330000
    # noi_margin = 620000/950000 = 0.6526... -> quantize(2) = "0.65"
    # expense_ratio = 330000/950000 = 0.3473... -> quantize(2) = "0.35"
    assert derived["noi_margin"] == "0.65"
    assert derived["expense_ratio"] == "0.35"
    assert derived["implied_cap_rate_at_ask"] is None

    # With --ask-price 10000000: implied_cap_rate_at_ask = 620000/10000000 = 0.062 (3 places)
    result2 = _run("derived", str(rr_file), str(t12_file), "--ask-price", "10000000")
    assert result2.returncode == 0, result2.stderr
    derived2 = json.loads(result2.stdout)
    assert derived2["noi_margin"] == "0.65"
    assert derived2["expense_ratio"] == "0.35"
    assert derived2["implied_cap_rate_at_ask"] == "0.062"


def test_cli_write_financials(tmp_path: Path, fixtures_dir: Path):
    # Produce summary JSONs first
    rr_path = fixtures_dir / "rent_rolls" / "office_standard.csv"
    t12_path = fixtures_dir / "t12s" / "standard_office.csv"

    rr_summary = _run("rent-roll-summary", str(rr_path),
                      "--reference-date", "2025-01-01").stdout
    t12_summary = _run("t12-summary", str(t12_path),
                       "--total-sqft", "100000").stdout

    rr_file = tmp_path / "rr.json"; rr_file.write_text(rr_summary)
    t12_file = tmp_path / "t12.json"; t12_file.write_text(t12_summary)
    derived = _run("derived", str(rr_file), str(t12_file)).stdout
    der_file = tmp_path / "der.json"; der_file.write_text(derived)

    out_xlsx = tmp_path / "financials.xlsx"
    result = _run(
        "write-financials",
        "--out", str(out_xlsx),
        "--rent-roll-csv", str(rr_path),
        "--rent-roll-summary", str(rr_file),
        "--t12-csv", str(t12_path),
        "--t12-summary", str(t12_file),
        "--derived", str(der_file),
    )
    assert result.returncode == 0, result.stderr
    assert out_xlsx.exists()

    # stdout must be JSON with a "wrote" key pointing at the xlsx
    payload = json.loads(result.stdout)
    assert payload["wrote"] == str(out_xlsx.resolve())

    # Workbook must contain at minimum these sheets
    import openpyxl
    wb = openpyxl.load_workbook(out_xlsx, read_only=True)
    sheet_names = set(wb.sheetnames)
    for required in ("rent_roll_summary", "t12_summary", "derived"):
        assert required in sheet_names, f"missing sheet: {required} (have {sheet_names})"


def test_cli_write_manifest(tmp_path: Path):
    # write_manifest takes an arbitrary dict and writes it as pretty JSON.
    manifest = {
        "deal_name": "Acme Office",
        "generated_at": "2026-04-22T00:00:00Z",
        "contents": [
            {"kind": "financials", "path": "financials.xlsx"},
            {"kind": "facts", "path": "facts.md"},
        ],
    }
    out_path = tmp_path / "manifest.json"
    result = _run("write-manifest", "--out", str(out_path), input=json.dumps(manifest))
    assert result.returncode == 0, result.stderr

    # stdout must be JSON-parseable and report the resolved out path.
    payload = json.loads(result.stdout)
    assert payload["wrote"] == str(out_path.resolve())

    # The file must exist on disk with the exact manifest contents.
    assert out_path.exists()
    written = json.loads(out_path.read_text(encoding="utf-8"))
    assert written == manifest


def test_integration_sample_deal_produces_financials(tmp_path: Path, fixtures_dir: Path):
    """End-to-end smoke: the CLI can chain inventory -> summaries -> financials."""
    import shutil
    sample = fixtures_dir / "integration" / "sample_deal"
    work = tmp_path / "work"
    work.mkdir()

    shutil.copy(sample / "rent_roll.csv", work / "rent_roll.csv")
    shutil.copy(sample / "t12.csv", work / "t12.csv")

    rr_summary = _run("rent-roll-summary", str(work / "rent_roll.csv"),
                      "--reference-date", "2025-01-01").stdout
    (work / "rr.json").write_text(rr_summary)

    rr_data = json.loads(rr_summary)
    t12_summary = _run("t12-summary", str(work / "t12.csv"),
                       "--total-sqft", str(rr_data["total_sqft"])).stdout
    (work / "t12.json").write_text(t12_summary)

    derived = _run("derived", str(work / "rr.json"), str(work / "t12.json")).stdout
    (work / "der.json").write_text(derived)

    out_xlsx = work / "financials.xlsx"
    result = _run(
        "write-financials",
        "--out", str(out_xlsx),
        "--rent-roll-csv", str(work / "rent_roll.csv"),
        "--rent-roll-summary", str(work / "rr.json"),
        "--t12-csv", str(work / "t12.csv"),
        "--t12-summary", str(work / "t12.json"),
        "--derived", str(work / "der.json"),
    )
    assert result.returncode == 0, result.stderr
    assert out_xlsx.exists()

    t12_data = json.loads(t12_summary)
    assert t12_data["gross_revenue"] == "264000"
    assert t12_data["effective_gross_income"] == "254000"
    assert t12_data["opex_total"] == "56000"
    assert t12_data["noi"] == "198000"
