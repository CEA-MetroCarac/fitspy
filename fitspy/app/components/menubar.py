from pathlib import Path
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSizePolicy, QToolBar, QWidget
from PySide6.QtCore import QSize

project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class MenuBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.actionManual = QAction(
            self,
            icon=QIcon(str(icons / "manual.png")),
            toolTip="Manual",
        )
        self.actionDarkMode = QAction(
            self,
            icon=QIcon(str(icons / "dark.png")),
            toolTip="Dark Mode",
        )
        self.actionLightMode = QAction(
            self,
            icon=QIcon(str(icons / "light-mode.svg")),
            toolTip="Light Mode",
        )
        self.actionAbout = QAction(
            self,
            icon=QIcon(str(icons / "about.png")),
            toolTip="About",
        )
        self.actionOpen = QAction(
            self,
            icon=QIcon(str(icons / "icons8-folder-96.png")),
            toolTip="Open spectra data, saved work or Excel file",
        )
        self.actionSave = QAction(
            self,
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save current work",
        )
        self.actionClearEnv = QAction(
            self,
            icon=QIcon(str(icons / "clear.png")),
            toolTip="Clear the environment",
        )
        self.actionRestoreDefaults = QAction(
            self,
            icon=QIcon(str(icons / "reinit_settings.png")),
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