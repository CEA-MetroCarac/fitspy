import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_2d_maps import gui_2d_maps
from utils import extract_results, display_is_ok

GUI = ['pyside']


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_2d_maps(tmp_path, gui):
    gui_2d_maps(dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[519.0597355357378, 900.589847580606, 8.043523159773423, 14.797537682645855],
            [518.7975124264627, 881.6155595872426, 8.197671043789663, 15.950864623098424],
            [518.6863952306043, 881.3211676783927, 7.900765837795629, 15.873993303729254],
            [518.8325169701028, 890.6385154988625, 8.032328226006065, 15.44842083166991],
            [518.9101495778642, 918.349518185171, 8.01455589734634, 14.86667422550771]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
        # assert result[:2] == approx(reference[:2], rel=1e-1)
