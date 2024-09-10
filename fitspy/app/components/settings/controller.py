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
        self.model.current_fit_model = spectrum

    def update_model(self, spectrum):
        self.model_builder.update_model(spectrum)
        self.fit_settings.update_model(spectrum)
