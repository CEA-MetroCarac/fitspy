import warnings
from fitspy.core.models import gaussian, lorentzian, gaussian_asym, lorentzian_asym, pseudovoigt

warnings.warn(
    "The module 'fitspy.models' is deprecated and will be removed in a future release. "
    "Please use 'fitspy.core.models' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['gaussian', 'lorentzian', 'gaussian_asym', 'lorentzian_asym', 'pseudovoigt']
