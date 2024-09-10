from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QCheckBox
from .model import Model

class PlotController(QObject):
    decodedSpectraMap = Signal(str, list)
    spectrumLoaded = Signal(str)
    spectrumDeleted = Signal(str, object)
    spectraMapDeleted = Signal(str)
    settingChanged = Signal(str, bool)

    def __init__(self, map2d_plot, view_options):
        super().__init__()
        self.model = Model()
        self.map2d_plot = map2d_plot
        self.view_options = view_options
        self.setup_connections()
    
    def setup_connections(self):
        self.map2d_plot.dock_widget.topLevelChanged.connect(self.map2d_plot.onDockWidgetTopLevelChanged)
        self.map2d_plot.tab_widget.currentChanged.connect(lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.map2d_plot.tab_widget.intensity_tab.range_slider.valueChanged.connect(lambda: self.map2d_plot.onTabWidgetCurrentChanged(self.model.current_map))
        self.model.spectrumLoaded.connect(self.spectrumLoaded)
        self.model.spectrumDeleted.connect(self.spectrumDeleted)
        self.model.spectraMapDeleted.connect(self.spectraMapDeleted)
        self.model.decodedSpectraMap.connect(self.decodedSpectraMap)
        self.model.mapSwitched.connect(self.map2d_plot.set_map)

        for checkbox in self.view_options.findChildren(QCheckBox):
            checkbox.stateChanged.connect(lambda state, cb=checkbox: self.view_option_changed(cb))
        
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

    def del_spectrum(self, fname):
        self.model.del_spectrum(fname)

    def del_map(self, fname):
        self.model.del_map(fname)

    def update_spectraplot(self, files):
        self.model.update_spectraplot(files)

    def get_spectrum(self, fname):
        return self.model.spectra.get_objects(fname)[0]