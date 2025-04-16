import sys
from pathlib import Path
import pytest
import numpy as np

examples_path = Path(__file__).resolve().parent.parent / 'examples'
sys.path.insert(0, str(examples_path))

from ex_nogui_auto_decomposition import auto_decomposition

REFS = [[142.2017338937751, 28029.56087034003, 8.277805414840545],
        [137.67515324567708, 18759.15930233963, 14.979941168937462],
        [366.6105573370797, 8114.486816783022, 43.73282414562729]]


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
