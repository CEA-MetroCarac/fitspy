import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_weights_in_fit import ex_nogui_weights_in_fit


def test_nogui_reload_model(tmpdir):
    results = ex_nogui_weights_in_fit(tmpdir)

    assert results[0] == pytest.approx([4., 14., 24., 34., 44.])
    assert results[1] == pytest.approx([10., 20., 30., 40., 50.])
