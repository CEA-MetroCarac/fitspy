import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_peak_models_parameters_setting import ex_nogui_peak_models_parameters_setting

REF = [199.91928386217884, 218.3402514001517, 300, 109.17012570007584]


def test_nogui_peak_models_parameters_setting():
    results = ex_nogui_peak_models_parameters_setting()

    assert results == pytest.approx(REF)
