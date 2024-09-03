from PySide6.QtCore import QObject, Signal

from fitspy.utils import get_dim
class Model(QObject):
    filesChanged = Signal()

    def __init__(self):
        super().__init__()
        self._files = []

    @property
    def files(self):
        return self._files

    # @files.setter
    def set_files(self, files):
        new_files = [file for file in files if file not in self._files]
        for file in new_files:
            if get_dim(file) == 2:  # 2D map
                pass
                # self.spectra_map_init.emit(file)
            else:
                self._files.append(file)
                # self.spectrum_requested.emit(file)
        
        if new_files:
            self.filesChanged.emit()

    def remove_files(self, files):
        for file in files:
            self._files.remove(file)
        self.filesChanged.emit()