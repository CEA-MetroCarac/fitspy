from PySide6.QtCore import QObject
from matplotlib.figure import Figure
import numpy as np

class PlotModel(QObject):
    def __init__(self):
        super().__init__()
    
    def show_all(self):
        # Placeholder
        x = np.linspace(0, 4 * np.pi, 100)
        y = np.sin(x)
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        return fig