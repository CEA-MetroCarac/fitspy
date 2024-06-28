import os
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from utils import is_2d_map

class SettingsModel(QObject):
    files_changed = Signal(list)
    spectrum_requested = Signal(object)
    frame_map_requested = Signal(object)
    spectra_map_init = Signal(object)

    def __init__(self):
        super().__init__()
        self._files = []

    def extend_files(self, files):
        self._files.extend(files)
        self.files_changed.emit(self._files)

    def set_files(self, files):
        new_files = [file for file in files if file not in self._files]
        for file in new_files:
            if is_2d_map(file):
                self.spectra_map_init.emit(file)
            else:
                self._files.append(file)
                self.spectrum_requested.emit(file)
                self.files_changed.emit(self._files)

    def set_folder(self, folder):
        """loads all *.txt files from a folder path"""
        folder_path = Path(folder)
        files = [str(file) for file in folder_path.iterdir() if file.suffix == ".txt"]
        self.set_files(files)

    def remove_file(self, files):
        for file in files:
            self._files.remove(file)
        self.files_changed.emit(self._files)

    def clear_files(self):
        self._files = []
        self.files_changed.emit(self._files)  # Emit signal when files list is cleared

    def get_files(self):
        return self._files
