from PySide6.QtCore import QObject, Signal
from matplotlib.figure import Figure
import numpy as np

class PlotModel(QObject):
    figureChanged = Signal(Figure)

    def __init__(self):
        super().__init__()
        self.fig = None

    def clear_plot(self):
        self.fig = None
        self.figureChanged.emit(None)
    
    def plot(self, selected_files):
        # PLACEHOLDER
        fig = Figure()
        ax = fig.add_subplot(111)
        for i, file in enumerate(selected_files):
            x = np.linspace(0, 4 * np.pi, 100)
            y = np.sin(x + i)
            ax.plot(x, y)
        self.fig = fig
        self.figureChanged.emit(fig)


    def update_plot(self, selected_files):
        print("Selected files:", selected_files)

        # if selected_files is empty list, clear the plot
        if not selected_files:
            self.clear_plot()
            return
        
        # Else, call plot method
        self.plot(selected_files)
