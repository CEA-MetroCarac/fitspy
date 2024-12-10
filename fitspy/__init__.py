from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel)
from .core.models import (gaussian, lorentzian, gaussian_asym, lorentzian_asym,
                           pseudovoigt)

VERSION = "2024.12dev"

PEAK_MODELS = {"Gaussian": gaussian,
               "Lorentzian": lorentzian,
               "PseudoVoigt": pseudovoigt,
               "GaussianAsym": gaussian_asym,
               "LorentzianAsym": lorentzian_asym}

PEAK_PARAMS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']

BKG_MODELS = {'None': None,
              'Constant': ConstantModel,
              'Linear': LinearModel,
              'Parabolic': ParabolicModel,
              'Exponential': ExponentialModel}

FIT_METHODS = {'Leastsq': 'leastsq', 'Least_squares': 'least_squares',
               'Nelder-Mead': 'nelder', 'SLSQP': 'slsqp'}
FIT_PARAMS = {'method': 'leastsq', 'fit_negative': False, 'fit_outliers': False,
              'max_ite': 200, 'coef_noise': 1, 'xtol': 1.e-4}

DEFAULTS = {
    'theme': 'dark',
    'ncpus' : 'Auto',
    'outliers_coef': 1.5,
    'click_mode': 'baseline',
    'peaks_cmap': 'Set1',
    'map_cmap': 'viridis',
    'figure_options': {
        'title': 'DEFAULT_TITLE (edit in toolbar)',
    },
    'view_options': {
        "raw": False,
        "legend": True,
        "fit": True,
        "negative_values": True,
        "outliers": True,
        "outliers_limits": True,
        "noise_level": True,
        "baseline": True,
        "subtract_bkg+baseline": True,
        "background": True,
        "residual": True,
        "peaks": True,
        "peak_labels": True,
        'preserve_axes': False,
    },
    "fit_params": {
        "method": "Leastsq",
        "fit_negative": False,
        "fit_outliers": False,
        "max_ite": 200,
        "coef_noise": 1,
        "xtol": 1.e-4,
    },
}