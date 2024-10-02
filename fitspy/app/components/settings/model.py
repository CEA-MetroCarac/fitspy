from PySide6.QtCore import QObject, Signal


class Model(QObject):
    currentModelChanged = Signal(dict)
    baselinePointsChanged = Signal(list)

    def __init__(self):
        super().__init__()
        self._current_fit_model = None
        self._fit_models = []
        self._baseline_points = []

    @property
    def current_fit_model(self):
        return self._current_fit_model

    @current_fit_model.setter
    def current_fit_model(self, fit_model):
        self._current_fit_model = fit_model
        self.currentModelChanged.emit(fit_model)

    @property
    def baseline_points(self):
        return self._baseline_points
    
    @baseline_points.setter
    def baseline_points(self, points):
        self._baseline_points = points
        self.baselinePointsChanged.emit(points)

    @property
    def fit_models(self):
        return self._fit_models

    @fit_models.setter
    def fit_models(self, fit_models):
        self._fit_models = fit_models
