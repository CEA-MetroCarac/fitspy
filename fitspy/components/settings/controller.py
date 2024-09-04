from PySide6.QtCore import QObject, Signal
from .model import Model

class SettingsController(QObject):
    def __init__(self, model_builder):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder
        self.setup_connections()

    def setup_connections(self):
        pass