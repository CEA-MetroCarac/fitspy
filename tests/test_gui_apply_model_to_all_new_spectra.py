import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_apply_model_to_all_new_spectra import gui_apply_model_to_all
from utils import extract_results, display_is_ok

GUI = ['pyside', 'tkinter']


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_apply_model_to_all(tmp_path, gui):
    gui_apply_model_to_all(dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[342.9457600721084, 378.1308709613353, 2.63705383055729],
            [342.915947718005, 376.40856906800724, 2.730686395444859],
            [342.8311792192351, 345.1669426213287, 2.702655359738426]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
