"""
Example illustrating the application of a 'Fitspy' model whose peak models for
the 2nd spectrum cover areas entirely defined by noise (peaks: 1, 11, 13, 14, 15)
"""

import sys
from pathlib import Path

from fitspy.apps import init_app, end_app

DATA = Path(__file__).parent / "data"


def ex_gui_peak_models_in_noise(dirname_res=None, gui='pyside'):
    """ Example of spectra automatic decomposition through the appli """
    appli, app = init_app(gui)

    # specify the dirname and the files to work with
    dirname = DATA / 'spectra_3'
    fnames = list(dirname.glob('*.txt'))
    appli.add_items(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    appli.load_model(fname_json=dirname / 'model.json')
    appli.apply_model_to_all()

    end_app(gui, appli, app, dirname_res=dirname_res)


if __name__ == "__main__":
    ex_gui_peak_models_in_noise(gui='pyside')
    # ex_gui_peak_models_in_noise(gui='tkinter')
