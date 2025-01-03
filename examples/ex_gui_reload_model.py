"""
Example of preprocessed spectra model reloading through the application
"""
from pathlib import Path

from fitspy.app.main import fitspy_launcher

DATA = Path(__file__).parent / "data"


def gui_reload_model():
    """ Example of preprocessed spectra model reloading through the appli """

    fitspy_launcher(fname_json=DATA / 'spectra_2' / 'model.json')


def gui_reload_model_2d_map():
    """ Example of preprocessed '2D map' spectra model reloading through the appli """

    fitspy_launcher(fname_json=DATA / '2D_maps' / 'model.json')


if __name__ == "__main__":
    # gui_reload_model()
    gui_reload_model_2d_map()
