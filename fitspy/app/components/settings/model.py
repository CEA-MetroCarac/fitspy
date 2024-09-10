from PySide6.QtCore import QObject, Signal

class Model(QObject):
    currentModelChanged = Signal(object)

    def __init__(self):
        super().__init__()
        self._current_fit_model = None

    @property
    def current_fit_model(self):
        return self._current_fit_model
    
    @current_fit_model.setter
    def current_fit_model(self, value):
        self._current_fit_model = value
        self.currentModelChanged.emit(value)