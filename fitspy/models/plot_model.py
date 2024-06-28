from PySide6.QtCore import QObject, Signal
from matplotlib.figure import Figure
import numpy as np

from utils import Spectrum, Spectra, SpectraMap

class PlotModel(QObject):
    figureChanged = Signal(Figure)
    extendFiles = Signal(list)

    def __init__(self):
        super().__init__()
        self.fig = None
        self.spectra = Spectra()
        self.spectra_maps = []

    def update_fig(self, selected_files):
        print("Selected files:", selected_files)
        self.fig = Figure()

        if not selected_files:
            self.figureChanged.emit(self.fig)
        else:
            ax = self.fig.add_subplot(111)
            for fname in selected_files:
                current_spectrum, _ = self.spectra.get_objects(fname)
                lines = current_spectrum.plot(ax)


            self.figureChanged.emit(self.fig)

    def spectrum_init(self, file):
        """ Create a Spectrum object from a file and add it to the spectra list """
        print("Spectrum creation")
        spectrum = Spectrum()
        spectrum.load_profile(file)
        # spectrum.attractors_params = attractors_params
        self.spectra.append(spectrum)

    def spectra_map_init(self, file):
        """ Create a Spectra object from a file and add it to the spectra list """
        print("Spectra map creation")

        spectra_map = SpectraMap()
        spectra_map.create_map(file)
        self.spectra.spectra_maps.append(spectra_map)
        # self.frame_map_requested.emit(spectra_map)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]

        # update the file list widget
        self.extendFiles.emit(fnames)