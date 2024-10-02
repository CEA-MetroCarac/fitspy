from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QGroupBox,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
    QLabel,
    QSpacerItem,
    QApplication,
)

from fitspy import FIT_METHODS, DEFAULTS
from .custom_spinbox import SpinBox, DoubleSpinBox

class FitSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Fit Solver Settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()

        self.fit_negative = QCheckBox("Fit negative values:")
        self.fit_negative.setChecked(DEFAULTS["fit_params"]["fit_negative"])

        self.fit_outliers = QCheckBox("Fit outliers:")
        self.fit_outliers.setChecked(DEFAULTS["fit_params"]["fit_outliers"])

        self.coef_noise_label = QLabel("Coefficient noise:")
        self.coef_noise = DoubleSpinBox()
        self.coef_noise.setValue(DEFAULTS["fit_params"]["coef_noise"])

        self.max_ite_label = QLabel("Maximum iterations:")
        self.max_ite = SpinBox()
        self.max_ite.setValue(DEFAULTS["fit_params"]["max_ite"])

        self.method_label = QLabel("Fit method:")
        self.method = QComboBox()
        self.method.addItems(FIT_METHODS.keys())
        self.method.setCurrentText(DEFAULTS["fit_params"]["method"])

        self.xtol_label = QLabel("x-tolerance:")
        self.xtol = DoubleSpinBox()
        self.xtol.setDecimals(6)
        self.xtol.setValue(DEFAULTS["fit_params"]["xtol"])

        vbox.addWidget(self.fit_negative)
        vbox.addWidget(self.fit_outliers)

        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.coef_noise_label)
        hbox0.addWidget(self.coef_noise)
        spacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        hbox0.addItem(spacer)
        vbox.addLayout(hbox0)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.max_ite_label)
        hbox1.addWidget(self.max_ite)
        hbox1.addItem(spacer)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.method_label)
        hbox2.addWidget(self.method)
        hbox2.addItem(spacer)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.xtol_label)
        hbox3.addWidget(self.xtol)
        hbox3.addItem(spacer)
        vbox.addLayout(hbox3)

        vbox.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(vbox)

class OtherSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Other settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        hbox = QHBoxLayout()

        self.coef_label = QLabel("Coef:")
        hbox.addWidget(self.coef_label)

        self.outliers_coef = DoubleSpinBox()
        self.outliers_coef.setRange(0.0, 100.0)
        self.outliers_coef.setSingleStep(0.1)
        hbox.addWidget(self.outliers_coef)

        self.outliers_removal = QPushButton("Outliers removal")
        self.outliers_removal.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox.addWidget(self.outliers_removal)

        hbox_2 = QHBoxLayout()
        self.save_only_path = QCheckBox("Save spectrum file path only", toolTip="If unchecked, saves the spectrum data")
        hbox_2.addWidget(self.save_only_path)

        vbox.addLayout(hbox)
        vbox.addLayout(hbox_2)
        self.setLayout(vbox)

class MoreSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 10, 10, 10)

        self.fit_settings = FitSettings()
        self.other_settings = OtherSettings()
        hbox.addWidget(self.fit_settings)
        hbox.addWidget(self.other_settings)

        self.setLayout(hbox)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)

    more_settings = MoreSettings()
    main_layout.addWidget(more_settings)

    main_widget.setLayout(main_layout)
    main_widget.show()

    sys.exit(app.exec())