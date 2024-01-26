"""
module description
"""
from fitspy import BKG_MODELS


def linear_user(x, slope, constant):
    return slope * x + constant


BKG_MODELS.update({'Linear_user': linear_user})
