from os.path import normpath
from PySide6.QtCore import QObject, Signal

from fitspy.core.utils import get_dim, load_from_json


class Model(QObject):
    spectrumListChanged = Signal(object)
    mapsListChanged = Signal()
    loadSpectra = Signal(object)
    loadSpectraMap = Signal(str)
    loadSpectrum = Signal(list)
    delSpectrum = Signal(dict)
    delSpectraMap = Signal(str)
    loadState = Signal(object)
    showToast = Signal(str, str, str)
    askConfirmation = Signal(str, object, tuple, dict)
    clear = Signal()

    def __init__(self):
        super().__init__()
        self._current_map = None
        self._spectramaps_fnames = {}
        self._spectrum_fnames = []

    @property
    def current_map(self):
        return self._current_map

    def set_current_map(self, map):
        self._current_map = map

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
        Remove spectra from the model and emit signal. Should not be manually called,
        this function is a called at the end of a signal chain to only reflect the deletion after
        the object is removed.
        If you want to remove a spectrum, use remove_files() instead.

        Parameters
        ----------
        items: dict
            A dictionary where keys can be None or a spectramap fname, and values are always a list
            of fname.
        """
        if not isinstance(items, dict):
            items = {None: items}

        # There will be only one key in the dictionary
        spectramap, fnames = next(iter(items.items()))

        if spectramap is not None:
            spectramap_fnames = [fname for fname in self._spectramaps_fnames[spectramap]
                                 if fname not in fnames]
            self._spectramaps_fnames[spectramap] = spectramap_fnames
        else:
            spectrum_fnames = [fname for fname in self._spectrum_fnames if fname not in fnames]
            self._spectrum_fnames = spectrum_fnames

        # Emit the signal once for the modified spectramap
        self.spectrumListChanged.emit(spectramap)

    def load_saved_work(self, files):
        """ Load saved work from a .json file """

        def handle_models(models):
            self.clear.emit()
            self.loadSpectra.emit(models)
            self.loadState.emit(models)
            self.showToast.emit("SUCCESS", "Work loaded.", "")

        if isinstance(files, str):
            files = [files]
        elif not isinstance(files, list):
            raise TypeError("files must be a list of file paths or a single file path as a string")

        files_json = [file for file in files if file.endswith(".json")]
        files_no_json = [file for file in files if not file.endswith(".json")]

        if len(files_json) > 1:
            self.showToast.emit("ERROR",
                                "Only one .json can be loaded at a time.",
                                "Please select only one .json file.")
            return []

        if len(files_json) == 1:
            models = load_from_json(files_json[0])
            # No confirmation needed if workspace is empty
            if not self.spectramaps_fnames and not self.spectrum_fnames:
                handle_models(models)
            else:
                self.askConfirmation.emit(
                    "Loading .json work will replace current work. Continue ?",
                    lambda: handle_models(models), (), {})

        return files_no_json

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

    def load_files(self, files: list):
        """Load files and categorize them as spectrum or spectramap files."""
        spectrum_files = []
        spectramap_files = []

        files = self.load_saved_work(files)
        if not files:  # if all files have been loaded, no need to continue
            return

        for file in files:
            if get_dim(file) == 2:  # 2D map
                spectramap_files.append(normpath(file))
            else:
                spectrum_files.append(normpath(file))

        if spectrum_files:
            self.load_spectrum_files(spectrum_files)
        if spectramap_files:
            self.load_spectramap_files(spectramap_files)

    def remove_files(self, files):
        """Remove files from the model and emit signals if files are removed.

        Parameters
        ----------
        files:  list or dict
        A list of files or a dictionary where keys can be None or a spectramap fname, and values
        are always a list of fname.
        When passed as a list, it should only be used by the app itself because when a user deletes
        spectrum from the list, we know these spectrum are from the current map due to how the app
        is built.
        Otherwise, a dictionary is necessary to identify each spectrum (whether it is from a map
        or not).
        """
        if not files:
            print("No files selected for deletion.")
            return

        if isinstance(files, list):
            if files[0] in self._spectramaps_fnames:  # Remove SpectraMap
                self.delSpectraMap.emit(files[0])
            else:
                self.delSpectrum.emit({self.current_map: files})
        elif isinstance(files, dict):
            self.delSpectrum.emit(files)

    def update_spectramap(self, map, fnames):
        """Update the spectramap with new filenames and emit signal."""
        self._spectramaps_fnames[map] = fnames
        self.mapsListChanged.emit()
