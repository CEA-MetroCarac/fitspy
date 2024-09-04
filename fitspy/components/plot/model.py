from PySide6.QtCore import QObject, Signal

from fitspy.utils import Spectra, Spectrum

class Model(QObject):
    decodedSpectraMap = Signal(str, list)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()

    @property
    def spectra(self):
        return self._spectra

    def spectramap_init(self, file):
        """ Create a Spectra object from a file and add it to the spectra list """
        from fitspy.utils import SpectraMap

        spectra_map = SpectraMap()
        spectra_map.create_map(file)
        self.spectra.spectra_maps.append(spectra_map)
        # self.frame_map_requested.emit(spectra_map)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]

        # update the file list widget
        self.decodedSpectraMap.emit(file, fnames)