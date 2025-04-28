import sys
from PySide6.QtWidgets import QApplication

from fitspy.apps.pyside.main_controller import MainController
from fitspy.apps.pyside.main_model import MainModel
from fitspy.apps.pyside.main_view import MainView
from fitspy.apps.pyside import DEFAULTS, DEFAULTS_INITIAL
from fitspy.apps import fitspy_launcher as fitspy_launcher_generic


class Appli:
    """Class to interact easily with the pyside app. (similarly to the tkinter app.)"""

    def __init__(self):
        self.model = MainModel()
        self.view = MainView()
        self.controller = MainController(self.model, self.view)

    @property
    def fnames(self):
        """Return the fnames related to the filenames in the selection box"""
        return self.view.spectrum_list.list.get_all_fnames()

    def add_items(self, fnames):
        """Add items from 'fnames' list"""
        self.controller.open(fnames)

    def outliers_calculation(self):
        """Function to calculate the outliers envelop
        (typically from all the spectra issued from a SpectraMap)"""
        self.controller.outliers_calculation()

    def load_model(self, fname_json):
        """Load a model from 'fname_json'"""
        self.controller.settings_controller.load_model(fname_json)

    def apply_model(self, fnames=None, ncpus=None):
        """Apply the model to a list of 'fnames' considering 'ncpu' as the number of threads
        to be used. if fnames is None, apply the model to all the spectra"""
        fnames = fnames or self.fnames
        if ncpus:
            self.model.ncpus = ncpus
        self.controller.files_controller.set_selection(
            self.view.spectrum_list.list, fnames
        )
        self.view.fit_model_editor.model_selector.set.click()
        self.view.fit_model_editor.model_settings.fit.click()

    def apply_model_to_all(self, ncpus=None):
        """Apply the model to all the spectra considering 'ncpu' as the number of threads
        to be used."""
        self.apply_model(fnames=None, ncpus=ncpus)

    def auto_eval(self, model_name=None, fnames=None):
        """Automatic peaks determination and fit evaluation applied to 'fnames' spectra
        considering each peak created from 'model_name' among ['Gaussian', 'Lorentzian', ...]
        """
        fnames = fnames or self.fnames
        self.controller.files_controller.set_selection(
            self.view.spectrum_list.list, fnames
        )

        spectra = self.controller.plot_controller.get_spectra()
        for spectrum in spectra:
            spectrum.baseline.mode = "Semi-Auto"
            spectrum.eval_baseline()
            spectrum.subtract_baseline()
            spectrum.auto_peaks(model_name)

        fit_status = {
            spectrum.fname: spectrum.result_fit for spectrum in spectra
        }
        self.controller.files_controller.colorize_from_fit_status(fit_status)
        self.controller.plot_controller.update_spectraplot()
        self.controller.update_fit_stats()

    def save_results(self, dirname_res=None, fnames=None):
        """Save spectra related to 'fnames' into 'dirname_res'"""
        self.controller.save_results(dirname_res=dirname_res, fnames=fnames)

    def save_figures(self, dirname_fig=None, fnames=None):
        """Save figures related to 'fnames' into 'dirname_res'"""
        self.controller.save_figures(dirname_fig=dirname_fig, fnames=fnames)

    def reinit_spectra(self, fnames=None):
        """Reinitialize the spectra"""
        fnames = fnames or self.fnames
        self.controller.files_controller.reinitSpectra.emit(fnames)

    def reload(self, fname_json):
        """Reload spectra as previously saved in the 'fname_json' file"""
        self.controller.files_controller.load_files(str(fname_json))


def init_app():
    """Return an Appli and QApplication instances"""
    if not QApplication.instance():
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()
        DEFAULTS.clear()
        DEFAULTS.update(DEFAULTS_INITIAL)
    qapp.setStyle("Fusion")
    appli = Appli()
    return appli, qapp


def end_app(appli, qapp, dirname_res=None):
    """Quit properly the appli after saving the results if 'dirname_res' is given (for pytest)"""
    if dirname_res is not None:
        appli.save_results(dirname_res=dirname_res)
        qapp.quit()
    else:
        appli.view.show()
        sys.exit(qapp.exec())


def fitspy_launcher(fname_json=None):
    """Launch the Pyside appli"""
    fitspy_launcher_generic(fname_json=fname_json, gui="pyside")


if __name__ == "__main__":
    fitspy_launcher()
