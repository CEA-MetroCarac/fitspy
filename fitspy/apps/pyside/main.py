import sys
from PySide6.QtWidgets import QApplication

from fitspy.core import Spectra
from fitspy.core.utils import load_from_json

from .main_controller import MainController
from .main_model import MainModel
from .main_view import MainView


class Appli:

    def __init__(self):
        self.model = MainModel()
        self.view = MainView()
        self.controller = MainController(self.model, self.view)

    @property
    def fnames(self):
        return self.view.spectrum_list.list.get_all_fnames()

    def add_items(self, fnames):
        self.controller.open(fnames)

    def outliers_calculation(self):
        self.controller.outliers_calculation()

    def load_model(self, fname_json):
        self.controller.settings_controller.load_model(fname_json)

    def apply_model(self, fnames=None, ncpus=None):
        fnames = fnames or self.fnames
        if ncpus:
            self.model.ncpus = ncpus
        self.controller.files_controller.set_selection(self.view.spectrum_list.list, fnames)
        self.view.fit_model_editor.model_selector.apply.click()
        self.view.fit_model_editor.model_settings.fit.click()

    def apply_model_to_all(self, ncpus=None):
        self.apply_model(fnames=None, ncpus=ncpus)

    def auto_eval(self, model_name=None, fnames=None):
        fnames = fnames or self.fnames
        self.controller.files_controller.set_selection(self.view.spectrum_list.list, fnames)

        spectra = self.controller.plot_controller.get_spectra()
        for spectrum in spectra:
            spectrum.baseline.mode = 'Semi-Auto'
            spectrum.eval_baseline()
            spectrum.subtract_baseline()
            spectrum.auto_peaks(model_name)

        fit_status = {spectrum.fname: spectrum.result_fit for spectrum in spectra}
        self.controller.files_controller.colorize_from_fit_status(fit_status)
        self.controller.plot_controller.update_spectraplot()

    def save_results(self, dirname_res=None, fnames=None):
        self.controller.save_results(dirname_res=dirname_res, fnames=fnames)

    def save_figures(self, dirname_fig=None, fnames=None):
        self.controller.save_figures(dirname_fig=dirname_fig, fnames=fnames)

    def reload(self, fname_json):
        self.controller.files_controller.load_files(str(fname_json))


def fitspy_launcher(fname_json=None):
    qapp = QApplication(sys.argv)
    qapp.setStyle("Fusion")
    appli = Appli()

    if fname_json is not None:
        appli.reload(fname_json)

    appli.view.show()
    sys.exit(qapp.exec())


if __name__ == "__main__":
    fitspy_launcher()
