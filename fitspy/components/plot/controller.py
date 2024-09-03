from PySide6.QtCore import QObject
# from .model import Model

class PlotController(QObject):
    def __init__(self, map2d_plot):
        super().__init__()
        # self.model = Model()
        self.map2d_plot = map2d_plot
        self.setup_connections()
    
    def setup_connections(self):
        self.map2d_plot.dock_widget.topLevelChanged.connect(self.map2d_plot.onDockWidgetTopLevelChanged)
        