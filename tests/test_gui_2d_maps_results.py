"""
GUI test: exploiting the fit results of a 2D map.

'test_gui_2d_maps' and 'test_gui_users_defined_models_2d_map' already check
that a model applied to a map produces the expected values in the per-spectrum
.csv files. This test covers the two ways users actually look at these results
in the application and that are not exercised elsewhere:

  - the results table returned by Spectra.get_results(),
  - the parameter colormap displayed in the 'Measurement sites' widget
    (SpectraMap.plot_map_update with var='x0'), which stays fully NaN if the
    peak labels and the fitted models get out of sync.
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

    fnames = appli.fnames[:NSPECTRA]
    appli.apply_model(fnames=fnames, ncpus=1)

    # the results table holds one row per fitted spectrum
    dfr = appli.get_results(fnames=fnames)
    assert dfr is not None and len(dfr) == NSPECTRA
    assert dfr["success"].all()
    assert dfr["m01_x0"].values == pytest.approx(520.0, abs=1.0)

    # the map displays the fitted 'x0' of the first peak label
    spectra_map = appli.controller.plot_controller.model.spectra.spectra_maps[0]
    label = sorted({lab for spectrum in spectra_map for lab in spectrum.peak_labels})[0]
    spectra_map.plot_map(appli.view.measurement_sites.ax)
    spectra_map.plot_map_update(var="x0", label=label)
    assert np.count_nonzero(~np.isnan(spectra_map.arr)) == NSPECTRA
    assert np.nanmean(spectra_map.arr) == pytest.approx(520.0, abs=1.0)

    end_app("pyside", appli, app, dirname_res=tmp_path)
