from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget

from fitspy.apps.pyside.utils import get_icon_path


class MenuBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.actionManual = QAction(self, icon=QIcon(get_icon_path("manual.png")),
                                    toolTip="Manual")
        self.actionTheme = QAction(self, icon=QIcon(get_icon_path("dark-light.png")),
                                    toolTip="Switch between dark and light mode")
        self.actionAbout = QAction(self, icon=QIcon(get_icon_path("about.png")),
                                   toolTip="About")
        self.actionOpen = QAction(self, icon=QIcon(get_icon_path("icons8-folder-96.png")),
                                  toolTip="Open spectra data, saved work or Excel file (Ctrl+O)",
                                  shortcut="Ctrl+O")
        self.actionSave = QAction(self, icon=QIcon(get_icon_path("save.png")),
                                  toolTip="Save current work (Ctrl+S)", shortcut="Ctrl+S")
        self.actionSaveData = QAction(self, icon=QIcon(get_icon_path("save_data.png")),
                                      toolTip="Save current work with data (Ctrl+Shift+S)",
                                      shortcut="Ctrl+Shift+S")
        self.actionClearEnv = QAction(self, icon=QIcon(get_icon_path("clear.png")),
                                      toolTip="Clear the environment (Ctrl+Shift+C)",
                                      shortcut="Ctrl+Shift+C")
        self.actionRestoreDefaults = QAction(self, icon=QIcon(get_icon_path("reinit_settings.png")),
                                             toolTip="Restore default settings")

        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(16777215, 50))
        self.setMovable(True)
        self.setIconSize(QSize(30, 30))
        self.setFloatable(False)

        actions = [
            self.actionOpen,
            self.actionSave,
            self.actionSaveData,
            self.actionClearEnv,
            self.actionRestoreDefaults,
            None,  # Separator
            QWidget(self),  # Spacer
            self.actionTheme,
            None,  # Separator
            self.actionManual,
            self.actionAbout,
        ]

        for action in actions:
            if action is None:
                self.addSeparator()
            elif isinstance(action, QWidget):
                action.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.addWidget(action)
            else:
                self.addAction(action)
