from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel, QRadioButton, QPushButton, QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import matplotlib.cbook as cbook

project_root = Path(__file__).resolve().parent.parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class CustomNavigationToolbar(NavigationToolbar2QT):
    def _icon(self, name):
        path_regular = cbook._get_data_path('images', name)
        path_large = path_regular.with_name(
            path_regular.name.replace('.png', '_large.png'))
        filename = str(path_large if path_large.exists() else path_regular)

        pm = QPixmap(filename)
        pm.setDevicePixelRatio(
            self.devicePixelRatioF() or 1)  # rarely, devicePixelRatioF=0
        if self.palette().color(self.backgroundRole()).value() < 128:
            icon_color = self.palette().color(self.foregroundRole())
            mask = pm.createMaskFromColor(
                QColor('black'),
                Qt.MaskMode.MaskOutColor)
            pm.fill(icon_color)
            pm.setMask(mask)
        return QIcon(pm)

    def update_icons(self):
        icon_map = {
            'Home': 'home.png',
            'Back': 'back.png',
            'Forward': 'forward.png',
            'Pan': 'move.png',
            'Zoom': 'zoom_to_rect.png',
            'Subplots': 'subplots.png',
            'Customize': 'qt4_editor_options.png',
            'Save': 'filesave.png'
        }

        # Update all icons in the toolbar
        for action in self.actions():
            icon_name = icon_map.get(action.text(), '').lower()
            if icon_name:
                action.setIcon(self._icon(icon_name))

class Toolbar(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        self.mpl_toolbar = CustomNavigationToolbar(self.canvas)
        baseline_radio = QRadioButton("Baseline")
        peaks_radio = QRadioButton("Fitting")
        x_axis_label = QLabel("X-axis unit:")
        x_axis_combobox = QComboBox()
        outliers_removal_button = QPushButton("Outliers removal")
        r2_label = QLabel("R2=0")
        copy_button = QPushButton(icon=QIcon(str(icons / "copy.png")))
        copy_button.setIconSize(QSize(24, 24))

        spacer1 = QSpacerItem(20, 20)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        hbox.addWidget(self.mpl_toolbar)
        hbox.addItem(spacer1)
        hbox.addWidget(x_axis_label)
        hbox.addWidget(x_axis_combobox)
        hbox.addWidget(baseline_radio)
        hbox.addWidget(peaks_radio)
        hbox.addItem(spacer2)
        hbox.addWidget(outliers_removal_button)
        hbox.addWidget(r2_label)
        hbox.addWidget(copy_button)

        self.setLayout(hbox)

    def update_toolbar_icons(self):
        self.mpl_toolbar.update_icons()