import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_auto_decomposition import auto_decomposition

REFS = [[142.20138680375223, 28162.255320876746, 8.670466023817895],
        [137.7556804297039, 19412.83928166068, 18.302702697333565],
        [366.6256443010156, 10544.22774218763, 65.74899212251415]]


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
        assert result == pytest.approx(reference, rel=1e-1)
