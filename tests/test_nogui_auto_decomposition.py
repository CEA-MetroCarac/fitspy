import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_auto_decomposition import auto_decomposition

REFS = [[142.20138763507413, 28162.24996899535, 8.670469601328865],
        [137.67691361112077, 19211.63226662505, 16.577782070805288],
        [365.76179011576136, 10569.776215226759, 68.88067368558646]]


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
        assert result == pytest.approx(reference, rel=2e-2)
