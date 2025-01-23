import warnings
from fitspy.core.spectra import Spectra

warnings.warn(
    "The module 'fitspy.spectra' is deprecated and will be removed in a future release. "
    "Please use 'fitspy.core.spectra' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['Spectra']
