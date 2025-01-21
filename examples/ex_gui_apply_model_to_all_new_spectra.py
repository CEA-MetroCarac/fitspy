"""
Example of 2D maps loading
"""
import sys
from pathlib import Path

from fitspy.apps import init_app, end_app

DATA = Path(__file__).parent / "data"


def gui_apply_model_to_all(dirname_res=None, gui='pyside'):
    """ Example of 2D maps loading """
    appli, app = init_app(gui)

    # specify the dirname and the files to work with
    dirname = DATA / 'spectra_2'
    fnames = list(dirname.glob('*.txt'))
    appli.add_items(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    appli.load_model(fname_json=dirname / 'model.json')
    appli.apply_model_to_all()

    # # save results and figures
    # appli.save_results(dirname_res='results')
    # appli.save_figures(dirname_fig='results')

    end_app(gui, appli, app, dirname_res=dirname_res)


if __name__ == "__main__":
    gui_apply_model_to_all(gui='pyside')
    # gui_apply_model_to_all(gui='tkinter')
