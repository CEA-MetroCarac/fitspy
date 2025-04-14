import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_auto_decomposition import auto_decomposition

REFS = [[142.20173394157536, 28029.553322965676, 8.277809848923237],
        [137.67515335154644, 18759.151666487996, 14.97995202104921],
        [365.54213838295374, 5707.388347846296, 27.396225431364314]]


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
        assert result == pytest.approx(reference, rel=5e-2)
