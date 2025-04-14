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

    refs = [[519.0684607467697, 900.4249868710439, 8.034550983225719, 14.715736704155534],
            [518.7955198169003, 881.5518532807071, 8.194732219253183, 15.96063214265735],
            [518.7020754300324, 881.1534894449298, 7.887725581023911, 15.71898061002282],
            [518.8363752383725, 890.6243181228442, 8.027605499330496, 15.410272948729979],
            [518.9240535481656, 918.1048452610236, 7.996505623914084, 14.734852747177257]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
        # assert result[:2] == approx(reference[:2], rel=1e-1)
