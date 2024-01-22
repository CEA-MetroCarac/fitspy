"""
Example of spectra fitting through the GUI and a model applied to all
"""
import os
import tkinter as tk
from pathlib import Path

from fitspy.app.gui import Appli

DATA = Path(__file__).parent / "data"


def gui_apply_model_to_all(dirname_res=None):
    """Example of spectra fitting and model applied to all through the appli """
    root = tk.Tk()
    appli = Appli(root)

    # specify the dirname to work with
    dirname = os.path.join(DATA, 'spectra_2')
    appli.add_items_from_dir(dirname=dirname)

    # load model and apply it to ALL SPECTRA
    fname_json = os.path.join(dirname, 'model.json')
    appli.load_model(fname_json=fname_json)
    appli.apply_model()

    # canvas rescaling
    appli.rescale()

    # save results and figures
    # appli.save_results(dirname_res='results')
    # appli.save_figures(dirname_fig='results')

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    gui_apply_model_to_all()
