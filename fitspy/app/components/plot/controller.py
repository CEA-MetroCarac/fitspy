from PySide6.QtCore import QObject, Signal
from .model import Model

class PlotController(QObject):
    decodedSpectraMap = Signal(str, list)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(object)
    spectraMapDeleted = Signal(str)
    settingChanged = Signal(str, bool)
    highlightSpectrum = Signal(str)

    def __init__(self, spectra_plot, map2d_plot, view_options):
        super().__init__()
        self.model = Model()
        self.spectra_plot = spectra_plot
        self.map2d_plot = map2d_plot
        self.view_options = view_options
        self.setup_connections()
    
    def setup_connections(self):
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

    def update_spectraplot(self, fnames):
        ax = self.spectra_plot.ax
        view_options = self.view_options.get_view_options()
        self.model.update_spectraplot(ax, fnames, view_options)

    def get_spectrum(self, fname):
        return self.model.spectra.get_objects(fname)[0]