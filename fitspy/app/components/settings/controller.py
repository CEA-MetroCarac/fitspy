from PySide6.QtCore import QObject, Signal
from .model import Model

class SettingsController(QObject):
    outliersCoefChanged = Signal(float)
    removeOutliers = Signal()

    def __init__(self, model_builder, more_settings):
        super().__init__()
        self.model = Model()
        self.model_builder = model_builder

        self.more_settings = more_settings
        self.fit_settings = more_settings.fit_settings
        self.solver_settings = more_settings.solver_settings
        self.setup_connections()

    def setup_connections(self):
        self.model.currentModelChanged.connect(self.update_model)
        self.solver_settings.outliers_coef.valueChanged.connect(self.outliersCoefChanged)
        self.solver_settings.outliers_removal.clicked.connect(self.removeOutliers)

    def set_model(self, spectrum):
        model = spectrum.save()
        self.model.current_fit_model = model

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)