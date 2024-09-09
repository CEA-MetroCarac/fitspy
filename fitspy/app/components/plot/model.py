from PySide6.QtCore import QObject, Signal

from fitspy.core import Spectra, Spectrum

class Model(QObject):
    decodedSpectraMap = Signal(str, list)
    mapSwitched = Signal(object)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(str, object)
    spectraMapDeleted = Signal(str)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()
        self.current_map = None

    @property
    def spectra(self):
        return self._spectra
    
    def load_spectrum(self, fnames):
        """ Load the given list of file names as spectra """
        for fname in fnames:
            spectrum = Spectrum()
            spectrum.load_profile(fname)
            self.spectra.append(spectrum)
            self.spectrumLoaded.emit(fname)

    def del_spectrum(self, fname):
        """ Remove the spectrum with the given file name """
        spectrum, parent = self.spectra.get_objects(fname)
        parent.remove(spectrum)
        
        if hasattr(parent, "fname"):
            self.spectrumDeleted.emit(fname, parent.fname)
        else:
            self.spectrumDeleted.emit(fname, None)

    def load_map(self, file):
        """ Create a Spectra object from a file and add it to the spectra list """
        from fitspy.core import SpectraMap

        spectra_map = SpectraMap.load_map(file)
        self.spectra.spectra_maps.append(spectra_map)

        fnames = [spectrum.fname for spectrum in spectra_map]
        self.decodedSpectraMap.emit(file, fnames)

    def del_map(self, fname):
        """ Remove the spectramap with the given file name """
        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.spectra.spectra_maps.remove(spectramap)
                self.spectraMapDeleted.emit(fname)
                break

    def switch_map(self, fname):
        if fname is None:
            self.current_map = None
            self.mapSwitched.emit(None)
            return

        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.current_map = spectramap
                self.mapSwitched.emit(spectramap)
                break
    
    def update_spectraplot(self, files):
        """ Update the plot with the given list of file names """
        print("update_spectraplot", files)