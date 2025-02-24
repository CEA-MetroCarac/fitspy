import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_2d_maps import gui_2d_maps
from utils import extract_results, display_is_ok

GUI = ['pyside', 'tkinter']


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_2d_maps(tmp_path, gui):
    gui_2d_maps(dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[519.0684024010793, 900.4203033836302, 8.034524162768186, 14.715997321882002],
            [518.7954831522079, 881.5478764692664, 8.194739134794649, 15.96084245188858],
            [518.7020745290181, 881.1525134056783, 7.8877400391386026, 15.719018760082593],
            [518.836370327552, 890.6208185699355, 8.02767223853531, 15.410391164292548],
            [518.924006721169, 918.1000550166215, 7.996515556717398, 14.735078181904104]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=3e-4)
        # assert result[:2] == approx(reference[:2], rel=1e-1)
