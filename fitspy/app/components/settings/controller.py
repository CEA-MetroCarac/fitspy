from PySide6.QtCore import QObject, Signal
from .model import Model

class SettingsController(QObject):
    settingChanged = Signal(str, object)
    removeOutliers = Signal()
    setSpectrumAttr = Signal(object, str, object)

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
            lambda value: self.settingChanged.emit("outliers_coef", value)
        )
        self.solver_settings.outliers_removal.clicked.connect(
            self.removeOutliers
        )

        self.export_settings.save_only_path.stateChanged.connect(
            lambda state: self.settingChanged.emit("save_only_path", state == 2)
        )
        
        # Baseline settings connections
        baseline = self.model_builder.model_settings.baseline
        baseline.slider.valueChanged.connect(
            lambda value: self.setSpectrumAttr.emit(None, "baseline.coef", value)
        )
        baseline.semi_auto.toggled.connect(
            lambda: self.setSpectrumAttr.emit(None, "baseline.mode", "Semi-Auto")
        )
        baseline.linear.toggled.connect(
            lambda: self.setSpectrumAttr.emit(None, "baseline.mode", "Linear")
        )
        baseline.polynomial.toggled.connect(
            lambda: self.setSpectrumAttr.emit(None, "baseline.mode", "Polynomial")
        )

    def set_model(self, spectrum):
        model = spectrum.save()
        self.model.current_fit_model = model

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)
