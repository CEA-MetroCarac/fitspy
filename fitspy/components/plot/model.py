from PySide6.QtCore import QObject, Signal

from utils import Spectra, Spectrum

class Model(QObject):
    filesChanged = Signal()

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()