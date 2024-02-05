import pytest
from pytest import approx

from examples.ex_gui_users_defined_models import ex_gui_users_models_from_txt
from examples.ex_gui_users_defined_models import ex_gui_users_models_from_py
from utils import extract_results, display_is_ok

REFS = [[520.1876881673046, 914.6124158904634, 9.567844475317354],
        [520.0556606848833, 894.5345845967921, 9.952711474248666],
        [519.9940849383077, 891.9396250396445, 9.841426352805783],
        [520.0467482325055, 901.1376908860237, 9.648304792926787],
        [520.0361487475782, 930.5679755394866, 9.522399137846483]]


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
@pytest.mark.parametrize("ncpus", [1])
def test_gui_users_models_from_txt(ncpus, tmp_path):
    ex_gui_users_models_from_txt(ncpus=ncpus, dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print("results from txt", results)

    for result, reference in zip(results, REFS):
        assert result == approx(reference, rel=1e-3)


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
@pytest.mark.parametrize("ncpus", [1])
def test_gui_users_models_from_py(ncpus, tmp_path):
    ex_gui_users_models_from_py(ncpus=ncpus, dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print("results from py", results)

    for result, reference in zip(results, REFS):
        assert result == approx(reference, rel=1e-3)
