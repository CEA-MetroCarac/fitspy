from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QLabel, QRadioButton, QPushButton, QSpacerItem, QSizePolicy

project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class Toolbar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        placeholder_label = QLabel("Placeholder matplotlib toolbar")
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

        hbox.addWidget(placeholder_label)
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

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    toolbar = Toolbar()
    toolbar.show()

    sys.exit(app.exec())