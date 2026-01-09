from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (QToolButton, QMenu, QCheckBox, QWidgetAction, QRadioButton,
                               QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QLabel)

from fitspy.apps.pyside.utils import to_title_case, get_icon_path
from fitspy.apps.pyside import DEFAULTS
from fitspy.apps.pyside.components.plot.abstractions import PlotNavigation


class ViewOptions(QToolButton):
    def __init__(self, checkboxes, parent=None):
        super(ViewOptions, self).__init__(parent)
        self.setText("View Options")
        self.setPopupMode(QToolButton.InstantPopup)
        self.checkboxes_definitions = checkboxes
        self.initUI()

    def initUI(self):
        self.menu = QMenu(self)
        self.setMenu(self.menu)

        self.checkboxes = {}
        for text, tooltip in self.checkboxes_definitions:
            checkbox = QCheckBox(text)
            checkbox.setToolTip(tooltip)
            action = QWidgetAction(self)
            action.setDefaultWidget(checkbox)
            self.menu.addAction(action)
            self.checkboxes[text] = checkbox

    def get_view_options(self):
        return {text: checkbox.isChecked() for text, checkbox in self.checkboxes.items()}


class Toolbar(QWidget):
    def __init__(self, navigation: PlotNavigation | None, view_options=ViewOptions, parent=None):
        super().__init__(parent)
        self.navigation = navigation

        # Generate checkboxes dynamically from DEFAULTS
        checkboxes = [(to_title_case(key), to_title_case(key))
                      for key in DEFAULTS["view_options"].keys()]  # (text, tooltip)

        self.view_options = (None if view_options is None else view_options(checkboxes=checkboxes))
        self.initUI()
        self.setup_shortcuts()

    def initUI(self):
        hbox = QHBoxLayout()
        navigation_widget = None if self.navigation is None else self.navigation.widget()
        self.baseline_radio = QRadioButton("Baseline points")
        self.peaks_radio = QRadioButton("Peaks points")
        self.highlight_radio = QRadioButton("Spectrum Sel.")
        self.copy_btn = QPushButton(icon=QIcon(get_icon_path("clipboard-copy.png")),
                                    toolTip="Copy Figure to Clipboard")
        self.copy_btn.setIconSize(QSize(24, 24))

        spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

        if navigation_widget is not None:
            hbox.addWidget(navigation_widget)
        hbox.addItem(spacer1)
        hbox.addWidget(QLabel('Click Mode:'))
        hbox.addWidget(self.baseline_radio)
        hbox.addWidget(self.peaks_radio)
        hbox.addWidget(self.highlight_radio)
        hbox.addItem(spacer2)
        if self.view_options:
            hbox.addWidget(self.view_options)
        hbox.addWidget(self.copy_btn)

        self.setLayout(hbox)

    def setup_shortcuts(self):
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        copy_shortcut.activated.connect(self.copy_btn.click)

    def get_selected_radio(self):
        if self.baseline_radio.isChecked():
            return "baseline"
        elif self.peaks_radio.isChecked():
            return "peaks"
        elif self.highlight_radio.isChecked():
            return "highlight"
        return None

    def update_toolbar_icons(self):
        if self.navigation is None:
            return

        widget = self.navigation.widget()
        if hasattr(widget, "update_icons"):
            widget.update_icons()
