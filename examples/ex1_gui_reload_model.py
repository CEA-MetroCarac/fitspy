"""
Example of preprocessed spectra model reloading through the application
"""
import os

from fitspy.app.gui import fitspy_launcher

DATA = os.path.join('..', 'examples', 'data')


def gui_reload_model():
    """ Example of preprocessed spectra model reloading through the appli """

    fname = os.path.join(DATA, 'spectra_2', 'model.json')
    fitspy_launcher(fname_json=fname)


if __name__ == "__main__":
    gui_reload_model()
