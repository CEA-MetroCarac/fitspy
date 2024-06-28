import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

class FrameMap(QWidget):
    def __init__(self, spectra_map, parent=None):
        super().__init__(parent)
        self.spectra_map = spectra_map
        self.initUI()

    def initUI(self):
        self.setWindowTitle(os.path.basename(self.spectra_map.fname))
        self.setMinimumSize(450, 400)  # New compact size
        main_layout = QVBoxLayout()  # Changed to QVBoxLayout for vertical stacking

        # Create the tab widget on top
        tab_widget = QTabWidget()
        tab_names = ["Intensity (sum)", "x0", "ampli", "fwhm", "fwhm_I", "fwhm_r", "alpha"]
        
        # Create a tab for each name in tab_names
        for name in tab_names:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            label = QLabel(f"{name} Placeholder")  # Placeholder label, replace as needed
            tab_layout.addWidget(label)
            tab.setLayout(tab_layout)
            tab_widget.addTab(tab, name)

        # Create the plot underneath the tabs
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        # Example plot
        ax = self.figure.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 0, 1])
        self.canvas.draw()

        # Add tab widget and plot layout to the main layout
        main_layout.addWidget(tab_widget)  # Add tab widget on top
        main_layout.addLayout(plot_layout)  # Add plot layout underneath

        self.setLayout(main_layout)
        self.setAttribute(Qt.WA_DeleteOnClose)