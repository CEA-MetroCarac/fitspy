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
    # refs = [[519.9424318275927, 909.044989427586, 9.431037718572544],
    #         [519.8161389632209, 862.2647695962206, 8.977313449464253],
    #         [519.6151859004931, 832.6779739275637, 8.46139537463687],
    #         [519.6930857481614, 858.5222625586348, 8.99635273373115],
    #         [519.8880811403608, 928.2394013220568, 9.15153606283462]]

    for result, reference in zip(results, refs):
        assert result[:2] == approx(reference[:2], rel=1e-1)
