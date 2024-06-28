import os
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from utils import SpectraMap

class SettingsModel(QObject):
    files_changed = Signal(list)
    frame_map_requested = Signal(object)

    def __init__(self):
        super().__init__()
        self._files = []


    def create_map(self, file):
        """ Create the 2D-map that consists in replacing the current spectra by
            the ones issued from the 2D-map extrusion """

        spectra_map = SpectraMap()
        spectra_map.create_map(file)
        self.frame_map_requested.emit(spectra_map)

        # remove 2D-map filename in the fileselector
        self._files.remove(file)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]
        
        # update the file list widget
        self._files.extend(fnames)
        self.files_changed.emit(self._files)

    def set_files(self, files):
        file_added = False
        for file in files:
            # Check if file is not already in the list and if it is a valid file
            if file not in self._files:
                # 2D-map detection:
                with open(file, 'r') as fid:
                    if fid.readline().startswith("\t"):
                        self._files.append(file)
                        self.create_map(file)
                        file_added = True
                    # TODO When fname_first_item is None ??
                    else:
                        pass
                        # TODO sepctrum creation, load_profile... 
        if file_added:
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
