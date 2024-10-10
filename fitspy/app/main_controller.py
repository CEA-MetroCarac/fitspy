import os
from PySide6.QtCore import QObject
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication
from pyqttoast import Toast, ToastPreset

from fitspy.core import update_widget_palette, to_snake_case, replace_icon_colors

from .main_model import MainModel
from .main_view import MainView
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
        self.apply_theme()
        self.apply_settings()

    def setup_connections(self):
        self.view.menuBar.actionRestoreDefaults.triggered.connect(self.model.restore_defaults)
        self.view.menuBar.actionLightMode.triggered.connect(lambda: self.set_setting("theme", "light"))
        self.view.menuBar.actionDarkMode.triggered.connect(lambda: self.set_setting("theme", "dark"))
        self.view.statusBox.ncpus.currentTextChanged.connect(lambda ncpus: self.set_setting("ncpus", ncpus))
        self.model.themeChanged.connect(self.on_theme_changed)
        self.model.defaultsRestored.connect(self.apply_settings)

        self.files_controller.loadSpectrum.connect(self.plot_controller.load_spectrum)
        self.files_controller.loadSpectraMap.connect(self.plot_controller.load_map)
        self.files_controller.delSpectrum.connect(self.plot_controller.del_spectrum)
        self.files_controller.delSpectraMap.connect(self.plot_controller.del_map)
        self.files_controller.spectraChanged.connect(self.plot_controller.set_current_spectrum)
        self.files_controller.spectraChanged.connect(self.change_current_fit_model)
        self.files_controller.mapChanged.connect(self.plot_controller.switch_map)
        self.files_controller.addMarker.connect(self.plot_controller.set_marker)

        self.plot_controller.showToast.connect(self.show_toast)
        self.plot_controller.spectrumLoaded.connect(self.files_controller.add_spectrum)
        self.plot_controller.spectrumDeleted.connect(self.files_controller.del_spectrum)
        self.plot_controller.spectraMapDeleted.connect(self.files_controller.del_map)
        self.plot_controller.decodedSpectraMap.connect(self.files_controller.update_spectramap)  # could be simplified : self.files_controller.model.update_spectramap
        self.plot_controller.settingChanged.connect(self.model.update_setting)
        self.plot_controller.highlightSpectrum.connect(self.files_controller.highlight_spectrum)
        self.plot_controller.baselinePointsChanged.connect(self.settings_controller.set_baseline_points)
        self.plot_controller.PeaksChanged.connect(self.settings_controller.update_peaks_table)
        self.plot_controller.progressUpdated.connect(self.update_progress)

        self.settings_controller.showToast.connect(self.show_toast)
        self.settings_controller.settingChanged.connect(self.set_setting)
        self.settings_controller.removeOutliers.connect(self.remove_outliers)
        self.settings_controller.setSpectrumAttr.connect(self.plot_controller.set_spectrum_attr)
        self.settings_controller.baselinePointsChanged.connect(self.plot_controller.set_baseline_points)
        self.settings_controller.applyBaseline.connect(self.plot_controller.apply_baseline)
        self.settings_controller.applySpectralRange.connect(self.plot_controller.apply_spectral_range)
        self.settings_controller.applyNormalization.connect(self.plot_controller.apply_normalization)
        self.settings_controller.updatePeakModel.connect(self.plot_controller.update_peak_model)
        self.settings_controller.updatePeakModel.emit(self.view.fit_model_editor.model_settings.fitting.peak_model.currentText())
        self.settings_controller.setPeaks.connect(self.plot_controller.set_peaks)
        self.settings_controller.fitRequested.connect(self.fit)

        app = QApplication.instance()
        app.aboutToQuit.connect(lambda: self.set_setting("figure_options_title", self.view.spectra_plot.ax.get_title()))
    
    def apply_settings(self):
        self.view.statusBox.ncpus.setCurrentText(self.model.ncpus)
        self.view.spectra_plot.ax.set_title(self.model.figure_options_title)
        self.view.more_settings.solver_settings.method.setCurrentText(self.model.fit_params_method)
        self.view.more_settings.solver_settings.fit_negative.setChecked(self.model.fit_params_fit_negative)
        self.view.more_settings.solver_settings.fit_outliers.setChecked(self.model.fit_params_fit_outliers)
        self.view.more_settings.solver_settings.max_ite.setValue(self.model.fit_params_max_ite)
        self.view.more_settings.solver_settings.coef_noise.setValue(self.model.fit_params_coef_noise)
        self.view.more_settings.solver_settings.xtol.setValue(self.model.fit_params_xtol)
        self.view.more_settings.other_settings.outliers_coef.setValue(self.model.outliers_coef)
        self.view.more_settings.other_settings.save_only_path.setChecked(self.model.save_only_path)

        if self.model.click_mode == "baseline":
            self.view.toolbar.baseline_radio.setChecked(True)
        elif self.model.click_mode == "fitting":
            self.view.toolbar.fitting_radio.setChecked(True)
    
        for label, checkbox in self.view.toolbar.view_options.checkboxes.items():
            setting = f"view_options_{to_snake_case(label)}"
            state = self.model.settings.value(setting, True, type=bool)
            checkbox.setChecked(state)

    def apply_theme(self):
        app = QApplication.instance()
        palette = self.model.dark_palette() if self.model.theme == "dark" else self.model.light_palette()
        app.setPalette(palette)
        update_widget_palette(self.view, palette)
        self.update_menu_icons(palette)
        self.view.toolbar.update_toolbar_icons()

    def update_menu_icons(self, palette):
        def update_icon(widget, old_color, new_color):
            current_icon = widget.icon()
            if not current_icon.isNull():
                new_icon = replace_icon_colors(current_icon, old_color, new_color)
                widget.setIcon(new_icon)

        def determine_colors(background_color):
            if background_color.value() < 128:
                return QColor(0, 0, 0), QColor(230, 230, 230)
            else:
                return QColor(230, 230, 230), QColor(0, 0, 0)

        background_color = palette.color(self.view.backgroundRole())
        old_color, new_color = determine_colors(background_color)

        widgets = (
            [action for action in self.view.menuBar.actions()] +
            [self.view.maps_list.deselect_btn, self.view.spectrum_list.sel_all, self.view.toolbar.copy_button]
        )

        for widget in widgets:
            update_icon(widget, old_color, new_color)

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
        else:
            self.plot_controller.update_spectraplot()
            self.settings_controller.clear_model()

    def remove_outliers(self):
        self.plot_controller.remove_outliers(self.model.outliers_coef)

    def show_toast(self, preset, title, text):
        preset_mapping = {
            "success": (ToastPreset.SUCCESS, ToastPreset.SUCCESS_DARK),
            "warning": (ToastPreset.WARNING, ToastPreset.WARNING_DARK),
            "error": (ToastPreset.ERROR, ToastPreset.ERROR_DARK),
            "info": (ToastPreset.INFORMATION, ToastPreset.INFORMATION_DARK),
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

    def get_ncpus(self, nfiles):
        """ Return the number of CPUs to work with """
        ncpus = self.model.ncpus #or self.fit_settings.params['ncpus'].get()
        if ncpus == "Auto":
            return max(1, min(int(nfiles / 8), int(os.cpu_count() / 2)))
        else:
            return int(ncpus)

    def fit(self, model_dict):
        nfiles = len(self.files_controller.get_selected_fnames())
        ncpus = self.get_ncpus(nfiles=nfiles)
        self.plot_controller.fit(model_dict, ncpus)

    def update_progress(self, spectra, nfiles, ncpu=None):
        if ncpu:
            max_cpus = os.cpu_count()
            self.view.statusBox.cpuCountLabel.setText(f"CPUs: {ncpu}/{max_cpus}")
        percent = 0
        while percent < 100:
            percent = 100 * spectra.pbar_index / nfiles
            self.view.statusBox.progressLabel.setText(f"{spectra.pbar_index}/{nfiles}")
            self.view.statusBox.progressBar.setValue(percent)
            QApplication.processEvents()