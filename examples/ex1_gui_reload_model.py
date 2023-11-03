"""
Example of preprocessed spectra model reloading through the application
"""
import os
from pathlib import Path

from fitspy.app.gui import fitspy_launcher

DATA = Path(__file__).parent / "data"


def gui_reload_model():
    """ Example of preprocessed spectra model reloading through the appli """

    fname = os.path.join(DATA, 'spectra_2', 'model.json')
    fitspy_launcher(fname_json=fname)


if __name__ == "__main__":
    gui_reload_model()
