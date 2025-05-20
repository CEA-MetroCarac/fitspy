from pathlib import Path
from PySide6.QtCore import QObject, Signal, QTimer

from fitspy.core.spectrum import Spectrum
from fitspy.apps.interactive_bounds import InteractiveBounds
from fitspy.apps.pyside.utils import to_snake_case
from fitspy.apps.pyside.components.plot.model import Model
from fitspy.apps.pyside import DEFAULTS


class PlotController(QObject):
    showToast = Signal(str, str, str)
    askConfirmation = Signal(str, object, tuple, dict)
    decodedSpectraMap = Signal(str, list)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    settingChanged = Signal(str, object)
    highlightSpectrum = Signal(list, bool)
    baselinePointsChanged = Signal(list)
    PeaksChanged = Signal(object)
    BkgChanged = Signal(dict)
    progressUpdated = Signal(object, int, int)
    colorizeFromFitStatus = Signal(dict)
    exportCSV = Signal(object)

    def __init__(self, spectra_plot, map2d_plot, toolbar):
        super().__init__()
        self.model = Model()
        self.spectra_plot = spectra_plot
        self.map2d_plot = map2d_plot
        self.toolbar = toolbar
        self.view_options = toolbar.view_options
        # self.too_many_objects_shown = False
        self.init_click_timer()
        self.setup_connections()

    def init_click_timer(self):
        def reset_click_counter():
            self.consecutive_clicks = 0

        self.consecutive_clicks = 0
        self.click_threshold = 1
        self.click_interval = 1000
        self.click_timer = QTimer()
        self.click_timer.setInterval(self.click_interval)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(reset_click_counter)

    def setup_connections(self):
        self.toolbar.copy_btn.clicked.connect(self.spectra_plot.copy_figure)
        self.spectra_plot.showToast.connect(self.showToast)

        self.map2d_plot.canvas.mpl_connect("button_press_event", self.map2d_plot.on_click)
        self.map2d_plot.dock_widget.topLevelChanged.connect(
            self.map2d_plot.onDockWidgetTopLevelChanged)
        self.map2d_plot.tab_widget.currentChanged.connect(
            lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.map2d_plot.tab_widget.intensity_tab.range_slider.valueChanged.connect(
            lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.map2d_plot.addMarker.connect(self.set_marker)

        for i in range(self.map2d_plot.tab_widget.count()):
            tab = self.map2d_plot.tab_widget.widget(i)
            tab.vrange_slider.valueChanged.connect(
                lambda: self.map2d_plot.update_plot(self.model.current_map))
            tab.export_btn.clicked.connect(
                lambda: self.exportCSV.emit(self.model.current_map))
            if hasattr(tab, "combo"):
                # FIXME FIX MAP2DPLOT MVC
                tab.combo.currentIndexChanged.connect(
                    lambda: self.map2d_plot.update_plot(self.model.current_map))

        self.model.showToast.connect(self.showToast)
        self.model.spectrumLoaded.connect(self.spectrumLoaded)
        self.model.spectrumDeleted.connect(self.spectrumDeleted)
        self.model.spectraMapDeleted.connect(self.spectraMapDeleted)
        self.model.decodedSpectraMap.connect(self.decodedSpectraMap)
        self.model.mapSwitched.connect(self.map2d_plot.set_map)
        self.model.baselinePointsChanged.connect(self.baselinePointsChanged)
        self.model.refreshPlot.connect(self.update_spectraplot)
        self.model.PeaksChanged.connect(self.PeaksChanged)
        self.model.progressUpdated.connect(self.progressUpdated)
        self.model.colorizeFromFitStatus.connect(self.colorizeFromFitStatus)
        self.model.askConfirmation.connect(self.askConfirmation)

        self.toolbar.baseline_radio.toggled.connect(self.on_click_mode_changed)
        self.toolbar.peaks_radio.toggled.connect(self.on_click_mode_changed)
        self.toolbar.highlight_radio.toggled.connect(self.on_click_mode_changed)

        self.spectra_plot.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.spectra_plot.canvas.mpl_connect("button_press_event", self.on_spectra_plot_click)

        # for label, checkbox in self.view_options.checkboxes.items():
        for checkbox in self.view_options.checkboxes.values():
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.view_option_changed(cb))

    def highlight_peak(self, index):
        """Highlight the peak at the given index in the spectrum plot."""
        ax = self.spectra_plot.ax
        self.model.highlight_peak(ax, index)

    def on_motion(self, event):
        view_options = self.view_options.get_view_options()
        if view_options["Annotations"]:
            ax = self.spectra_plot.ax
            self.model.on_motion(ax, event)

    def set_marker(self, spectrum_or_fname_or_coords):
        if self.model.current_map:
            fname = self.model.current_map.set_marker(spectrum_or_fname_or_coords)
            if fname:
                self.highlightSpectrum.emit([fname], True)

    def view_option_changed(self, checkbox):
        label = f"view_options_{to_snake_case(checkbox.text())}"
        state = checkbox.isChecked()
        self.settingChanged.emit(label, state)
        self.update_spectraplot()

    def load_map(self, fname):
        self.model.load_map(fname)

    def switch_map(self, fname):
        self.model.switch_map(fname)

    def load_spectra(self, models):
        self.model.load_spectra(models)

    def load_spectrum(self, fnames):
        self.model.load_spectrum(fnames)

    def del_spectrum(self, items):
        self.model.del_spectrum(items)

    def del_map(self, fname):
        self.model.del_map(fname)

    def reinit_spectra(self, fnames):
        self.model.reinit_spectra(fnames)

    def set_current_spectra(self, fnames):
        if isinstance(fnames, str):
            fnames = [fnames]

        self.model.ibounds = None

        if len(fnames) == 1 and fnames[0].endswith('.json'):
            spectrum = Spectrum.create_from_model(fnames[0])
            self.model.current_spectra = [spectrum] if spectrum is not None else []
        else:
            self.model.current_spectra = [self.model.spectra.get_objects(fname)[0]
                                          for fname in fnames if fname != '']
            if len(self.model.current_spectra) > 0:
                self.model.ibounds = InteractiveBounds(self.model.current_spectra[0],
                                                       self.spectra_plot.ax,
                                                       cmap=DEFAULTS["peaks_cmap"],
                                                       bind_func=self.model.refresh)
                self.update_plot_title()
            else:
                self.spectra_plot.ax.clear()
                self.spectra_plot.ax.figure.canvas.draw_idle()

    def update_plot_title(self):
        if self.model.current_spectra:
            model_name = None
            if self.model.current_spectra[0]:
                model_name = Path(self.model.current_spectra[0].fname).name
            self.spectra_plot.ax.set_title(model_name)

    def update_spectraplot(self):
        ax = self.spectra_plot.ax
        view_options = self.view_options.get_view_options()
        self.model.update_spectraplot(ax, view_options, self.toolbar.mpl_toolbar)

    def get_spectra(self, fname=None):
        if fname is None:
            return self.model.current_spectra
        return self.model.spectra.get_objects(fname)[0]

    def outliers_calculation(self, coef):
        self.model.spectra.outliers_limit_calculation(coef=coef)
        self.update_spectraplot()

    def on_click_mode_changed(self):
        """Callback for radio button state changes."""
        selected_mode = self.toolbar.get_selected_radio()
        if selected_mode and selected_mode != self.model.current_mode:
            self.model.current_mode = selected_mode
            self.settingChanged.emit("click_mode", selected_mode)

    def on_spectra_plot_click(self, event):
        """Callback for click events on the spectra plot."""
        # Do not add baseline or peak points when pan or zoom are selected
        if self.toolbar.mpl_toolbar.is_pan_active() or self.toolbar.mpl_toolbar.is_zoom_active():
            self.consecutive_clicks += 1
            self.click_timer.start()
            if self.consecutive_clicks > self.click_threshold:
                self.showToast.emit(
                    "INFO",
                    "Pan/Zoom Mode",
                    "If you want to add baseline or peak points, disable pan/zoom mode.",
                )
            return
        else:
            self.consecutive_clicks = 0

        x, y = event.xdata, event.ydata
        point_type = self.toolbar.get_selected_radio()

        if point_type == "highlight":
            fnames = self.model.highlight_spectrum(self.spectra_plot.ax, event)
            self.highlightSpectrum.emit(fnames, False)

        elif point_type == "baseline":
            if event.button == 1:
                self.model.add_baseline_point(x, y)
            else:
                self.model.del_baseline_point(x)

        else:  # point_type == "peaks":
            if self.model.ibounds is not None and self.model.ibounds.interact_with_bbox(event):
                self.model.refresh()
            else:
                if event.button == 1:
                    self.model.add_peak_point(self.model.peak_model, x)
                else:
                    self.model.del_peak_point(x)

    def set_spectrum_attr(self, attr, value, fnames=None):
        if fnames is None:
            for spectrum in self.model.current_spectra:
                self.model.set_spectrum_attr(spectrum.fname, attr, value)
        else:
            for fname in fnames:
                self.model.set_spectrum_attr(fname, attr, value)

        self.update_spectraplot()

    def set_baseline_points(self, points):
        self.model.set_baseline_points(points)

    def apply_baseline(self):
        self.colorizeFromFitStatus.emit({s.fname: None for s in self.model.current_spectra})
        self.model.preprocess()
        self.update_spectraplot()

    def apply_spectral_range(self, vmin, vmax, fnames=None):
        if fnames is None:
            fnames = [spectrum.fname for spectrum in self.model.current_spectra]

        for fname in fnames:
            self.model.set_spectrum_attr(fname, "range_min", vmin)
            self.model.set_spectrum_attr(fname, "range_max", vmax)

        self.colorizeFromFitStatus.emit({fname: None for fname in fnames})
        self.model.preprocess()
        self.update_spectraplot()

    def apply_normalization(self, state, vmin, vmax):
        # for selected_spectrum
        for spectrum in self.model.current_spectra:
            self.model.set_spectrum_attr(spectrum.fname, "normalize", state)
            self.model.set_spectrum_attr(spectrum.fname, "normalize_range_min", vmin)
            self.model.set_spectrum_attr(spectrum.fname, "normalize_range_max", vmax)
            self.colorizeFromFitStatus.emit({spectrum.fname: None})
            spectrum.preprocess()

        self.update_spectraplot()

    def update_peak_model(self, model):
        self.model.peak_model = model

    def set_peaks(self, peaks):
        if not self.model.current_spectra:
            return
        spectrum = self.model.current_spectra[0]
        spectrum.set_attributes(peaks)
        self.update_spectraplot()

    def set_bkg_model(self, model):
        for i, spectrum in enumerate(self.model.current_spectra):
            spectrum.set_bkg_model(model)
            spectrum.result_fit = lambda: None
            if i == 0 and spectrum.bkg_model:
                self.BkgChanged.emit(spectrum.bkg_model.param_hints)
        self.update_spectraplot()

    def set_bkg(self, bkg):
        if not self.model.current_spectra:
            return
        for spectrum in self.model.current_spectra:
            spectrum.set_attributes(bkg)

        self.update_spectraplot()

    def set_spectra_attributes(self, models):
        self.model.spectra.set_attributes(models, preprocess=True)

    def fit(self, model_dict, ncpus):
        fnames = [spectrum.fname for spectrum in self.model.current_spectra]
        self.model.apply_model(model_dict=model_dict, fnames=fnames, ncpus=ncpus)

    def save_models(self, fname_json, fnames):
        self.model.save_models(fname_json, fnames)
