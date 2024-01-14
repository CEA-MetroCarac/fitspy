from pathlib import Path
import shutil
import runpy
from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel, ExpressionModel)

from fitspy.models import (gaussian, lorentzian,
                           gaussian_asym, lorentzian_asym, pseudovoigt)

VERSION = "2024.1"

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

Path.mkdir(FITSPY_DIR, exist_ok=True)

# move and rename old settings file
fname = Path.home() / '.fitspy.json'
if fname.exists():
    shutil.move(fname, SETTINGS_FNAME)

# add users models from '.py' file
for name in ["models.py", "bkg_models.py"]:
    fname = FITSPY_DIR / name
    if fname.exists():
        runpy.run_path(fname, run_name='__main__')
