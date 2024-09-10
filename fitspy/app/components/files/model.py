from PySide6.QtCore import QObject, Signal
from fitspy.core import get_dim

class Model(QObject):
    spectrumListChanged = Signal(object)
    mapsListChanged = Signal()
    loadSpectraMap = Signal(str)
    loadSpectrum = Signal(list)
    delSpectrum = Signal(list)
    delSpectraMap = Signal(str)

    def __init__(self):
        super().__init__()
        self._spectramaps_fnames = {}
        self._spectrum_fnames = []

    @property
    def spectramaps_fnames(self):
        return self._spectramaps_fnames

    @property
    def spectrum_fnames(self):
        return self._spectrum_fnames
    
    def add_spectrum(self, fname):
        """Add a spectrum to the model and emit signal."""
        self._spectrum_fnames.append(fname)
        self.spectrumListChanged.emit(None)

    def del_spectrum(self, items):
        """
        Remove spectra from the model and emit signal.

        Parameters:
        items (dict): A dictionary where keys can be None or a spectramap fname, 
                    and values are always a list of fname.
        """
        if not isinstance(items, dict):
            items = {None: items}

        # There will be only one key in the dictionary
        spectramap, fnames = next(iter(items.items()))

        if spectramap is not None:
            for fname in fnames:
                self._spectramaps_fnames[spectramap].remove(fname)
        else:
            for fname in fnames:
                self._spectrum_fnames.remove(fname)

        # Emit the signal once for the modified spectramap
        self.spectrumListChanged.emit(spectramap)

    def load_spectrum_files(self, files):
        """Load spectrum files and emit signal if new files are added."""
        new_files = [file for file in files if file not in self._spectrum_fnames]
        if new_files:
            self.loadSpectrum.emit(files)

    def load_spectramap_files(self, files):
        """Load spectramap files and emit signal for each new file."""
        new_files = [file for file in files if file not in self._spectramaps_fnames]
        for file in new_files:
            self.loadSpectraMap.emit(file)

    def del_map(self, file):
        """Remove a spectramap from the model and emit signal."""
        del self._spectramaps_fnames[file]
        self.mapsListChanged.emit()

    def load_files(self, files):
        """Load files and categorize them as spectrum or spectramap files."""
        spectrum_files = []
        spectramap_files = []

        for file in files:
            if get_dim(file) == 2:  # 2D map
                spectramap_files.append(file)
            else:
                spectrum_files.append(file)

        if spectrum_files:
            self.load_spectrum_files(spectrum_files)
        if spectramap_files:
            self.load_spectramap_files(spectramap_files)

    def remove_files(self, files):
        """Remove files from the model and emit signals if files are removed."""
        if not files:
            print("No files selected for deletion.")
            return

        if files[0] in self._spectramaps_fnames:  # Remove SpectraMap
            self.delSpectraMap.emit(files[0])
        else:
            self.delSpectrum.emit(files)

    def update_spectramap(self, file, fnames):
        """Update the spectramap with new filenames and emit signal."""
        self._spectramaps_fnames[file] = fnames
        self.mapsListChanged.emit()