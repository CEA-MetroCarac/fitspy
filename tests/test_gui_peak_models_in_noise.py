import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_peak_models_in_noise import ex_gui_peak_models_in_noise
from utils import extract_results, display_is_ok

GUI = ['pyside', 'tkinter']


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_peak_models_in_noise(tmp_path, gui):
    ex_gui_peak_models_in_noise(dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[183.97390206707158, 43.34103197326187, 88.17499327790364],
            [183.9526502120302, 0.0, 0.0]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
