"""
Example of preprocessed spectra model reloading through the application
"""
from pathlib import Path

from fitspy.apps import fitspy_launcher, init_app, end_app

DATA = Path(__file__).parent / "data"


def gui_reload_model(gui='pyside'):
    """ Example of preprocessed spectra model reloading through the appli """

    fitspy_launcher(fname_json=DATA / 'spectra_2' / 'model.json', gui=gui)


def gui_reload_model_2d_map(gui='pyside'):
    """ Example of preprocessed '2D map' spectra model reloading through the appli """

    fitspy_launcher(fname_json=DATA / '2D_maps' / 'model.json', gui=gui)


def gui_reload_model_with_data(dirname_res=None, gui='pyside'):
    """ Example of preprocessed spectra model + data reloading through the appli """

    # fitspy_launcher(fname_json=DATA / 'spectra_2' / 'model_data.json', gui=gui)

    # -> to be able to save results in dirname_res for pytest
    appli, app = init_app(gui)
    appli.reload(fname_json=DATA / 'spectra_2' / 'model_data.json')
    end_app(gui, appli, app, dirname_res=dirname_res)


if __name__ == "__main__":
    gui_reload_model(gui='pyside')
    # gui_reload_model(gui='tkinter')
    # gui_reload_model_2d_map(gui='pyside')
    # gui_reload_model_2d_map(gui='tkinter')
    # gui_reload_model_with_data(gui='pyside')
    # gui_reload_model_with_data(gui='tkinter')
