import numpy as np
import sys
import pytest
from pathlib import Path
from pytest import approx

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from test_gui_auto_decomposition import REFS

from ex_nogui_auto_decomposition import auto_decomposition


def test_auto_decomposition():
    spectra = auto_decomposition(verbosity=False)

    results = []
    for i in range(3):
        x0 = spectra[i].peak_models[0].param_hints['x0']['value']
        ampli = spectra[i].peak_models[0].param_hints['ampli']['value']
        fwhm = spectra[i].peak_models[0].param_hints['fwhm']['value']
        results.append([x0, ampli, fwhm])
    # print(results)

    for result, reference in zip(results, REFS):
        assert result == approx(reference, rel=2e-2)
