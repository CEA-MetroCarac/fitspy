import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_peak_models_parameters_setting import ex_nogui_peak_models_parameters_setting


def test_nogui_peak_models_parameters_setting():
    results = ex_nogui_peak_models_parameters_setting()

    assert results == pytest.approx([199.919, 218.340, 300, 109.170], abs=1e-1)
