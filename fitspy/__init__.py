from pathlib import Path
import shutil
from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel)

from fitspy.utils import load_models_from_txt, load_models_from_py
from fitspy.models import (gaussian, lorentzian, gaussian_asym, lorentzian_asym,
                           pseudovoigt)

VERSION = "2024.2beta"

FITSPY_DIR = Path.home() / "Fitspy"
SETTINGS_FNAME = FITSPY_DIR / "settings.json"

MODELS = {"Gaussian": gaussian,
          "Lorentzian": lorentzian,
          "PseudoVoigt": pseudovoigt,
          "GaussianAsym": gaussian_asym,
          "LorentzianAsym": lorentzian_asym}

PARAMS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']

BKG_MODELS = {'None': None,
              'Constant': ConstantModel,
              'Linear': LinearModel,
              'Parabolic': ParabolicModel,
              'Exponential': ExponentialModel}

# create FITSPY_DIR if not exists
Path.mkdir(FITSPY_DIR, exist_ok=True)

# move and rename old settings file
fname = Path.home() / '.fitspy.json'
if fname.exists():
    shutil.move(fname, SETTINGS_FNAME)

# add users models from '.txt' file
load_models_from_txt(FITSPY_DIR / "models.txt", MODELS)
load_models_from_txt(FITSPY_DIR / "bkg_models.txt", BKG_MODELS)

# add users models from '.py' file
load_models_from_py(FITSPY_DIR / "models.py")
load_models_from_py(FITSPY_DIR / "bkg_models.py")
