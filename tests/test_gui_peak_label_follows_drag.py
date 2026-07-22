"""
Regression test for issue #71:
'Peaks Label not following when dragging peak interactively'.

When a peak is dragged interactively (pyqtgraph backend), its text label must
track the peak in real time - not only after the mouse is released.
"""
import numpy as np
import pytest

pg = pytest.importorskip("pyqtgraph")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

import matplotlib

from fitspy.core.spectrum import Spectrum
from fitspy.apps.pyside import DEFAULTS
from fitspy.apps.pyside.components.plot.backend_manager import MplLikeAxes
from fitspy.apps.pyside.components.plot.model import Model


VIEW_OPTIONS = {
    "Weights": False,
    "Outliers": False,
    "Outliers limits": False,
    "Negative values": False,
    "Peaks": True,
    "Peak decomposition": False,
    "Noise level": False,
    "Baseline": False,
    "Background": False,
    "Fit": False,
    "Subtract bkg+baseline": False,
    "Residual": False,
    "Legend": False,
    "Interactive bounds": True,
    "Peak labels": True,
    "X-log": False,
    "Y-log": False,
}


def _qapp():
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _make_spectrum():
    spectrum = Spectrum()
    x = np.arange(0.0, 100.0)
    y = 1000.0 * np.exp(-((x - 50.0) ** 2) / (2 * 5.0 ** 2)) + 1.0
    spectrum.x, spectrum.y = x, y
    spectrum.x0, spectrum.y0 = x.copy(), y.copy()
    spectrum.add_peak_model("Lorentzian", x0=50.0)  # label defaults to "1"
    return spectrum


def _label_x(ax, text):
    """x-position (data coords) of the peak-label TextItem matching `text`."""
    xs = []
    for item in ax.plot_item.items:
        if isinstance(item, pg.TextItem):
            try:
                plain = item.textItem.toPlainText()
            except Exception:
                plain = None
            if plain == text:
                xs.append(item.pos().x())
    assert len(xs) == 1, f"expected exactly one label {text!r}, found {len(xs)}"
    return xs[0]


def test_peak_label_follows_peak_during_interactive_drag(monkeypatch):
    # the running app replaces this string with a real mpl colormap at startup;
    # patch it here without polluting the shared DEFAULTS for other tests
    monkeypatch.setitem(DEFAULTS, "peaks_cmap", matplotlib.colormaps["tab10"])

    _qapp()
    plot_widget = pg.PlotWidget()
    ax = MplLikeAxes(plot_widget.getPlotItem())

    spectrum = _make_spectrum()
    model = Model()
    model.current_spectra = [spectrum]
    model.peak_model = "Lorentzian"
    model.init_ibounds(ax)
    model.update_spectraplot(ax, VIEW_OPTIONS)

    # label starts at the peak position
    assert _label_x(ax, "1") == pytest.approx(50.0)

    # simulate an interactive drag of the peak to x0 = 70 (no mouse release)
    bbox = model.ibounds.bboxes[0]
    bbox.dragging = "all"
    bbox.last_x = bbox.x0
    bbox.on_move(70.0)

    # param hint moved...
    assert spectrum.peak_models[0].param_hints["x0"]["value"] == pytest.approx(70.0)
    # ...and the label must have followed WITHOUT a full replot / release
    assert _label_x(ax, "1") == pytest.approx(70.0)
