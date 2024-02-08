from pathlib import Path
import shutil
import matplotlib.pyplot as plt
from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel)

from fitspy.utils import load_models_from_txt, load_models_from_py
from fitspy.models import (gaussian, lorentzian, gaussian_asym, lorentzian_asym,
                           pseudovoigt)

VERSION = "2024.3beta"

FITSPY_DIR = Path.home() / "Fitspy"
SETTINGS_FNAME = FITSPY_DIR / "settings.json"

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

# MODELS_NAMES = list(PEAK_MODELS.keys()) + list(BKG_MODELS.keys())

FIT_METHODS = {'Leastsq': 'leastsq', 'Least_squares': 'least_squares',
               'Nelder-Mead': 'nelder', 'SLSQP': 'slsqp'}
FIT_PARAMS = {'method': 'leastsq', 'fit_negative': False, 'fit_outliers': False,
              'max_ite': 200, 'coef_noise': 1, 'xtol': 1.e-4}
ATTRACTORS_PARAMS = {'distance': 20, 'prominence': None,
                     'width': None, 'height': None, 'threshold': None}
NCPUS = ['auto', 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32]
CMAP = plt.get_cmap("tab10")

################################################################################

# create FITSPY_DIR if not exists
Path.mkdir(FITSPY_DIR, exist_ok=True)

# move and rename old settings file
fname = Path.home() / '.fitspy.json'
if fname.exists():
    shutil.move(fname, SETTINGS_FNAME)

# add users models from '.txt' file
load_models_from_txt(FITSPY_DIR / "peak_models.txt", PEAK_MODELS)
load_models_from_txt(FITSPY_DIR / "bkg_models.txt", BKG_MODELS)

# add users models from '.py' file
load_models_from_py(FITSPY_DIR / "peak_models.py")
load_models_from_py(FITSPY_DIR / "bkg_models.py")
