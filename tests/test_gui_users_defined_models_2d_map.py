import sys
from pathlib import Path
import pytest

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_gui_users_defined_models_2d_map import (ex_gui_users_models_from_txt,
                                                ex_gui_users_models_from_py)
from utils import extract_results, display_is_ok

GUI = ['pyside', 'tkinter']

REFS = [[520.1831869201959, 914.2251483716625, 9.564640452707362],
        [520.0392791068225, 891.6160584025431, 9.940131898953696],
        [519.9866776205414, 885.66321943769, 9.707212537881095],
        [520.0460423126672, 895.6053984636752, 9.604471066389609],
        [520.027027026052, 932.8866912354766, 9.565131282488492]]


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
@pytest.mark.parametrize("ncpus", [1])
def test_gui_users_models_from_txt(ncpus, tmp_path, gui):
    ex_gui_users_models_from_txt(ncpus=ncpus, dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print("results from txt", results)

    for result, reference in zip(results, REFS):
        assert result == pytest.approx(reference, rel=1e-3)


@pytest.mark.parametrize("gui", GUI)
@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
@pytest.mark.parametrize("ncpus", [1])
def test_gui_users_models_from_py(ncpus, tmp_path, gui):
    ex_gui_users_models_from_py(ncpus=ncpus, dirname_res=tmp_path, gui=gui)

    results = extract_results(dirname_res=tmp_path)
    # print("results from py", results)

    for result, reference in zip(results, REFS):
        assert result == pytest.approx(reference, rel=1e-3)
