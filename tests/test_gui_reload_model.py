import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_reload_model import gui_reload_model_with_data
from utils import extract_results, display_is_ok

GUI = ['pyside', 'tkinter']


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_reload_model_with_data(tmp_path, gui):
    gui_reload_model_with_data(dirname_res=tmp_path, gui=gui)

