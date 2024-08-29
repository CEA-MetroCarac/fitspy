from PySide6.QtCore import QMetaObject, QObject
from .main_model import MainModel
from .main_view import MainView

class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.view = MainView()
        self.model = MainModel()
        self.setupConnections()

    def setupConnections(self):
        QMetaObject.connectSlotsByName(self)