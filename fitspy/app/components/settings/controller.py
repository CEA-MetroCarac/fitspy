import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from .model import Model

from fitspy import FIT_METHODS
from fitspy.core.utils import save_to_json, load_from_json

TYPES = "JSON Files (*.json);;All Files (*)"


class SettingsController(QObject):
    settingChanged = Signal(str, object)
    removeOutliers = Signal()
    setSpectrumAttr = Signal(str, object)
    baselinePointsChanged = Signal(list)
    applyBaseline = Signal()
    applySpectralRange = Signal(float, float)
    applyNormalization = Signal(bool, object, object)
    updatePeakModel = Signal(str)
    setPeaks = Signal(object)
    fitRequested = Signal(object)
    showToast = Signal(str, str, str)

    def __init__(self, model_builder, more_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder
        self.more_settings = more_settings
        self.solver_settings = more_settings.solver_settings
        self.other_settings = more_settings.other_settings
        self.setup_connections()

    def setup_connections(self):
        model_settings = self.model_builder.model_settings
        model_selector = self.model_builder.model_selector
        self.model.currentModelChanged.connect(self.apply_model)

        # Spectral range settings
        spectral_range = model_settings.spectral_range
        spectral_range.apply.clicked.connect(self.apply_spectral_range)

        # Baseline settings
        baseline = self.model_builder.model_settings.baseline
        baseline_modes = {
        baseline.semi_auto: "Semi-Auto",
        baseline.linear: "Linear",
        baseline.polynomial: "Polynomial"
        }

        for button, mode in baseline_modes.items():
            button.toggled.connect(lambda checked, mode=mode: self.update_and_emit("baseline.mode", mode) if checked else None)
    
        baseline.slider.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.coef", value)
        )

        baseline.attached.toggled.connect(
            lambda checked: self.update_and_emit("baseline.attached", checked)
        )
        baseline.sigma.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.sigma", value)
        )
        baseline.order.valueChanged.connect(
            lambda value: self.update_and_emit("baseline.order_max", value)
        )
        baseline.apply.clicked.connect(self.applyBaseline)

        # Normalization settings
        normalization = model_settings.normalization
        normalization.normalize.toggled.connect(self.apply_normalization)
        normalization.range_min.editingFinished.connect(self.apply_normalization)
        normalization.range_max.editingFinished.connect(self.apply_normalization)

        # Fitting settings
        model_settings.fitting.peak_model.currentTextChanged.connect(self.updatePeakModel)
        model_settings.fitting.background_model.currentTextChanged.connect(lambda: print("TODO Implement me"))

        # Save model
        model_settings.save.clicked.connect(self.save_model)
        model_settings.fit.clicked.connect(self.request_fit)

        # Peaks + Baseline Table
        self.model_builder.baseline_table.baselinePointsChanged.connect(self.set_baseline_points)
        self.model_builder.bounds_chbox.stateChanged.connect(self.model_builder.peaks_table.show_bounds)
        self.model_builder.peaks_table.peaksChanged.connect(self.update_model_dict)
        self.model.baselinePointsChanged.connect(self.baselinePointsChanged)
        self.model.baselinePointsChanged.connect(self.model_builder.baseline_table.set_points)

        # Model selector
        model_selector.load_button.clicked.connect(self.load_model)
        model_selector.combo_box.currentTextChanged.connect(self.select_model)
        model_selector.apply.clicked.connect(self.apply_model)

        # Other settings
        self.solver_settings.fit_negative.toggled.connect(
            lambda checked: self.update_model_dict_with_key("fit_params.fit_negative", checked)
        )
        self.solver_settings.fit_outliers.toggled.connect(
            lambda checked: self.update_model_dict_with_key("fit_params.fit_outliers", checked)
        )
        self.solver_settings.method.currentTextChanged.connect(
            lambda text: self.update_model_dict_with_key("fit_params.method", FIT_METHODS[text])
        )
        self.solver_settings.max_ite.valueChanged.connect(
            lambda value: self.update_model_dict_with_key("fit_params.max_ite", value)
        )
        self.solver_settings.coef_noise.valueChanged.connect(
            lambda value: self.update_model_dict_with_key("fit_params.coef_noise", value)
        )
        self.solver_settings.xtol.valueChanged.connect(
            lambda value: self.update_model_dict_with_key("fit_params.xtol", value)
        )

        self.other_settings.outliers_coef.valueChanged.connect(
            lambda value: self.settingChanged.emit("outliers_coef", value)
        )
        self.other_settings.outliers_removal.clicked.connect(
            self.removeOutliers
        )

        self.other_settings.save_only_path.stateChanged.connect(
            lambda state: self.settingChanged.emit("save_only_path", state == 2)
        )

    def update_and_emit(self, key, value):
        # self.update_model_dict_with_key(key, value)
        self.setSpectrumAttr.emit(key, value)

    def update_model_dict_with_key(self, key, value):
        self.model.blockSignals(True)
        keys = key.split('.')
        current_dict = self.model.current_fit_model
        for k in keys[:-1]:
            if k not in current_dict:
                current_dict[k] = {}
            current_dict = current_dict[k]
        current_dict[keys[-1]] = value
        self.model.blockSignals(False)
    
    def set_model(self, spectrum):
        """ Set the current model to the spectrum model"""
        if isinstance(spectrum, dict):
            model = spectrum
        else:
            model = spectrum.save()
            model['baseline'].pop('y_eval')

        self.model.current_fit_model = model

    def update_model_dict(self, model_dict):
        # Uncesseray to block signals as the update occurs key by key
        for key, value in model_dict.items():
            self.model.current_fit_model[key] = value
        
        if 'peak_models' in model_dict or 'peak_label' in model_dict:
            self.setPeaks.emit(model_dict)

    def clear_model(self):
        self.model.current_fit_model = {}

    def save_model(self):
        fname = QFileDialog.getSaveFileName(None, "Save File", "", TYPES)[0]
        if fname:
            save_to_json(fname, self.model.current_fit_model)

    def load_model(self):
        fname = QFileDialog.getOpenFileName(None, "Load File", "", TYPES)[0]
        if fname:
            if fname not in self.model.fit_models:
                self.model_builder.model_selector.combo_box.addItem(fname)
                self.model.fit_models.append(fname)

            index = self.model_builder.model_selector.combo_box.findText(fname)
            self.model_builder.model_selector.combo_box.setCurrentIndex(index)
            self.select_model(fname)

    def select_model(self, fname):
        self.model.current_fit_model = load_from_json(fname)

    def apply_model(self, fit_model):
        """ Reflects the changes in the model to the GUI """
        self.model_builder.update_model(fit_model)

        points = fit_model.get('baseline', {}).get('points', [[],[]])
        self.set_baseline_points(points)
        self.update_peaks_table(fit_model)


    def set_baseline_points(self, points):
        self.model.baseline_points = points
        if points[0]:
            # Uncesseray to block signals, signals are not triggered when setting specific keys
            self.model.current_fit_model['baseline']['points'] = points

    def apply_spectral_range(self):
        spectral_range = self.model_builder.model_settings.spectral_range
        range_min = spectral_range.range_min.value()
        range_max = spectral_range.range_max.value()

        # if both are not None and range_min is >= range_max then show an error message
        if range_min is not None and range_max is not None:
            if range_min >= range_max:
                self.showToast.emit("error", "Invalid spectral range", "Minimum value must be less than maximum value")
                return
        self.update_model_dict({
            "range_min": range_min,
            "range_max": range_max
        })

        self.applySpectralRange.emit(range_min, range_max)

    def apply_normalization(self, checked=None):
        if checked is None:
            checked = self.model_builder.model_settings.normalization.normalize.isChecked()

        normalization = self.model_builder.model_settings.normalization
        range_min = normalization.range_min.value()
        range_max = normalization.range_max.value()

        if range_min is not None and range_max is not None and checked:
            if range_min >= range_max:
                self.showToast.emit("error", "Invalid normalization range", "Minimum value must be less than maximum value")
                return

        self.update_model_dict({'normalize': checked, 'normalize_range_min': range_min, 'normalize_range_max': range_max})
        self.applyNormalization.emit(checked, range_min, range_max)

    def update_peaks_table(self, spectrum):
        self.model_builder.peaks_table.clear()
        if not spectrum:
            return

        self.model.blockSignals(True)

        def extract_params(param_dict):
            return {
                "min": param_dict["min"],
                "value": param_dict["value"],
                "max": param_dict["max"],
                "vary": param_dict["vary"]
            }

        def add_row_from_params(prefix, label, model_name, params):
            x0_params = extract_params(params["x0"])
            ampli_params = extract_params(params["ampli"])
            fwhm_params = extract_params(params["fwhm"])

            row_params = {
                "prefix": prefix,
                "label": label,
                "model_name": model_name,
                "x0_min": x0_params["min"],
                "x0": x0_params["value"],
                "x0_max": x0_params["max"],
                "x0_vary": x0_params["vary"],
                "ampli_min": ampli_params["min"],
                "ampli": ampli_params["value"],
                "ampli_max": ampli_params["max"],
                "ampli_vary": ampli_params["vary"],
                "fwhm_min": fwhm_params["min"],
                "fwhm": fwhm_params["value"],
                "fwhm_max": fwhm_params["max"],
                "fwhm_vary": fwhm_params["vary"]
            }

            self.model_builder.peaks_table.add_row(**row_params)

        if isinstance(spectrum, dict):
            fit_model = spectrum
            peak_models = fit_model.get('peak_models', {})
            peak_labels = fit_model.get('peak_labels', [])

            for key, model_dict in peak_models.items():
                label = peak_labels[key]
                prefix = f'm{key+1:02d}_'
                for model_name, params in model_dict.items():
                    add_row_from_params(prefix, label, model_name, params)
        else:
            for label, model in zip(spectrum.peak_labels, spectrum.peak_models):
                add_row_from_params(model._prefix, label, model.name2, model.param_hints)
            self.set_model(spectrum)

        self.model.blockSignals(False)

    def request_fit(self):
        model_dict = self.model.current_fit_model
        self.fitRequested.emit(model_dict)