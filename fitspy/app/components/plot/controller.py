from PySide6.QtCore import QObject, Signal
from .model import Model

class PlotController(QObject):
    showToast = Signal(str, str)
    decodedSpectraMap = Signal(str, list)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    settingChanged = Signal(str, bool)
    highlightSpectrum = Signal(str)

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
        
        self.model.spectrumLoaded.connect(self.spectrumLoaded)
        self.model.spectrumDeleted.connect(self.spectrumDeleted)
        self.model.spectraMapDeleted.connect(self.spectraMapDeleted)
        self.model.decodedSpectraMap.connect(self.decodedSpectraMap)
        self.model.mapSwitched.connect(self.map2d_plot.set_map)

        for label, checkbox in self.view_options.checkboxes.items():
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.view_option_changed(cb))
        
    def set_marker(self, spectrum_or_fname_or_coords):
        fname = self.model.current_map.set_marker(spectrum_or_fname_or_coords)
        self.highlightSpectrum.emit(fname)

    def view_option_changed(self, checkbox):
        label = checkbox.text()
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
        self.update_spectraplot()

    def update_spectraplot(self):
        ax = self.spectra_plot.ax
        view_options = self.view_options.get_view_options()
        self.model.update_spectraplot(ax, view_options)

    def get_spectrum(self, fname):
        return self.model.spectra.get_objects(fname)[0]

    def remove_outliers(self, coef):
        self.model.spectra.outliers_limit_calculation(coef=coef)
        self.update_spectraplot()