from pathlib import Path

from deal_pack.sources import copy_sources


def test_copy_basic(tmp_path: Path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "my rent roll.xlsx").write_bytes(b"x")
    (src / "T12 2024.pdf").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "my rent roll.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "high"},
        {"source_path": str(src / "T12 2024.pdf"),
         "classified_as": "t12", "classification_confidence": "high"},
    ]

    copy_sources(out, classifications)

    assert (out / "sources" / "rent-roll.xlsx").exists()
    assert (out / "sources" / "t12.pdf").exists()


def test_copy_multiple_same_type_gets_suffix(tmp_path: Path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "rr1.xlsx").write_bytes(b"x")
    (src / "rr2.xlsx").write_bytes(b"y")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "rr1.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "high"},
        {"source_path": str(src / "rr2.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "high"},
    ]
    copy_sources(out, classifications)
    names = sorted(p.name for p in (out / "sources").iterdir())
    assert names == ["rent-roll-2.xlsx", "rent-roll.xlsx"]


def test_unclassified_goes_to_unclassified_folder(tmp_path: Path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "mystery.bin").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "mystery.bin"),
         "classified_as": "other", "classification_confidence": "low"},
    ]
    copy_sources(out, classifications)
    assert (out / "sources" / "unclassified" / "mystery.bin").exists()


def test_leases_go_to_leases_subfolder(tmp_path: Path):
    src = tmp_path / "in"
    src.mkdir()
    (src / "Acme Lease.pdf").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "Acme Lease.pdf"),
         "classified_as": "lease", "classification_confidence": "high"},
    ]
    copy_sources(out, classifications)
    files = list((out / "sources" / "leases").iterdir())
    assert len(files) == 1
    assert files[0].suffix == ".pdf"


def test_rerun_does_not_duplicate_named_class(tmp_path: Path):
    """Re-running with the same classifications must NOT accumulate numbered duplicates."""
    src = tmp_path / "in"
    src.mkdir()
    (src / "rr.xlsx").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "rr.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "high"},
    ]

    copy_sources(out, classifications)
    copy_sources(out, classifications)

    names = sorted(p.name for p in (out / "sources").iterdir())
    assert names == ["rent-roll.xlsx"]


def test_missing_source_is_reported_not_crashed(tmp_path: Path):
    """A missing source_path must be collected as a warning, not abort the loop."""
    src = tmp_path / "in"
    src.mkdir()
    (src / "present.xlsx").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "ghost.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "high"},
        {"source_path": str(src / "present.xlsx"),
         "classified_as": "t12", "classification_confidence": "high"},
    ]

    warnings = copy_sources(out, classifications)

    assert len(warnings) == 1
    assert "ghost.xlsx" in warnings[0]
    # The good file still copies
    assert (out / "sources" / "t12.xlsx").exists()


def test_low_confidence_lease_still_goes_to_leases(tmp_path: Path):
    """Confidence-routing policy: lease/photo overrides low-confidence gate.
    (Only other named classes with low confidence go to unclassified/.)"""
    src = tmp_path / "in"
    src.mkdir()
    (src / "maybe-lease.pdf").write_bytes(b"x")
    (src / "maybe-rent-roll.xlsx").write_bytes(b"x")
    out = tmp_path / "pack"
    out.mkdir()

    classifications = [
        {"source_path": str(src / "maybe-lease.pdf"),
         "classified_as": "lease", "classification_confidence": "low"},
        {"source_path": str(src / "maybe-rent-roll.xlsx"),
         "classified_as": "rent_roll", "classification_confidence": "low"},
    ]
    copy_sources(out, classifications)

    # lease + low → still leases/
    assert any((out / "sources" / "leases").iterdir())
    # rent_roll + low → unclassified/
    assert (out / "sources" / "unclassified").exists()
    assert any((out / "sources" / "unclassified").iterdir())
