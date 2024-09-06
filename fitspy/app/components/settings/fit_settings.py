from PySide6.QtWidgets import QGroupBox, QGridLayout, QCheckBox, QSpinBox, QComboBox, QDoubleSpinBox, QLabel, QApplication

class FitSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Fit Algorithm settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        grid = QGridLayout()

        fit_negative_checkbox = QCheckBox("Fit negative values:")
        max_iterations_label = QLabel("Maximum iterations:")
        max_iterations_input = QSpinBox()
        fit_method_label = QLabel("Fit method:")
        fit_method_combo = QComboBox()
        fit_method_combo.addItems(["Method 1", "Method 2", "Method 3"])  # Add your fit methods here
        x_tolerance_label = QLabel("x-tolerance:")
        x_tolerance_input = QDoubleSpinBox()
        x_tolerance_input.setDecimals(6)

        grid.addWidget(fit_negative_checkbox, 0, 0, 1, 2)
        grid.addWidget(max_iterations_label, 1, 0)
        grid.addWidget(max_iterations_input, 1, 1)
        grid.addWidget(fit_method_label, 2, 0)
        grid.addWidget(fit_method_combo, 2, 1)
        grid.addWidget(x_tolerance_label, 3, 0)
        grid.addWidget(x_tolerance_input, 3, 1)

        self.setLayout(grid)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    fit_settings = FitSettings()
    fit_settings.show()

    sys.exit(app.exec())