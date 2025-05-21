import os
from threading import Thread
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox

# import fitspy
from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum
from fitspy.core.spectra_map import SpectraMap
from fitspy.core.utils import closest_index, closest_item, measure_time
from fitspy.apps.pyside import DEFAULTS

CMAP = matplotlib.colormaps['tab10']
LABEL_OFFSET_RATIO = 0.005  # Ratio to offset label above the peak
YLIM_BUFFER_RATIO = 0.05  # Ratio to extend y-axis limit


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
    progressUpdated = Signal(object, int, int)
    colorizeFromFitStatus = Signal(dict)
    showToast = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self._spectra = Spectra()
        self.current_map = None
        self.current_spectra = []
        self.current_mode = None  # plot click mode
        self.peak_model = None
        self.tmp = None
        self.linewidth = 0.5
        self.lines = []
        self.nearest_lines = []

    def set_spectrum_attr(self, fname, attr, value):
        # .json model's "dummy spectrum" is not stored in self.spectra
        if fname == self.current_spectra[0].fname:
            spectrum = self.current_spectra[0]
        else:
            spectrum = self.spectra.get_objects(fname)[0]

        attrs = attr.split(".")
        for attr in attrs[:-1]:
            spectrum = getattr(spectrum, attr)
        setattr(spectrum, attrs[-1], value)

    @property
    def spectra(self):
        return self._spectra

    def load_spectra(self, models):
        """ Load spectra from 'models' related to a .json file """
        self._spectra = Spectra.load(dict_spectra=models, preprocess=True)

        for spectrum in self.spectra:
            self.spectrumLoaded.emit(spectrum.fname)

        for spectra_map in self.spectra.spectra_maps:
            fname = spectra_map.fname
            fnames = [spectrum.fname for spectrum in spectra_map]
            self.decodedSpectraMap.emit(fname, fnames)

    def load_spectrum(self, fnames):
        """Load the given list of file names as spectra"""
        for fname in fnames:
            fname = os.path.normpath(fname)
            try:
                spectrum = Spectrum()
                spectrum.load_profile(fname)
                self.spectra.append(spectrum)
                self.spectrumLoaded.emit(fname)
            except:
                self.showToast.emit("ERROR", "Failed to load spectrum", fname)

    def del_spectrum(self, items):
        """
        Remove the spectrum(s) with the given file name(s).

        Parameters
        ----------
        items: dict
            Dictionary where keys can be None or a spectramap fname,
            and values are always a list of fname.
        """
        deleted_spectra = defaultdict(list)

        for _, fnames in items.items():
            for fname in fnames:
                spectrum, parent = self.spectra.get_objects(fname)
                parent.remove(spectrum)

                parent_fname = getattr(parent, "fname", None)
                deleted_spectra[parent_fname].append(fname)

        self.spectrumDeleted.emit(deleted_spectra)

    def load_map(self, fname):
        """Create a Spectra object from a fname and add it to the spectra list"""
        # from fitspy.core import SpectraMap
        fname = os.path.normpath(fname)

        try:
            spectra_map = SpectraMap.load_map(fname)
            self.spectra.spectra_maps.append(spectra_map)

            fnames = [spectrum.fname for spectrum in spectra_map]
            self.decodedSpectraMap.emit(fname, fnames)
        except:
            QMessageBox.warning(None, "Warning", f"FAILED to load: {Path(fname).name}")

    def del_map(self, fname):
        """Remove the spectramap with the given file name"""
        for spectramap in self.spectra.spectra_maps:
            if spectramap.fname == fname:
                self.spectra.spectra_maps.remove(spectramap)
                self.spectraMapDeleted.emit(fname)
                break

    def reinit_spectra(self, fnames):
        fit_status_dict = {}
        for fname in fnames:
            spectrum = self.spectra.get_objects(fname)[0]
            spectrum.reinit()
            fit_status_dict[fname] = None
        self.colorizeFromFitStatus.emit(fit_status_dict)

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
        first_spectrum = self.current_spectra[0]
        if first_spectrum.baseline.mode not in ["Linear", "Polynomial"]:
            self.showToast.emit(
                "info",
                "Baseline Mode",
                "Baseline mode must be 'Linear' or 'Polynomial' to add points.",
            )
            return

        if first_spectrum.baseline.is_subtracted:
            self.askConfirmation.emit(
                "This action will reinitialize the spectrum. Continue?",
                self._add_baseline_point, (x, y), {})
            return

        self._add_baseline_point(x, y)

    def _add_baseline_point(self, x, y):
        first_spectrum = self.current_spectra[0]
        if first_spectrum.baseline.is_subtracted:
            for spectrum in self.current_spectra:
                spectrum.load_profile(spectrum.fname)
                spectrum.apply_range()
                spectrum.baseline.is_subtracted = False
                spectrum.baseline.points = [[], []]
                spectrum.baseline.add_point(x, y)
        for spectrum in self.current_spectra:
            spectrum.baseline.add_point(x, y)

        self.baselinePointsChanged.emit(first_spectrum.baseline.points)

    def del_baseline_point(self, x):
        first_spectrum = self.current_spectra[0]
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
        if self.current_spectra:
            self.current_spectra[0].baseline.points = points
            self.refreshPlot.emit()

    def add_peak_point(self, model, x):
        spectrum = self.current_spectra[0]
        x0 = closest_item(spectrum.x, x)
        spectrum.add_peak_model(model, x0=x0)
        self.PeaksChanged.emit(spectrum)
        self.refreshPlot.emit()

    def refresh(self):
        self.PeaksChanged.emit(self.current_spectra[0])
        # self.refreshPlot.emit()

    def del_peak_point(self, x):
        first_spectrum = self.current_spectra[0]
        if len(first_spectrum.peak_models) > 0:
            dist_min = np.inf
            for i, peak_model in enumerate(first_spectrum.peak_models):
                x0 = peak_model.param_hints["x0"]["value"]
                dist = abs(x0 - x)
                if dist < dist_min:
                    dist_min, ind_min = dist, i
            first_spectrum.del_peak_model(ind_min)
        self.PeaksChanged.emit(first_spectrum)
        self.refreshPlot.emit()

    def highlight_spectrum(self, ax, event):
        """Highlight all spectrum under the cursor"""

        if self.lines and event.inaxes == ax:
            # reassign standard properties to the previous nearest lines
            for line in self.nearest_lines:
                line.set(linewidth=0.2, color='k', zorder=0)

            title = None
            self.nearest_lines, fnames, labels = [], [], []
            num_secondary = len(self.current_spectra) - 1
            # spectrum_lines = [self.lines[0]] + self.lines[-num_secondary:]
            spectrum_lines = [self.lines[0]]
            if num_secondary > 0:
                spectrum_lines += self.lines[-num_secondary:]

            for i, line in enumerate(spectrum_lines):
                if line.contains(event)[0]:
                    if len(self.nearest_lines) < 10:
                        color = CMAP(len(self.nearest_lines))
                        line.set(linewidth=1, color=color, zorder=1)
                        self.nearest_lines.append(line)
                        fname = self.current_spectra[i].fname
                        fnames.append(fname)
                        labels.append(Path(fname).name)
                    else:
                        title = "The nearest lines exceed 10.\n"
                        title += "  Show the first 10 ones"

            ax.legend(self.nearest_lines, labels, title=title, loc=1)
            ax.get_figure().canvas.draw_idle()
            return fnames

    def highlight_peak(self, ax, peak_index, xdata=None, ydata=None):
        """Highlight a peak by its index (for table hover/click)."""
        # Remove previous highlights
        if self.tmp is not None:
            [x.remove() for x in self.tmp]
            self.tmp = None
        nspectra = len(self.current_spectra)
        lines = self.lines[1:-(nspectra - 1)] if nspectra > 1 else self.lines[1:]
        if not (0 <= peak_index < len(lines)):
            ax.figure.canvas.draw_idle()
            return
        line = lines[peak_index]
        if line.axes is None or line.figure is None:
            return

        # Highlight the line
        x = line.get_xdata()
        y = line.get_ydata()
        color = line.get_color()
        linestyle = line.get_linestyle()
        self.tmp = [ax.plot(x, y, c=color, ls=linestyle, lw=3)[0]]

        def annotate_params(x_annot, y_annot, i, color):
            spectrum = self.current_spectra[0]
            if self.line_bkg_visible:
                model = spectrum.bkg_model if i == 0 else spectrum.peak_models[i - 1]
            else:
                model = spectrum.peak_models[i]
            text = []
            for key in ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r']:
                if key in model.param_hints:
                    text.append(f"{key}: {model.param_hints[key]['value']:.4g}")
            text = "\n".join(text)
            bbox = {"facecolor": 'w', "edgecolor": color, "boxstyle": 'round'}
            self.tmp.append(ax.annotate(text, xy=(x_annot, y_annot), xycoords="data",
                                        bbox=bbox, verticalalignment="bottom"))

        # Default annotation position to center
        if xdata is None or ydata is None:
            xdata = x[len(x) // 2] if len(x) else 0
            ydata = y[len(y) // 2] if len(y) else 0
        annotate_params(xdata, ydata, peak_index, color)
        ax.figure.canvas.draw_idle()

    def on_motion(self, ax, event):
        if self.tmp is not None:
            [x.remove() for x in self.tmp]
            self.tmp = None

        nspectra = len(self.current_spectra)
        lines = self.lines[1:-(nspectra - 1)] if nspectra > 1 else self.lines[1:]

        if len(lines) > 0 and event.inaxes == ax:
            for i, line in enumerate(lines):
                if line.axes is None or line.figure is None:
                    continue
                if line.contains(event)[0]:
                    self.highlight_peak(ax, i, event.xdata, event.ydata)
                    break
            ax.figure.canvas.draw_idle()

    def preprocess(self):
        for spectrum in self.current_spectra:
            spectrum.preprocess()

    def get_view_limits(self, ax):
        """Get the current view limits of the plot."""
        if not ax.has_data():
            return None, None
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        return xlim, ylim

    def set_view_limits(self, ax, xlim, ylim):
        if xlim and ylim:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

    def store_original_view_limits(self, ax):
        self.original_xlim, self.original_ylim = self.get_view_limits(ax)

    # @measure_time
    def update_spectraplot(self, ax, view_options, toolbar):
        """Update the plot with the current spectra"""
        xlim, ylim = self.get_view_limits(ax)
        if not hasattr(self, "original_xlim") or not hasattr(self, "original_ylim"):
            self.store_original_view_limits(ax)

        current_title = ax.get_title()
        ax.clear()
        ax.set_title(current_title)
        self.tmp = None

        if not self.current_spectra:
            ax.get_figure().canvas.draw_idle()
            return

        # 'interactive' baseline points management
        spectrum = self.current_spectra[0]
        baseline = spectrum.baseline
        if not baseline.is_subtracted:
            x, y = spectrum.x, None
            if baseline.attached or baseline.mode == "Semi-Auto":
                y = spectrum.y
            baseline.plot(ax, x, y, attached=baseline.attached)

        self.lines = []
        first_spectrum = True
        interactive_bounds = view_options["Interactive bounds"] * (self.ibounds is not None)
        cmap_peaks = DEFAULTS['peaks_cmap']
        for spectrum in self.current_spectra:
            self.lines += spectrum.plot(
                ax,
                show_weights=view_options["Weights"] * first_spectrum,
                show_outliers=view_options["Outliers"],
                show_outliers_limit=view_options["Outliers limits"] * first_spectrum,
                show_negative_values=view_options["Negative values"] * first_spectrum,
                show_peak_models=view_options["Peaks"] * (not interactive_bounds) * first_spectrum,
                show_peak_decomposition=view_options["Peak decomposition"] * first_spectrum,
                show_noise_level=view_options["Noise level"] * first_spectrum,
                show_baseline=view_options["Baseline"] * first_spectrum,
                show_background=view_options["Background"] * first_spectrum,
                show_result=view_options["Fit"] * first_spectrum,
                subtract_baseline=view_options["Subtract bkg+baseline"],
                subtract_bkg=view_options["Subtract bkg+baseline"],
                kwargs=None if first_spectrum else {'c': 'k', 'lw': 0.1, 'zorder': 0},
                cmap_peaks=cmap_peaks)
            if first_spectrum:
                if view_options.get("Residual", False):
                    spectrum.plot_residual(ax)
                if view_options.get("Legend", False):
                    ax.legend(loc=1)
            first_spectrum = False

        spectrum = self.current_spectra[0]
        self.line_bkg_visible = view_options.get("Background", False) and spectrum.bkg_model

        if interactive_bounds:
            self.ibounds.update()
            inds = spectrum.inds_local_minima()
            for ind in inds:
                ax.axvline(spectrum.x[ind], ls=':', lw=0.3)
            if view_options["Peaks"]:
                self.lines += [bbox.tmp[0] for bbox in self.ibounds.bboxes if bbox.tmp]

        # Add Peak labels annotations
        if view_options.get("Peak labels", True):
            dy_label = LABEL_OFFSET_RATIO * spectrum.y.max()
            annotation_y = []
            for i, label in enumerate(spectrum.peak_labels):
                if not label:
                    continue
                model = spectrum.peak_models[i]
                x0 = model.param_hints["x0"]["value"]
                ind = closest_index(spectrum.x, x0)
                x_label, y_label = spectrum.x[ind], spectrum.y[ind]

                if view_options.get("Subtract bkg+baseline") and spectrum.bkg_model is not None:
                    bkg_model = spectrum.bkg_model
                    y_label -= bkg_model.eval(bkg_model.make_params(), x=x_label)

                xy = (x_label, y_label + dy_label)
                annotation_y.append(y_label + 2 * dy_label)
                ax.annotate(
                    label,
                    xy=xy,
                    xytext=(0, 20),
                    xycoords="data",
                    textcoords="offset points",
                    ha="center",
                    size=14,
                    arrowprops={"fc": 'k', "arrowstyle": '->'},
                    verticalalignment="bottom",
                    annotation_clip=True,
                )

            # Adjust y-axis to contain peak labels
            if annotation_y:
                max_annotation_y = max(annotation_y)
                current_ylim = ax.get_ylim()
                if max_annotation_y > current_ylim[1]:
                    ax.set_ylim(top=max_annotation_y + YLIM_BUFFER_RATIO * spectrum.y.max())

        if view_options.get("Preserve axes", False):
            self.set_view_limits(ax, xlim, ylim)

        if view_options.get("X-log", False):
            ax.set_xscale("log")

        if view_options.get("Y-log", False):
            ax.set_yscale("log")

        # refresh the plot and the toolbar
        ax.figure.canvas.draw_idle()
        toolbar.update()
        toolbar.push_current()

    def apply_model(self, model_dict=None, fnames=None, ncpus=None):
        """Apply model to the selected spectra"""
        if model_dict is None:
            self.showToast("error", "No model has been loaded", "")
            return

        nfiles = len(fnames)
        fit_status = {fname: None for fname in fnames}
        for fname in fnames:
            spectrum, _ = self.spectra.get_objects(fname)
            # spectrum.set_attributes(model_dict)
            fit_status[fname] = spectrum
        self.spectra.pbar_index = 0
        show_progressbar = False

        args = (model_dict, fnames, ncpus, show_progressbar)
        thread = Thread(target=self.spectra.apply_model, args=args)
        thread.start()
        self.progressUpdated.emit(self.spectra, nfiles, ncpus)
        thread.join()

        fit_status = {fname: spectrum.result_fit for fname, spectrum in fit_status.items()}
        self.colorizeFromFitStatus.emit(fit_status)
        self.PeaksChanged.emit(self.current_spectra[0])
        self.refreshPlot.emit()

    def save_models(self, fname_json, fnames=None):
        self.spectra.save(fname_json, fnames=fnames)
