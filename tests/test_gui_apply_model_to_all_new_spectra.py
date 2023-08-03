import pytest
from pytest import approx

from examples.ex2_gui_apply_model_to_all_new_spectra import \
    gui_apply_model_to_all
from utils import extract_results


# def test_gui_apply_model_to_all(tmp_path):
#     gui_apply_model_to_all(dirname_res=tmp_path)

#     results = extract_results(dirname_res=tmp_path)
#     # print(results)

#     refs = [[342.9457211120893, 378.09030982705525, 2.6380066104951028],
#             [342.9150412043217, 375.82154387665815, 2.745553299964265],
#             [342.83109830632253, 345.13789148228784, 2.7035947899485047]]

#     for result, reference in zip(results, refs):
#         assert result == approx(reference, rel=1e-3)
