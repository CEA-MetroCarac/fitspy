DELIMITER = "@"  # Used by Spectra/SpectraMap (in set_attributes) and main_controller.py (in save and load .fspy) to identify correct spectrum object as "map@fname"

from .utils import *
from .baseline import BaseLine
from .spectrum import Spectrum
from .spectra import Spectra
from .spectra_map import SpectraMap