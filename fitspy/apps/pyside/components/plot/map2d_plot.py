import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                               QPushButton, QTabWidget, QDockWidget)

from superqt import QLabeledDoubleRangeSlider as QRangeSlider

from fitspy.apps.pyside.components.custom_widgets import ComboBox
from fitspy.apps.pyside import DEFAULTS


class CommonTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initCommonUI()

    def initCommonUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        h_layout1 = QHBoxLayout()

        self.vrange_slider = QRangeSlider()
        self.vrange_slider.setRange(0, 0)
        self.vrange_slider.setDecimals(2)
        self.vrange_slider.setOrientation(Qt.Horizontal)

        self.export_btn = QPushButton("Export .csv")

        h_layout1.addWidget(QLabel("Range:"))
        h_layout1.addWidget(self.vrange_slider)
        # h_layout1.addStretch() # Adds spacer
        h_layout1.addWidget(self.export_btn)

        self.layout.addLayout(h_layout1)


class CommonTabWithCombo(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        label = QLabel("Label: ")
        self.combo = ComboBox()

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.combo)

        self.layout.addLayout(hbox)


class IntensityTab(CommonTab):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        h_layout2 = QHBoxLayout()
        h_layout2.setSpacing(10)
        self.range_label = QLabel("X-Range")
        self.range_slider = QRangeSlider()
        self.range_slider.barColor = "#3c94ed"
        h_layout2.addWidget(self.range_label)
        h_layout2.addWidget(self.range_slider)

        self.layout.addLayout(h_layout2)


class Settings(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.intensity_tab = IntensityTab()
        self.x0_tab = CommonTabWithCombo()
        self.fwhm_tab = CommonTabWithCombo()
        self.fwhml_tab = CommonTabWithCombo()
        self.fwhmr_tab = CommonTabWithCombo()
        self.alpha_tab = CommonTabWithCombo()

        self.addTab(self.intensity_tab, "Intensity (sum)")
        self.addTab(self.x0_tab, "x0")
        self.addTab(self.fwhm_tab, "fwhm")
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
        self.dock_widget.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

        self.dock_container = QWidget()
        self.dock_layout = QVBoxLayout(self.dock_container)
        self.dock_layout.setContentsMargins(0, 0, 0, 0)
        self.dock_layout.setSpacing(0)

        # Settings that are displayed when the dock widget is undocked
        self.tab_widget = Settings()
        self.dock_layout.addWidget(self.tab_widget)

        # Spectra 2D Map
        self.figure = Figure(layout="compressed")
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.dock_layout.addWidget(self.canvas)

        self.dock_widget.setWidget(self.dock_container)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    # Event Handlers
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

    def onTabWidgetCurrentChanged(self, spectramap):
        self.update_labels(spectramap)
        self.update_plot(spectramap)

    # Plotting Functions
    def set_map(self, spectramap):
        if not spectramap:
            self.clear_map()
        else:
            self.plot_spectramap(spectramap)
            self.update_colorbar()
            self.update_vrange_slider(spectramap)

    def clear_map(self):
        self.ax.clear()
        self.canvas.draw_idle()
        self.remove_colorbar()

    def plot_spectramap(self, spectramap):
        spectramap.plot_map(self.ax,
                            range_slider=self.tab_widget.intensity_tab.range_slider,
                            cmap=DEFAULTS["map_cmap"])

    def update_plot(self, spectramap):
        xrange = self.tab_widget.intensity_tab.range_slider.value()
        var = self.tab_widget.tabText(self.tab_widget.currentIndex())
        current_tab = self.tab_widget.currentWidget()

        label = current_tab.combo.currentText() if hasattr(current_tab, "combo") else ""

        if hasattr(current_tab, "vrange_slider"):
            current_tab.vrange_slider.blockSignals(True)
            self.update_plot_map(spectramap, xrange, var, label, current_tab)
            current_tab.vrange_slider.blockSignals(False)

        vmin, vmax = current_tab.vrange_slider.value()
        spectramap.plot_map_update(vmin=vmin, vmax=vmax, xrange=xrange, var=var, label=label,
                                   cmap=DEFAULTS["map_cmap"])

    def update_plot_map(self, spectramap, xrange, var, label, current_tab):
        spectramap.plot_map_update(xrange=xrange, var=var, label=label, cmap=DEFAULTS["map_cmap"])
        vmin, vmax = current_tab.vrange_slider.minimum(), current_tab.vrange_slider.maximum()

        if not np.all(np.isnan(spectramap.arr)):
            rvmin, rvmax = np.nanmin(spectramap.arr), np.nanmax(spectramap.arr)
        
            if (vmin, vmax) != (rvmin, rvmax):
                current_tab.vrange_slider.setRange(rvmin, rvmax)
                current_tab.vrange_slider.setValue((rvmin, rvmax))

    # Colorbar Functions
    def add_colorbar(self):
        if not self.colorbar and self.ax.images:
            self.colorbar = self.figure.colorbar(self.ax.images[0], ax=self.ax)
            self.canvas.draw_idle()

    def remove_colorbar(self):
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None
            self.canvas.draw_idle()

    def update_colorbar(self):
        if self.dock_widget.isFloating():
            self.add_colorbar()
        else:
            self.remove_colorbar()

    # Utility Functions
    def collect_unique_labels(self, spectramap):
        return sorted(list(set([label for spectrum in spectramap
                                for label in spectrum.peak_labels])))

    def update_labels(self, spectramap):
        labels = self.collect_unique_labels(spectramap)
        if labels:
            spectramap.label = labels[0]
        self.update_combo_box(labels)

    def update_combo_box(self, labels):
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, "combo"):
            current_tab.combo.clear()
            current_tab.combo.addItems(labels)

    def update_vrange_slider(self, spectramap, current_tab=None):
        if current_tab is None:
            current_tab = self.tab_widget.currentWidget()

        if hasattr(current_tab, "vrange_slider"):
            current_tab.vrange_slider.blockSignals(True)
            self.set_slider_range_and_value(current_tab, spectramap)
            current_tab.vrange_slider.blockSignals(False)

    def set_slider_range_and_value(self, current_tab, spectramap):
        rvmin, rvmax = np.nanmin(spectramap.arr), np.nanmax(spectramap.arr)
        if not np.all(np.isnan(spectramap.arr)):
            current_tab.vrange_slider.setRange(rvmin, rvmax)
            current_tab.vrange_slider.setValue((rvmin, rvmax))

    def get_current_title(self):
        return self.tab_widget.tabText(self.tab_widget.currentIndex())


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
