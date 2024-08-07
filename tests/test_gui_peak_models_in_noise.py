import pytest
from pytest import approx

from examples.ex_gui_peak_models_in_noise import ex_gui_peak_models_in_noise
from utils import extract_results, display_is_ok


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_peak_models_in_noise(tmp_path):
    ex_gui_peak_models_in_noise(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[183.97390206707158, 43.34103197326187, 88.17499327790364],
            [183.9526502120302, 0.0, 0.1]]


    for result, reference in zip(results, refs):
        assert result == approx(reference, rel=1e-3)
