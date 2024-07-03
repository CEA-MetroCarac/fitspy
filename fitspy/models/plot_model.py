from PySide6.QtCore import QObject, Signal
from matplotlib.figure import Figure
import numpy as np

from utils import Spectrum, Spectra, SpectraMap

class PlotModel(QObject):
    figureChanged = Signal(Figure, tuple, tuple)
    elementVisibilityToggled = Signal()
    extendFiles = Signal(list)

    def __init__(self, settings):
        super().__init__()
        self.fig = None
        self.spectra = Spectra()
        self.settings = settings
        self.selected_files = []

    def update_fig(self, selected_files, xlim=None, ylim=None):
        """ Update the figure with the selected files """
        self.selected_files = selected_files

        if self.fig is not None:
            self.fig.clear()
        else:
            self.fig = Figure()

        if not selected_files:
            self.figureChanged.emit(self.fig, None, None)
        else:
            ax = self.fig.add_subplot(111)
            show_attractors = self.settings["attractors_params"]["enabled"]
            for fname in selected_files:
                current_spectrum, _ = self.spectra.get_objects(fname)

                attractors_params_copy = self.settings["attractors_params"].copy()
                attractors_params_copy.pop("enabled", False)

                current_spectrum.attractors_params = attractors_params_copy
                current_spectrum.plot(ax, show_attractors=show_attractors)

            if xlim and ylim:
                ax.set_xlim(xlim)
                ax.set_ylim(ylim)

            self.figureChanged.emit(self.fig, xlim, ylim)

    def toggle_element_visibility(self, element_key):
        """Toggle the visibility of a plot element for given spectra.
        
        Args:
            element_key (str): Can be 'main_line', 'attractors', 'outliers', 'outliers_limit', 'negative_values', 'noise_level', 'baseline', 'background', 'peak_models' or 'result'.
        """
        if not self.fig.axes:
            return

        ax = self.fig.axes[0]
        canvas = self.fig.canvas
        updated_elements = set()

        # Save the initial canvas background
        background = canvas.copy_from_bbox(self.fig.bbox)

        for fname in self.selected_files:
            spectrum, _ = self.spectra.get_objects(fname)
            if spectrum and element_key in spectrum.plot_elements:
                elements = spectrum.plot_elements[element_key]
                if not isinstance(elements, (list, tuple)):
                    elements = [elements]

                for element in elements:
                    element.set_visible(not element.get_visible())
                    updated_elements.add(element)

        # Restore the background
        canvas.restore_region(background)

        # Redraw only the elements that were toggled
        for element in updated_elements:
            ax.draw_artist(element)

        # Blit the updated regions
        canvas.blit(self.fig.bbox)

        self.elementVisibilityToggled.emit()

    def spectrum_init(self, file):
        """ Create a Spectrum object from a file and add it to the spectra list """
        print("Spectrum creation")
        spectrum = Spectrum()
        spectrum.load_profile(file)
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

    def set_outliers_coeff(self, value):
        """ Set the outliers coefficient """
        self.settings["outliers_coef"] = value
        print("Outliers coefficient set to:", value)

    def outliers_calculation(self):
        """ Calculate the outliers (limit) """
        coef = float(self.outliers_coef.get())
        self.spectra.outliers_limit_calculation(coef=coef)
        # if self.is_show_all:
        #     self.show_all()
        # else:
        #     self.plot()