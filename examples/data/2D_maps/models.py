"""
module description
"""
from fitspy import MODELS


def lorentzian_user(x, ampli, x0, fwhm):
    return ampli * fwhm ** 2 / (4 * ((x - x0) ** 2 + fwhm ** 2 / 4))


MODELS.update({'Lorentzian_user': lorentzian_user})
