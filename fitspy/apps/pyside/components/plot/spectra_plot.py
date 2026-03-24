import pyqtgraph as pg

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout

from fitspy.apps.pyside.components.plot.backend_manager import MplLikeAxes


class SpectraPlot(QWidget):
    showToast = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget()
        self.plot_item = self.plot_widget.getPlotItem()
        self.ax = MplLikeAxes(self.plot_item)

        self.plot_widget.getViewBox().setMenuEnabled(False)
        self.plot_widget.setBackground('w')

        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def copy_figure(self):
        """Copy the figure to the clipboard using Pyside6 QClipboard"""
        clipboard = QApplication.clipboard()
        pixmap = self.plot_widget.grab()
        clipboard.setPixmap(pixmap)
        self.showToast.emit("success", "Figure copied to clipboard", "")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    spectra_plot = SpectraPlot()
    spectra_plot.show()
    sys.exit(app.exec())
