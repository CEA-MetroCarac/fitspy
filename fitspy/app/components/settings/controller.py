from PySide6.QtCore import QObject, Signal
from .model import Model

class SettingsController(QObject):
    settingChanged = Signal(str, object)
    removeOutliers = Signal()
    setSpectrumAttr = Signal(object, str, object)
    baselinePointsChanged = Signal(list)

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
        self.model_builder.baseline_table.baselinePointChanged.connect(self.update_baseline_points)
        self.other_settings.outliers_coef.valueChanged.connect(
            lambda value: self.settingChanged.emit("outliers_coef", value)
        )
        self.other_settings.outliers_removal.clicked.connect(
            self.removeOutliers
        )

        self.other_settings.save_only_path.stateChanged.connect(
            lambda state: self.settingChanged.emit("save_only_path", state == 2)
        )

        # Baseline settings connections
        baseline = self.model_builder.model_settings.baseline
        baseline.slider.valueChanged.connect(
            lambda value: self.setSpectrumAttr.emit(None, "baseline.coef", value)
        )
        baseline.semi_auto.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit(None, "baseline.mode", "Semi-Auto") if checked else None
        )
        baseline.linear.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit(None, "baseline.mode", "Linear") if checked else None
        )
        baseline.polynomial.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit(None, "baseline.mode", "Polynomial") if checked else None
        )
        baseline.attached.toggled.connect(
            lambda checked: self.setSpectrumAttr.emit(None, "baseline.attached", checked)
        )

    def set_model(self, spectrum):
        model = spectrum.save()
        self.model.current_fit_model = model

    def update_model(self, fit_model):
        self.model_builder.update_model(fit_model)
        self.fit_settings.update_model(fit_model)
        print("UPDATING MODEL")
        self.set_baseline_points(fit_model['baseline']['points'])

    def set_baseline_points(self, points):
        self.model.baseline_points = points

    def update_baseline_points(self, index, x, y):
        baseline_points = self.model.baseline_points
        baseline_points[0][index] = x
        baseline_points[1][index] = y

        # Combine the X and Y values into a list of tuples
        points = list(zip(baseline_points[0], baseline_points[1]))

        # Sort the list of tuples by the X values
        points.sort(key=lambda point: point[0])

        # Separate the sorted tuples back into the X and Y lists
        sorted_x, sorted_y = zip(*points)

        self.model.baseline_points = [list(sorted_x), list(sorted_y)]