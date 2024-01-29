"""
module description
"""
from fitspy import BKG_MODELS


def linear_user(x, slope, intercept):
    return slope * x + intercept


BKG_MODELS.update({'Linear_user': linear_user})
