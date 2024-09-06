from PySide6.QtCore import QObject, Signal
from fitspy.core import get_dim

class Model(QObject):
    spectrumListChanged = Signal()
    mapsListChanged = Signal()
    spectraMapInit = Signal(str)

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

    def load_spectrum_files(self, files):
        """Load spectrum files and emit signal if new files are added."""
        new_files = [file for file in files if file not in self._spectrum_fnames]
        self._spectrum_fnames.extend(new_files)
        if new_files:
            self.spectrumListChanged.emit()

    def load_spectramap_files(self, files):
        """Load spectramap files and emit signal for each new file."""
        new_files = [file for file in files if file not in self._spectramaps_fnames]
        for file in new_files:
            self.spectraMapInit.emit(file)

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
        spectrum_files_removed = False
        spectramap_files_removed = False

        for file in files:
            if file in self._spectrum_fnames:  # Remove spectrum
                self._spectrum_fnames.remove(file)
                spectrum_files_removed = True
            if file in self._spectramaps_fnames:  # Remove SpectraMap
                del self._spectramaps_fnames[file]
                spectramap_files_removed = True

            for _, spectrum_list in self._spectramaps_fnames.items():  # Remove spectrum from SpectraMap
                if file in spectrum_list:
                    spectrum_list.remove(file)
                    spectramap_files_removed = True

        if spectrum_files_removed:
            self.spectrumListChanged.emit()
        if spectramap_files_removed:
            self.mapsListChanged.emit()

    def update_spectramap(self, file, fnames):
        """Update the spectramap with new filenames and emit signal."""
        self._spectramaps_fnames[file] = fnames
        self.mapsListChanged.emit()