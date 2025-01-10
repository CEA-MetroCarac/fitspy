"""
Example of 2D maps loading
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
import tkinter as tk

from fitspy.apps.pyside.main import Appli
from fitspy.apps.tkinter.gui import Appli as Appli_tk

DATA = Path(__file__).parent / "data"


def gui_2d_maps(dirname_res=None, gui='pyside'):
    """ Example of 2D maps loading """
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        qapp = QApplication([])
        qapp.setStyle("Fusion")
        appli = Appli()
    else:
        root = tk.Tk()
        appli = Appli_tk(root)

    # specify the dirname and the files to work with
    dirname = DATA / '2D_maps'
    ordered_map = dirname / 'ordered_map.txt'
    unordered_map = dirname / 'unordered_map.txt'
    appli.add_items(fnames=[ordered_map, unordered_map])

    # spectra from 'ordered_map.txt' and 'unordered_map.txt' differ -> DO NOT APPLY
    # appli.outliers_calculation()

    # auto-evaluation on the first 5 of 1520 spectra belonging to 'ordered_map.txt'
    appli.auto_eval(model_name='LorentzianAsym', fnames=appli.spectra.fnames[:5])

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
    gui_2d_maps(gui='pyside')
    # gui_2d_maps(gui='tkinter')
