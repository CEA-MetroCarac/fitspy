import numpy as np
import pytest
from pytest import approx

from examples.ex_nogui_auto_decomposition import auto_decomposition


def test_auto_decomposition():
    spectra = auto_decomposition(verbosity=False)

    # refs = []
    # for i in range(3):
    #     ampli = spectra[i].peak_models[0].param_hints['ampli']['value']
    #     refs.append([np.sum(spectra[i].y), ampli])
    # print(refs)

    refs = [[695742.9828417138, 28035.104052186613],
            [645910.1509814768, 18783.270429923425],
            [588544.9856527029, 8125.02943468474]]

    assert len(spectra) > 0
    for spectrum, ref in zip(spectra, refs):
        ampli = spectrum.peak_models[0].param_hints['ampli']['value']
        assert np.sum(spectrum.y) == approx(ref[0], rel=1e-2)
        assert ampli == approx(ref[1], rel=1e-2)
