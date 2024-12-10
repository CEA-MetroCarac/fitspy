import os
from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from pyqttoast import Toast, ToastPreset

import fitspy
from fitspy.core import (
    update_widget_palette,
    to_snake_case,
    replace_icon_colors,
    save_to_json,
    DELIMITER,
)

from .components.plot import PlotController
from .components.files import FilesController
from .components.settings import SettingsController

TYPES = "Fitspy Workspace (*.fspy);;Spectrum/Spectramap (*.json *.txt);;JSON Files (*.json);;Text Files (*.txt)"


class MainController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.view = view
        self.model = model
        self.files_controller = FilesController(
            self.view.spectrum_list, self.view.maps_list
        )
        self.plot_controller = PlotController(
            self.view.spectra_plot,
            self.view.measurement_sites,
            self.view.toolbar,
        )
        self.settings_controller = SettingsController(
            self.view.fit_model_editor, self.view.more_settings
        )
        self.setup_connections()
        self.apply_theme()
        self.apply_settings()

    def setup_connections(self):
        self.view.menuBar.actionOpen.triggered.connect(self.open)
        self.view.menuBar.actionSave.triggered.connect(self.save)
        self.view.menuBar.actionClearEnv.triggered.connect(self.clear)

        self.view.menuBar.actionRestoreDefaults.triggered.connect(
            self.model.restore_defaults
        )
        self.view.menuBar.actionLightMode.triggered.connect(
            lambda: self.set_setting("theme", "light")
        )
        self.view.menuBar.actionDarkMode.triggered.connect(
            lambda: self.set_setting("theme", "dark")
        )
        self.view.menuBar.actionManual.triggered.connect(self.open_manual)
        self.view.menuBar.actionAbout.triggered.connect(self.view.about)
        self.view.statusBox.ncpus.currentTextChanged.connect(
            lambda ncpus: self.set_setting("ncpus", ncpus)
        )
        self.model.themeChanged.connect(self.on_theme_changed)
        self.model.defaultsRestored.connect(self.apply_settings)
        self.model.peaksCmapChanged.connect(self.update_peaks_cmap)
        self.model.mapCmapChanged.connect(self.update_map_cmap)

        self.files_controller.showToast.connect(self.show_toast)
        self.files_controller.askConfirmation.connect(
            self.show_confirmation_dialog
        )
        self.files_controller.loadSpectrum.connect(
            self.plot_controller.load_spectrum
        )
        self.files_controller.loadSpectraMap.connect(
            self.plot_controller.load_map
        )
        self.files_controller.delSpectrum.connect(
            self.plot_controller.del_spectrum
        )
        self.files_controller.delSpectraMap.connect(
            self.plot_controller.del_map
        )
        self.files_controller.spectraChanged.connect(
            self.plot_controller.set_current_spectrum
        )
        self.files_controller.spectraChanged.connect(
            self.change_current_fit_model
        )
        self.files_controller.mapChanged.connect(
            self.plot_controller.switch_map
        )
        self.files_controller.addMarker.connect(self.plot_controller.set_marker)
        self.files_controller.loadState.connect(self.load_state)
        self.files_controller.saveResults.connect(self.save_results)

        self.plot_controller.showToast.connect(self.show_toast)
        self.plot_controller.askConfirmation.connect(
            self.show_confirmation_dialog
        )
        self.plot_controller.spectrumLoaded.connect(
            self.files_controller.add_spectrum
        )
        self.plot_controller.spectrumDeleted.connect(
            self.files_controller.del_spectrum
        )
        self.plot_controller.spectraMapDeleted.connect(
            self.files_controller.del_map
        )
        self.plot_controller.decodedSpectraMap.connect(
            self.files_controller.update_spectramap
        )  # could be simplified : self.files_controller.model.update_spectramap
        self.plot_controller.settingChanged.connect(self.model.update_setting)
        self.plot_controller.highlightSpectrum.connect(
            self.files_controller.highlight_spectrum
        )
        self.plot_controller.baselinePointsChanged.connect(
            self.settings_controller.set_baseline_points
        )
        self.plot_controller.PeaksChanged.connect(
            self.settings_controller.update_peaks_table
        )
        self.plot_controller.BkgChanged.connect(
            self.settings_controller.update_bkg_table
        )
        self.plot_controller.progressUpdated.connect(self.update_progress)
        self.plot_controller.colorizeFromFitStatus.connect(
            self.files_controller.colorize_from_fit_status
        )
        self.plot_controller.exportCSV.connect(self.export_to_csv)

        self.settings_controller.showToast.connect(self.show_toast)
        self.settings_controller.settingChanged.connect(self.set_setting)
        self.settings_controller.removeOutliers.connect(self.remove_outliers)
        self.settings_controller.setSpectrumAttr.connect(
            self.plot_controller.set_spectrum_attr
        )
        self.settings_controller.baselinePointsChanged.connect(
            self.plot_controller.set_baseline_points
        )
        self.settings_controller.applyBaseline.connect(self.apply_baseline)
        self.settings_controller.applySpectralRange.connect(
            self.plot_controller.apply_spectral_range
        )
        self.settings_controller.applyNormalization.connect(
            self.plot_controller.apply_normalization
        )
        self.settings_controller.updatePeakModel.connect(
            self.plot_controller.update_peak_model
        )
        self.settings_controller.updatePeakModel.emit(
            self.view.fit_model_editor.model_settings.fitting.peak_model.currentText()
        )
        self.settings_controller.setBkgModel.connect(
            self.plot_controller.set_bkg_model
        )
        self.settings_controller.setPeaks.connect(
            self.plot_controller.set_peaks
        )
        self.settings_controller.setBkg.connect(self.plot_controller.set_bkg)
        self.settings_controller.fitRequested.connect(self.fit)

        app = QApplication.instance()
        app.aboutToQuit.connect(
            lambda: self.set_setting(
                "figure_options_title", self.view.spectra_plot.ax.get_title()
            )
        )

    def apply_settings(self):
        self.view.statusBox.ncpus.setCurrentText(self.model.ncpus)
        self.view.spectra_plot.ax.set_title(self.model.figure_options_title)
        self.view.more_settings.solver_settings.method.setCurrentText(
            self.model.fit_params_method
        )
        self.view.more_settings.solver_settings.fit_negative.setChecked(
            self.model.fit_params_fit_negative
        )
        self.view.more_settings.solver_settings.fit_outliers.setChecked(
            self.model.fit_params_fit_outliers
        )
        self.view.more_settings.solver_settings.max_ite.setValue(
            self.model.fit_params_max_ite
        )
        self.view.more_settings.solver_settings.coef_noise.setValue(
            self.model.fit_params_coef_noise
        )
        self.view.more_settings.solver_settings.xtol.setValue(
            self.model.fit_params_xtol
        )
        self.view.more_settings.other_settings.outliers_coef.setValue(
            self.model.outliers_coef
        )
        self.view.more_settings.other_settings.peaks_cmap.setCurrentText(
            self.model.peaks_cmap
        )
        self.view.more_settings.other_settings.map_cmap.setCurrentText(
            self.model.map_cmap
        )

        if self.model.click_mode == "baseline":
            self.view.toolbar.baseline_radio.setChecked(True)
        elif self.model.click_mode == "fitting":
            self.view.toolbar.fitting_radio.setChecked(True)

        for (
            label,
            checkbox,
        ) in self.view.toolbar.view_options.checkboxes.items():
            setting = f"view_options_{to_snake_case(label)}"
            state = self.model.settings.value(setting, True, type=bool)
            checkbox.setChecked(state)

    def load_state(self, selected, models):
        # Restore model attributes to each spectrum
        self.plot_controller.set_spectra_attributes(models)

        # Delete spectrum that are in spectrum list but not in models (deleted by user from map(s))
        spectrum_ids = self.files_controller.get_all_spectrum_ids(DELIMITER)
        items = [
            fname for fname in spectrum_ids if fname not in models
        ]  # spectrum_ids to be deleted
        if items:
            items = self.files_controller.convert_spectrum_ids_to_dict(
                items, DELIMITER
            )
            self.files_controller.remove_files(items)

        # Restore selection
        self.files_controller.set_selection(
            self.view.maps_list.list, selected["map"]
        )
        self.files_controller.set_selection(
            self.view.spectrum_list.list, selected["spectra"]
        )

    def open(self):
        fnames = QFileDialog.getOpenFileNames(None, "Load File", "", TYPES)[0]
        self.files_controller.load_files(fnames)

    def save(self):
        maps_list = self.files_controller.get_map_fnames()
        spectrum_list = self.files_controller.get_spectrum_fnames()
        map, spectra = self.files_controller.get_full_selection()
        fname = QFileDialog.getSaveFileName(
            None, "Save File", "", TYPES.split(";;")[0]
        )[0]
        if fname:
            # Getting the models of all spectrum objects
            fit_models = self.plot_controller.get_fit_models(DELIMITER)

            data = {
                "files": {
                    "maps_list": maps_list,
                    "spectrum_list": spectrum_list,
                },
                "selected": {"map": map, "spectra": spectra},
                "models": fit_models,
            }
            save_to_json(fname, data)

    def clear(self):
        if self.files_controller.get_all_spectrum_ids(DELIMITER):
            if not self.show_confirmation_dialog(
                "Current work will be cleared. Continue ?"
            ):
                return

        # Remove all spectra and maps
        self.files_controller.clear()

    def apply_theme(self):
        app = QApplication.instance()
        palette = (
            self.model.dark_palette()
            if self.model.theme == "dark"
            else self.model.light_palette()
        )
        app.setPalette(palette)
        update_widget_palette(self.view, palette)
        self.update_menu_icons(palette)
        self.view.toolbar.update_toolbar_icons()

    def update_menu_icons(self, palette):
        def update_icon(widget, old_color, new_color):
            current_icon = widget.icon()
            if not current_icon.isNull():
                new_icon = replace_icon_colors(
                    current_icon, old_color, new_color
                )
                widget.setIcon(new_icon)

        def determine_colors(background_color):
            if background_color.value() < 128:
                return QColor(0, 0, 0), QColor(230, 230, 230)
            else:
                return QColor(230, 230, 230), QColor(0, 0, 0)

        background_color = palette.color(self.view.backgroundRole())
        old_color, new_color = determine_colors(background_color)

        widgets = [action for action in self.view.menuBar.actions()] + [
            self.view.maps_list.deselect_btn,
            self.view.spectrum_list.sel_all,
            self.view.toolbar.copy_btn,
        ]

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

    def apply_baseline(self):
        mode = self.settings_controller.get_baseline_mode()
        if (
            mode == "Semi-Auto"
            and len(self.files_controller.get_selected_fnames()) > 20
        ):
            self.show_confirmation_dialog(
                "Processing Semi-Auto on more than 20 spectra may take a long time. Continue ?",
                self.plot_controller.apply_baseline,
            )
        else:
            self.plot_controller.apply_baseline()

    def show_confirmation_dialog(
        self, message, callback=None, args=(), kwargs={}
    ):
        reply = QMessageBox.question(
            None,
            "Confirmation",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            if callback:
                callback(*args, **kwargs)
            return True
        else:
            print("Operation aborted by the user.")
            return False

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
        """Return the number of CPUs to work with"""
        ncpus = self.model.ncpus  # or self.fit_settings.params['ncpus'].get()
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
            self.view.statusBox.cpuCountLabel.setText(
                f"CPUs: {ncpu}/{max_cpus}"
            )
        percent = 0
        while percent < 100:
            percent = 100 * spectra.pbar_index / nfiles
            self.view.statusBox.progressLabel.setText(
                f"{spectra.pbar_index}/{nfiles}"
            )
            self.view.statusBox.progressBar.setValue(percent)
            QApplication.processEvents()

    def export_to_csv(self, spectramap):
        from pathlib import Path

        fname = Path(spectramap.fname).stem
        var = self.view.measurement_sites.get_current_title()

        if "Intensity" in var:
            fname += "_intensity"
        else:
            label = getattr(spectramap, "label", None)
            fname += f"_{var}_{label}" if label else f"_{var}"

        fname = QFileDialog.getSaveFileName(
            None, "Save File", f"{fname}.csv", "CSV Files (*.csv)"
        )[0]

        if fname:
            spectramap.export_to_csv(fname)
            self.show_toast("SUCCESS", "Exported", f"{fname} has been saved.")

    def save_results(self, list_widget):
        selected_items = [item.text() for item in list_widget.selectedItems()]
        spectra = self.plot_controller.model.parent()

        if not selected_items:
            self.show_toast("ERROR", "No Selection", "No spectrum selected.")
            return

        directory = QFileDialog.getExistingDirectory(
            None, "Select Save Directory"
        )
        if directory:
            spectra.save_results(directory, selected_items)
            self.show_toast("SUCCESS", "Saved", f"Results saved to {directory}")

    def open_manual(self):
        url = QUrl("https://cea-metrocarac.github.io/fitspy/doc/index.html")
        QDesktopServices.openUrl(url)

    def update_peaks_cmap(self):
        fitspy.DEFAULTS["peaks_cmap"] = (
            self.view.more_settings.other_settings.peaks_cmap.currentColormap().to_mpl()
        )
        self.settings_controller.update_peaks_table(
            self.plot_controller.get_spectrum()[0], block_signals=False
        )

    def update_map_cmap(self):
        fitspy.DEFAULTS["map_cmap"] = (
            self.view.more_settings.other_settings.map_cmap.currentColormap().to_mpl()
        )
        self.view.measurement_sites.update_plot(
            self.plot_controller.model.current_map
        )
