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

# create FITSPY_DIR if not exists
Path.mkdir(FITSPY_DIR, exist_ok=True)

# move and rename old settings file
fname = Path.home() / '.fitspy.json'
if fname.exists():
    shutil.move(fname, SETTINGS_FNAME)

# add users models from '.txt' file
for name, models in zip(["models.txt", "bkg_models.txt"], [MODELS, BKG_MODELS]):
    fname = FITSPY_DIR / name
    if fname.exists():
        with open(fname, 'r') as fid:
            for line in fid.readlines():
                words = line.split('=')
                if len(words) == 2:
                    name, expr = words[0], words[1]
                    try:
                        model = ExpressionModel(expr, independent_vars=['x'])
                        model.__name__ = name
                        models.update({name: model})
                        print(f"{name} ADDED")
                    except:
                        print(f"{name} INCORRECT EXPRESSION")
                      
# add users models from '.py' file
for name in ["models.py", "bkg_models.py"]:
    fname = FITSPY_DIR / name
    if fname.exists():
        runpy.run_path(fname)
