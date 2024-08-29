from PySide6.QtCore import QMetaObject
from .main_model import MainModel
from .main_view import MainView

class MainController:
    def __init__(self):

        self.view = MainView()
        self.model = MainModel()
        self.setupConnections()

    def setupConnections(self):
        QMetaObject.connectSlotsByName(self)