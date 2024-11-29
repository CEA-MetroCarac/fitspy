from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget
from PySide6.QtCore import QSize

from fitspy.core import get_icon_path

class MenuBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.actionManual = QAction(
            self,
            icon=QIcon(get_icon_path("manual.png")),
            toolTip="Manual",
        )
        self.actionDarkMode = QAction(
            self,
            icon=QIcon(get_icon_path("dark.png")),
            toolTip="Dark Mode",
        )
        self.actionLightMode = QAction(
            self,
            icon=QIcon(get_icon_path("light-mode.png")),
            toolTip="Light Mode",
        )
        self.actionAbout = QAction(
            self,
            icon=QIcon(get_icon_path("about.png")),
            toolTip="About",
        )
        self.actionOpen = QAction(
            self,
            icon=QIcon(get_icon_path("icons8-folder-96.png")),
            toolTip="Open spectra data, saved work or Excel file (Ctrl+O)",
            shortcut="Ctrl+O",
        )
        self.actionSave = QAction(
            self,
            icon=QIcon(get_icon_path("save.png")),
            toolTip="Save current work (Ctrl+S)",
            shortcut="Ctrl+S",
        )
        self.actionClearEnv = QAction(
            self,
            icon=QIcon(get_icon_path("clear.png")),
            toolTip="Clear the environment (Ctrl+Shift+C)",
            shortcut="Ctrl+Shift+C",
            
        )
        self.actionRestoreDefaults = QAction(
            self,
            icon=QIcon(get_icon_path("reinit_settings.png")),
            toolTip="Restore default settings",
        )

        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(16777215, 50))
        self.setMovable(True)
        self.setIconSize(QSize(30, 30))
        self.setFloatable(False)

        actions = [
            self.actionOpen, self.actionSave, self.actionClearEnv, self.actionRestoreDefaults,
            None,  # Separator
            QWidget(self),  # Spacer
            self.actionDarkMode, self.actionLightMode,
            None,  # Separator
            self.actionManual, self.actionAbout,
        ]

        for action in actions:
            if action is None:
                self.addSeparator()
            elif isinstance(action, QWidget):
                action.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.addWidget(action)
            else:
                self.addAction(action)