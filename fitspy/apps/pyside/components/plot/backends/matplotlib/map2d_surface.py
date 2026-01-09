from __future__ import annotations

from typing import Callable, Optional

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

from fitspy.apps.pyside.components.plot.abstractions import PointerEvent
from fitspy.apps.pyside.components.plot.backends.matplotlib import pointer_event_from_mpl


class MatplotlibMap2DSurface:
    def __init__(self):
        self.figure = Figure(layout="compressed")
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self._click_callback: Optional[Callable[[PointerEvent], None]] = None
        self.colorbar = None

        self.canvas.mpl_connect("button_press_event", self._on_click)

    def widget(self):
        return self.canvas

    def connect_click(self, callback: Callable[[PointerEvent], None]) -> None:
        self._click_callback = callback

    def _on_click(self, event) -> None:
        if self._click_callback is None:
            return
        self._click_callback(pointer_event_from_mpl(event))

    def clear(self) -> None:
        self.ax.clear()
        self.canvas.draw_idle()
        self.remove_colorbar()

    def plot_spectramap(self, spectramap, range_slider, cmap) -> None:
        spectramap.plot_map(self.ax, range_slider=range_slider, cmap=cmap)

    def plot_update(self, spectramap, *, vmin, vmax, xrange, var, label, cmap) -> None:
        spectramap.plot_map_update(
            vmin=vmin,
            vmax=vmax,
            xrange=xrange,
            var=var,
            label=label,
            cmap=cmap,
        )

    def plot_prepare_vrange(self, spectramap, *, xrange, var, label, cmap) -> None:
        spectramap.plot_map_update(xrange=xrange, var=var, label=label, cmap=cmap)

    def add_colorbar(self) -> None:
        if not self.colorbar and self.ax.images:
            self.colorbar = self.figure.colorbar(self.ax.images[0], ax=self.ax)
            self.canvas.draw_idle()

    def remove_colorbar(self) -> None:
        if self.colorbar:
            self.colorbar.remove()
            self.colorbar = None
            self.canvas.draw_idle()

    def update_colorbar(self, floating: bool) -> None:
        if floating:
            self.add_colorbar()
        else:
            self.remove_colorbar()
