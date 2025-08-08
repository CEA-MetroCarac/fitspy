from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtGui import QClipboard, QImage, QPixmap


class SpectraPlot(QWidget):
    showToast = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.figure = Figure(layout="compressed")
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def copy_figure(self):
        """Copy the figure to the clipboard using Pyside6 QClipboard"""
        clipboard = QClipboard()

        # Get the figure as a QPixmap
        buffer = self.canvas.buffer_rgba()
        width, height = self.canvas.get_width_height()
        pixmap = QPixmap.fromImage(QImage(buffer, width, height, QImage.Format_ARGB32))

        clipboard.setPixmap(pixmap)
        self.showToast.emit("success", "Figure copied to clipboard", "")


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    spectra_plot = SpectraPlot()
    spectra_plot.show()
    sys.exit(app.exec())
