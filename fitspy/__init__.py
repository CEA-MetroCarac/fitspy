from pathlib import Path

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

BKG_MODELS = ['None', 'Constant', 'Linear', 'Parabolic', 'Exponential']

# add users models
for model in get_func(Path.home() / "fitspy_users_models.txt"):
    MODELS.update({model[0]: model[1]})
