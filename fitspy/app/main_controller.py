from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from pyqttoast import Toast, ToastPreset

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
        self.plot_controller = PlotController(self.view.spectra_plot, self.view.measurement_sites, self.view.toolbar)
        self.settings_controller = SettingsController(self.view.fit_model_editor, self.view.more_settings)
        self.setup_connections()
        self.apply_settings()

    def setup_connections(self):
        self.view.menuBar.actionRestoreDefaults.triggered.connect(self.model.restore_defaults)
        self.view.menuBar.actionLightMode.triggered.connect(lambda: self.set_setting("theme", "light"))
        self.view.menuBar.actionDarkMode.triggered.connect(lambda: self.set_setting("theme", "dark"))
        self.view.statusBar.ncpus.currentTextChanged.connect(lambda ncpus: self.set_setting("ncpus", ncpus))
        self.model.themeChanged.connect(self.on_theme_changed)
        self.model.defaultsRestored.connect(self.apply_settings)

        self.files_controller.loadSpectrum.connect(self.plot_controller.load_spectrum)
        self.files_controller.loadSpectraMap.connect(self.plot_controller.load_map)
        self.files_controller.delSpectrum.connect(self.plot_controller.del_spectrum)
        self.files_controller.delSpectraMap.connect(self.plot_controller.del_map)
        self.files_controller.spectraChanged.connect(self.plot_controller.set_current_spectrum)
        self.files_controller.mapChanged.connect(self.plot_controller.switch_map)
        self.files_controller.currentModelChanged.connect(self.change_current_fit_model)
        self.files_controller.addMarker.connect(self.plot_controller.set_marker)

        self.plot_controller.showToast.connect(self.show_toast)
        self.plot_controller.spectrumLoaded.connect(self.files_controller.add_spectrum)
        self.plot_controller.spectrumDeleted.connect(self.files_controller.del_spectrum)
        self.plot_controller.spectraMapDeleted.connect(self.files_controller.del_map)
        self.plot_controller.decodedSpectraMap.connect(self.files_controller.update_spectramap)  # could be simplified : self.files_controller.model.update_spectramap
        self.plot_controller.settingChanged.connect(self.model.update_setting)
        self.plot_controller.highlightSpectrum.connect(self.files_controller.highlight_spectrum)

        self.settings_controller.settingChanged.connect(self.set_setting)
        self.settings_controller.removeOutliers.connect(self.remove_outliers)

    def apply_settings(self):
        self.apply_theme()
        self.view.statusBar.ncpus.setCurrentText(self.model.ncpus)
        self.view.more_settings.solver_settings.outliers_coef.setValue(self.model.outliers_coef)
        self.view.more_settings.export_settings.save_only_path.setChecked(self.model.save_only_path)

        for label, checkbox in self.view.toolbar.view_options.checkboxes.items():
            state = self.model.settings.value(label, False, type=bool)
            checkbox.setChecked(state)

    def apply_theme(self):
        app = QApplication.instance()
        if self.model.theme == "dark":
            palette = self.model.dark_palette()
        else:
            palette = self.model.light_palette()

        app.setPalette(palette)
        update_widget_palette(self.view, palette)
        self.view.toolbar.update_toolbar_icons()

    def on_theme_changed(self):
        self.apply_theme()

    def set_setting(self, setting_name, value):
        if hasattr(self.model, setting_name):
            setattr(self.model, setting_name, value)
        else:
            raise AttributeError(f"Setting '{setting_name}' not found in model")

    def change_current_fit_model(self, fnames):
        if fnames:
            spectrum = self.plot_controller.get_spectrum(fnames[0])
            self.settings_controller.set_model(spectrum)

    def remove_outliers(self):
        self.plot_controller.remove_outliers(self.model.outliers_coef)

    def show_toast(self, title, text, preset="success"):
        preset_mapping = {
            "success": (ToastPreset.SUCCESS, ToastPreset.SUCCESS_DARK),
            "warning": (ToastPreset.WARNING, ToastPreset.WARNING_DARK),
            "error": (ToastPreset.ERROR, ToastPreset.ERROR_DARK),
            "information": (ToastPreset.INFORMATION, ToastPreset.INFORMATION_DARK),
        }

        current_theme = self.model.theme
        is_dark_theme = current_theme == "dark"

        toast = Toast(self.view)
        toast.setDuration(3000)
        toast.setTitle(title)
        toast.setText(text)

        # Select the appropriate preset based on the theme
        selected_preset = preset_mapping[preset.lower()][is_dark_theme]
        toast.applyPreset(selected_preset)

        toast.show()