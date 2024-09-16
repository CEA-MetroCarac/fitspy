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

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()
        self.current_map = None
        self.current_spectrum = []

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

    def update_spectraplot(self, ax, view_options):
        """ Update the plot with the current spectra """
        ax.clear()

        # signal to retrieve view options
        parent = self.current_map or self.spectra

        first_spectrum = True

        for spectrum in self.current_spectrum:
            fname = spectrum.fname
            spectrum = self.spectra.get_objects(fname, parent)[0]
            x0, y0 = spectrum.x0, spectrum.y0

            # Plot outliers in green
            if spectrum.outliers_limit is not None:
                inds = np.where(y0 > spectrum.outliers_limit)[0]
                if len(inds) > 0:
                    ax.plot(x0[inds], y0[inds], 'o', c='lime')

            if first_spectrum:
                spectrum.plot(ax,
                            show_outliers=view_options.get("Outliers", False),
                            show_outliers_limit=view_options.get("Outliers limits", False),
                            show_negative_values=view_options.get("Negative values", False),
                            show_noise_level=view_options.get("Noise level", False),
                            show_baseline=view_options.get("Baseline", False),
                            show_background=view_options.get("Background", False),
                            )
                first_spectrum = False
            else:
                ax.plot(x0, y0, 'k-', lw=0.2, zorder=0)
        
            # self.current_map.set_marker(spectrum)
            # self.current_map.plot_map_update()
            # self.current_map.plot_map(self.current_map.ax)

        # refresh the plot
        ax.get_figure().canvas.draw()
