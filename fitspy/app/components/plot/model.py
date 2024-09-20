import numpy as np
from collections import defaultdict
from PySide6.QtCore import QObject, Signal

from fitspy.core import Spectra, Spectrum

class Model(QObject):
    decodedSpectraMap = Signal(str, list)
    mapSwitched = Signal(object)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    baselinePointsChanged = Signal(list)
    refreshPlot = Signal()
    askConfirmation = Signal(str, object, tuple, dict)
    showToast = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()
        self.current_map = None
        self.current_spectrum = []

    def set_spectrum_attr(self, fname, attr, value):
        spectrum = self.spectra.get_objects(fname, parent=self.current_map or self.spectra)[0]
        attrs = attr.split('.')
        for attr in attrs[:-1]:
            spectrum = getattr(spectrum, attr)
        setattr(spectrum, attrs[-1], value)

    @property
    def spectra(self):
        return self._spectra
    
    def load_spectrum(self, fnames):
        """ Load the given list of file names as spectra """
        for fname in fnames:
            spectrum = Spectrum()
            spectrum.load_profile(fname)
            self.spectra.append(spectrum)
            self.spectrumLoaded.emit(fname)

    def del_spectrum(self, map_fname, fnames):
        """Remove the spectrum(s) with the given file name(s)."""
        deleted_spectra = defaultdict(list)

        if map_fname:
            parent = next((sm for sm in self.spectra.spectra_maps if sm.fname == map_fname), None)
        else:
            parent = self.spectra
        
        for fname in fnames:
            spectrum = self.spectra.get_objects(fname, parent)[0]
            parent.remove(spectrum)

            parent_fname = getattr(parent, "fname", None)
            deleted_spectra[parent_fname].append(fname)

        self.spectrumDeleted.emit(deleted_spectra)

    def load_map(self, file):
        """ Create a Spectra object from a file and add it to the spectra list """
        from fitspy.core import SpectraMap

        spectra_map = SpectraMap.load_map(file)
        self.spectra.spectra_maps.append(spectra_map)

        fnames = [spectrum.fname for spectrum in spectra_map]
        self.decodedSpectraMap.emit(file, fnames)

    def del_map(self, fname):
        """ Remove the spectramap with the given file name """
        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.spectra.spectra_maps.remove(spectramap)
                self.spectraMapDeleted.emit(fname)
                break

    def switch_map(self, fname):
        if fname is None:
            self.current_map = None
            self.mapSwitched.emit(None)
            return

        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.current_map = spectramap
                self.mapSwitched.emit(spectramap)
                break

    def add_baseline_point(self, x, y):
        first_spectrum = self.current_spectrum[0]
        if first_spectrum.baseline.mode not in ['Linear', 'Polynomial']:
            self.showToast.emit("info", "No Baseline Mode", "Baseline mode must be 'Linear' or 'Polynomial' to add points.")
            return

        if first_spectrum.baseline.is_subtracted:
            self.askConfirmation.emit(
                "This action will reinitialize the spectrum. Continue?",
                self._add_baseline_point,
                (x, y),
                {}
            )
            return

        self._add_baseline_point(x, y)

    def _add_baseline_point(self, x, y):
        first_spectrum = self.current_spectrum[0]
        if first_spectrum.baseline.is_subtracted:
            for spectrum in self.current_spectrum:
                spectrum.load_profile(spectrum.fname)
                spectrum.apply_range()
                spectrum.baseline.is_subtracted = False
                spectrum.baseline.points = [[], []]
                spectrum.baseline.add_point(x, y)
        for spectrum in self.current_spectrum:
            spectrum.baseline.add_point(x, y)

        self.baselinePointsChanged.emit(first_spectrum.baseline.points)

    def del_baseline_point(self, x):
        first_spectrum = self.current_spectrum[0]
        if len(first_spectrum.baseline.points[0]) == 0:
            return
        dist_min = np.inf
        for i, x0 in enumerate(first_spectrum.baseline.points[0]):
            dist = abs(x0 - x)
            if dist < dist_min:
                dist_min, ind_min = dist, i
        first_spectrum.baseline.points[0].pop(ind_min)
        first_spectrum.baseline.points[1].pop(ind_min)
        self.baselinePointsChanged.emit(first_spectrum.baseline.points)

    def set_baseline_points(self, points):
        if self.current_spectrum:
            self.current_spectrum[0].baseline.points = points
            self.refreshPlot.emit()

    def add_peak_point(self, x, y):
        print(f"Adding peak point at x: {x}, y: {y}")
        self.refreshPlot.emit()

    def del_peak_point(self, x):
        if len(self.current_spectrum[0]) > 0:
            dist_min = np.inf
            for i, peak_model in enumerate(self.current_spectrum[0].peak_model):
                x0 = peak_model.param_hints["x0"]["value"]
                dist = abs(x0 - x)
                if dist < dist_min:
                    dist_min, ind_min = dist, i
            self.current_spectrum[0].del_peak_model(ind_min)
            self.current_spectrum[0].result_fit = lambda: None

        self.refreshPlot.emit()

        # self.paramsview.update()
        # self.plot()

    def preprocess(self):
        for spectrum in self.current_spectrum:
            spectrum.preprocess()

    def update_spectraplot(self, ax, view_options):
        """ Update the plot with the current spectra """
        ax.clear()
        # plotted_spectra = {line.get_label(): line for line in ax.lines if line.get_label() != "Baseline"}
        # current_spectrum_ids = [str(id(spectrum)) for spectrum in self.current_spectrum]
        first_spectrum = True
        for spectrum in self.current_spectrum:
            x0, y0 = spectrum.x0, spectrum.y0

            # Plot outliers in green
            if spectrum.outliers_limit is not None:
                inds = np.where(y0 > spectrum.outliers_limit)[0]
                if len(inds) > 0:
                    ax.plot(x0[inds], y0[inds], 'o', c='lime')

            if first_spectrum:
                spectrum.preprocess()
                spectrum.plot(ax,
                            show_outliers=view_options.get("Outliers", False),
                            show_outliers_limit=view_options.get("Outliers limits", False),
                            show_negative_values=view_options.get("Negative values", False),
                            show_noise_level=view_options.get("Noise level", False),
                            show_baseline=view_options.get("Baseline", False),
                            show_background=view_options.get("Background", False),
                            subtract_baseline=view_options.get("Subtract baseline", False),
                            # label=f"Spectrum_{spectrum_id}"")
                            )

                # Fix duplicate baseline
                for line in ax.lines:
                    if line.get_label() == "Baseline":
                        line.remove()

                # baseline plotting
                baseline = spectrum.baseline
                if not baseline.is_subtracted:
                    x, y = spectrum.x, None
                    if baseline.attached or baseline.mode == "Semi-Auto":
                        y = spectrum.y
                    baseline.plot(ax, x, y, attached=baseline.attached)

                first_spectrum = False
            else:
                ax.plot(x0, y0, 'k-', lw=0.2, zorder=0)

        if view_options.get("Legend", False):
            ax.legend()
        
            # self.current_map.set_marker(spectrum)
            # self.current_map.plot_map_update()
            # self.current_map.plot_map(self.current_map.ax)
        
        # refresh the plot
        ax.get_figure().canvas.draw_idle()
