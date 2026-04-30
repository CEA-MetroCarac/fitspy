"""
Example of multiple backgrounds fitting
"""
import numpy as np
import matplotlib.pyplot as plt

from fitspy.core.spectrum import Spectrum
from fitspy.core.models import lorentzian


def ex_nogui_multiple_backgrounds(show_plots=False):
    """ Example of multiple backgrounds fitting """

    # Raw profile to be fitted
    x = np.linspace(0, 600, 250)
    y = lorentzian(x, ampli=200, fwhm=30, x0=200)
    y += 0.1 * x + 10  # linear component (bkg)
    y += 100 * np.exp(-x / 200)  # exponential component (bkg)

    # Spectrum object definition
    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y

    spectrum.add_peak_model('Lorentzian', x0=200)
    spectrum.add_bkg_model('Linear')
    spectrum.add_bkg_model('Exponential')

    y_model = np.zeros_like(x)
    for peak_model in spectrum.peak_models:
        params = peak_model.make_params()
        y_model += peak_model.eval(params, x=spectrum.x)
    for bkg_model in spectrum.bkg_models:
        params = bkg_model.make_params()
        y_model += bkg_model.eval(params, x=spectrum.x)

    # fitting
    spectrum.fit()
    y_fit = spectrum.result_fit.best_fit

    x1 = spectrum.bkg_models[0].param_hints['intercept']['value']
    y1 = spectrum.bkg_models[0].param_hints['slope']['value']
    x2 = spectrum.bkg_models[1].param_hints['amplitude']['value']
    y2 = spectrum.bkg_models[1].param_hints['decay']['value']

    print(x1, y1, x2, y2)

    if show_plots:

        plt.figure()
        plt.plot(x, y, 'ko', lw=0.5, mfc='none', ms=3, label='raw data')
        plt.plot(x, y_model, ls='dashed', label='guess init')
        plt.plot(x, y_fit, label='fit')
        plt.legend()
        plt.show()

    else:
        return x1, y1, x2, y2


if __name__ == "__main__":
    ex_nogui_multiple_backgrounds(show_plots=True)
