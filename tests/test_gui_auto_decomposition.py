import pytest
from pytest import approx

from examples.ex_gui_auto_decomposition import gui_auto_decomposition
from utils import extract_results, display_is_ok


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_auto_decomposition(tmp_path):
    gui_auto_decomposition(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[142.2063952870293, 28071.7840261713, 8.30198514788677],
            [137.76247944776298, 18872.059537827474, 14.717825224085768],
            [365.9688879244104, 10719.133628864241, 71.84603593278625]]

    for result, reference in zip(results, refs):
        assert result == approx(reference, rel=2e-2)
