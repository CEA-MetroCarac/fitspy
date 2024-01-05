from fitspy.models import (gaussian, lorentzian,
                           gaussian_asym, lorentzian_asym, pseudovoigt)

MODELS = {"Gaussian": gaussian,
          "Lorentzian": lorentzian,
          "PseudoVoigt": pseudovoigt,
          "GaussianAsym": gaussian_asym,
          "LorentzianAsym": lorentzian_asym}

BKG_MODELS = ['None', 'Constant', 'Linear', 'Parabolic', 'Exponential']

KEYS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']

VERSION = "2024.1"
