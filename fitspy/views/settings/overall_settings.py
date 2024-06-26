from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton
from .float_input import FloatInput

class OverallSettings(QGroupBox):
    def __init__(self):
        super().__init__("Overall Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.x_range_layout = QHBoxLayout()
        self.x_range_layout.addWidget(QLabel("X-range:"))
        self.x_range_min = FloatInput()
        self.x_range_layout.addWidget(self.x_range_min)
        self.x_range_max = FloatInput()
        self.x_range_layout.addWidget(self.x_range_max)
        self.x_range_apply = QPushButton("Apply to all")
        self.x_range_layout.addWidget(self.x_range_apply)
        self.layout.addLayout(self.x_range_layout)

        self.attractors_layout = QHBoxLayout()
        self.attractors = QCheckBox("Attractors")
        self.attractors_layout.addWidget(self.attractors)
        self.attractors_settings = QPushButton("Attractors Settings")
        self.attractors_layout.addWidget(self.attractors_settings)
        self.layout.addLayout(self.attractors_layout)

        self.outliers_layout = QHBoxLayout()
        self.calc_outliers = QPushButton("Outliers Calc.")
        self.outliers_layout.addWidget(self.calc_outliers)
        self.outliers_coeff = FloatInput()
        self.outliers_layout.addWidget(QLabel("Coef:"))
        self.outliers_layout.addWidget(self.outliers_coeff)
        self.layout.addLayout(self.outliers_layout)