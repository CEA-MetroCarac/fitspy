# DONE
"""
Example of 2D maps loading
"""
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import MainController as Appli

DATA = Path(__file__).parent / "data"

def gui_2d_maps(dirname_res=None):
    """ Example of 2D maps loading """
    app = QApplication([])
    app.setStyle("Fusion")
    appli = Appli()

    # specify the dirname to work with
    str_map = str(DATA / '2D_maps' / 'ordered_map.txt')
    unstr_map = str(DATA / '2D_maps' / 'unordered_map.txt')
    appli.open(fnames=[str_map, unstr_map])

    # main_controller.remove_outliers() # spectra from the maps differ: DO NOT APPLY

    # automatic evaluation on the first 5 spectra

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        return

    appli.view.show()
    app.exec()


if __name__ == "__main__":
    gui_2d_maps(r"H:\Documents\fitspy\results")