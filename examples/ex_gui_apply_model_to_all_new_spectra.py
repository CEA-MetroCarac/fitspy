"""
Example of 2D maps loading
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import Appli

DATA = Path(__file__).parent / "data"


def gui_apply_model_to_all(dirname_res=None):
    """ Example of 2D maps loading """
    qapp = QApplication([])
    qapp.setStyle("Fusion")
    appli = Appli()

    # specify the dirname and the files to work with
    dirname = DATA / 'spectra_2'
    fnames = dirname.glob('*.txt')
    appli.add_items(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    appli.load_model(fname_json=dirname / 'model.json')
    appli.apply_model()

    # # save results and figures
    # appli.save_results(dirname_res='results')
    # appli.save_figures(dirname_fig='results')

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        qapp.quit()
        return

    appli.view.show()
    sys.exit(qapp.exec())


if __name__ == "__main__":
    gui_apply_model_to_all()
