import pytest
from pytest import approx

from examples.ex_gui_2d_maps import gui_2d_maps
from utils import extract_results, display_is_ok


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_2d_maps(tmp_path):
    gui_2d_maps(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[520.3121368156001, 904.3819512688175, 9.704633018161001]]

    for result, reference in zip(results, refs):
        assert result[:2] == approx(reference[:2], rel=1e-1)
