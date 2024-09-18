from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QDockWidget, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTabWidget, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from superqt import QLabeledDoubleRangeSlider as QRangeSlider

from fitspy.app.components.settings import DoubleSpinBox


class CommonTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCommonUI()

    def initCommonUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(3)
        h_layout1 = QHBoxLayout()

        range_min = DoubleSpinBox()
        range_min.setDecimals(2)
        range_min.setRange(-9999.99, 9999.99)
        range_max = DoubleSpinBox()
        range_max.setDecimals(2)
        range_max.setRange(-9999.99, 9999.99)

        self.export_button = QPushButton("Export .csv")

        h_layout1.addWidget(QLabel("Min/Max:"))
        h_layout1.addWidget(range_min)
        h_layout1.addWidget(QLabel("/"))
        h_layout1.addWidget(range_max)
        h_layout1.addStretch()
        h_layout1.addWidget(self.export_button)

        self.layout.addLayout(h_layout1)

class IntensityTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        h_layout2 = QHBoxLayout()
        h_layout2.setSpacing(10)
        self.range_label = QLabel("X-Range")
        self.range_slider = QRangeSlider()
        self.range_slider.barColor = '#3c94ed'
        h_layout2.addWidget(self.range_label)
        h_layout2.addWidget(self.range_slider)

        self.layout.addLayout(h_layout2)

class x0Tab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout.addWidget(QLabel("X0"))

class FWHMLTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout.addWidget(QLabel("FWHM_L"))

class FWHMRTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout.addWidget(QLabel("FWHM_R"))

class AlphaTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout.addWidget(QLabel("Alpha"))

class Settings(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.intensity_tab = IntensityTab()
        self.x0_tab = x0Tab()
        self.fwhml_tab = FWHMLTab()
        self.fwhmr_tab = FWHMRTab()
        self.alpha_tab = AlphaTab()

        self.addTab(self.intensity_tab, "Intensity (sum)")
        self.addTab(self.x0_tab, "x0")
        self.addTab(self.fwhml_tab, "fwhm_l")
        self.addTab(self.fwhmr_tab, "fwhm_r")
        self.addTab(self.alpha_tab, "alpha")

        self.setMaximumHeight(120)
        self.setVisible(False)

class Map2DPlot(QMainWindow):
    addMarker = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.colorbar = None

    def initUI(self):
        self.dock_widget = QDockWidget("Measurement sites (Drag to undock)", self)
        self.dock_widget.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

        self.dock_container = QWidget()
        self.dock_layout = QVBoxLayout(self.dock_container)
        self.dock_layout.setContentsMargins(0, 0, 0, 0)
        self.dock_layout.setSpacing(0)

        # Settings that are displayed when the dock widget is undocked
        self.tab_widget = Settings()
        self.dock_layout.addWidget(self.tab_widget)

        # Spectra 2D Map
        self.figure = Figure(layout='compressed')
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.dock_layout.addWidget(self.canvas)

        self.dock_widget.setWidget(self.dock_container)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    def on_click(self, event):
        """Callback for mouse click event."""
        x, y = event.xdata, event.ydata
        self.addMarker.emit((x, y))

    def onDockWidgetTopLevelChanged(self, floating):
        if floating:
            self.dock_widget.resize(600, 600)
            self.tab_widget.setVisible(True)
            self.add_colorbar()
        else:
            self.dock_widget.resize(300, 300)
            self.tab_widget.setVisible(False)
            self.remove_colorbar()

    def add_colorbar(self):
        if not self.colorbar and self.ax.images:
            self.colorbar = self.figure.colorbar(self.ax.images[0], ax=self.ax)
            self.canvas.draw()

    def remove_colorbar(self):
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None
            self.canvas.draw()

    def set_map(self, spectramap):
        if not spectramap:
            self.ax.clear()
            self.canvas.draw()
            self.remove_colorbar()
        else:
            spectramap.plot_map(self.ax, range_slider=self.tab_widget.intensity_tab.range_slider)
            if self.dock_widget.isFloating():
                self.add_colorbar()
            else:
                self.remove_colorbar()

    def onTabWidgetCurrentChanged(self, spectramap):
        xrange = self.tab_widget.intensity_tab.range_slider.value()
        var = self.tab_widget.tabText(self.tab_widget.currentIndex())
        spectramap.plot_map_update(xrange=xrange, var=var)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = QMainWindow()
    main.setCentralWidget(QLabel("Central Widget"))
    map2d_plot = Map2DPlot(main)
    main.setCentralWidget(map2d_plot)
    main.show()
    sys.exit(app.exec())