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
    # print([[float(v) for v in row] for row in results])

    refs = [[519.828125, 900.0790380810653, 9.370228944175173, 13.451707220872208],
            [519.828125, 880.2267946084944, 9.961363337259716, 14.09902552630537],
            [519.828125, 877.4370858435809, 9.931432325779353, 13.953648413631203],
            [519.828125, 890.9546186060418, 9.674808815205369, 13.653814217758756],
            [519.828125, 918.3718519575558, 9.54456943957933, 13.254647942228354]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
        # assert result[:2] == approx(reference[:2], rel=1e-1)
