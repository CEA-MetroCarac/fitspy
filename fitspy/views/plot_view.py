from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout

class PlotView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a figure and add a subplot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Create a toolbar for the plot
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Create and set layout for this widget
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Set the title of the plot
        self.ax.set_title("DEFAULT")

        # Set the labels of the plot
        self.ax.set_xlabel("X Label")
        self.ax.set_ylabel("Y Label")