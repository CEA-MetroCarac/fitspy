from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QCheckBox, QPushButton, QFormLayout
from PySide6.QtCore import Signal
from .float_input import FloatInput

class AttractorsSettingsDialog(QDialog):
    params_updated = Signal(dict)
    toggle_element_visibility = Signal(str)

    def __init__(self, attractors_settings, enabled):
        super().__init__()
        self.setWindowTitle("Attractors Settings")
        self.enabled = enabled
        layout = QFormLayout()

        # Create and add settings fields
        self.distance_input = FloatInput(default=attractors_settings["distance"], label="Distance:")
        layout.addRow(self.distance_input)

        self.prominence_input = FloatInput(label="Prominence:")
        self.prominence_input.setValue(attractors_settings["prominence"])
        layout.addRow(self.prominence_input)

        self.width_input = FloatInput(label="Width:")
        self.width_input.setValue(attractors_settings["width"])
        layout.addRow(self.width_input)

        self.height_input = FloatInput(label="Height:")
        self.height_input.setValue(attractors_settings["height"])
        layout.addRow(self.height_input)

        self.threshold_input = FloatInput(label="Threshold:")
        self.threshold_input.setValue(attractors_settings["threshold"])
        layout.addRow(self.threshold_input)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.update_parameters)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def update_parameters(self):
        enabled = self.enabled()
        params = {
        "attractors": {
            "distance": self.distance_input.value(),
            "prominence": self.prominence_input.value(),
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "threshold": self.threshold_input.value(),
            "enabled": enabled
        }
    }
        self.params_updated.emit(params)
        self.accept()

class OverallSettings(QGroupBox):
    def __init__(self, settings):
        super().__init__("Overall Settings")
        attractors_settings = settings["attractors"]
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.attractors_layout = QHBoxLayout()
        self.attractors = QCheckBox("Attractors")
        self.attractors.setChecked(attractors_settings["enabled"])

        # Create the dialog once and keep it for toggling visibility
        self.attractors_settings_dialog = AttractorsSettingsDialog(attractors_settings, self.attractors.isChecked)
        self.attractors_settings_dialog.setVisible(False)

        self.attractors.stateChanged.connect(lambda: self.attractors_settings_dialog.toggle_element_visibility.emit("attractors"))
        self.attractors_layout.addWidget(self.attractors)
        self.attractors_settings = QPushButton("Attractors Settings")
        self.attractors_settings.clicked.connect(self.toggle_attractors_settings_dialog)
        self.attractors_layout.addWidget(self.attractors_settings)
        self.layout.addLayout(self.attractors_layout)

        self.outliers_layout = QHBoxLayout()
        self.calc_outliers = QPushButton("Outliers Calc.")
        self.outliers_layout.addWidget(self.calc_outliers)
        self.outliers_coeff = FloatInput(default=settings["outliers"]["coef"], step=0.1, label="Coef:")
        self.outliers_layout.addWidget(self.outliers_coeff)
        self.layout.addLayout(self.outliers_layout)

    def toggle_attractors_settings_dialog(self):
        # Toggle the visibility of the dialog
        if self.attractors_settings_dialog.isVisible():
            self.attractors_settings_dialog.setVisible(False)
        else:
            self.attractors_settings_dialog.exec_()  # Use exec_() to make it modal if needed