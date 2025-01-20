"""
Example illustrating the application of a 'Fitspy' model whose peak models for
the 2nd spectrum cover areas entirely defined by noise (peaks: 1, 11, 13, 14, 15)
"""

import sys
from pathlib import Path
import tkinter as tk
try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    pass

from fitspy.apps.pyside.main import Appli
from fitspy.apps.tkinter.gui import Appli as Appli_tk

DATA = Path(__file__).parent / "data"


def ex_gui_peak_models_in_noise(dirname_res=None, gui='pyside'):
    """ Example of spectra automatic decomposition through the appli """
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        qapp = QApplication([])
        qapp.setStyle("Fusion")
        appli = Appli()
    else:
        root = tk.Tk()
        appli = Appli_tk(root)

    # specify the dirname and the files to work with
    dirname = DATA / 'spectra_3'
    fnames = list(dirname.glob('*.txt'))
    appli.add_items(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    appli.load_model(fname_json=dirname / 'model.json')
    appli.apply_model_to_all()

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        if gui == 'pyside':
            qapp.quit()
        else:
            root.destroy()
        return

    if gui == 'pyside':
        appli.view.show()
        sys.exit(qapp.exec())
    else:
        root.mainloop()


if __name__ == "__main__":
    ex_gui_peak_models_in_noise(gui='pyside')
    # ex_gui_peak_models_in_noise(gui='tkinter')
