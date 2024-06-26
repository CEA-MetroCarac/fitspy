from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton

class OverallSettings(QGroupBox):
    def __init__(self):
        super().__init__("Overall Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.x_range_layout = QHBoxLayout()
        self.x_range_layout.addWidget(QLabel("X-range:"))
        self.x_range_min = QLineEdit()
        self.x_range_layout.addWidget(self.x_range_min)
        self.x_range_max = QLineEdit()
        self.x_range_layout.addWidget(self.x_range_max)
        self.layout.addLayout(self.x_range_layout)

        self.attractors_layout = QHBoxLayout()
        self.attractors = QCheckBox("Attractors")
        self.attractors_layout.addWidget(self.attractors)
        self.layout.addLayout(self.attractors_layout)

        self.outliers_layout = QHBoxLayout()
        self.calc_outliers = QPushButton("Calculate Outliers")
        self.outliers_layout.addWidget(self.calc_outliers)
        self.outliers_coeff = QLineEdit()
        self.outliers_layout.addWidget(self.outliers_coeff)
        self.layout.addLayout(self.outliers_layout)