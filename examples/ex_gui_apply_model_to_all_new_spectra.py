# TODO SAVE FIGURES MISSING
"""
Example of 2D maps loading
"""
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import MainController, MainModel, MainView

DATA = Path(__file__).parent / "data"

def gui_apply_model_to_all(dirname_res=None):
    """ Example of 2D maps loading """
    app = QApplication([])
    app.setStyle("Fusion")
    model = MainModel()
    view = MainView()
    main_controller = MainController(model, view)

    # specify the dirname to work with
    dirname = str(DATA / 'spectra_2')
    fnames = [str(f) for f in Path(dirname).rglob('*.txt')]
    main_controller.open(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    fname_json = str(DATA / 'spectra_2' / 'model.json')
    main_controller.settings_controller.load_model(fname_json)
    view.spectrum_list.sel_all.click()
    view.fit_model_editor.model_selector.apply.click()
    # view.fit_model_editor.model_settings.fit.click()

    # # save results and figures
    # list_widget = view.spectrum_list.list
    # fnames = [list_widget.item(i).text() for i in range(list_widget.count())]
    # results_dir = 'results'
    # if not os.path.exists(results_dir):
    #     os.makedirs(results_dir)

    # main_controller.save_results(dirname_res=results_dir, fnames=fnames)
    # main_controller.save_figures(dirname_fig='results')

    # save and destroy for pytest
    if dirname_res is not None:
        main_controller.save_results(dirname_res=dirname_res, fnames=fnames)
        return

    main_controller.view.show()
    app.exec()


if __name__ == "__main__":
    gui_apply_model_to_all()