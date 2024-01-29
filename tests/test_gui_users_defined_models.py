import pytest
from pytest import approx

from examples.ex_gui_users_defined_models import ex_gui_users_models_from_txt
from examples.ex_gui_users_defined_models import ex_gui_users_models_from_py
from utils import extract_results, display_is_ok

REFS = [[520.1862765603815, 915.2649558822233, 9.57229876472696],
        [520.0548336803745, 895.8558065545101, 9.941802903292885],
        [519.9924492642288, 892.7863717814992, 9.84735702289229],
        [520.0449179477414, 903.3890860484772, 9.642083813467073],
        [520.0348659274093, 931.4012074028958, 9.52151902889371]]


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
