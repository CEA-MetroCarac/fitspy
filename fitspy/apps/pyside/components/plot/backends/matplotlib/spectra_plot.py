from __future__ import annotations

from typing import Callable, Optional

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from fitspy.apps.pyside.components.plot.abstractions import PointerEvent, PlotNavigation, SpectraPresenter
from fitspy.apps.pyside.components.plot.backends.matplotlib import pointer_event_from_mpl
from .spectra_presenter import MatplotlibSpectraPresenter


class MatplotlibSpectraPlot(QWidget):
    showToast = Signal(str, str, str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._motion_callback: Optional[Callable[[PointerEvent], None]] = None
        self._click_callback: Optional[Callable[[PointerEvent], None]] = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.figure = Figure(layout="compressed")
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def connect_motion(self, callback: Callable[[PointerEvent], None]) -> None:
        self._motion_callback = callback
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)

    def connect_click(self, callback: Callable[[PointerEvent], None]) -> None:
        self._click_callback = callback
        self.canvas.mpl_connect("button_press_event", self._on_click)

    def _on_motion(self, event) -> None:
        if self._motion_callback is None:
            return
        self._motion_callback(pointer_event_from_mpl(event))

    def _on_click(self, event) -> None:
        if self._click_callback is None:
            return
        self._click_callback(pointer_event_from_mpl(event))

    def copy_figure(self) -> None:
        clipboard = QApplication.clipboard()
        buffer = self.canvas.buffer_rgba()
        width, height = self.canvas.get_width_height()
        pixmap = QPixmap.fromImage(QImage(buffer, width, height, QImage.Format_ARGB32))
        clipboard.setPixmap(pixmap)
        self.showToast.emit("success", "Figure copied to clipboard", "")

    def set_title(self, title: str) -> None:
        self.ax.set_title(title)

    def get_title(self) -> str:
        return self.ax.get_title()

    def create_presenter(self, model, navigation: Optional[PlotNavigation]) -> SpectraPresenter:
        return MatplotlibSpectraPresenter(model=model, spectra_plot=self, navigation=navigation)
