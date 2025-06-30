import os
import types
from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from fitspy.core.utils import load_from_json, save_to_json
from fitspy.core import models_bichromatic
from fitspy.apps.pyside import DEFAULTS
from fitspy.apps.pyside.main_model import MainModel
from fitspy.apps.pyside.main_view import MainView
from fitspy.apps.pyside.utils import (
    update_widget_palette,
    to_snake_case,
    replace_icon_colors,
)
from fitspy.apps.pyside.components.plot import PlotController
from fitspy.apps.pyside.components.files import FilesController
from fitspy.apps.pyside.components.settings import SettingsController


class MainController(QObject):
    def __init__(self, model=None, view=None):
        super().__init__()
        self.view = view or MainView()
        self.model = model or MainModel()
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
        self.view.menuBar.actionSaveData.triggered.connect(
            lambda: self.save(save_data=True)
        )
        self.view.menuBar.actionClearEnv.triggered.connect(self.clear)
        self.view.menuBar.actionRestoreDefaults.triggered.connect(
            self.model.restore_defaults
        )
        self.view.menuBar.actionTheme.triggered.connect(
            lambda: self.set_setting(
                "theme", "light" if self.model.theme == "dark" else "dark"
            )
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
        self.files_controller.loadSpectra.connect(
            self.plot_controller.load_spectra
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
        self.files_controller.reinitSpectra.connect(
            lambda fnames: (
                self.plot_controller.reinit_spectra(fnames),
                self.change_current_fit_model(fnames),
                self.update_fit_stats(),
            )
        )
        self.files_controller.spectraChanged.connect(
            lambda fnames: self.plot_controller.set_current_spectra(
                fnames or self.settings_controller.get_model_fname()
            )
        )
        self.files_controller.spectraChanged.connect(
            self.change_current_fit_model
        )
        self.files_controller.spectraChanged.connect(self.update_fit_stats)
        self.files_controller.mapChanged.connect(
            self.plot_controller.switch_map
        )
        self.files_controller.mapChanged2.connect(self.change_map)
        self.files_controller.addMarker.connect(self.plot_controller.set_marker)
        self.files_controller.loadState.connect(self.load_state)
        self.files_controller.saveResults.connect(
            lambda fnames: self.save_results(fnames=fnames)
        )

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
        # could be simplified : self.files_controller.model.update_spectramap
        self.plot_controller.decodedSpectraMap.connect(
            self.files_controller.update_spectramap
        )
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
        self.settings_controller.calculateOutliers.connect(
            self.outliers_calculation
        )
        self.settings_controller.setSpectrumAttr.connect(
            self.plot_controller.set_spectrum_attr
        )
        self.settings_controller.baselinePointsChanged.connect(
            self.plot_controller.set_baseline_points
        )
        self.settings_controller.setModel.connect(self.apply_model)
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
        self.settings_controller.saveModels.connect(self.save_models)
        self.settings_controller.fitRequested.connect(self.fit)
        self.settings_controller.modelSelectionChanged.connect(
            self.on_model_selection_changed
        )
        self.settings_controller.peakSelected.connect(
            self.plot_controller.highlight_peak
        )
        app = QApplication.instance()
        app.aboutToQuit.connect(
            lambda: self.set_setting(
                "figure_options_title", self.view.spectra_plot.ax.get_title()
            )
        )

    def apply_settings(self):
        self.view.statusBox.ncpus.setCurrentText(self.model.ncpus)
        self.view.spectra_plot.ax.set_title(self.model.figure_options_title)
        self.view.more_settings.other_settings.cb_bichromatic.setChecked(
            self.model.bichromatic_models_enable
        )
        for (
                button
        ) in self.view.more_settings.other_settings.bichromatic_group.buttons():
            if button.text() == self.model.bichromatic_models_mode:
                button.setChecked(True)
                models_bichromatic.MODE = button.text()
                break
        self.view.more_settings.other_settings.outliers_coef.setValue(
            self.model.outliers_coef
        )
        self.view.more_settings.other_settings.peaks_cmap.setCurrentText(
            self.model.peaks_cmap
        )
        self.view.more_settings.other_settings.map_cmap.setCurrentText(
            self.model.map_cmap
        )
        radio_button = getattr(
            self.view.toolbar, f"{self.model.click_mode}_radio"
        )
        radio_button.setChecked(True)

        for (
                label,
                checkbox,
        ) in self.view.toolbar.view_options.checkboxes.items():
            setting = f"view_options_{to_snake_case(label)}"
            state = getattr(self.model, setting)
            checkbox.setChecked(state)

    def load_state(self, models):
        # # Restore model attributes to each spectrum
        # self.plot_controller.set_spectra_attributes(models)

        fit_status = {
            model["fname"]: model["result_fit_success"]
            for model in models.values()
            if "result_fit_success" in model
        }
        self.files_controller.colorize_from_fit_status(fit_status)

        spectra = self.plot_controller.get_spectra()
        if spectra:
            self.settings_controller.set_model(spectra[0])

    def open(self, fnames: list = None):
        if not fnames:
            # fnames = QFileDialog.getOpenFileNames(None, "Load File", "", TYPES)[0]
            fnames = QFileDialog.getOpenFileNames(None, "Load File(s)")[0]
        fnames = [str(fname) for fname in fnames]
        self.files_controller.load_files(fnames)

    def save(self, save_data=False):
        fname_json = QFileDialog.getSaveFileName(
            None, "Save File", "", "JSON Files (*.json);;All Files (*)"
        )[0]
        if fname_json:
            self.plot_controller.model.spectra.save(
                fname_json=fname_json, save_data=save_data
            )

    def clear(self):
        # if self.files_controller.get_all_spectrum_ids(DELIMITER):
        if len(self.plot_controller.model.spectra) > 0:
            if not self.show_confirmation_dialog(
                    "Current work will be cleared. Continue ?"
            ):
                return

        self.files_controller.clear()  # Remove all spectra and maps
        self.settings_controller.clear_models()  # remove all loaded models

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

        widgets = list(self.view.menuBar.actions()) + [
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
            spectrum = self.plot_controller.get_spectra(fnames[0])
            self.settings_controller.set_model(spectrum)
        else:
            self.settings_controller.select_model(
                self.settings_controller.get_model_fname()
            )

    def change_map(self):
        current_map = self.plot_controller.model.current_map
        if current_map:
            fit_status = {
                spectrum.fname: spectrum.result_fit.success
                for spectrum in current_map
                if getattr(spectrum.result_fit, "success", None) is not None
            }
            self.plot_controller.colorizeFromFitStatus.emit(fit_status)

    def outliers_calculation(self):
        self.plot_controller.outliers_calculation(self.model.outliers_coef)

    def apply_baseline(self):
        self.plot_controller.apply_baseline()

    def show_confirmation_dialog(
            self, message, callback=None, args=(), kwargs=None
    ):
        reply = QMessageBox.question(
            None,
            "Confirmation",
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            if callback:
                kwargs = kwargs or {}
                callback(*args, **kwargs)
            return True
        else:
            print("Operation aborted by the user.")
            return False

    def show_toast(self, preset, title, text, duration=3000):
        try:  # https://github.com/niklashenning/pyqttoast/issues/23
            from pyqttoast import Toast, ToastPreset
        except:
            print(f"[{preset.upper()}] {title}: {text}")
            return

        preset_mapping = {
            "success": (ToastPreset.SUCCESS, ToastPreset.SUCCESS_DARK),
            "warning": (ToastPreset.WARNING, ToastPreset.WARNING_DARK),
            "error": (ToastPreset.ERROR, ToastPreset.ERROR_DARK),
            "info": (ToastPreset.INFORMATION, ToastPreset.INFORMATION_DARK),
        }

        current_theme = self.model.theme
        is_dark_theme = current_theme == "dark"

        toast = Toast(self.view)
        toast.setDuration(duration)
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
        self.update_fit_stats()

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
            # self.show_toast("SUCCESS", "Exported", f"{fname} has been saved.")

    def save_results(self, dirname_res=None, fnames=None):
        list_widget = self.view.spectrum_list.list
        selected_items = fnames or list_widget.get_all_fnames()
        if not selected_items:
            # self.show_toast("ERROR", "No Selection", "No spectrum selected.")
            return

        directory = dirname_res or QFileDialog.getExistingDirectory(
            None, "Select Save Directory"
        )
        if directory:
            self.plot_controller.model.spectra.save_results(
                directory, selected_items
            )
            # self.show_toast("SUCCESS", "Saved", f"Results saved into {directory}")

    def save_figures(self, dirname_fig=None, fnames=None):
        list_widget = self.view.spectrum_list.list
        selected_items = fnames or list_widget.get_all_fnames()
        if not selected_items:
            # self.show_toast("ERROR", "No Selection", "No spectrum selected.")
            return

        directory = dirname_fig or QFileDialog.getExistingDirectory(
            None, "Select Save Directory"
        )
        if directory:
            self.plot_controller.model.spectra.save_results(
                directory, selected_items
            )
            # self.show_toast("SUCCESS", "Saved", f"Figures saved into {directory}")

    def open_manual(self):
        url = QUrl("https://cea-metrocarac.github.io/fitspy/index.html")
        QDesktopServices.openUrl(url)

    def update_peaks_cmap(self):
        DEFAULTS["peaks_cmap"] = (
            self.view.more_settings.other_settings.peaks_cmap.currentColormap().to_mpl()
        )
        if self.plot_controller.get_spectra():
            self.settings_controller.update_peaks_table(
                self.plot_controller.get_spectra()[0], block_signals=False
            )

    def update_map_cmap(self):
        DEFAULTS["map_cmap"] = (
            self.view.more_settings.other_settings.map_cmap.currentColormap().to_mpl()
        )
        if self.plot_controller.model.current_map:
            self.view.measurement_sites.update_plot(
                self.plot_controller.model.current_map
            )

    def save_models(self, fnames=None):
        fname_json = QFileDialog.getSaveFileName(
            None, "Save File", "", "JSON Files (*.json);;All Files (*)"
        )[0]
        if fname_json:
            if fnames is None:
                fnames = self.files_controller.get_selected_fnames()

            if not fnames:  # empty selection for .json model preview
                model_data = load_from_json(
                    self.settings_controller.get_model_fname()
                )
                current_model = self.settings_controller.model.current_fit_model
                model_data[0].update(current_model)
                save_to_json(fname_json, model_data)
            else:
                self.plot_controller.save_models(fname_json, fnames)

    def apply_model(self, model_dict):
        spectra = self.plot_controller.get_spectra()
        if spectra:
            for spectrum in spectra:
                spectrum.set_attributes(model_dict)
                spectrum.preprocess()
            self.settings_controller.set_model(spectra[0])

    def on_model_selection_changed(self):
        if self.view.spectrum_list.selectedItems():
            self.view.spectrum_list.clearSelection()
        else:
            self.files_controller.spectraChanged.emit([])

    def show_fit_stats(self):
        self.view.fit_stats.showNormal()
        self.view.fit_stats.raise_()
        self.view.fit_stats.activateWindow()

    def update_fit_stats(self):
        spectra = self.plot_controller.get_spectra()
        if spectra:
            spectrum = spectra[0]
            result_fit = getattr(spectrum, "result_fit", None)

            if result_fit is None or isinstance(result_fit, types.FunctionType):
                text = "No fit result."
            else:
                from lmfit import fit_report
                text = fit_report(result_fit)

            self.view.fit_stats.set_text(text)
        else:
            self.view.fit_stats.set_text("")
