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


def gui_apply_model_to_all(dirname_res=None, gui='pyside'):
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
    dirname = DATA / 'spectra_2'
    fnames = list(dirname.glob('*.txt'))
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
    gui_apply_model_to_all(gui='pyside')
    # gui_apply_model_to_all(gui='tkinter')
