from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QDockWidget, QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout, QTabWidget, QSizePolicy, QPushButton
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas
from superqt import QLabeledDoubleRangeSlider as QRangeSlider

class CommonTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCommonUI()

    def initCommonUI(self):
        self.layout = QVBoxLayout(self)
        # self.layout.setSpacing(0)  # TODO If its not 0 then impossible to redock the dock widget
        h_layout1 = QHBoxLayout()
        
        x_min_input = QDoubleSpinBox()
        x_min_input.setDecimals(2)
        x_min_input.setRange(-9999.99, 9999.99)
        x_max_input = QDoubleSpinBox()
        x_max_input.setDecimals(2)
        x_max_input.setRange(-9999.99, 9999.99)

        export_button = QPushButton()#QPushButton("Export .csv")
        # increase size of button
        export_button.setFixedSize(72, 10)
        # export_button.setStyleSheet("QPushButton {min-width: 100px; min-height: 30px;}")
        # make button as small as possible, fit to text
        # export_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        h_layout1.addWidget(QLabel("Min/Max:"))
        h_layout1.addWidget(x_min_input)
        h_layout1.addWidget(QLabel("/"))
        h_layout1.addWidget(x_max_input)
        h_layout1.addStretch()
        h_layout1.addWidget(export_button)

        self.layout.addLayout(h_layout1)

class IntensityTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        h_layout2 = QHBoxLayout()
        # h_layout2.setSpacing(20)
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
        intensity_tab = IntensityTab()
        x0_tab = x0Tab()
        fwhml_tab = FWHMLTab()
        fwhmr_tab = FWHMRTab()
        alpha_tab = AlphaTab()

        self.addTab(intensity_tab, "intensity (sum)")
        self.addTab(x0_tab, "x0")
        self.addTab(fwhml_tab, "fwhm_l")
        self.addTab(fwhmr_tab, "fwhm_r")
        self.addTab(alpha_tab, "alpha")

        # self.setMaximumHeight(100)
        self.setVisible(False)

class Map2DPlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.colorbar = None

    def initUI(self):
        # self.setMinimumSize(317, 300)

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
        self.figure = Figure(layout='tight')
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.dock_layout.addWidget(self.canvas)

        self.dock_widget.setWidget(self.dock_container)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

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
        if self.colorbar is None:
            self.colorbar = self.figure.colorbar(self.ax.images[0], ax=self.ax)
            self.canvas.draw()

    def remove_colorbar(self):
        if self.colorbar is not None:
            self.colorbar.remove()
            self.colorbar = None
            self.canvas.draw()

    def set_map(self, spectramap):
        self.ax.clear()
        self.ax.imshow(spectramap.arr, extent=spectramap.extent)
        if self.dock_widget.isFloating():
            self.add_colorbar()
        else:
            self.remove_colorbar()
        self.canvas.draw()

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