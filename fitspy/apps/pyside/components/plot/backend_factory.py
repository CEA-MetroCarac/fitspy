from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fitspy.apps.pyside.components.plot.abstractions import Map2DPlot, PlotNavigation, SpectraPlot


@dataclass(frozen=True, slots=True)
class PlotBackendComponents:
    spectra_plot: SpectraPlot
    map2d_plot: Map2DPlot
    navigation: Optional[PlotNavigation]

def create_plot_backend() -> PlotBackendComponents:
    try:
        from fitspy.apps.pyside.components.plot.map2d_plot import Map2DPlot
        from fitspy.apps.pyside.components.plot.backends.matplotlib.navigation import MatplotlibNavigation
        from fitspy.apps.pyside.components.plot.backends.matplotlib.map2d_surface import MatplotlibMap2DSurface
        from fitspy.apps.pyside.components.plot.backends.matplotlib.spectra_plot import MatplotlibSpectraPlot

        spectra_plot = MatplotlibSpectraPlot()
        map2d_surface = MatplotlibMap2DSurface()
        map2d_plot = Map2DPlot(surface=map2d_surface)

        navigation = MatplotlibNavigation(spectra_plot.canvas)
        return PlotBackendComponents(spectra_plot=spectra_plot, map2d_plot=map2d_plot, navigation=navigation)
    except Exception as e:
        raise RuntimeError(f"Plot backend initialization failed: {e}") from e
