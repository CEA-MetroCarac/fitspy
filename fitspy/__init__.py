from pathlib import Path
from lmfit.models import (ConstantModel, LinearModel, ParabolicModel,
                          ExponentialModel)

from fitspy.utils import get_func
from fitspy.models import (gaussian, lorentzian,
                           gaussian_asym, lorentzian_asym, pseudovoigt)

VERSION = "2024.1"

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

# add users models
for model in get_func(Path.home() / "fitspy_users_models.py"):
    MODELS.update({model[0]: model[1]})

# add users BKG models
for bkg_model in get_func(Path.home() / "fitspy_users_bkg_models.py"):
    BKG_MODELS.update({bkg_model[0]: bkg_model[1]})
