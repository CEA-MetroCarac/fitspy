from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol


@dataclass(frozen=True, slots=True)
class PointerEvent:
    """Backend-agnostic pointer event.

    Matplotlib/PyQtGraph events can be adapted to this shape.

    Attributes
    ----------
    xdata, ydata:
        Data coordinates under the cursor (or None if not available).
    button:
        Mouse button number when applicable (1=left, 2=middle, 3=right), else None.
    in_plot_area:
        Whether the event occurred inside the plotting area.
    raw:
        Backend-native event object for backend implementations that need it.
        App/controller code must not depend on this.
    """

    xdata: Optional[float]
    ydata: Optional[float]
    button: Optional[int]
    in_plot_area: bool
    raw: Any = None


class PlotNavigation(Protocol):
    """Optional backend navigation controls (pan/zoom/home/etc.)."""

    def widget(self) -> Any: ...

    def is_pan_active(self) -> bool: ...

    def is_zoom_active(self) -> bool: ...

    def update(self) -> None: ...

    def push_current(self) -> None: ...


class SpectraPresenter(ABC):
    """Presenter contract for spectra plot widgets. This mediates between the plot model and view."""

    @abstractmethod
    def on_current_spectra_changed(self) -> None: ...

    @abstractmethod
    def update(self, view_options: dict[str, bool]) -> None: ...

    @abstractmethod
    def highlight_peak(self, index: int) -> None: ...

    @abstractmethod
    def on_motion(self, event: PointerEvent, view_options: dict[str, bool]) -> None: ...

    @abstractmethod
    def on_click(
        self,
        event: PointerEvent,
        click_mode: Optional[str],
        navigation: Optional[PlotNavigation],
    ) -> Optional[list[str]]:
        """Returns a list of spectrum IDs if spectra were highlighted, else None."""


class SpectraPlot(Protocol):
    """Plot widget contract. Concrete widgets are expected to be Qt widgets."""

    def connect_motion(self, callback: Callable[[PointerEvent], None]) -> None: ...

    def connect_click(self, callback: Callable[[PointerEvent], None]) -> None: ...

    def copy_figure(self) -> None: ...

    def set_title(self, title: str) -> None: ...

    def get_title(self) -> str: ...

    def create_presenter(self, model: Any, navigation: Optional[PlotNavigation]) -> SpectraPresenter: ...


class Map2DPlot(Protocol):
    def connect_click(self, callback: Callable[[PointerEvent], None]) -> None: ...

    def connect_add_marker(self, callback: Callable[[tuple[Optional[float], Optional[float]]], None]) -> None: ...

    def set_map(self, spectramap: Any) -> None: ...

    def update_plot(self, spectramap: Any) -> None: ...

    def get_current_title(self) -> str: ...
