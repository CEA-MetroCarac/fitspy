from PySide6.QtCore import QObject, Signal, Qt, QSettings
from PySide6.QtGui import QColor, QPalette
from fitspy import DEFAULTS

class MainModel(QObject):
    themeChanged = Signal()
    defaultsRestored = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("CEA-MetroCarac", "Fitspy")  # these are stored in registry
        
        def create_setting(default, type, signal=None):
            return {"value": None, "default": default, "type": type, "signal": signal}

        self._settings = {
            "theme": create_setting(DEFAULTS["theme"], str, self.themeChanged),
            "ncpus": create_setting(DEFAULTS["ncpus"], str),
            "outliers_coef": create_setting(DEFAULTS["outliers_coef"], float),
            "save_only_path": create_setting(DEFAULTS["save_only_path"], bool),
            "click_mode": create_setting(DEFAULTS["click_mode"], str),
            "baseline": create_setting(DEFAULTS["view_options"]["baseline"], bool),
            "negative_values": create_setting(DEFAULTS["view_options"]["negative_values"], bool),
            "outliers": create_setting(DEFAULTS["view_options"]["outliers"], bool),
            "outliers_limits": create_setting(DEFAULTS["view_options"]["outliers_limits"], bool),
            "noise_level": create_setting(DEFAULTS["view_options"]["noise_level"], bool),
            "subtract_baseline": create_setting(DEFAULTS["view_options"]["subtract_baseline"], bool),
            "background": create_setting(DEFAULTS["view_options"]["background"], bool),
            "residual": create_setting(DEFAULTS["view_options"]["residual"], bool),
            "peaks": create_setting(DEFAULTS["view_options"]["peaks"], bool),
        }
        
        for key, setting in self._settings.items():
            setting["value"] = self.settings.value(key, setting["default"], type=setting["type"])

    def update_setting(self, label, state):
        if label in self._settings:
            self._settings[label]["value"] = state
            self.settings.setValue(label, state)
            if self._settings[label]["signal"]:
                self._settings[label]["signal"].emit()

    def __getattr__(self, name):
        if name in self._settings:
            return self._settings[name]["value"]
        raise AttributeError(f"'MainModel' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ["_settings", "settings", "themeChanged", "defaultsRestored"]:
            super().__setattr__(name, value)
        elif name in self._settings:
            self.update_setting(name, value)
        else:
            super().__setattr__(name, value)

    def dark_palette(self):
        """Palette color for dark mode of the appli's GUI"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(70, 70, 70))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(65, 65, 65))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(64, 64, 64))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.PlaceholderText, QColor(140, 140, 140))
        return dark_palette

    def light_palette(self):
        """Palette color for light mode of the appli's GUI"""
        light_palette = QPalette()
        light_palette.setColor(QPalette.Window, QColor(225, 225, 225))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(QPalette.Base, QColor(215, 215, 215))
        light_palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
        light_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Button, QColor(230, 230, 230))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(QPalette.BrightText, Qt.red)
        light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, Qt.black)
        light_palette.setColor(QPalette.PlaceholderText, QColor(150, 150, 150))
        return light_palette
    
    def restore_defaults(self):
        self.settings.clear()
        for key, setting in self._settings.items():
            self.update_setting(key, setting["default"])
        self.defaultsRestored.emit()