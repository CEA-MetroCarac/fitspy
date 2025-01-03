"""
Example illustrating the application of a 'Fitspy' model whose peak models for
the 2nd spectrum cover areas entirely defined by noise (peaks: 1, 11, 13, 14, 15)
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import Appli

DATA = Path(__file__).parent / "data"


def ex_gui_peak_models_in_noise(dirname_res=None):
    """ Example of spectra automatic decomposition through the appli """
    qapp = QApplication([])
    qapp.setStyle("Fusion")
    appli = Appli()

    # specify the dirname and the files to work with
    dirname = DATA / 'spectra_3'
    fnames = dirname.glob('*.txt')
    appli.add_items(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    appli.load_model(fname_json=dirname / 'model.json')
    appli.apply_model()

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        qapp.quit()
        return

    appli.view.show()
    sys.exit(qapp.exec())


if __name__ == "__main__":
    ex_gui_peak_models_in_noise()
