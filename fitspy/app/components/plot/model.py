from PySide6.QtCore import QObject, Signal

from fitspy.core import Spectra

class Model(QObject):
    decodedSpectraMap = Signal(str, list)
    mapSwitched = Signal(object)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()

    @property
    def spectra(self):
        return self._spectra

    def create_map(self, file):
        """ Create a Spectra object from a file and add it to the spectra list """
        from fitspy.core import SpectraMap

        spectra_map = SpectraMap.load_map(file)
        self.spectra.spectra_maps.append(spectra_map)

        fnames = [spectrum.fname for spectrum in spectra_map]
        self.decodedSpectraMap.emit(file, fnames)

    def switch_map(self, fname):
        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.mapSwitched.emit(spectramap)
                break