import pytest
from pytest import approx

from examples.ex_gui_peak_models_in_noise import ex_gui_peak_models_in_noise
from utils import extract_results, display_is_ok


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_peak_models_in_noise(tmp_path):
    ex_gui_peak_models_in_noise(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[183.96516988686062, 43.40369992828406, 88.2046106657544],
            [184.892578, 0.0, 0.1]]

    for result, reference in zip(results, refs):
        assert result == approx(reference, rel=1e-3)
