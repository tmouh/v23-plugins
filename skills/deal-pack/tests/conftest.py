from pathlib import Path
import pytest

FIXTURES = Path(__file__).parent / "fixtures"

@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES

@pytest.fixture
def tmp_pack_dir(tmp_path: Path) -> Path:
    out = tmp_path / "deal-pack-out"
    out.mkdir()
    return out
