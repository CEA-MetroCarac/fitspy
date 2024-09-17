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
        fit_model = self.model.current_fit_model
        fit_model.pop("fname")
        fname = QFileDialog.getSaveFileName(None, "Save File", "", TYPES)[0]
        if fname:
            save_to_json(fname, fit_model)

    def load_model(self):
        fname = QFileDialog.getOpenFileName(None, "Load File", "", TYPES)[0]
        if fname:
            self.model_builder.model_selector.fit_models.append(fname)
            self.model_builder.model_selector.combo_box.addItem(fname)

    def select_model(self, fname_json):
        self.model.current_fit_model = load_from_json(fname_json)

    def apply_model(self):
        pass
