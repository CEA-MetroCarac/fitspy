"""
Regression tests for issue #74:
'Preserve or Adapt Peak Parameter Settings When Changing Model in Peaks Table'.

Switching a peak's model must carry the fwhm configuration across models:
  - Gaussian (fwhm)  -> GaussianAsym (fwhm_l, fwhm_r): copy value + bounds.
  - GaussianAsym     -> Gaussian    (fwhm):            collapse to the mean.
Shared-name parameters (x0, ampli) must keep persisting as before.
"""
import pytest
import matplotlib

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from fitspy.apps.pyside.components.settings.peaks_table import PeaksTable
from fitspy.apps.pyside import DEFAULTS


def _qapp():
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def _add_row(table, model_name, **overrides):
    params = dict(
        prefix="1", label="peak1", model_name=model_name,
        x0=10, x0_min=0, x0_max=20,
        ampli=5, ampli_min=0, ampli_max=10,
    )
    params.update(overrides)
    table.add_row(show_bounds=True, show_expr=False, **params)


def _param_values(table, row, param_name):
    col = table.table.get_column_index(f"MIN | {param_name} | MAX")
    return table.table.cellWidget(row, col).get_values()


def _set_model(table, row, model_name):
    combo = table.table.cellWidget(row, table.table.get_column_index("Model"))
    combo.setCurrentText(model_name)


def test_fwhm_copies_to_asym_on_model_switch(monkeypatch):
    monkeypatch.setitem(DEFAULTS, "peaks_cmap", matplotlib.colormaps["tab10"])
    _qapp()
    table = PeaksTable()
    _add_row(table, "Gaussian", fwhm=3, fwhm_min=0.5, fwhm_max=8)

    _set_model(table, 0, "GaussianAsym")

    for param in ("fwhm_l", "fwhm_r"):
        vals = _param_values(table, 0, param)
        assert vals["value"] == 3
        assert vals["min"] == 0.5
        assert vals["max"] == 8


def test_asym_fwhm_collapses_to_mean_on_model_switch(monkeypatch):
    monkeypatch.setitem(DEFAULTS, "peaks_cmap", matplotlib.colormaps["tab10"])
    _qapp()
    table = PeaksTable()
    _add_row(table, "GaussianAsym",
             fwhm_l=2, fwhm_l_min=0, fwhm_l_max=6,
             fwhm_r=4, fwhm_r_min=0, fwhm_r_max=10)

    _set_model(table, 0, "Gaussian")

    vals = _param_values(table, 0, "fwhm")
    assert vals["value"] == 3   # mean(2, 4)
    assert vals["min"] == 0     # mean(0, 0)
    assert vals["max"] == 8     # mean(6, 10)


def test_shared_params_persist_across_switch(monkeypatch):
    monkeypatch.setitem(DEFAULTS, "peaks_cmap", matplotlib.colormaps["tab10"])
    _qapp()
    table = PeaksTable()
    _add_row(table, "Gaussian", fwhm=3, fwhm_min=0.5, fwhm_max=8)

    _set_model(table, 0, "GaussianAsym")

    x0 = _param_values(table, 0, "x0")
    ampli = _param_values(table, 0, "ampli")
    assert x0["value"] == 10
    assert ampli["value"] == 5
