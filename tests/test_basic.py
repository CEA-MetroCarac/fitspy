"""
basic tests suite
"""
import numpy as np
from pytest import approx
import pytest

from fitspy.core.spectrum import Spectrum
from fitspy.core.models import gaussian


@pytest.fixture
def basic_spectrum():
    spectrum = Spectrum()
    spectrum.x = np.arange(0., 300.)
    spectrum.y = 100 * np.ones_like(spectrum.x)
    spectrum.x0 = spectrum.x.copy()
    spectrum.y0 = spectrum.y.copy()
    spectrum.add_peak_model('Gaussian', x0=100)
    spectrum.add_peak_model('Gaussian', x0=200)
    return spectrum


@pytest.fixture
def basic_spectrum2():
    spectrum = Spectrum()
    x = np.arange(0., 100.)
    y = gaussian(x, ampli=20, fwhm=20, x0=40) + gaussian(x, ampli=30, fwhm=10, x0=60)
    spectrum.x = x
    spectrum.y = y
    spectrum.x0 = spectrum.x.copy()
    spectrum.y0 = spectrum.y.copy()
    spectrum.add_peak_model('Gaussian', x0=30)
    spectrum.add_peak_model('Gaussian', x0=65)

    # import matplotlib.pyplot as plt
    # _, ax= plt.subplots()
    # spectrum.fit()
    #
    # spectrum.plot(ax)
    # plt.show()

    return spectrum


def test_with_no_constraint(basic_spectrum2):
    basic_spectrum2.fit()

    assert basic_spectrum2.peak_models[0].param_hints['ampli']['value'] == approx(20, abs=1)
    assert basic_spectrum2.peak_models[1].param_hints['ampli']['value'] == approx(30, abs=1)


def test_with_fixed_ampli(basic_spectrum2):
    basic_spectrum2.peak_models[0].param_hints['ampli']['vary'] = False
    basic_spectrum2.fit()

    assert basic_spectrum2.peak_models[0].param_hints['ampli']['value'] == approx(10, abs=1)
    assert basic_spectrum2.peak_models[1].param_hints['ampli']['value'] == approx(27, abs=1)


def test_with_expression(basic_spectrum2):
    basic_spectrum2.peak_models[1].param_hints['ampli']['expr'] = 'm01_ampli*0.5'
    basic_spectrum2.fit()

    assert basic_spectrum2.peak_models[1].param_hints['ampli']['value'] == \
           0.5 * basic_spectrum2.peak_models[0].param_hints['ampli']['value']


def test_with_fixed_ampli_and_expression(basic_spectrum2):
    basic_spectrum2.peak_models[0].param_hints['ampli']['vary'] = False
    basic_spectrum2.peak_models[1].param_hints['ampli']['expr'] = 'm01_ampli*0.5'
    basic_spectrum2.fit()

    assert basic_spectrum2.peak_models[0].param_hints['ampli']['value'] == approx(10, abs=1)
    assert basic_spectrum2.peak_models[1].param_hints['ampli']['value'] == approx(5, abs=1)


def test_apply_range(basic_spectrum):
    basic_spectrum.apply_range(range_min=50, range_max=150)
    assert np.all(basic_spectrum.x >= 50)
    assert np.all(basic_spectrum.x <= 150)
    assert np.all(basic_spectrum.y == 100)


def test_calculate_outliers(basic_spectrum):
    basic_spectrum.outliers_limit = 110 * np.ones_like(basic_spectrum.x)
    x_outliers, _ = basic_spectrum.calculate_outliers()
    assert x_outliers is None

    basic_spectrum.y0[10] = 120
    basic_spectrum.apply_range(range_min=0, range_max=20)
    basic_spectrum.outliers_limit = 110 * np.ones_like(basic_spectrum.x0)
    x_outliers, _ = basic_spectrum.calculate_outliers()
    assert len(x_outliers) == 1
    assert x_outliers[0] == 10


def test_normalization(basic_spectrum):
    basic_spectrum.y[10] = 120
    basic_spectrum.normalize = True
    basic_spectrum.normalize_range_min = 20
    basic_spectrum.normalize_range_max = 30
    basic_spectrum.normalization()
    assert np.min(basic_spectrum.y) == approx(100.0)
    assert np.max(basic_spectrum.y) == approx(120.0)

    basic_spectrum.normalize_range_min = 0
    basic_spectrum.normalize_range_max = 20
    basic_spectrum.normalization()
    assert np.min(basic_spectrum.y) == approx(100 / 120 * 100)
    assert np.max(basic_spectrum.y) == approx(100.0)


def test_linear_baseline(basic_spectrum):
    basic_spectrum.baseline.mode = 'Linear'
    basic_spectrum.baseline.attached = False
    basic_spectrum.baseline.add_point(50, 50)
    basic_spectrum.baseline.add_point(150, 50)
    basic_spectrum.eval_baseline()
    basic_spectrum.subtract_baseline()
    assert basic_spectrum.baseline.y_eval is not None
    assert basic_spectrum.baseline.is_subtracted
    assert np.all(basic_spectrum.y == 50)


def test_semiauto_baseline(basic_spectrum):
    x = basic_spectrum.x
    peak = 50 * np.exp(-((x - 150) ** 2) / (2 * 20 ** 2))
    basic_spectrum.y = basic_spectrum.y + peak
    basic_spectrum.auto_baseline()
    assert basic_spectrum.baseline.mode == 'Semi-Auto'
    basic_spectrum.eval_baseline()

    # Check that the maximum of the evaluated baseline occurs near the peak position (x=150)
    idx_peak = np.argmax(basic_spectrum.baseline.y_eval)
    peak_position = basic_spectrum.x[idx_peak]
    assert abs(peak_position - 150) < 5


def test_remove_models(basic_spectrum):
    basic_spectrum.remove_models()
    assert len(basic_spectrum.peak_models) == 0
    assert basic_spectrum.bkg_model is None


def test_fit_method(basic_spectrum):
    basic_spectrum.fit(fit_method='least_squares')
    assert basic_spectrum.result_fit.success


def test_reinit(basic_spectrum):
    basic_spectrum.apply_range(range_min=50, range_max=150)
    basic_spectrum.reinit()
    assert basic_spectrum.range_min is None
    assert basic_spectrum.range_max is None
    assert np.all(basic_spectrum.x == basic_spectrum.x0)
    assert np.all(basic_spectrum.y == basic_spectrum.y0)


def test_del_peak_model(basic_spectrum):
    basic_spectrum.del_peak_model(0)
    assert len(basic_spectrum.peak_models) == 1
    assert len(basic_spectrum.peak_labels) == 1


def test_reorder(basic_spectrum):
    basic_spectrum.peak_models[0].param_hints['x0']['value'] = 150
    basic_spectrum.peak_models[1].param_hints['x0']['value'] = 50
    reordered_models = basic_spectrum.reorder()
    assert reordered_models[0].param_hints['x0']['value'] == 50
    reordered_models_reversed = basic_spectrum.reorder(reverse=True)
    assert reordered_models_reversed[0].param_hints['x0']['value'] == 150
