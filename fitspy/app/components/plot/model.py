from copy import deepcopy
import numpy as np
from collections import defaultdict
from PySide6.QtCore import QObject, Signal

from fitspy.core import Spectra, Spectrum

# class SpectraWorker(QObject):
#     from superqt.utils import thread_worker
#     progress_updated = Signal(int)
#     finished = Signal()
#     errored = Signal(Exception)

#     def __init__(self, spectra):
#         super().__init__()
#         self.spectra = spectra

#     @thread_worker
#     def apply_model(self, model_dict, fnames=None, ncpus=1):
#         try:
#             self.spectra.apply_model(model_dict, fnames, ncpus)
#             print(self.spectra.pbar_index)
#             yield 100  # Emit 100% progress when done
#         except Exception as e:
#             self.errored.emit(e)
#         finally:
#             self.finished.emit()


class Model(QObject):
    decodedSpectraMap = Signal(str, list)
    mapSwitched = Signal(object)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    baselinePointsChanged = Signal(list)
    refreshPlot = Signal()
    askConfirmation = Signal(str, object, tuple, dict)
    PeaksChanged = Signal(object)
    showToast = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()
        self.current_map = None
        self.current_spectrum = []
        self.peak_model = None
        self.tmp = None
        self.linewidth = 0.5
        self.lines = None
        # self.worker = SpectraWorker(self._spectra)
        # self.worker.progress_updated.connect(self.update_progress_bar)
        # self.worker.finished.connect(self.on_worker_finished)
        # self.worker.errored.connect(self.on_worker_errored)

    def update_progress_bar(self, value):
        # self.progressbar.setValue(value)
        print(value)

    def on_worker_finished(self):
        self.refreshPlot.emit()
        # Additional cleanup or UI updates

    def on_worker_errored(self, exc):
        print(f"Error: {exc}")
        # Handle the error

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
            self.showToast.emit("info", "Baseline Mode", "Baseline mode must be 'Linear' or 'Polynomial' to add points.")
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

    def add_peak_point(self, ax, model, x, y):
        first_spectrum = self.current_spectrum[0]

        # to take into account the strong aspect ratio in the axis represent.
        ratio = 1. / ax.get_data_ratio() ** 2

        inds = range(len(first_spectrum.x))
        x_sp, y_sp = first_spectrum.x, first_spectrum.y
        dist_min = np.inf
        for ind in inds:
            dist = (x_sp[ind] - x) ** 2 + ratio * (y_sp[ind] - y) ** 2
            if dist < dist_min:
                dist_min, ind_min = dist, ind

        first_spectrum.add_peak_model(model, x0=x_sp[ind_min])
        self.PeaksChanged.emit(first_spectrum)
        self.refreshPlot.emit()

    def del_peak_point(self, x):
        first_spectrum = self.current_spectrum[0]
        if len(first_spectrum.peak_models) > 0:
            dist_min = np.inf
            for i, peak_model in enumerate(first_spectrum.peak_models):
                x0 = peak_model.param_hints["x0"]["value"]
                dist = abs(x0 - x)
                if dist < dist_min:
                    dist_min, ind_min = dist, i
            first_spectrum.del_peak_model(ind_min)
            first_spectrum.result_fit = lambda: None
        self.PeaksChanged.emit(first_spectrum)
        self.refreshPlot.emit()

    def on_motion(self, ax, event):
        def annotate_params(i, color='k'):
            """ Annotate figure with fit parameters """
            spectrum = self.current_spectrum[0]
            x = spectrum.x
            if not self.line_bkg_visible:
                model = spectrum.peak_models[i]
                x0 = model.param_hints['x0']['value']
            elif i == 0:
                model = spectrum.bkg_model
                x0 = 0.5 * (x[0] + x[-1])
            else:
                model = spectrum.peak_models[i - 1]
                x0 = model.param_hints['x0']['value']

            y0 = model.eval(model.make_params(), x=x0)
            xy = (x0, min(y0, ax.get_ylim()[1]))

            text = []
            for name, val in model.param_hints.items():
                text.append(f"{name}: {val['value']:.4g}")
            text = '\n'.join(text)

            bbox = dict(facecolor='w', edgecolor=color, boxstyle='round')
            self.tmp = ax.annotate(text, xy=xy, xycoords='data',
                                    bbox=bbox, verticalalignment='top')
                
        if self.lines is not None and event.inaxes == ax:
            for i, line in enumerate(self.lines):
                if line.contains(event)[0]:
                    line.set_linewidth(3)
                    if self.tmp is not None:
                        self.tmp.remove()
                    annotate_params(i, color=line.get_c())
                else:
                    line.set_linewidth(self.linewidth)

            ax.figure.canvas.draw_idle()

    def preprocess(self):
        for spectrum in self.current_spectrum:
            spectrum.preprocess()

    def update_spectraplot(self, ax, view_options):
        """ Update the plot with the current spectra """
        ax.clear()
        if not self.current_spectrum:
            ax.get_figure().canvas.draw_idle()
            return
        
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
                result_fit = spectrum.result_fit
                baseline = spectrum.baseline

                self.lines = spectrum.plot(ax,
                            show_outliers=view_options.get("Outliers", False),
                            show_outliers_limit=view_options.get("Outliers limits", False),
                            show_negative_values=view_options.get("Negative values", False),
                            show_noise_level=view_options.get("Noise level", False),
                            show_baseline=view_options.get("Baseline", False),
                            show_background=view_options.get("Background", False),
                            subtract_baseline=view_options.get("Subtract baseline", False),
                            # label=f"Spectrum_{spectrum_id}"")
                            )
                self.line_bkg_visible = view_options.get("Background", False) and spectrum.bkg_model

                # baseline plotting
                if not baseline.is_subtracted:
                    x, y = spectrum.x, None
                    if baseline.attached or baseline.mode == "Semi-Auto":
                        y = spectrum.y
                    baseline.plot(ax, x, y, attached=baseline.attached)

                # Peak labels
                if view_options.get("Peak labels", True):
                    from fitspy.core import closest_index
                    dy = 0.02 * spectrum.y.max()
                    for i, label in enumerate(spectrum.peak_labels):
                        if label == '':
                            continue
                        model = spectrum.peak_models[i]
                        x0 = model.param_hints['x0']['value']
                        y = spectrum.y[closest_index(spectrum.x, x0)]
                        xy = (x0, y + dy)
                        xytext = (x0, y + 4 * dy)
                        ax.annotate(label, xy=xy, xytext=xytext, xycoords='data',
                                        ha='center', size=14, arrowprops=dict(fc='k'))

                first_spectrum = False
            else:
                ax.plot(x0, y0, 'k-', lw=0.2, zorder=0)

        if view_options.get("Legend", False):
            ax.legend()

        self.tmp = None
        self.linewidth = 0.5
        if hasattr(result_fit, "success") and result_fit.success:
            self.linewidth = 1
        
            # self.current_map.set_marker(spectrum)
            # self.current_map.plot_map_update()
            # self.current_map.plot_map(self.current_map.ax)
        
        # refresh the plot
        ax.get_figure().canvas.draw_idle()

    def apply_model(self, model_dict=None, fnames=None, fit_params=None, ncpus=None):
        """ Apply model to the selected spectra """
        model_dict = model_dict #or deepcopy(self.model_dict)

        if model_dict is None:
            # showerror(message='No model has been loaded')
            print("No model has been loaded")
            # show toast
            return

        if fnames is None:
            fnames = self.fileselector.filenames
            fnames = [fnames[i] for i in self.fileselector.lbox.curselection()]

        nfiles = len(fnames)
        # ncpus = self.get_ncpus(nfiles=nfiles)

        if fit_params is not None:
            for fname in fnames:
                spectrum, _ = self.spectra.get_objects(fname)
                spectrum.fit_params = deepcopy(fit_params)

        # self.worker.apply_model(model_dict, fnames, ncpus).start()
        from threading import Thread
        self.spectra.pbar_index = 0
        show_progressbar = False
        args = (model_dict, fnames, ncpus, show_progressbar)
        thread = Thread(target=self.spectra.apply_model, args=args)
        thread.start()
        print(self.spectra.pbar_index)
        # self.progressbar.update(self.spectra, nfiles, ncpus)
        thread.join()
        # self.colorize_from_fit_status(fnames)
        # self.reassign_current_spectrum(self.current_spectrum.fname)
        # self.update()
        self.refreshPlot.emit()