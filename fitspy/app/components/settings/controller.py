import json
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from .model import Model


class SettingsController(QObject):
    def __init__(self, model_builder, fit_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder
        self.fit_settings = fit_settings
        self.setup_connections()

    def setup_connections(self):
        self.model.currentModelChanged.connect(self.update_model)

        model_settings = self.model_builder.model_settings
        model_settings.save_button.clicked.connect(self.save_model_settings)

    def set_model(self, spectrum):
        self.model.current_fit_model = spectrum

    def update_model(self, spectrum):
        self.model_builder.update_model(spectrum)
        self.fit_settings.update_model(spectrum)

    def save_model_settings(self):
        spectral_range = self.model_builder.model_settings.spectral_range
        baseline = self.model_builder.model_settings.baseline
        normalization = self.model_builder.model_settings.normalization
        fitting = self.model_builder.model_settings.fitting

        params = {}

        params['spectral_range'] = {
            'x_min': spectral_range.x_min.value(),
            'x_max': spectral_range.x_max.value()}

        params['baseline'] = {
            'semi_auto': baseline.radio_semi_auto.isChecked(),
            'linear': baseline.radio_linear.isChecked(),
            'polynomial': baseline.radio_polynomial.isChecked(),
            'polynomial_order': baseline.spin_polynomial_order.value(),
            'attached': baseline.attached.isChecked(),
            'sigma': baseline.spin_sigma.value()}

        params['normalization'] = {
            'x_min': normalization.x_min.value(),
            'x_max': normalization.x_max.value(),
            'normalize': normalization.normalize.isChecked()}

        params['fit_models'] = {
            'background_model': fitting.background_model.currentText(),
            'peak_model': fitting.peak_model.currentText()}

        params['fit_settings'] = {
            'fit_negative': self.fit_settings.fit_negative_checkbox.isChecked(),
            'fit_outliers': self.fit_settings.fit_outliers_checkbox.isChecked(),
            'coef_noise': self.fit_settings.coef_noise_input.value(),
            'max_iterations': self.fit_settings.max_iterations_input.value(),
            'method': self.fit_settings.fit_method_combo.currentText(),
            'xtol': self.fit_settings.xtol_input.value()}

        types = "JSON Files (*.json);;All Files (*)"
        fname = QFileDialog.getSaveFileName(None, "Save File", "", types)[0]
        if fname:
            with open(fname, 'w') as file:
                json.dump(params, file, indent=4)
