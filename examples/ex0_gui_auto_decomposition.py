"""
Example of spectra automatic decomposition through the application
"""
import os
import tkinter as tk
from pathlib import Path

from fitspy.app.gui import Appli

DATA = Path(__file__).parent / "data"


def gui_auto_decomposition(dirname_res=None):
    """ Example of spectra automatic decomposition through the appli """

    root = tk.Tk()
    appli = Appli(root)

    # specify the dirname to work with
    dirname = os.path.join(DATA, 'spectra_1')
    appli.add_items_from_dir(dirname=dirname)

    # all spectra automatic processing (baseline and peaks evaluation + fitting)
    appli.auto_eval_all()

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    gui_auto_decomposition()
