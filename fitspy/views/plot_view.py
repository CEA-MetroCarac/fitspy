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
        self._init_canvas_and_toolbar(fig)
# class PlotView(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Create a figure and add a subplot
#         self.figure = Figure()
#         self.canvas = FigureCanvas(self.figure)
#         self.ax = self.figure.add_subplot(111)

#         # Create a toolbar for the plot
#         self.toolbar = NavigationToolbar2QT(self.canvas, self)

#         # Create and set layout for this widget
#         layout = QVBoxLayout()
#         layout.addWidget(self.toolbar)
#         layout.addWidget(self.canvas)
#         self.setLayout(layout)

#         # Set the title of the plot
#         self.ax.set_title("DEFAULT")

#         # Set the labels of the plot
#         self.ax.set_xlabel("X Label")
#         self.ax.set_ylabel("Y Label")