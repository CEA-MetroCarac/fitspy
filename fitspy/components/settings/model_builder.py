from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QDoubleSpinBox, QRadioButton, QSlider, QSpinBox, QVBoxLayout, QGroupBox, QHBoxLayout, QScrollArea, QPushButton, QCheckBox, QLabel, QWidget, QComboBox, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon

project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class Overall(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(0, 0, 0, 0)

        # Add "Spike removal" button
        spike_removal_button = QPushButton("Spike removal")

        # Add horizontal spacer
        h_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Add "X-axis unit:" label
        x_axis_label = QLabel("X-axis unit:")

        # Add ComboBox
        x_axis_combobox = QComboBox()

        # Add widgets to the horizontal layout
        h_layout.addWidget(spike_removal_button)
        h_layout.addItem(h_spacer)
        h_layout.addWidget(x_axis_label)
        h_layout.addWidget(x_axis_combobox)

        # Add the horizontal layout to the main vertical layout
        vbox_layout.addLayout(h_layout)

class SpectralRange(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Spectral range")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("X min/max:")

        # Add float input fields
        x_min_input = QDoubleSpinBox()
        x_min_input.setDecimals(2)
        x_min_input.setRange(-9999.99, 9999.99)

        x_max_input = QDoubleSpinBox()
        x_max_input.setDecimals(2)
        x_max_input.setRange(-9999.99, 9999.99)

        # Add "Apply" button
        apply_button = QPushButton("Apply")

        # Add widgets to the horizontal layout
        h_layout.addWidget(label)
        h_layout.addWidget(x_min_input)
        h_layout.addWidget(QLabel("/"))
        h_layout.addWidget(x_max_input)
        h_layout.addWidget(apply_button)

        # Add the horizontal layout to the main vertical layout
        vbox_layout.addLayout(h_layout)

class Baseline(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Baseline")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.HLayout1 = QHBoxLayout()
        self.HLayout1.setSpacing(5)
        self.HLayout1.setContentsMargins(0, 0, 0, 0)

        self.radio_semi_auto = QRadioButton(text="Semi-Auto :")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50) 
        self.import_button = QPushButton(text="Import")

        self.HLayout1.addWidget(self.radio_semi_auto)
        self.HLayout1.addWidget(self.slider)
        self.HLayout1.addWidget(self.import_button)

        self.HLayout2 = QHBoxLayout()
        self.HLayout2.setSpacing(5)
        self.HLayout2.setContentsMargins(0, 0, 0, 0)

        self.radio_linear = QRadioButton(text="Linear")
        self.radio_polynomial = QRadioButton(text="Polynomial - Order :")
        self.spin_polynomial_order = QSpinBox()

        self.HLayout2.addWidget(self.radio_linear)
        self.HLayout2.addWidget(self.radio_polynomial)
        self.HLayout2.addWidget(self.spin_polynomial_order)

        self.HLayout3 = QHBoxLayout()
        self.HLayout3.setSpacing(5)
        self.HLayout3.setContentsMargins(0, 0, 0, 0)

        self.checkbox_attached = QCheckBox(text="Attached")
        self.label_sigma = QLabel(text="Sigma (smoothing):")
        self.spin_sigma = QSpinBox()

        self.HLayout3.addWidget(self.checkbox_attached)
        self.HLayout3.addWidget(self.label_sigma)
        self.HLayout3.addWidget(self.spin_sigma)

        vbox_layout.addLayout(self.HLayout1)
        vbox_layout.addLayout(self.HLayout2)
        vbox_layout.addLayout(self.HLayout3)

        self.apply_button = QPushButton(text="Apply")
        vbox_layout.addWidget(self.apply_button)


class Peaks(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Peaks")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.model_label = QLabel(text="Peak model")
        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cbb_fit_models = QComboBox()
        self.clear_peaks = QPushButton(text="Clear peaks")

        self.HLayout = QHBoxLayout()
        self.HLayout.setSpacing(5)
        self.HLayout.setStretch(2, 65)
        self.HLayout.setContentsMargins(0, 0, 0, 0)
        self.HLayout.addWidget(self.model_label)
        self.HLayout.addItem(self.HSpacer)
        self.HLayout.addWidget(self.cbb_fit_models)
        self.HLayout.addWidget(self.clear_peaks)

        vbox_layout.addLayout(self.HLayout)

class ModelSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setObjectName("fit_model_editor")
        self.setEnabled(True)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the main layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Add the widgets to the main layout
        self.overall = Overall(self)
        self.spectral_range = SpectralRange(self)
        self.baseline = Baseline(self)
        self.peaks = Peaks(self)
        main_layout.addWidget(self.overall)
        main_layout.addWidget(self.spectral_range)
        main_layout.addWidget(self.baseline)
        main_layout.addWidget(self.peaks)

        HLayout = QHBoxLayout()
        HLayout.setSpacing(5)
        HLayout.setContentsMargins(2, 2, 2, 2)

        save_button = QPushButton(
            text="Save Model",
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save the fit model as a JSON file",
            objectName="save_model",
        )
        fit_button = QPushButton("Fit")

        HLayout.addWidget(save_button)
        HLayout.addWidget(fit_button)

        main_layout.addLayout(HLayout)

        scroll_area.setWidget(container)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)

class PeakTable(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Peak table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)  # 8 columns
        self.table_widget.setHorizontalHeaderLabels(["Label", "Model", "X0", "fix X0", "Fwhm", "fix Fwhm", "Ampli", "Fix Ampli"])
        self.table_widget.setShowGrid(False)

        self.table_widget.setRowCount(10)
        for row in range(10):
            # Label (text input)
            label_item = QTableWidgetItem(f"Label {row + 1}")
            self.table_widget.setItem(row, 0, label_item)

            # Model (combo box)
            model_combo = QComboBox()
            model_combo.addItems(["Model 1", "Model 2", "Model 3"])  # Example items
            self.table_widget.setCellWidget(row, 1, model_combo)

            # X0 (float input)
            x0_input = QLineEdit()
            x0_input.setText(f"{row + 1}.0")
            self.table_widget.setCellWidget(row, 2, x0_input)

            # fix X0 (checkbox)
            fix_x0_checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 3, fix_x0_checkbox)

            # Fwhm (float input)
            fwhm_input = QLineEdit()
            fwhm_input.setText(f"{row + 1}.0")
            self.table_widget.setCellWidget(row, 4, fwhm_input)

            # fix Fwhm (checkbox)
            fix_fwhm_checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 5, fix_fwhm_checkbox)

            # Ampli (float input)
            ampli_input = QLineEdit()
            ampli_input.setText(f"{row + 1}.0")
            self.table_widget.setCellWidget(row, 6, ampli_input)

            # Fix Ampli (checkbox)
            fix_ampli_checkbox = QCheckBox()
            self.table_widget.setCellWidget(row, 7, fix_ampli_checkbox)

        # Create a scroll area and set the table widget as its widget
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

class ModelSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        h_layout = QHBoxLayout(self)
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel("Select a model:")

        combo_box = QComboBox()
        combo_box.setPlaceholderText("Select a model for fitting")

        apply_button = QPushButton("Apply Model")

        load_button = QPushButton("Load Model")

        h_layout.addWidget(label)
        h_layout.addWidget(combo_box)
        h_layout.addWidget(apply_button)
        h_layout.addWidget(load_button)

        self.setLayout(h_layout)

class ModelManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.peak_table = PeakTable(self)
        self.model_selector = ModelSelector(self)
        
        layout.addWidget(self.peak_table)
        layout.addWidget(self.model_selector)

class ModelBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.model_settings = ModelSettings(self)
        self.model_manager = ModelManager(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.model_settings)
        layout.addWidget(self.model_manager)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    model_builder = ModelBuilder()
    model_builder.show()
    sys.exit(app.exec())
