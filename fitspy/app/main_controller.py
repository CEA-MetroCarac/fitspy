from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
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
        self.plot_controller = PlotController(self.view.measurement_sites)
        self.settings_controller = SettingsController(self.view.fit_model_editor)
        self.setup_connections()
        self.load_settings()

    def setup_connections(self):
        self.view.menuBar.actionLightMode.triggered.connect(self.on_actionLightMode_triggered)
        self.view.menuBar.actionDarkMode.triggered.connect(self.on_actionDarkMode_triggered)
        self.model.themeChanged.connect(self.on_theme_changed)

        self.files_controller.spectraMapInit.connect(self.plot_controller.create_map)
        self.files_controller.mapChanged.connect(self.plot_controller.switch_map)
        self.plot_controller.decodedSpectraMap.connect(self.files_controller.update_spectramap)  # could be simplified : self.files_controller.model.update_spectramap

    def load_settings(self):
        self.apply_theme()

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