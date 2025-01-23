import warnings
from fitspy.core.baseline import BaseLine

warnings.warn(
    "The module 'fitspy.baseline' is deprecated and will be removed in a future release. "
    "Please use 'fitspy.core.baseline' instead.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = ['BaseLine']
