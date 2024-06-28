import os
from pathlib import Path
from PySide6.QtCore import QObject, Signal

from utils import SpectraMap

class SettingsModel(QObject):
    filesChanged = Signal(list)  # Signal to emit when the files list changes

    def __init__(self):
        super().__init__()
        self._files = []

    def frame_map_creation(self, spectra_map):
        xy_map = spectra_map.xy_map

        if spectra_map.marker is not None:
            [x.remove() for x in spectra_map.marker]
        
        # TODO


    def create_map(self, file):
        """ Create the 2D-map that consists in replacing the current spectra by
            the ones issued from the 2D-map extrusion """

        spectra_map = SpectraMap()
        spectra_map.create_map(file)
        # TODO spectra_maps should be in plot_model
        # self.spectra_maps.append(spectra_map)
        # self.frame_map_creation(spectra_map)
        # spectra_map.plot_map(spectra_map.ax)

        # remove 2D-map filename in the fileselector
        self._files.remove(file)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]
        
        # update the file list widget
        self._files.extend(fnames)
        self.filesChanged.emit(self._files)

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
            self.filesChanged.emit(self._files)

    def set_folder(self, folder):
        """loads all *.txt files from a folder path"""
        folder_path = Path(folder)
        files = [str(file) for file in folder_path.iterdir() if file.suffix == ".txt"]
        self.set_files(files)

    def remove_file(self, files):
        for file in files:
            self._files.remove(file)
        self.filesChanged.emit(self._files)

    def clear_files(self):
        self._files = []
        self.filesChanged.emit(self._files)  # Emit signal when files list is cleared

    def get_files(self):
        return self._files
