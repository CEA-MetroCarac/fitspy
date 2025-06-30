import copy
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog

from fitspy import FIT_METHODS, BKG_MODELS, PEAK_MODELS
from fitspy.core import models_bichromatic
from fitspy.core.utils import load_from_json, load_models_from_txt, load_models_from_py
from fitspy.apps.pyside.components.settings.model import Model

TYPES = "JSON Files (*.json);;All Files (*)"


class SettingsController(QObject):
    settingChanged = Signal(str, object)
    calculateOutliers = Signal()
    setSpectrumAttr = Signal(str, object)
    baselinePointsChanged = Signal(list)
    setModel = Signal(object)
    applyBaseline = Signal()
    applySpectralRange = Signal(object, object)
    applyNormalization = Signal(bool, object, object)
    updatePeakModel = Signal(str)
    setBkgModel = Signal(str)
    setPeaks = Signal(dict)
    setBkg = Signal(dict)
    saveModels = Signal()
    fitRequested = Signal(object)
    replayModels = Signal(object)  # dict doesnt work with json serialization
    showToast = Signal(str, str, str)
    modelSelectionChanged = Signal(str)
    peakSelected = Signal(int)

    def __init__(self, model_builder, more_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder
        self.more_settings = more_settings
        self.solver_settings = more_settings.solver_settings
        self.other_settings = more_settings.other_settings
        self.setup_connections()
        self.load_default_models()

    def setup_connections(self):
        model_settings = self.model_builder.model_settings
        model_selector = self.model_builder.model_selector
        self.model.currentModelChanged.connect(self.apply_model)

        # Spectral range settings
        spectral_range = model_settings.spectral_range
        spectral_range.apply.clicked.connect(self.apply_spectral_range)

        # Baseline settings
        baseline = model_settings.baseline
        baseline_modes = {
            baseline.none: None,
            baseline.semi_auto: "Semi-Auto",
            baseline.linear: "Linear",
            baseline.polynomial: "Polynomial",
        }

        for button, mode in baseline_modes.items():
            button.toggled.connect(
                lambda checked, mode=mode: (self.update_and_emit("baseline.mode", mode)
                                            if checked else None))

        baseline.slider.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.coef", value))
        baseline.attached.toggled.connect(
            lambda checked: self.update_and_emit("baseline.attached", checked))
        baseline.sigma.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.sigma", value))
        baseline.order.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.order_max", value))
        baseline.apply.clicked.connect(self.applyBaseline)

        # Normalization settings
        normalization = model_settings.normalization
        normalization.normalize.toggled.connect(self.apply_normalization)
        normalization.range_min.editingFinished.connect(self.apply_normalization)
        normalization.range_max.editingFinished.connect(self.apply_normalization)

        # Fitting settings
        fitting = model_settings.fitting
        fitting.peak_model.currentTextChanged.connect(self.switch_peak_model)
        fitting.bkg_model.currentTextChanged.connect(self.switch_bkg_model)
        fitting.loadPeakModel.connect(lambda fname: self.load_user_models(PEAK_MODELS, fname))
        fitting.loadBkgModel.connect(lambda fname: self.load_user_models(BKG_MODELS, fname))

        # Save model
        model_settings.save.clicked.connect(self.saveModels)
        model_settings.fit.clicked.connect(self.request_fit)

        # Peaks + Baseline Table
        model_builder = self.model_builder
        model_builder.baseline_table.baselinePointsChanged.connect(self.set_baseline_points)
        model_builder.bounds_chbox.stateChanged.connect(model_builder.peaks_table.show_bounds)
        model_builder.expr_chbox.stateChanged.connect(model_builder.peaks_table.show_expr)
        model_builder.bounds_chbox.stateChanged.connect(model_builder.bkg_table.show_bounds)
        model_builder.expr_chbox.stateChanged.connect(model_builder.bkg_table.show_expr)
        model_builder.peaks_table.peaksChanged.connect(self.update_model_dict)
        model_builder.peaks_table.showToast.connect(self.showToast)
        model_builder.peaks_table.peakSelected.connect(self.peakSelected)
        model_builder.bkg_table.bkgChanged.connect(self.update_model_dict)
        model_builder.bkg_table.showToast.connect(self.showToast)
        self.model.baselinePointsChanged.connect(self.baselinePointsChanged)
        self.model.baselinePointsChanged.connect(model_builder.baseline_table.set_points)

        # Model selector
        model_selector.combo_box.itemAdded.connect(
            lambda fname: self.load_model(fname))
        model_selector.add.clicked.connect(self.load_model)
        model_selector.set.clicked.connect(
            lambda: self.select_model(model_selector.combo_box.currentText()))
        model_selector.combo_box.currentTextChanged.connect(self.modelSelectionChanged)

        # Other settings
        self.solver_settings.fit_negative.toggled.connect(
            lambda checked: self.update_and_emit("fit_params.fit_negative", checked))
        self.solver_settings.fit_outliers.toggled.connect(
            lambda checked: self.update_and_emit("fit_params.fit_outliers", checked))
        self.solver_settings.independent_models.toggled.connect(
            lambda checked: self.update_and_emit("fit_params.independent_models", checked))
        self.solver_settings.method.currentTextChanged.connect(
            lambda text: self.update_and_emit("fit_params.method", FIT_METHODS[text]))
        self.solver_settings.max_ite.valueChanged.connect(
            lambda value: self.update_and_emit("fit_params.max_ite", value))
        self.solver_settings.coef_noise.valueChanged.connect(
            lambda value: self.update_and_emit("fit_params.coef_noise", value))
        self.solver_settings.xtol.valueChanged.connect(
            lambda value: self.update_and_emit("fit_params.xtol", value))

        self.other_settings.cb_bichromatic.toggled.connect(self.toggle_bichromatic_models)
        self.other_settings.bichromatic_group.buttonClicked.connect(self.update_bichromatic_mode)
        self.other_settings.outliers_coef.valueChanged.connect(
            lambda value: self.settingChanged.emit("outliers_coef", value))
        self.other_settings.outliers_calculation.clicked.connect(self.calculateOutliers)
        self.other_settings.peaks_cmap.currentColormapChanged.connect(
            lambda cmap: self.settingChanged.emit("peaks_cmap", cmap.name.split(":")[1]))
        self.other_settings.map_cmap.currentColormapChanged.connect(
            lambda cmap: self.settingChanged.emit("map_cmap", cmap.name.split(":")[1]))

    def load_default_models(self):
        HOME = Path.home()
        self.load_user_models(PEAK_MODELS, fname=HOME / "Fitspy" / "peak_models.txt")
        self.load_user_models(PEAK_MODELS, fname=HOME / "Fitspy" / "peak_models.py")
        self.load_user_models(BKG_MODELS, fname=HOME / "Fitspy" / "bkg_models.txt")
        self.load_user_models(BKG_MODELS, fname=HOME / "Fitspy" / "bkg_models.py")

    def update_and_emit(self, key, value):
        key, value = self.update_model_dict_with_key(key, value)
        self.setSpectrumAttr.emit(key, value)

    def update_model_dict_with_key(self, key, value):
        """
        Update settings controller model dict by key, e.g. "fit_params.method" will update the
        "method" key in the "fit_params" dictionary

        Returns
        -------
        key: Spectrum()
            attribute to be updated
        value:
            New value to be set
        """
        self.model.blockSignals(True)
        keys = key.split(".")
        current_dict = self.model.current_fit_model
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = {}
            current_dict = current_dict[k]
        current_dict[keys[-1]] = value
        self.model.blockSignals(False)

        if key.startswith("fit_params"):
            return "fit_params", current_dict
        return key, value

    def set_model(self, spectrum):
        """Set the current model to the spectrum model"""
        if isinstance(spectrum, dict):
            model = spectrum
        else:
            model = spectrum.save()
            model["baseline"].pop("y_eval")
            model.pop("fname", None)  # TODO: what happens for fit_results=None with success as attr

        self.model.current_fit_model = copy.deepcopy(model)

    def update_model_dict(self, model_dict):
        # Unnecessary to block signals as the update occurs key by key
        for key, value in model_dict.items():
            self.model.current_fit_model[key] = value

        if "peak_models" in model_dict or "peak_label" in model_dict:
            self.setPeaks.emit(model_dict)
        if "bkg_model" in model_dict:
            self.setBkg.emit(model_dict)

    def clear_current_model(self):
        self.model.current_fit_model = {}

    def clear_models(self):
        """Clear all loaded models from the model selector combo box and the loaded_models list."""
        combo_box = self.model_builder.model_selector.combo_box
        combo_box.clear()
        self.model.loaded_models.clear()
        self.clear_current_model()

    def load_model(self, fname=None):
        if not fname:
            fname = QFileDialog.getOpenFileName(None, "Load File", "", TYPES)[0]

        if fname:
            fname = str(fname)
            if fname not in self.model.loaded_models:
                self.model_builder.model_selector.combo_box.addItem(fname)
                self.model.loaded_models.append(fname)

            index = self.model_builder.model_selector.combo_box.findText(fname)
            self.model_builder.model_selector.combo_box.setCurrentIndex(index)

    def select_model(self, fname):
        if fname == "":
            return

        try:
            models = load_from_json(fname)
            first_key = next(iter(models))

            if first_key in ['0', 0]:
                first_model = models[first_key]  # Dict of models
            else:
                first_model = models  # Single model

            first_model.pop("fname", None)
            self.setModel.emit(first_model)  # Applying in Spectrum objects first
        except Exception:
            self.showToast.emit(
                "error",
                "Invalid model",
                "Model can not be loaded",
            )

    def apply_model(self, fit_model):
        """Reflects the changes in the model to the GUI"""
        self.model_builder.update_model(fit_model)
        self.solver_settings.update_settings(fit_model.get("fit_params", {}))
        points = fit_model.get("baseline", {}).get("points", [[], []])
        self.set_baseline_points(points)
        self.update_peaks_table(fit_model)

        bkg_model_dict = fit_model.get("bkg_model") or {}
        bkg_model = next(iter(bkg_model_dict), "None")
        self.update_bkg_table(bkg_model_dict.get(bkg_model, {}))

    def set_baseline_points(self, points=[[], []]):
        self.model.baseline_points = points
        if points[0]:
            # Uncesseray to block signals, signals are not triggered when setting specific keys
            self.model.current_fit_model["baseline"]["points"] = points

    def apply_spectral_range(self):
        spectral_range = self.model_builder.model_settings.spectral_range
        range_min = spectral_range.range_min.value()
        range_max = spectral_range.range_max.value()

        # if both are not None and range_min is >= range_max then show an error message
        if range_min is not None and range_max is not None:
            if range_min >= range_max:
                self.showToast.emit(
                    "error",
                    "Invalid spectral range",
                    "Minimum value must be less than maximum value",
                )
                return
        self.update_model_dict({"range_min": range_min, "range_max": range_max})
        self.applySpectralRange.emit(range_min, range_max)

    def apply_normalization(self, checked=None):
        if checked is None:
            checked = self.model_builder.model_settings.normalization.normalize.isChecked()

        normalization = self.model_builder.model_settings.normalization
        range_min = normalization.range_min.value()
        range_max = normalization.range_max.value()

        if range_min is not None and range_max is not None and checked:
            if range_min >= range_max:
                self.showToast.emit(
                    "error",
                    "Invalid normalization range",
                    "Minimum value must be less than maximum value",
                )
                return

        self.update_model_dict({"normalize": checked,
                                "normalize_range_min": range_min,
                                "normalize_range_max": range_max})
        self.applyNormalization.emit(checked, range_min, range_max)

    def update_peaks_table(self, spectrum, block_signals=True):
        self.model_builder.peaks_table.clear()
        if not spectrum:
            return

        if block_signals:
            self.model.blockSignals(True)

        def extract_params(param_dict):
            return {
                "min": param_dict.get("min"),
                "value": param_dict.get("value"),
                "max": param_dict.get("max"),
                "vary": param_dict.get("vary"),
                "expr": param_dict.get("expr"),
            }

        def add_row_from_params(prefix, label, model_name, params):
            row_params = {
                "prefix": prefix,
                "label": label,
                "model_name": model_name,
            }

            for param_name, param_data in params.items():
                param_values = extract_params(param_data)
                param_key = param_name.lower()
                row_params[f"{param_key}_min"] = param_values.get("min")
                row_params[param_key] = param_values.get("value")
                row_params[f"{param_key}_max"] = param_values.get("max")
                row_params[f"{param_key}_fixed"] = not param_values.get("vary")
                row_params[f"{param_key}_expr"] = param_values.get("expr")

            show_bounds = self.model_builder.bounds_chbox.isChecked()
            show_expr = self.model_builder.expr_chbox.isChecked()
            self.model_builder.peaks_table.add_row(show_bounds, show_expr, **row_params)

        if isinstance(spectrum, dict):
            fit_model = spectrum
            peak_models = fit_model.get("peak_models", fit_model.get("models"))
            peak_labels = fit_model.get("peak_labels", fit_model.get("models_labels"))

            for key, model_dict in peak_models.items():
                label = peak_labels[key]
                prefix = f"m{key + 1:02d}_"
                for model_name, params in model_dict.items():
                    add_row_from_params(prefix, label, model_name, params)

            self.update_model_dict(fit_model)
        else:
            for label, model in zip(spectrum.peak_labels, spectrum.peak_models):
                x0 = model.param_hints['x0']['value']
                self.model_builder.peaks_table.fwhm = spectrum.dx(x0=x0)
                add_row_from_params(model._prefix, label, model.name2, model.param_hints)
            self.set_model(spectrum)

        if block_signals:
            self.model.blockSignals(False)

    def request_fit(self):
        model_dict = self.model.current_fit_model
        self.fitRequested.emit(model_dict)

    def preview_model(self, checked):
        combo_box = self.model_builder.model_selector.combo_box
        current_index = combo_box.currentIndex()
        current_text = combo_box.currentText().replace(" (Preview)", "")

        def lock_inputs(state):
            widgets_to_disable = [
                self.model_builder.model_settings.container,
                self.model_builder.model_selector,
                self.model_builder.baseline_table,
                self.model_builder.bkg_table.table,
                self.model_builder.peaks_table.table,
                self.solver_settings,
            ]

            for widget in widgets_to_disable:
                widget.setDisabled(state)

        if checked:
            # Backup the current fit model
            self.model.backup_fit_model = copy.deepcopy(
                self.model.current_fit_model
            )
            combo_box.setItemText(current_index, current_text + " (Preview)")
            model = load_from_json(current_text)
            model = model[next(iter(model))]
            model.pop("fname", None)
            self.setModel.emit(model)  # Applied before lock cause if peaks table is empty,
            # nothing will be locked
            lock_inputs(True)
        else:
            # Restore the backup fit model
            if self.model.backup_fit_model is not None:
                model = copy.deepcopy(self.model.backup_fit_model)
            combo_box.setItemText(current_index, current_text)
            lock_inputs(False)
            self.setModel.emit(model)

    def switch_peak_model(self, model_name):
        self.model_builder.tab_widget.setCurrentIndex(0)
        self.updatePeakModel.emit(model_name)

    def switch_bkg_model(self, model_name):
        self.model_builder.tab_widget.setCurrentIndex(1)
        self.model_builder.bkg_table.bkg_model = model_name
        self.model_builder.bkg_table.update_columns_based_on_model()
        self.setBkgModel.emit(model_name)

    def update_bkg_table(self, param_hints):
        self.model_builder.bkg_table.update_row(param_hints)

    def get_baseline_mode(self):
        return self.model.current_fit_model["baseline"]["mode"]

    def load_user_models(self, models: dict, fname=None):
        if fname is None:
            fname_str = QFileDialog.getOpenFileName(None, "Select File", "",
                                                    "Python and Text Files (*.py *.txt)")[0]
            fname = Path(fname_str) if fname_str else None

        if isinstance(fname, str):
            fname = Path(fname)

        if fname and fname.exists():
            initial_keys = set(models.keys())
            if fname.suffix == ".txt":
                load_models_from_txt(str(fname), models)
            else:
                load_models_from_py(str(fname))
            new_keys = set(models.keys()) - initial_keys
            if new_keys:
                self.showToast.emit("SUCCESS", "Models Loaded", ", ".join(new_keys))
            else:
                self.showToast.emit("WARNING", "Something went wrong",
                                    "No new models were found in the file")
        self.model_builder.model_settings.fitting.update_combo_boxes()

    def get_model_fname(self):
        return self.model_builder.model_selector.combo_box.currentText()
    
    def toggle_bichromatic_models(self, checked):
        """Handle bichromatic models enable/disable"""
        if checked:
            models_bichromatic.add_models()
        # WARNING : to maintain consistency, models cannot be removed once added
        # else:
        #     models_bichromatic.remove_models()
        
        fitting = self.model_builder.model_settings.fitting
        fitting.update_combo_boxes()
        
        self.settingChanged.emit("bichromatic_models_enable", checked)

    def update_bichromatic_mode(self, button):
        """Update bichromatic mode when button is clicked"""
        mode = button.text()
        models_bichromatic.MODE = mode
        self.settingChanged.emit("bichromatic_models_mode", mode)

