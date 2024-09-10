from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel)
from .core.models import (gaussian, lorentzian, gaussian_asym, lorentzian_asym,
                           pseudovoigt)

from .core import *

VERSION = "2024.8dev"

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
}