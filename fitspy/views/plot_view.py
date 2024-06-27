from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout

class PlotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self._init_canvas_and_toolbar(Figure())

    def _init_canvas_and_toolbar(self, fig):
        # If canvas or toolbar exists, remove them
        if hasattr(self, 'canvas'):
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        if hasattr(self, 'toolbar'):
            self.layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()

        # Create and add new canvas and toolbar
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def display_figure(self, fig):
        if fig is None:
            fig = Figure()
        fig.tight_layout()
        self._init_canvas_and_toolbar(fig)