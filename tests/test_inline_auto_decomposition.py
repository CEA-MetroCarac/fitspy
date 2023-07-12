import numpy as np
import pytest
from pytest import approx

from examples.ex4_inline_auto_decomposition import inline_auto_decomposition


def test_inline_auto_decomposition(tmp_path):
    spectra = inline_auto_decomposition(verbosity=False)

    # refs = []
    # for i in range(3):
    #     ampli = spectra[i].models[0].param_hints['ampli']['value']
    #     refs.append([np.sum(spectra[i].y), ampli])
    # print(refs)

    refs = [[896641.9940061372, 28146.72777729365],
            [890727.8824949837, 18920.21153480585],
            [737968.1326228122, 9630.572508960488]]

    for spectrum, ref in zip(spectra, refs):
        ampli = spectrum.models[0].param_hints['ampli']['value']
        assert np.sum(spectrum.y) == approx(ref[0])
        assert ampli == approx(ref[1], rel=1e-3)
