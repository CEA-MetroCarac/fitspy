from PySide6.QtWidgets import (
    QSizePolicy,
    QGroupBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QSpacerItem,
    QApplication,
)

from fitspy import FIT_METHODS

class FitSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Fit Algorithm settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()

        self.fit_negative_checkbox = QCheckBox("Fit negative values:")
        self.max_iterations_label = QLabel("Maximum iterations:")
        self.max_iterations_input = QSpinBox()
        self.fit_method_label = QLabel("Fit method:")
        self.fit_method_combo = QComboBox()
        self.fit_method_combo.addItems(FIT_METHODS.keys())
        self.x_tolerance_label = QLabel("x-tolerance:")
        self.x_tolerance_input = QDoubleSpinBox()
        self.x_tolerance_input.setDecimals(6)

        vbox.addWidget(self.fit_negative_checkbox)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.max_iterations_label)
        hbox1.addWidget(self.max_iterations_input)
        hbox1.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.fit_method_label)
        hbox2.addWidget(self.fit_method_combo)
        hbox2.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.x_tolerance_label)
        hbox3.addWidget(self.x_tolerance_input)
        hbox3.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox3)

        vbox.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(vbox)

    def update_model(self, spectrum):
         # Find the key in FIT_METHODS that matches the value of spectrum.fit_params["method"]
        method_value = spectrum.fit_params["method"]
        method_key = next((key for key, value in FIT_METHODS.items() if value == method_value), None)
        if method_key is not None:
            self.fit_method_combo.setCurrentText(method_key)

        self.fit_negative_checkbox.setChecked(spectrum.fit_params["fit_negative"])
        # TODO fit_outliers
        self.max_iterations_input.setValue(spectrum.fit_params["max_ite"])
        # TODO coef_noise
        self.x_tolerance_input.setValue(spectrum.fit_params["xtol"])

class MoreSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 10, 10, 10)

        self.fit_settings = FitSettings()
        vbox.addWidget(self.fit_settings)

        self.setLayout(vbox)

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