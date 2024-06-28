from PySide6.QtCore import QObject, Signal
from matplotlib.figure import Figure
import numpy as np

class PlotModel(QObject):
    figureChanged = Signal(Figure)

    def __init__(self):
        super().__init__()
        self.fig = None
        self.spectra_maps = []

    def update_fig(self, selected_files):
        # PLACEHOLDER
        print("Selected files:", selected_files)
        self.fig = Figure()

        if not selected_files:
            self.figureChanged.emit(self.fig)
        else:
            ax = self.fig.add_subplot(111)
            for i, file in enumerate(selected_files):
                x = np.linspace(0, 4 * np.pi, 100)
                y = np.sin(x + i)
                ax.plot(x, y)
            self.figureChanged.emit(self.fig)
