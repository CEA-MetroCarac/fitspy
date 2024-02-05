import numpy as np
import pytest
from pytest import approx

from examples.ex_nogui_auto_decomposition import auto_decomposition


def test_auto_decomposition():
    spectra = auto_decomposition(verbosity=False)

    # refs = []
    # for i in range(3):
    #     ampli = spectra[i].models[0].param_hints['ampli']['value']
    #     refs.append([np.sum(spectra[i].y), ampli])
    # print(refs)

    refs = [[896641.9940061372, 28142.739608259562],
            [890727.8824949837, 18900.368843277593],
            [737968.1326228122, 9618.511108857907]]

    assert len(spectra) > 0
    for spectrum, ref in zip(spectra, refs):
        ampli = spectrum.peak_models[0].param_hints['ampli']['value']
        assert np.sum(spectrum.y) == approx(ref[0], rel=1e-2)
        assert ampli == approx(ref[1], rel=1e-2)
