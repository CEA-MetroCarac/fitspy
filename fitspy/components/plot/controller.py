from PySide6.QtCore import QObject, Signal
from .model import Model

class PlotController(QObject):
    decodedSpectraMap = Signal(str, list)

    def __init__(self, map2d_plot):
        super().__init__()
        self.model = Model()
        self.map2d_plot = map2d_plot
        self.setup_connections()
    
    def setup_connections(self):
        self.map2d_plot.dock_widget.topLevelChanged.connect(self.map2d_plot.onDockWidgetTopLevelChanged)
        self.model.decodedSpectraMap.connect(self.decodedSpectraMap)
        self.model.mapSwitched.connect(self.map2d_plot.set_map)

    def create_map(self, fname):
        self.model.create_map(fname)

    def switch_map(self, fname):
        self.model.switch_map(fname)