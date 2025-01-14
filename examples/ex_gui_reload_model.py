"""
Example of preprocessed spectra model reloading through the application
"""
from pathlib import Path

from fitspy.apps.pyside.main import fitspy_launcher
from fitspy.apps.tkinter.gui import fitspy_launcher as fitspy_launcher_tk

DATA = Path(__file__).parent / "data"


def gui_reload_model(gui='pyside'):
    """ Example of preprocessed spectra model reloading through the appli """
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        fitspy_launcher(fname_json=DATA / 'spectra_2' / 'model.json')
    else:
        fitspy_launcher_tk(fname_json=DATA / 'spectra_2' / 'model.json')


def gui_reload_model_2d_map(gui='pyside'):
    """ Example of preprocessed '2D map' spectra model reloading through the appli """
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        fitspy_launcher(fname_json=DATA / '2D_maps' / 'model.json')
    else:
        fitspy_launcher_tk(fname_json=DATA / '2D_maps' / 'model.json')


if __name__ == "__main__":
    gui_reload_model(gui='pyside')
    # gui_reload_model(gui='tkinter')
    # gui_reload_model_2d_map(gui='pyside')
    # gui_reload_model_2d_map(gui='tkinter')
