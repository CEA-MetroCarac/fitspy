from PySide6.QtCore import QObject, Signal
from matplotlib.figure import Figure

from utils import Spectra, Spectrum

class PlotModel(QObject):
    axChanged = Signal(object, tuple, tuple)
    elementVisibilityToggled = Signal()
    extendFiles = Signal(list)

    def __init__(self, settings):
        super().__init__()
        self.fig = Figure()
        self.spectra = Spectra()
        self.settings = settings
        self.selected_files = []

    def update_fig(self, selected_files, xlim=None, ylim=None):
        """Update the axes with the selected files."""
        if not selected_files:
            self.axChanged.emit(None, None, None)
        else:
            ax = self.fig.add_subplot(111)
            show_attractors = self.settings["attractors"]["enabled"]
            for fname in selected_files:
                current_spectrum, _ = self.spectra.get_objects(fname)
                attractors_params_copy = self.settings["attractors"].copy()
                attractors_params_copy.pop("enabled", False)
                current_spectrum.attractors_params = attractors_params_copy
                current_spectrum.plot(ax, show_attractors=show_attractors)

            self.axChanged.emit(ax, xlim, ylim)

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
        from utils.spectra_map import SpectraMap

        spectra_map = SpectraMap()
        spectra_map.create_map(file)
        self.spectra.spectra_maps.append(spectra_map)
        # self.frame_map_requested.emit(spectra_map)

        # add each spectra related to the 2D-map
        fnames = [spectrum.fname for spectrum in spectra_map]

        # update the file list widget
        self.extendFiles.emit(fnames)

    def outliers_calc(self):
        """ Calculate the outliers (limit) """
        coef = float(self.settings["outliers"]["coef"])
        self.spectra.outliers_limit_calculation(coef=coef)