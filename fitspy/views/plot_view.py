from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout

from .frame_map import FrameMap

class CustomNavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self.original_xlim = None
        self.original_ylim = None

    def set_original_view_limits(self, xlim, ylim):
        self.original_xlim = xlim
        self.original_ylim = ylim

    def home(self, *args):
        if self.original_xlim and self.original_ylim:
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(self.original_xlim)
            ax.set_ylim(self.original_ylim)
            self.canvas.draw()
        else:
            super().home(*args)

class PlotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.canvas = None
        self.toolbar = None
        self.original_xlim = None
        self.original_ylim = None
        self._init_canvas_and_toolbar(Figure())

    def _init_canvas_and_toolbar(self, fig):
        # If canvas or toolbar exists, remove them
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        if self.toolbar:
            self.layout.removeWidget(self.toolbar)
            self.toolbar.deleteLater()

        # Create and add new canvas and toolbar
        self.canvas = FigureCanvas(fig)
        self.toolbar = CustomNavigationToolbar(self.canvas, self)
        self.toolbar.set_original_view_limits(self.original_xlim, self.original_ylim)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)

    def frame_map_init(self, spectra_map):
        self.frame_map_window = FrameMap(spectra_map)
        self.frame_map_window.show()

    def display_figure(self, fig, xlim=None, ylim=None):
        fig.tight_layout()
        self._init_canvas_and_toolbar(fig)
        if xlim and ylim:
            self.set_view_limits(xlim, ylim)
        else:
            self.store_original_view_limits()

    def get_view_limits(self):
        if hasattr(self, 'canvas') and self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            return ax.get_xlim(), ax.get_ylim()
        return None, None

    def set_view_limits(self, xlim, ylim):
        if hasattr(self, 'canvas') and self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            self.canvas.draw()

    def store_original_view_limits(self):
        if hasattr(self, 'canvas') and self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            self.original_xlim = ax.get_xlim()
            self.original_ylim = ax.get_ylim()

    def update_element_visibility(self):
        """Method to handle element visibility updates without full redraw."""
        # Use blitting to update element visibility without full redraw
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)