import warnings
from fitspy.core.spectra_map import SpectraMap

warnings.warn(
    "The module 'fitspy.spectra_map' is deprecated and will be removed in a future release. "
    "Please use 'fitspy.core.spectra_map' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['SpectraMap']
