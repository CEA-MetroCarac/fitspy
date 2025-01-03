"""
Example of 2D maps loading
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import Appli

DATA = Path(__file__).parent / "data"


def gui_2d_maps(dirname_res=None):
    """ Example of 2D maps loading """
    qapp = QApplication([])
    qapp.setStyle("Fusion")
    appli = Appli()

    # specify the dirname and the files to work with
    dirname = DATA / '2D_maps'
    ordered_map = dirname / 'ordered_map.txt'
    unordered_map = dirname / 'unordered_map.txt'
    appli.add_items(fnames=[ordered_map, unordered_map])

    # spectra from 'ordered_map.txt' and 'unordered_map.txt' differ -> DO NOT APPLY
    # appli.remove_outliers()

    # auto-evaluation on the first 5 of 1520 spectra belonging to 'ordered_map.txt'
    appli.auto_eval(model_name='LorentzianAsym', fnames=appli.fnames[:5])

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        qapp.quit()
        return

    appli.view.show()
    sys.exit(qapp.exec())


if __name__ == "__main__":
    gui_2d_maps()
