"""
Example of spectra processing using users-defined model through the application
"""
import tkinter as tk
from pathlib import Path

from fitspy.app.gui import Appli
from fitspy.utils import load_models_from_txt, load_models_from_py
from fitspy import MODELS, BKG_MODELS

DATA = Path(__file__).parent / "data"
DIRNAME = DATA / "2D_maps"


def ex_gui_users_models_from_txt(ncpus=1, dirname_res=None):
    """ Example using users models defined from literal expression in a .txt """
    load_models_from_txt(DIRNAME / "models.txt", MODELS)
    load_models_from_txt(DIRNAME / "bkg_models.txt", BKG_MODELS)
    ex_gui_users_models(ncpus=ncpus, dirname_res=dirname_res)


def ex_gui_users_models_from_py(ncpus=1, dirname_res=None):
    """ Example using users models defined from functions in a .py """
    load_models_from_py(DIRNAME / "models.py")
    load_models_from_py(DIRNAME / "bkg_models.py")
    ex_gui_users_models(ncpus=ncpus, dirname_res=dirname_res)


def ex_gui_users_models(ncpus=1, dirname_res=None):
    """ Application of the users-defined models to a 2D-map """
    fname_json = DIRNAME / "model.json"

    root = tk.Tk()
    appli = Appli(root)

    appli.ncpus = ncpus
    appli.add_items(fnames=[DIRNAME / 'ordered_map.txt'])
    appli.load_model(fname_json=fname_json)
    appli.apply_model(fnames=appli.spectra.fnames[:5])

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return

    root.mainloop()


if __name__ == '__main__':
    # ex_gui_users_models_from_txt()
    ex_gui_users_models_from_py()