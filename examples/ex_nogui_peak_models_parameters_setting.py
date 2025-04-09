"""
Example of peak models parameters setting
"""
import numpy as np
import matplotlib.pyplot as plt

from fitspy.core.spectrum import Spectrum, empty_expr
from fitspy.core.models import lorentzian, gaussian, lorentzian_asym


def ex_nogui_peak_models_parameters_setting(show_plots=False):
    """ Example of peak models parameters setting """

    # Raw profile to be fitted
    x = np.linspace(0, 600, 250)
    y = lorentzian(x, ampli=200, fwhm=30, x0=200)
    y += gaussian(x, ampli=120, fwhm=70, x0=300)
    y += lorentzian_asym(x, ampli=300, fwhm_l=40, fwhm_r=20, x0=500)

    # Peak models parameters setting
    peaks_params = {1: {'name': 'Lorentzian',
                        'x0': {'value': 180, 'min': 150, 'max': 220},
                        'fwhm': {'value': 40, 'min': 20, 'max': 60},
                        'ampli': {'expr': "2*m02_ampli"}},

                    2: {'name': 'Gaussian',
                        'x0': {'value': 300, 'vary': False},
                        'fwhm': {'value': 60, 'min': 40, 'max': 80}},

                    3: {'name': 'LorentzianAsym',
                        'x0': {'value': 480, 'min': 450, 'max': 620},
                        'fwhm_l': {'value': 30, 'min': 10, 'max': 50},
                        'fwhm_r': {'value': 30, 'min': 10, 'max': 50}}}

    # Spectrum object definition

    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y

    # create peaks with default values (name and x0 are mandatory values)
    for params in peaks_params.values():
        spectrum.add_peak_model(params['name'], params['x0']['value'])

    # replace default values with the user's ones ('min', 'max', 'vary', 'expr')
    for peak_model, params in zip(spectrum.peak_models, peaks_params.values()):
        [peak_model.set_param_hint(key, **vals) for key, vals in params.items() if key != 'name']

    # related initial profile as "guess init"
    y_model = np.zeros_like(x)
    for peak_model in spectrum.peak_models:
        with empty_expr(peak_model):  # remove 'expr' that can not be interpreted by make_params()
            params = peak_model.make_params()
        y_model += peak_model.eval(params, x=spectrum.x)

    # fitting
    spectrum.fit()
    y_fit = spectrum.result_fit.best_fit

    x1 = spectrum.peak_models[0].param_hints['x0']['value']
    y1 = spectrum.peak_models[0].param_hints['ampli']['value']
    x2 = spectrum.peak_models[1].param_hints['x0']['value']
    y2 = spectrum.peak_models[1].param_hints['ampli']['value']

    print(x1, y1, x2, y2)

    if show_plots:

        plt.figure()
        plt.plot(x, y, 'ko', lw=0.5, mfc='none', ms=3, label='raw data')
        plt.plot(x, y_model, ls='dashed', label='guess init')
        plt.plot(x, y_fit, label='fit')
        plt.legend()

        x0, y0 = (320, 250)
        text = f'{round(y1, 2)} / {round(y2, 2)} = {y1 / y2}'
        plt.text(x0, y0 + 10, text, ha='center', va='center')
        plt.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="->"))
        plt.annotate('', xy=(x2, y2), xytext=(x0, y0), arrowprops=dict(arrowstyle="->"))

        plt.show()

    else:
        return x1, y1, x2, y2


if __name__ == "__main__":
    ex_nogui_peak_models_parameters_setting(show_plots=True)
