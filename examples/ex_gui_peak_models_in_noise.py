"""
Example illustrating the application of a 'Fitspy' model whose peak models for
the 2nd spectrum cover areas entirely defined by noise (peaks: 1, 11, 13, 14,
15)
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from fitspy.app import MainController as Appli

DATA = Path(__file__).parent / "data"

def ex_gui_peak_models_in_noise(dirname_res=None):
    """ Example of spectra automatic decomposition through the appli """
    app = QApplication([])
    app.setStyle("Fusion")
    appli = Appli()

    # specify the dirname to work with
    dirname = DATA / 'spectra_3'
    fnames = [str(f) for f in dirname.glob('*.txt')]
    appli.open(fnames=fnames)

    # load model and apply it to ALL SPECTRA
    fname_json = str(dirname / 'model.json')
    appli.settings_controller.load_model(fname_json)
    appli.view.spectrum_list.sel_all.click()
    appli.view.fit_model_editor.model_selector.apply.click()
    appli.view.fit_model_editor.model_settings.fit.click()

    # save and destroy for pytest
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        app.quit()
        return

    appli.view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    ex_gui_peak_models_in_noise()