from PySide6.QtCore import QObject, Signal, Qt, QSettings
from PySide6.QtGui import QColor, QPalette
from fitspy import DEFAULTS

class MainModel(QObject):
    themeChanged = Signal()
    defaultsRestored = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("CEA-MetroCarac", "Fitspy")  # these are stored in registry
        self._theme = self.settings.value("theme", DEFAULTS["theme"])
        self._ncpus = self.settings.value("ncpus", DEFAULTS["ncpus"])
        self._outliers_coef = self.settings.value("outliers_coef", DEFAULTS["outliers_coef"], type=float)
        self._save_only_path = self.settings.value("save_only_path", DEFAULTS["save_only_path"], type=bool)

    def update_setting(self, label, state):
        self.settings.setValue(label, state)

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if value in ["light", "dark"] and value != self._theme:
            self._theme = value
            self.settings.setValue("theme", value)
            self.themeChanged.emit()

    @property
    def ncpus(self):
        return self._ncpus

    @ncpus.setter
    def ncpus(self, value):
        if value == "Auto" or value.isdigit():
            if value != self._ncpus:
                self._ncpus = value
                self.settings.setValue("ncpus", value)
        else:
            raise ValueError("ncpus must be 'Auto' or a string representing a positive integer")
        
    @property
    def outliers_coef(self):
        return self._outliers_coef
    
    @outliers_coef.setter
    def outliers_coef(self, value):
        if value > 0:
            if value != self._outliers_coef:
                self._outliers_coef = value
                self.settings.setValue("outliers_coef", value)
        else:
            raise ValueError("outliers_coef must be a positive float")
        
    @property
    def save_only_path(self):
        return self._save_only_path
    
    @save_only_path.setter
    def save_only_path(self, value):
        if value != self._save_only_path:
            self._save_only_path = value
            self.settings.setValue("save_only_path", value)

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
        self._theme = DEFAULTS["theme"]
        self.ncpus = DEFAULTS["ncpus"]
        self.outliers_coef = DEFAULTS["outliers_coef"]
        self.save_only_path = DEFAULTS["save_only_path"]
        self.defaultsRestored.emit()