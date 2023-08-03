import pytest
from pytest import approx

from examples.ex0_gui_auto_decomposition import gui_auto_decomposition
from utils import extract_results


def test_gui_auto_decomposition(tmp_path):
    gui_auto_decomposition(dirname_res=tmp_path)

    results = extract_results(dirname_res=tmp_path)
    # print(results)

    refs = [[142.20616011719073, 28080.063179759956, 8.29468693999813],
            [137.76510890707695, 18898.387213281483, 14.653606449091361],
            [365.93083875575996, 10720.161126347022, 72.09201006313779]]

    for result, reference in zip(results, refs):
        assert result == approx(reference, rel=1e-3)
