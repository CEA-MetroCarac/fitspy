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

    refs = [[519.0598404532075, 900.5819823059829, 8.04336240368973, 14.796357953389354],
            [518.8053176006631, 881.4294359888734, 8.189554268841054, 15.874466689976543],
            [518.6870537736993, 881.3126190354161, 7.9002075677256896, 15.86751666154244],
            [518.8389270287249, 890.6397735803048, 8.029808987147522, 15.39499284012152],
            [518.9112778501792, 918.3360431035568, 8.013536113636265, 14.85654542809592]]

    for result, reference in zip(results, refs):
        assert result == pytest.approx(reference, rel=1e-3)
        # assert result[:2] == approx(reference[:2], rel=1e-1)
