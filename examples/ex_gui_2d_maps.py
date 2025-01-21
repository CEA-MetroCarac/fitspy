"""
Example of 2D maps loading
"""
import sys
from pathlib import Path

from fitspy.apps import init_app, end_app

DATA = Path(__file__).parent / "data"


def gui_2d_maps(dirname_res=None, gui='pyside'):
    """ Example of 2D maps loading """
    appli, app = init_app(gui)

    # specify the dirname and the files to work with
    dirname = DATA / '2D_maps'
    ordered_map = dirname / 'ordered_map.txt'
    unordered_map = dirname / 'unordered_map.txt'
    appli.add_items(fnames=[ordered_map, unordered_map])

    # appli.outliers_calculation()

    # auto-evaluation on the first 5 of 1520 spectra belonging to 'ordered_map.txt'
    appli.auto_eval(model_name='LorentzianAsym', fnames=appli.fnames[:5])

    end_app(gui, appli, app, dirname_res=dirname_res)


if __name__ == "__main__":
    gui_2d_maps(gui='pyside')
    # gui_2d_maps(gui='tkinter')
