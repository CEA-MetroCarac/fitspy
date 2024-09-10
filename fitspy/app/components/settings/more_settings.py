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

class FitSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Fit Algorithm settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()

        fit_negative_checkbox = QCheckBox("Fit negative values:")
        max_iterations_label = QLabel("Maximum iterations:")
        max_iterations_input = QSpinBox()
        fit_method_label = QLabel("Fit method:")
        fit_method_combo = QComboBox()
        fit_method_combo.addItems(["Method 1", "Method 2", "Method 3"])  # Add your fit methods here
        x_tolerance_label = QLabel("x-tolerance:")
        x_tolerance_input = QDoubleSpinBox()
        x_tolerance_input.setDecimals(6)

        vbox.addWidget(fit_negative_checkbox)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(max_iterations_label)
        hbox1.addWidget(max_iterations_input)
        hbox1.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(fit_method_label)
        hbox2.addWidget(fit_method_combo)
        hbox2.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(x_tolerance_label)
        hbox3.addWidget(x_tolerance_input)
        hbox3.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        vbox.addLayout(hbox3)

        vbox.addItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(vbox)

class MoreSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 10, 10, 10)

        fit_settings = FitSettings()
        vbox.addWidget(fit_settings)

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