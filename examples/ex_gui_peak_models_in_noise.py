# TODO
"""
Example illustrating the application of a 'Fitspy' model whose peak models for
the 2nd spectrum cover areas entirely defined by noise (peaks: 1, 11, 13, 14,
15)
"""
import tkinter as tk
from pathlib import Path

from fitspy.app.gui import Appli
from fitspy import PEAK_MODELS, BKG_MODELS

DATA = Path(__file__).parent / "data"
DIRNAME = DATA / "spectra_3"


def ex_gui_peak_models_in_noise(dirname_res=None):
    root = tk.Tk()
    appli = Appli(root)

    fnames = [DIRNAME / "spectrum_3_1.txt", DIRNAME / "spectrum_3_2.txt"]
    fname_json = DIRNAME / "model.json"

    appli.add_items(fnames=fnames)
    appli.load_model(fname_json=fname_json)
    appli.apply_model_to_all()

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return

    root.mainloop()


if __name__ == '__main__':
    ex_gui_peak_models_in_noise()
