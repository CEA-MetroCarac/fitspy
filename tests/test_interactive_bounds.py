import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

import numpy as np

from fitspy.apps.interactive_bounds import InteractiveBounds
from fitspy.core.spectrum import Spectrum


def test_interactive_bounds_updates_colors_when_cmap_changes():
    spectrum = Spectrum()
    spectrum.x = np.arange(0.0, 100.0)
    spectrum.y = np.ones_like(spectrum.x)
    spectrum.x0 = spectrum.x.copy()
    spectrum.y0 = spectrum.y.copy()
    spectrum.add_peak_model("Gaussian", x0=50)

    fig, ax = plt.subplots()
    try:
        bounds = InteractiveBounds(spectrum, ax, cmap=matplotlib.colormaps["tab10"])
        bounds.update()
        initial_color = to_hex(bounds.bboxes[0].line.get_color())

        bounds.set_cmap(matplotlib.colormaps["Dark2"])
        bounds.update()
        updated_color = to_hex(bounds.bboxes[0].line.get_color())

        assert updated_color != initial_color
    finally:
        plt.close(fig)