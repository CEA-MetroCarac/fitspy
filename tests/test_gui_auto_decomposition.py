import pytest
from pytest import approx

from examples.ex_gui_auto_decomposition import gui_auto_decomposition
from utils import extract_results, display_is_ok


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_auto_decomposition(tmp_path):
    gui_auto_decomposition(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[142.20639528801823, 28071.78403149393, 8.301985144865942],
            [137.7624794685612, 18872.059509383627, 14.717825498291326],
            [365.9346475383543, 10717.74486424568, 72.09944175956193]]

    for result, reference in zip(results, refs):
        assert result == approx(reference, rel=2e-2)
