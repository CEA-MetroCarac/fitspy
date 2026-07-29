"""
GUI test: exploiting the fit results of a 2D map.

'test_gui_2d_maps' and 'test_gui_users_defined_models_2d_map' already check
that a model applied to a map produces the expected values in the per-spectrum
.csv files. This test covers the two ways users actually look at these results
in the application and that are not exercised elsewhere:

  - the results table returned by Spectra.get_results(),
  - the parameter colormap of the 'Measurement sites' widget. Selecting the
    'x0' tab before fitting used to leave its peak-label combo empty, and
    nothing refreshed the map once the fit was done: the map stayed blank
    until the user switched tabs back and forth.
"""
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("PySide6.QtWidgets")

from fitspy.apps import init_app, end_app

from utils import display_is_ok

DIRNAME = Path(__file__).resolve().parent.parent / "examples" / "data" / "2D_maps"
NSPECTRA = 5


@pytest.mark.skipif(not display_is_ok(), reason="DISPLAY problem")
def test_gui_2d_maps_results_exploitation(tmp_path):
    appli, app = init_app("pyside")
    appli.add_items(fnames=[DIRNAME / "ordered_map.txt"])
    appli.load_model(fname_json=DIRNAME / "model.json")

    # the user undocks the map widget and selects the 'x0' tab before fitting
    sites = appli.view.measurement_sites
    sites.dock_widget.setFloating(True)
    tabs = [sites.tab_widget.tabText(i) for i in range(sites.tab_widget.count())]
    sites.tab_widget.setCurrentIndex(tabs.index("x0"))
    app.processEvents()

    fnames = appli.fnames[:NSPECTRA]
    appli.apply_model(fnames=fnames, ncpus=1)
    app.processEvents()

    # the results table holds one row per fitted spectrum
    dfr = appli.get_results(fnames=fnames)
    assert dfr is not None and len(dfr) == NSPECTRA
    assert dfr["success"].all()
    assert dfr["m01_x0"].values == pytest.approx(520.0, abs=1.0)

    # the peak labels are proposed and the map displays the fitted 'x0',
    # without the user having to touch the widget again
    combo = sites.tab_widget.currentWidget().combo
    assert [combo.itemText(i) for i in range(combo.count())] == ["1", "2", "3", "4", "5"]

    spectra_map = appli.controller.plot_controller.model.spectra.spectra_maps[0]
    assert np.count_nonzero(~np.isnan(spectra_map.arr)) == NSPECTRA
    assert np.nanmean(spectra_map.arr) == pytest.approx(520.0, abs=1.0)

    end_app("pyside", appli, app, dirname_res=tmp_path)
