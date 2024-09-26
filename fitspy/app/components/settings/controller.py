from PySide6.QtCore import QObject, Signal
from .model import Model

class SettingsController(QObject):
    settingChanged = Signal(str, object)
    removeOutliers = Signal()
    setSpectrumAttr = Signal(str, object)
    baselinePointsChanged = Signal(list)
    applyBaseline = Signal()
    applySpectralRange = Signal(float, float)
    applyNormalization = Signal(bool, object, object)
    updatePeakModel = Signal(str)
    showToast = Signal(str, str, str)

    def __init__(self, model_builder, more_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder

        self.more_settings = more_settings
        self.fit_settings = more_settings.fit_settings
        self.other_settings = more_settings.other_settings
        self.setup_connections()

    def setup_connections(self):
        self.model.currentModelChanged.connect(self.update_model)
        self.model.baselinePointsChanged.connect(self.baselinePointsChanged)
        self.model.baselinePointsChanged.connect(self.model_builder.baseline_table.set_points)
        self.model_builder.baseline_table.baselinePointsChanged.connect(self.set_baseline_points)
        self.model_builder.bounds_chbox.stateChanged.connect(self.model_builder.peaks_table.show_bounds)

        self.model_builder.model_settings.fitting.peak_model_combo.currentTextChanged.connect(self.updatePeakModel)
        self.model_builder.model_settings.fitting.bkg_model_combo.currentTextChanged.connect(lambda: print("TODO Implement me"))
        self.other_settings.outliers_coef.valueChanged.connect(
            lambda value: self.settingChanged.emit("outliers_coef", value)
        )
        self.other_settings.outliers_removal.clicked.connect(
            self.removeOutliers
        )

        self.other_settings.save_only_path.stateChanged.connect(
            lambda state: self.settingChanged.emit("save_only_path", state == 2)
        )

        # Spectral range settings connections
        spectral_range = self.model_builder.model_settings.spectral_range
        spectral_range.apply.clicked.connect(self.apply_spectral_range)

        # Baseline settings connections
        baseline = self.model_builder.model_settings.baseline
        baseline.slider.valueChanged.connect(
            lambda value: self.setSpectrumAttr.emit("baseline.coef", value)
        )
        baseline.semi_auto.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit("baseline.mode", "Semi-Auto") if checked else None
        )
        baseline.linear.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit("baseline.mode", "Linear") if checked else None
        )
        baseline.polynomial.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit("baseline.mode", "Polynomial") if checked else None
        )
        baseline.attached.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit("baseline.attached", checked)
        )
        baseline.sigma.valueChanged.connect(
            lambda value: self.setSpectrumAttr.emit("baseline.sigma", value)
        )
        baseline.order.valueChanged.connect(
            lambda value: self.setSpectrumAttr.emit("baseline.order_max", value)
        )
        baseline.apply.clicked.connect(self.applyBaseline)

        # Normalization settings connections
        normalization = self.model_builder.model_settings.normalization
        normalization.normalize.toggled.connect(self.apply_normalization)
        normalization.range_min.editingFinished.connect(self.apply_normalization)
        normalization.range_max.editingFinished.connect(self.apply_normalization)

    def set_model(self, spectrum):
        if isinstance(spectrum, dict):
            model = spectrum
        else:
            model = spectrum.save()
            
        self.model.current_fit_model = model

    def clear_model(self):
        self.model.current_fit_model = None

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)
        print("UPDATING MODEL")
        
        points = fit_model.get('baseline', {}).get('points', [[],[]])
        self.set_baseline_points(points)
        self.update_peaks_table(fit_model)

    def set_baseline_points(self, points):
        self.model.baseline_points = points
        if points[0]:
            self.model.blockSignals(True)
            self.model.current_fit_model['baseline']['points'] = points
            self.model.blockSignals(False)

    def apply_spectral_range(self):
        spectral_range = self.model_builder.model_settings.spectral_range
        range_min = spectral_range.range_min.value()
        range_max = spectral_range.range_max.value()

        # if both are not None and range_min is >= range_max then show an error message
        if range_min is not None and range_max is not None:
            if range_min >= range_max:
                self.showToast.emit("Error", "Invalid spectral range", "Minimum value must be less than maximum value")
                return

        self.applySpectralRange.emit(range_min, range_max)

    def apply_normalization(self, checked=None):
        if checked is None:
            checked = self.model_builder.model_settings.normalization.normalize.isChecked()

        normalization = self.model_builder.model_settings.normalization
        range_min = normalization.range_min.value()
        range_max = normalization.range_max.value()

        if range_min is not None and range_max is not None and checked:
            if range_min >= range_max:
                self.showToast.emit("Error", "Invalid normalization range", "Minimum value must be less than maximum value")
                return

        self.applyNormalization.emit(checked, range_min, range_max)

    def update_peaks_table(self, spectrum):
        self.model_builder.peaks_table.clear()
        if not spectrum:
            return

        self.model.blockSignals(True)

        def add_row(prefix, label, model_name, x0, ampli, fwhm):
            self.model_builder.peaks_table.add_row(prefix, label, model_name, x0, ampli, fwhm)

        if isinstance(spectrum, dict):
            fit_model = spectrum
            peak_models = fit_model.get('peak_models', {})
            peak_labels = fit_model.get('peak_labels', [])

            for key, model_dict in peak_models.items():
                label = peak_labels[key]
                for model_name, params in model_dict.items():
                    prefix = f'm{key+1:02d}_'
                    x0 = params["x0"]["value"]
                    ampli = params["ampli"]["value"]
                    fwhm = params["fwhm"]["value"]
                    add_row(prefix, label, model_name, x0, ampli, fwhm)
        else:
            for label, model in zip(spectrum.peak_labels, spectrum.peak_models):
                x0 = model.param_hints["x0"]["value"]
                ampli = model.param_hints["ampli"]["value"]
                fwhm = model.param_hints["fwhm"]["value"]
                model_name = model.name2
                prefix = model._prefix
                add_row(prefix, label, model_name, x0, ampli, fwhm)

            self.set_model(spectrum)

        self.model.blockSignals(False)