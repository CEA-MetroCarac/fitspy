import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_multiple_backgrounds import ex_nogui_multiple_backgrounds


def test_nogui_multiple_backgrounds():
    results = ex_nogui_multiple_backgrounds()

    assert results == pytest.approx([10, 0.1, 100, 200])
