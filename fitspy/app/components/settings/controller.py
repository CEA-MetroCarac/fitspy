from PySide6.QtCore import QObject, Signal
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

    def set_model(self, spectrum):
        model = spectrum.save()
        self.model.current_fit_model = model

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)
