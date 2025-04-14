from PySide6.QtCore import QObject, Signal, Qt, QSettings
from PySide6.QtGui import QColor, QPalette

from fitspy.apps.pyside import DEFAULTS, SETTINGS_KEY_MIGRATIONS, SETTINGS_VALUE_MIGRATIONS
from fitspy import VERSION


class MainModel(QObject):
    themeChanged = Signal()
    peaksCmapChanged = Signal()
    mapCmapChanged = Signal()
    defaultsRestored = Signal()

    def __init__(self):
        super().__init__()
        self.settings = QSettings("CEA-MetroCarac", "Fitspy")  # these are stored in registry
        self._settings = {}
        self._migrate_settings()
        self._initialize_settings()

    def _migrate_settings(self):
        """Check if stored version matches current version and migrate settings if needed"""
        stored_version = self.settings.value("version", None)
        if stored_version != VERSION:
            print(f"Version changed from {stored_version} to {VERSION}, updating settings...")

            self._migrate_setting_keys()
            self._migrate_setting_values()

            self.settings.setValue("version", VERSION)
            self.settings.sync()

    def _migrate_setting_keys(self):
        """Migrate old setting keys to new keys"""
        for new_key, old_keys in SETTINGS_KEY_MIGRATIONS.items():
            for old_key in old_keys:
                if self.settings.contains(old_key):
                    value = self.settings.value(old_key)
                    self.settings.setValue(new_key, value)
                    self.settings.remove(old_key)

    def _migrate_setting_values(self):
        """Migrate values for existing settings"""
        for key, value_map in SETTINGS_VALUE_MIGRATIONS.items():
            if self.settings.contains(key):
                current_value = self.settings.value(key)
                if current_value in value_map:
                    new_value = value_map[current_value]
                    print(f"Migrating setting {key} from '{current_value}' to '{new_value}'")
                    self.settings.setValue(key, new_value)

    def _initialize_settings(self):
        """Initialize settings from DEFAULTS and QSettings."""
        signal_map = {
            "theme": self.themeChanged,
            "peaks_cmap": self.peaksCmapChanged,
            "map_cmap": self.mapCmapChanged,
        }

        def create_setting(default, type, signal=None):
            return {
                "value": None,
                "default": default,
                "type": type,
                "signal": signal,
            }

        # Dynamically generate settings from DEFAULTS
        for key, default in DEFAULTS.items():
            if isinstance(default, dict):
                for sub_key, sub_default in default.items():
                    full_key = f"{key}_{sub_key}"
                    signal = signal_map.get(full_key)
                    self._settings[full_key] = create_setting(sub_default,
                                                              type(sub_default), signal)
            else:
                signal = signal_map.get(key)
                self._settings[key] = create_setting(default, type(default), signal)

        # Set initial values from QSettings
        for key, setting in self._settings.items():
            setting["value"] = self.settings.value(key, setting["default"], type=setting["type"])

    def update_setting(self, label, state):
        """Update a setting and emit its signal if applicable."""
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
        if name in [
            "_settings",
            "settings",
            "themeChanged",
            "defaultsRestored",
        ]:
            super().__setattr__(name, value)
        elif name in self._settings:
            self.update_setting(name, value)
        else:
            super().__setattr__(name, value)

    def _set_palette_colors(self, palette, colors):
        for role, color in colors.items():
            if isinstance(color, Qt.GlobalColor):
                color = QColor(color)
            palette.setColor(role, color)
            palette.setColor(QPalette.Disabled, role, color.darker(150))

    def dark_palette(self):
        """Palette color for dark mode of the app's GUI"""
        dark_palette = QPalette()
        colors = {
            QPalette.Window: QColor(70, 70, 70),
            QPalette.WindowText: Qt.white,
            QPalette.Base: QColor(65, 65, 65),
            QPalette.AlternateBase: QColor(45, 45, 45),
            QPalette.ToolTipBase: QColor(53, 53, 53),
            QPalette.ToolTipText: Qt.white,
            QPalette.Text: Qt.white,
            QPalette.Button: QColor(64, 64, 64),
            QPalette.ButtonText: Qt.white,
            QPalette.BrightText: Qt.red,
            QPalette.Link: QColor(42, 130, 218),
            QPalette.Highlight: QColor(42, 130, 218),
            QPalette.HighlightedText: Qt.white,
            QPalette.PlaceholderText: QColor(140, 140, 140),
        }
        self._set_palette_colors(dark_palette, colors)
        return dark_palette

    def light_palette(self):
        """Palette color for light mode of the app's GUI"""
        light_palette = QPalette()
        colors = {
            QPalette.Window: QColor(225, 225, 225),
            QPalette.WindowText: Qt.black,
            QPalette.Base: QColor(215, 215, 215),
            QPalette.AlternateBase: QColor(230, 230, 230),
            QPalette.ToolTipBase: QColor(255, 255, 255),
            QPalette.ToolTipText: Qt.black,
            QPalette.Text: Qt.black,
            QPalette.Button: QColor(230, 230, 230),
            QPalette.ButtonText: Qt.black,
            QPalette.BrightText: Qt.red,
            QPalette.Link: QColor(42, 130, 218),
            QPalette.Highlight: QColor(42, 130, 218),
            QPalette.HighlightedText: Qt.black,
            QPalette.PlaceholderText: QColor(150, 150, 150),
        }
        self._set_palette_colors(light_palette, colors)
        return light_palette

    def restore_defaults(self):
        """Restore all settings to their default values."""
        self.settings.clear()
        for key, setting in self._settings.items():
            self.update_setting(key, setting["default"])
        self.defaultsRestored.emit()

    def clear_settings(self):
        """Clear all settings from the registry."""
        self.settings.clear()
        self.settings.sync()
