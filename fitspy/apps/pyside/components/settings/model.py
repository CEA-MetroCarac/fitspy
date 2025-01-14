from PySide6.QtCore import QObject, Signal


class Model(QObject):
    currentModelChanged = Signal(dict)
    baselinePointsChanged = Signal(list)

    def __init__(self):
        super().__init__()
        self._current_fit_model = {}
        self._baseline_points = []
        self._backup_fit_model = None
        self._loaded_models = []

        self._create_property("current_fit_model", self.currentModelChanged)
        self._create_property("baseline_points", self.baselinePointsChanged)
        self._create_property("backup_fit_model")
        self._create_property("loaded_models")

    def _create_property(self, attr_name, signal=None):
        private_name = f"_{attr_name}"

        def getter(self):
            return getattr(self, private_name)

        def setter(self, value):
            setattr(self, private_name, value)
            if signal:
                signal.emit(value)

        setattr(self.__class__, attr_name, property(getter, setter))
