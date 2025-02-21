"""
basic tests suite
"""
import numpy as np
from pytest import approx

from fitspy.core.spectrum import Spectrum


def generate_basic_spectrum():
    spectrum = Spectrum()
    spectrum.x = np.arange(0., 300.)
    spectrum.y = 100 * np.ones_like(spectrum.x)
    spectrum.add_peak_model('Gaussian', x0=100)
    spectrum.add_peak_model('Gaussian', x0=200)
    return spectrum


def test_with_no_constraint():
    spectrum = generate_basic_spectrum()
    spectrum.fit()

    assert spectrum.peak_models[0].param_hints['ampli']['value'] == approx(82., abs=1)
    assert spectrum.peak_models[1].param_hints['ampli']['value'] == approx(82., abs=1)


def test_with_fixed_ampli():
    spectrum = generate_basic_spectrum()
    spectrum.peak_models[0].param_hints['ampli']['vary'] = False
    spectrum.fit()

    assert spectrum.peak_models[0].param_hints['ampli']['value'] == 100.
    assert spectrum.peak_models[1].param_hints['ampli']['value'] == approx(81., abs=1)


def test_with_expression():
    spectrum = generate_basic_spectrum()
    spectrum.peak_models[1].param_hints['ampli']['expr'] = 'm01_ampli*0.5'
    spectrum.fit()

    assert spectrum.peak_models[1].param_hints['ampli']['value'] == \
           0.5 * spectrum.peak_models[0].param_hints['ampli']['value']


def test_with_fixed_ampli_and_expression():
    spectrum = generate_basic_spectrum()
    spectrum.peak_models[0].param_hints['ampli']['vary'] = False
    spectrum.peak_models[1].param_hints['ampli']['expr'] = 'm01_ampli*0.5'
    spectrum.fit()

    assert spectrum.peak_models[0].param_hints['ampli']['value'] == 100.
    assert spectrum.peak_models[1].param_hints['ampli']['value'] == 50.
