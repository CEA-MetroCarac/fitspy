from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QCheckBox
from .main_model import MainModel
from .main_view import MainView
from fitspy.core import update_widget_palette

from .components.plot import PlotController
from .components.files import FilesController
from .components.settings import SettingsController

class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.view = MainView()
        self.model = MainModel()
        self.files_controller = FilesController(self.view.spectrum_list, self.view.maps_list)
        self.plot_controller = PlotController(self.view.measurement_sites, self.view.view_options)
        self.settings_controller = SettingsController(self.view.fit_model_editor, self.view.more_settings.fit_settings)
        self.setup_connections()
        self.apply_settings()

    def setup_connections(self):
        self.view.menuBar.actionRestoreDefaults.triggered.connect(self.model.restore_defaults)
        self.view.menuBar.actionLightMode.triggered.connect(self.on_actionLightMode_triggered)
        self.view.menuBar.actionDarkMode.triggered.connect(self.on_actionDarkMode_triggered)
        self.view.statusBar.ncpus.currentTextChanged.connect(self.set_ncpus)
        self.model.themeChanged.connect(self.on_theme_changed)
        self.model.defaultsRestored.connect(self.apply_settings)

        self.files_controller.loadSpectrum.connect(self.plot_controller.load_spectrum)
        self.files_controller.loadSpectraMap.connect(self.plot_controller.load_map)
        self.files_controller.delSpectrum.connect(self.plot_controller.del_spectrum)
        self.files_controller.delSpectraMap.connect(self.plot_controller.del_map)
        self.files_controller.spectraPlotChanged.connect(self.plot_controller.update_spectraplot)
        self.files_controller.mapChanged.connect(self.plot_controller.switch_map)
        self.files_controller.currentModelChanged.connect(self.change_current_fit_model)

        self.plot_controller.spectrumLoaded.connect(self.files_controller.add_spectrum)
        self.plot_controller.spectrumDeleted.connect(self.files_controller.del_spectrum)
        self.plot_controller.spectraMapDeleted.connect(self.files_controller.del_map)
        self.plot_controller.decodedSpectraMap.connect(self.files_controller.update_spectramap)  # could be simplified : self.files_controller.model.update_spectramap
        self.plot_controller.settingChanged.connect(self.model.update_setting)

    def apply_settings(self):
        self.apply_theme()
        self.view.statusBar.ncpus.setCurrentText(self.model.ncpus)

        for checkbox in self.view.view_options.findChildren(QCheckBox):
            label = checkbox.text()
            state = self.model.settings.value(label, False, type=bool)
            checkbox.setChecked(state)

    def on_actionLightMode_triggered(self):
        self.model.theme = "light"

    def on_actionDarkMode_triggered(self):
        self.model.theme = "dark"

    def apply_theme(self):
        app = QApplication.instance()
        if self.model.theme == "dark":
            palette = self.model.dark_palette()
        else:
            palette = self.model.light_palette()

        app.setPalette(palette)
        update_widget_palette(self.view, palette)

    def on_theme_changed(self):
        self.apply_theme()

    def set_ncpus(self, ncpus):
        self.model.ncpus = ncpus

    def change_current_fit_model(self, fnames):
        if fnames:
            spectrum = self.plot_controller.get_spectrum(fnames[0])
            self.settings_controller.set_model(spectrum)