"""
Example of spectra processing using users-defined model through the application
"""
import sys
from pathlib import Path

from fitspy.apps import init_app, end_app
from fitspy.core.utils import load_models_from_txt, load_models_from_py
from fitspy import PEAK_MODELS, BKG_MODELS

DATA = Path(__file__).parent / "data"
DIRNAME = DATA / "2D_maps"


def ex_gui_users_models_from_txt(ncpus=1, dirname_res=None, gui='pyside'):
    """ Example using users models defined from literal expression in a .txt """
    load_models_from_txt(DIRNAME / "peak_models.txt", PEAK_MODELS)
    load_models_from_txt(DIRNAME / "bkg_models.txt", BKG_MODELS)
    ex_gui_users_models(ncpus=ncpus, dirname_res=dirname_res, gui=gui)


def ex_gui_users_models_from_py(ncpus=1, dirname_res=None, gui='pyside'):
    """ Example using users models defined from functions in a .py """
    load_models_from_py(DIRNAME / "peak_models.py")
    load_models_from_py(DIRNAME / "bkg_models.py")
    ex_gui_users_models(ncpus=ncpus, dirname_res=dirname_res, gui=gui)


def ex_gui_users_models(ncpus=1, dirname_res=None, gui='pyside'):
    """ Application of the users-defined models to a 2D-map """
    appli, app = init_app(gui)

    # appli.model.ncpus = ncpus
    appli.add_items(fnames=[DIRNAME / 'ordered_map.txt'])

    appli.outliers_calculation()

    # fname_json = DIRNAME / "model.json"
    # appli.load_model(fname_json)
    appli.load_model(fname_json=DIRNAME / "model_user.json")
    appli.apply_model(fnames=appli.fnames[:5], ncpus=ncpus)

    end_app(gui, appli, app, dirname_res=dirname_res)


if __name__ == "__main__":
    ex_gui_users_models_from_py(ncpus=1, gui='pyside')
    # ex_gui_users_models_from_py(ncpus=1, gui='tkinter')
