from __future__ import annotations

from pathlib import Path
from typing import Optional

from fitspy.apps.interactive_bounds import InteractiveBounds
from fitspy.apps.pyside import DEFAULTS
from fitspy.apps.pyside.components.plot.abstractions import PlotNavigation, PointerEvent, SpectraPresenter


class _NoopNavigation:
    def widget(self):  # pragma: no cover
        return None

    def is_pan_active(self) -> bool:
        return False

    def is_zoom_active(self) -> bool:
        return False

    def update(self) -> None:
        return

    def push_current(self) -> None:
        return


class MatplotlibSpectraPresenter(SpectraPresenter):
    def __init__(self, model, spectra_plot, navigation: Optional[PlotNavigation]):
        self.model = model
        self.spectra_plot = spectra_plot
        self.navigation = navigation
        self._noop_navigation = _NoopNavigation()
        self._last_view_options: dict[str, bool] = {}

    def _nav(self):
        return self.navigation if self.navigation is not None else self._noop_navigation

    def on_current_spectra_changed(self) -> None:
        self.model.ibounds = None

        if getattr(self.model, "current_spectra", None):
            spectrum = self.model.current_spectra[0]
            spectrum_fname = getattr(spectrum, "fname", "") if spectrum else ""

            if spectrum and spectrum_fname and not str(spectrum_fname).endswith(".json"):
                self.model.ibounds = InteractiveBounds(
                    spectrum,
                    self.spectra_plot.ax,
                    cmap=DEFAULTS["peaks_cmap"],
                    bind_func=self.model.refresh,
                )

            title = Path(str(spectrum_fname)).name if spectrum_fname else ""
            self.spectra_plot.set_title(title)
        else:
            self.spectra_plot.ax.clear()
            self.spectra_plot.ax.figure.canvas.draw_idle()

        if self._last_view_options:
            self.update(self._last_view_options)

    def update(self, view_options: dict[str, bool]) -> None:
        self._last_view_options = dict(view_options)
        self.model.update_spectraplot(self.spectra_plot.ax, view_options, self._nav())

    def highlight_peak(self, index: int) -> None:
        self.model.highlight_peak(self.spectra_plot.ax, index)

    def on_motion(self, event: PointerEvent, view_options: dict[str, bool]) -> None:
        self._last_view_options = dict(view_options)
        if event.raw is None:
            return
        self.model.on_motion(self.spectra_plot.ax, event.raw)

    def on_click(
        self,
        event: PointerEvent,
        click_mode: Optional[str],
    ) -> Optional[list[str]]:
        if event.raw is None or not event.in_plot_area:
            return None

        x = event.xdata
        y = event.ydata
        button = event.button

        if click_mode == "highlight":
            return self.model.highlight_spectrum(self.spectra_plot.ax, event.raw)

        if x is None:
            return None

        if click_mode == "baseline":
            if button == 1 and y is not None:
                self.model.add_baseline_point(x, y)
            elif button == 3:
                self.model.del_baseline_point(x)
            if self._last_view_options:
                self.update(self._last_view_options)
            return None

        if click_mode == "peaks":
            if self.model.ibounds is not None and self.model.ibounds.interact_with_bbox(event.raw):
                self.model.refresh()
                return None

            if button == 1:
                if getattr(self.model, "peak_model", None) is None:
                    if hasattr(self.model, "showToast"):
                        self.model.showToast.emit("ERROR", "No peak model selected", "")
                    return None
                self.model.add_peak_point(self.model.peak_model, x)
            elif button == 3:
                self.model.del_peak_point(x)
            if self._last_view_options:
                self.update(self._last_view_options)
            return None

        return None
