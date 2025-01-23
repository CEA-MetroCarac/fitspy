import warnings
from fitspy.core.spectrum import Spectrum

warnings.warn(
    "The module 'fitspy.spectrum' is deprecated and will be removed in a future release. "
    "Please use 'fitspy.core.spectrum' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['Spectrum']
