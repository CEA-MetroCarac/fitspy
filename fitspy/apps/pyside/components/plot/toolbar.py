from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib import cbook

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap, QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import (QToolButton, QMenu, QCheckBox, QWidgetAction, QRadioButton,
                               QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QLabel)

from fitspy.apps.pyside.utils import to_title_case, get_icon_path
from fitspy.apps.pyside import DEFAULTS


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


class CustomNavigationToolbar(NavigationToolbar2QT):
    def _icon(self, name):
        path_regular = cbook._get_data_path("images", name)
        path_large = path_regular.with_name(path_regular.name.replace(".png", "_large.png"))
        filename = str(path_large if path_large.exists() else path_regular)

        pm = QPixmap(filename)
        pm.setDevicePixelRatio(self.devicePixelRatioF() or 1)  # rarely, devicePixelRatioF=0
        if self.palette().color(self.backgroundRole()).value() < 128:
            icon_color = self.palette().color(self.foregroundRole())
            mask = pm.createMaskFromColor(QColor("black"), Qt.MaskMode.MaskOutColor)
            pm.fill(icon_color)
            pm.setMask(mask)
        return QIcon(pm)

    def update_icons(self):
        icon_map = {
            "Home": "home.png",
            "Back": "back.png",
            "Forward": "forward.png",
            "Pan": "move.png",
            "Zoom": "zoom_to_rect.png",
            "Subplots": "subplots.png",
            "Customize": "qt4_editor_options.png",
            "Save": "filesave.png",
        }

        # Update all icons in the toolbar
        for action in self.actions():
            icon_name = icon_map.get(action.text(), "").lower()
            if icon_name:
                action.setIcon(self._icon(icon_name))

    def is_pan_active(self):
        for action in self.actions():
            if action.text() == "Pan":
                return action.isChecked()
        return False

    def is_zoom_active(self):
        for action in self.actions():
            if action.text() == "Zoom":
                return action.isChecked()
        return False


class Toolbar(QWidget):
    def __init__(self, canvas, view_options=ViewOptions, parent=None):
        super().__init__(parent)
        self.canvas = canvas

        # Generate checkboxes dynamically from DEFAULTS
        checkboxes = [(to_title_case(key), to_title_case(key))
                      for key in DEFAULTS["view_options"].keys()]  # (text, tooltip)

        self.view_options = (None if view_options is None else view_options(checkboxes=checkboxes))
        self.initUI()
        self.setup_shortcuts()

    def initUI(self):
        hbox = QHBoxLayout()
        self.mpl_toolbar = CustomNavigationToolbar(self.canvas)
        self.baseline_radio = QRadioButton("Baseline points")
        self.peaks_radio = QRadioButton("Peaks points")
        self.highlight_radio = QRadioButton("Spectrum Sel.")
        self.copy_btn = QPushButton(icon=QIcon(get_icon_path("clipboard-copy.png")),
                                    toolTip="Copy Figure to Clipboard")
        self.copy_btn.setIconSize(QSize(24, 24))

        spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

        hbox.addWidget(self.mpl_toolbar)
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
        self.mpl_toolbar.update_icons()
