from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QDialog, QCheckBox, QPushButton, QFormLayout
from PySide6.QtCore import Signal
from .float_input import FloatInput

class AttractorsSettingsDialog(QDialog):
    parametersUpdated = Signal(dict)

    def __init__(self, attractors_settings, enabled):
        super().__init__()
        self.setWindowTitle("Attractors Settings")
        self.enabled = enabled
        layout = QFormLayout()

        # Create and add settings fields
        self.distance_input = FloatInput()
        self.distance_input.setValue(attractors_settings["distance"])
        layout.addRow("Distance:", self.distance_input)

        self.prominence_input = FloatInput()
        self.prominence_input.setValue(attractors_settings["prominence"])
        layout.addRow("Prominence:", self.prominence_input)

        self.width_input = FloatInput()
        self.width_input.setValue(attractors_settings["width"])
        layout.addRow("Width:", self.width_input)

        self.height_input = FloatInput()
        self.height_input.setValue(attractors_settings["height"])
        layout.addRow("Height:", self.height_input)

        self.threshold_input = FloatInput()
        self.threshold_input.setValue(attractors_settings["threshold"])
        layout.addRow("Threshold:", self.threshold_input)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.update_parameters)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def update_parameters(self):
        enabled = self.enabled()
        params = {
        "attractors_params": {
            "distance": self.distance_input.value(),
            "prominence": self.prominence_input.value(),
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "threshold": self.threshold_input.value(),
            "enabled": enabled
        }
    }
        self.parametersUpdated.emit(params)
        self.accept()

class OverallSettings(QGroupBox):
    def __init__(self, attractors_settings):
        super().__init__("Overall Settings")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.attractors_layout = QHBoxLayout()
        self.attractors = QCheckBox("Attractors")
        self.attractors.setChecked(attractors_settings["enabled"])
        self.attractors.stateChanged.connect(lambda state: self.update_attractors_enabled(state))
        self.attractors_layout.addWidget(self.attractors)
        self.attractors_settings = QPushButton("Attractors Settings")
        self.attractors_settings.clicked.connect(self.toggle_attractors_settings_dialog)
        self.attractors_layout.addWidget(self.attractors_settings)
        self.layout.addLayout(self.attractors_layout)

        self.outliers_layout = QHBoxLayout()
        self.calc_outliers = QPushButton("Outliers Calc.")
        self.outliers_layout.addWidget(self.calc_outliers)
        self.outliers_coeff = FloatInput()
        self.outliers_layout.addWidget(QLabel("Coef:"))
        self.outliers_layout.addWidget(self.outliers_coeff)
        self.layout.addLayout(self.outliers_layout)

        # Create the dialog once and keep it for toggling visibility
        self.attractors_settings_dialog = AttractorsSettingsDialog(attractors_settings, self.attractors.isChecked)
        self.attractors_settings_dialog.setVisible(False)  # Initially hidden

    def update_attractors_enabled(self, state):
        # Fetch current settings from the dialog
        current_settings = {
            "distance": self.attractors_settings_dialog.distance_input.value(),
            "prominence": self.attractors_settings_dialog.prominence_input.value(),
            "width": self.attractors_settings_dialog.width_input.value(),
            "height": self.attractors_settings_dialog.height_input.value(),
            "threshold": self.attractors_settings_dialog.threshold_input.value(),
            "enabled": state == 2  # Update the enabled state based on the checkbox
        }
        # Emit the updated parameters
        self.attractors_settings_dialog.parametersUpdated.emit({"attractors_params": current_settings})

    def toggle_attractors_settings_dialog(self):
        # Toggle the visibility of the dialog
        if self.attractors_settings_dialog.isVisible():
            self.attractors_settings_dialog.setVisible(False)
        else:
            self.attractors_settings_dialog.exec_()  # Use exec_() to make it modal if needed