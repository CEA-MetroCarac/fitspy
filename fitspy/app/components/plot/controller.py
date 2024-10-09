from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox

from fitspy.core import to_snake_case
from .model import Model

class PlotController(QObject):
    showToast = Signal(str, str, str)
    decodedSpectraMap = Signal(str, list)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    settingChanged = Signal(str, object)
    highlightSpectrum = Signal(str)
    baselinePointsChanged = Signal(list)
    PeaksChanged = Signal(object)
    progressUpdated = Signal(object, int, int)

    def __init__(self, spectra_plot, map2d_plot, toolbar):
        super().__init__()
        self.model = Model()
        self.spectra_plot = spectra_plot
        self.map2d_plot = map2d_plot
        self.toolbar = toolbar
        self.view_options = toolbar.view_options
        self.setup_connections()
    
    def setup_connections(self):
        self.toolbar.copy_button.clicked.connect(self.spectra_plot.copy_figure)
        self.spectra_plot.showToast.connect(self.showToast)

        self.map2d_plot.canvas.mpl_connect('button_press_event', self.map2d_plot.on_click)
        self.map2d_plot.dock_widget.topLevelChanged.connect(self.map2d_plot.onDockWidgetTopLevelChanged)
        self.map2d_plot.tab_widget.currentChanged.connect(lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.map2d_plot.tab_widget.intensity_tab.range_slider.valueChanged.connect(lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.map2d_plot.addMarker.connect(self.set_marker)
        
        for i in range(self.map2d_plot.tab_widget.count()):
            tab = self.map2d_plot.tab_widget.widget(i)
            tab.vrange_slider.valueChanged.connect(lambda: self.map2d_plot.update_plot(self.model.current_map))
            if hasattr(tab, 'combo'):
                # FIXME FIX MAP2DPLOT MVC
                tab.combo.currentIndexChanged.connect(lambda: self.map2d_plot.update_plot(self.model.current_map))

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
        self.model.askConfirmation.connect(self.show_confirmation_dialog)

        self.toolbar.fitting_radio.toggled.connect(self.on_click_mode_changed)
        self.spectra_plot.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.spectra_plot.canvas.mpl_connect('button_press_event', self.on_spectra_plot_click)

        for label, checkbox in self.view_options.checkboxes.items():
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.view_option_changed(cb))

    def on_motion(self, event):
        ax = self.spectra_plot.ax
        self.model.on_motion(ax, event)
        
    def set_marker(self, spectrum_or_fname_or_coords):
        fname = self.model.current_map.set_marker(spectrum_or_fname_or_coords)
        self.highlightSpectrum.emit(fname)

    def view_option_changed(self, checkbox):
        label = to_snake_case(checkbox.text())
        state = checkbox.isChecked()
        self.settingChanged.emit(label, state)
        self.update_spectraplot()

    def load_map(self, fname):
        self.model.load_map(fname)

    def switch_map(self, fname):
        self.model.switch_map(fname)

    def load_spectrum(self, fnames):
        self.model.load_spectrum(fnames)

    def del_spectrum(self, map, fnames):
        self.model.del_spectrum(map, fnames)

    def del_map(self, fname):
        self.model.del_map(fname)

    def set_current_spectrum(self, fnames):
        parent = self.model.current_map if self.model.current_map else self.model.spectra
        self.model.current_spectrum = [self.model.spectra.get_objects(fname, parent)[0] for fname in fnames]

    def update_spectraplot(self):
        ax = self.spectra_plot.ax
        view_options = self.view_options.get_view_options()
        self.model.update_spectraplot(ax, view_options)

    def get_spectrum(self, fname):
        return self.model.spectra.get_objects(fname)[0]

    def remove_outliers(self, coef):
        self.model.spectra.outliers_limit_calculation(coef=coef)
        self.update_spectraplot()

    def on_click_mode_changed(self):
        """Callback for radio button state changes."""
        if self.toolbar.baseline_radio.isChecked():
            self.settingChanged.emit("click_mode", "baseline")
        elif self.toolbar.fitting_radio.isChecked():
            self.settingChanged.emit("click_mode", "fitting")

    def on_spectra_plot_click(self, event):
        """Callback for click events on the spectra plot."""
        # Do not add baseline or peak points when pan or zoom are selected
        if self.toolbar.mpl_toolbar.is_pan_active() or self.toolbar.mpl_toolbar.is_zoom_active():
            return
        
        # if event.button not in [1, 3]:
        #     return  # Ignore middle mouse button
        action = 'add' if event.button == 1 else 'del'
        point_type = 'baseline' if self.toolbar.baseline_radio.isChecked() else 'peak'

        if action == 'add':
            if point_type == 'baseline':
                self.model.add_baseline_point(event.xdata, event.ydata)
            else:
                self.model.add_peak_point(self.spectra_plot.ax, self.model.peak_model, event.xdata, event.ydata)
        elif action == 'del':
            if point_type == 'baseline':
                self.model.del_baseline_point(event.xdata)
            else:
                self.model.del_peak_point(event.xdata)

    def set_spectrum_attr(self, attr, value, fnames=None):
        if fnames is None:
            for spectrum in self.model.current_spectrum:
                self.model.set_spectrum_attr(spectrum.fname, attr, value)
        else:
            for fname in fnames:
                self.model.set_spectrum_attr(fname, attr, value)

        self.update_spectraplot()

    def set_baseline_points(self, points):
        self.model.set_baseline_points(points)

    def apply_baseline(self):
        self.model.preprocess()
        self.update_spectraplot()

    def apply_spectral_range(self, min, max, fnames=None):
        if fnames is None:
            for spectrum in self.model.current_spectrum:
                self.model.set_spectrum_attr(spectrum.fname, "range_min", min)
                self.model.set_spectrum_attr(spectrum.fname, "range_max", max)
        else:
            for fname in fnames:
                self.model.set_spectrum_attr(fname, "range_min", min)
                self.model.set_spectrum_attr(fname, "range_max", max)

        self.model.preprocess()
        self.update_spectraplot()

    def apply_normalization(self, state, min, max):
        # for all spectrum
        parent = self.model.current_map if self.model.current_map else self.model.spectra
        for spectrum in parent:
            self.model.set_spectrum_attr(spectrum.fname, "normalize", state)
            self.model.set_spectrum_attr(spectrum.fname, "normalize_range_min", min)
            self.model.set_spectrum_attr(spectrum.fname, "normalize_range_max", max)
            spectrum.preprocess()
            
        self.update_spectraplot()

    def show_confirmation_dialog(self, message, callback, args, kwargs):
        reply = QMessageBox.question(None, 'Confirmation', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print(args)
            callback(*args, **kwargs)
        else:
            print("Operation aborted by the user.")

    def update_peak_model(self, model):
        self.model.peak_model = model

    def set_peaks(self, peaks):
        spectrum = self.model.current_spectrum[0]
        spectrum.set_attributes(peaks)
        self.update_spectraplot()

    def fit(self, model_dict, ncpus):
        print("Fitting")
        fit_params = model_dict.get('fit_params', {})
        fnames = [spectrum.fname for spectrum in self.model.current_spectrum]
        self.model.apply_model(model_dict=model_dict, fnames=fnames, fit_params=fit_params, ncpus=ncpus)