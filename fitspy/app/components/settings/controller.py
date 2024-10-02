import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from .model import Model
from fitspy.core.utils import save_to_json, load_from_json

TYPES = "JSON Files (*.json);;All Files (*)"


class SettingsController(QObject):
    settingChanged = Signal(str, object)
    removeOutliers = Signal()

    def __init__(self, model_builder, more_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder
        self.more_settings = more_settings
        self.fit_settings = more_settings.fit_settings
        self.solver_settings = more_settings.solver_settings
        self.export_settings = more_settings.export_settings
        self.setup_connections()

    def setup_connections(self):
        self.model.currentModelChanged.connect(self.update_model)

        self.solver_settings.outliers_coef.valueChanged.connect(
            lambda value: self.settingChanged.emit("outliers_coef", value))
        self.solver_settings.outliers_removal.clicked.connect(
            self.removeOutliers)

        self.export_settings.save_only_path.stateChanged.connect(
            lambda state: self.settingChanged.emit("save_only_path", state == 2)
        )

        model_settings = self.model_builder.model_settings
        model_selector = self.model_builder.model_selector
        model_settings.save_button.clicked.connect(self.save_model)
        model_selector.load_button.clicked.connect(self.load_model)
        model_selector.combo_box.currentTextChanged.connect(self.select_model)
        model_selector.apply_button.clicked.connect(self.apply_model)

    def set_model(self, spectrum):
        model = spectrum.save()
        self.model.current_fit_model = model

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)

    def save_model(self):
        spectral_range = self.model_builder.model_settings.spectral_range
        baseline = self.model_builder.model_settings.baseline
        baseline_mode = baseline.button_group.checkedButton()
        normalization = self.model_builder.model_settings.normalization
        fitting = self.model_builder.model_settings.fitting

        params_baseline = {
            'mode': baseline_mode.text() if baseline_mode else None,
            'coef': baseline.slider.value(),
            'points': [[], []],
            'order_max': baseline.spin_poly_order.value(),
            'attached': baseline.attached.isChecked(),
            'sigma': baseline.spin_sigma.value()}

        params_fit = {
            'method': self.fit_settings.fit_method_combo.currentText(),
            'fit_negative': self.fit_settings.fit_negative_checkbox.isChecked(),
            'fit_outliers': self.fit_settings.fit_outliers_checkbox.isChecked(),
            'coef_noise': self.fit_settings.coef_noise_input.value(),
            'max_ite': self.fit_settings.max_ite_input.value(),
            'xtol': self.fit_settings.xtol_input.value()}

        params_tot = {
            'range_min': spectral_range.range_min.value(),
            'range_max': spectral_range.range_max.value(),
            'normalize': normalization.normalize.isChecked(),
            'normalize_range_min': normalization.range_min.value(),
            'normalize_range_max': normalization.range_max.value(),
            'baseline': params_baseline,
            'fit_params': params_fit,
            'background_model': fitting.background_model.currentText(),
            'peak_labels': [],
            'peak_models': {},
        }

        fname = QFileDialog.getSaveFileName(None, "Save File", "", TYPES)[0]
        if fname:
            save_to_json(fname, params_tot)

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

    def apply_model(self):
        pass
