from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from .main_model import MainModel
from .main_view import MainView
from fitspy.utils import update_widget_palette

class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.view = MainView()
        self.model = MainModel()
        self.setup_connections()
        self.load_settings()
    
    def setup_connections(self):
        self.view.menuBar.actionLightMode.triggered.connect(self.on_actionLightMode_triggered)
        self.view.menuBar.actionDarkMode.triggered.connect(self.on_actionDarkMode_triggered)
        self.model.themeChanged.connect(self.on_theme_changed)

    def load_settings(self):
        self.apply_theme()

    def on_actionLightMode_triggered(self):
        print("Light mode triggered")
        self.model.theme = "light"

    def on_actionDarkMode_triggered(self):
        print("Dark mode triggered")
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