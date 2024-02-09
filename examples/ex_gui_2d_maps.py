"""
Example of 2D maps loading
"""
import os
import tkinter as tk
from pathlib import Path

from fitspy.app.gui import Appli

DATA = Path(__file__).parent / "data"


def gui_2d_maps(dirname_res=None):
    """ Example of 2D maps loading """
    root = tk.Tk()
    appli = Appli(root)

    # specify the dirname to work with
    str_map = os.path.join(DATA, '2D_maps', 'ordered_map.txt')
    unstr_map = os.path.join(DATA, '2D_maps', 'unordered_map.txt')
    appli.add_items(fnames=[str_map, unstr_map])

    # appli.outliers_calculation() # spectra from the maps differ: DO NOT APPLY

    # automatic evaluation on the first 5 spectra
    appli.auto_eval(fnames=appli.spectra.fnames[:5])
    # appli.auto_eval_all() # 1520+2700 = 4220 spectra to handle (could be long)

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        root.destroy()
        return

    root.mainloop()


if __name__ == "__main__":
    gui_2d_maps()
