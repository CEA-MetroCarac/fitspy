from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QGroupBox,
    QPushButton,
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
        self.fit_outliers_checkbox = QCheckBox("Fit outliers:")
        self.coef_noise_label = QLabel("Coefficient noise:")
        self.coef_noise_input = QDoubleSpinBox()
        self.max_ite_label = QLabel("Maximum iterations:")
        self.max_ite_input = QSpinBox()
        self.fit_method_label = QLabel("Fit method:")
        self.fit_method_combo = QComboBox()
        self.fit_method_combo.addItems(FIT_METHODS.keys())
        self.x_tol_label = QLabel("x-tolerance:")
        self.x_tol_input = QDoubleSpinBox()
        self.x_tol_input.setDecimals(6)

        vbox.addWidget(self.fit_negative_checkbox)
        vbox.addWidget(self.fit_outliers_checkbox)

        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.coef_noise_label)
        hbox0.addWidget(self.coef_noise_input)
        hbox0.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(hbox0)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.max_ite_label)
        hbox1.addWidget(self.max_ite_input)
        hbox1.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.fit_method_label)
        hbox2.addWidget(self.fit_method_combo)
        hbox2.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.x_tol_label)
        hbox3.addWidget(self.x_tol_input)
        hbox3.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        vbox.addLayout(hbox3)

        vbox.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(vbox)

    def update_model(self, model):
        fit_params = model['fit_params']
        
        # Find the key in FIT_METHODS that matches the value of fit_params["method"]
        method_value = fit_params['method']
        method_key = next((key for key, value in FIT_METHODS.items() if value == method_value), None)
        if method_key is not None:
            self.fit_method_combo.setCurrentText(method_key)

        self.fit_negative_checkbox.setChecked(fit_params['fit_negative'])
        self.fit_outliers_checkbox.setChecked(fit_params['fit_outliers'])
        self.max_ite_input.setValue(fit_params['max_ite'])
        self.coef_noise_input.setValue(fit_params['coef_noise'])
        self.x_tol_input.setValue(fit_params['xtol'])

class SolverSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Solver settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        hbox = QHBoxLayout()

        self.coef_label = QLabel("Coef:")
        hbox.addWidget(self.coef_label)

        self.outliers_coef = QDoubleSpinBox()
        self.outliers_coef.setRange(0.0, 100.0)
        self.outliers_coef.setSingleStep(0.1)
        hbox.addWidget(self.outliers_coef)

        self.outliers_removal = QPushButton("Outliers removal")
        self.outliers_removal.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox.addWidget(self.outliers_removal)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox.addItem(spacer)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

class MoreSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 10, 10, 10)

        self.fit_settings = FitSettings()
        self.solver_settings = SolverSettings()
        hbox.addWidget(self.fit_settings)
        hbox.addWidget(self.solver_settings)

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