import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_reload_model import ex_nogui_reload_model

REFS = [[342.9457564696991, 378.13400093534824, 2.636983225184053],
        [342.9160159719629, 376.4534016430965, 2.7295716784484503],
        [342.831170750272, 345.1637632551555, 2.702748182015513]]


def test_nogui_reload_model():
    spectra = ex_nogui_reload_model()

    results = []
    for i in range(3):
        x0 = spectra[i].peak_models[0].param_hints['x0']['value']
        ampli = spectra[i].peak_models[0].param_hints['ampli']['value']
        fwhm = spectra[i].peak_models[0].param_hints['fwhm']['value']
        results.append([x0, ampli, fwhm])
    # print(results)

    for result, reference in zip(results, REFS):
        assert result == pytest.approx(reference, rel=1e-2)
