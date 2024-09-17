from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QDoubleSpinBox, QRadioButton, QSlider, QSpinBox, \
    QVBoxLayout, QGroupBox, QHBoxLayout, QScrollArea, QPushButton, QCheckBox, \
    QLabel, QWidget, QComboBox, QSpacerItem, QSizePolicy

from .peaks_table import PeaksTable
from fitspy import PEAK_MODELS, BKG_MODELS

project_root = Path(__file__).resolve().parent.parent.parent.parent
icons = project_root / 'resources' / 'iconpack'


class Normalization(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)
        self.setTitle("Normalization")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        self.range_min = QDoubleSpinBox()
        self.range_min.setDecimals(2)
        self.range_min.setRange(-9999.99, 9999.99)

        self.range_max = QDoubleSpinBox()
        self.range_max.setDecimals(2)
        self.range_max.setRange(-9999.99, 9999.99)

        self.normalize = QCheckBox("Normalize")

        h_layout.addWidget(QLabel("X min/max:"))
        h_layout.addWidget(self.range_min)
        h_layout.addWidget(QLabel("/"))
        h_layout.addWidget(self.range_max)
        h_layout.addWidget(self.normalize)


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

        self.range_min = QDoubleSpinBox()
        self.range_min.setDecimals(2)
        self.range_min.setRange(-9999.99, 9999.99)

        self.range_max = QDoubleSpinBox()
        self.range_max.setDecimals(2)
        self.range_max.setRange(-9999.99, 9999.99)

        apply_button = QPushButton("Apply")

        h_layout.addWidget(label)
        h_layout.addWidget(self.range_min)
        h_layout.addWidget(QLabel("/"))
        h_layout.addWidget(self.range_max)
        h_layout.addWidget(apply_button)

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

        self.radio_semi_auto = QRadioButton("Semi-Auto :")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)
        # self.slider.setValue(5) 
        self.import_button = QPushButton("Import")

        self.HLayout1.addWidget(self.radio_semi_auto)
        self.HLayout1.addWidget(self.slider)
        self.HLayout1.addWidget(self.import_button)

        self.HLayout2 = QHBoxLayout()
        self.HLayout2.setSpacing(5)
        self.HLayout2.setContentsMargins(0, 0, 0, 0)

        self.radio_linear = QRadioButton("Linear")
        self.radio_polynomial = QRadioButton("Polynomial - Order :")
        self.spin_poly_order = QSpinBox()

        self.HLayout2.addWidget(self.radio_linear)
        self.HLayout2.addWidget(self.radio_polynomial)
        self.HLayout2.addWidget(self.spin_poly_order)

        self.HLayout3 = QHBoxLayout()
        self.HLayout3.setSpacing(5)
        self.HLayout3.setContentsMargins(0, 0, 0, 0)

        self.attached = QCheckBox("Attached")
        self.label_sigma = QLabel("Sigma (smoothing):")
        self.spin_sigma = QSpinBox()

        self.HLayout3.addWidget(self.attached)
        self.HLayout3.addWidget(self.label_sigma)
        self.HLayout3.addWidget(self.spin_sigma)

        vbox_layout.addLayout(self.HLayout1)
        vbox_layout.addLayout(self.HLayout2)
        vbox_layout.addLayout(self.HLayout3)

        self.apply_button = QPushButton("Apply")
        vbox_layout.addWidget(self.apply_button)


class Fitting(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Fitting")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.peak_model = self.create_section(vbox_layout, "Peak model:",
                                              PEAK_MODELS.keys())
        self.background_model = self.create_section(vbox_layout,
                                                    "Background model:",
                                                    BKG_MODELS.keys())

    def create_section(self, layout, label_text, items=[]):
        label = QLabel(label_text)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        combo_box = QComboBox()
        combo_box.addItems(items)
        clear_button = QPushButton("Load")

        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setStretch(2, 65)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(label)
        h_layout.addItem(spacer)
        h_layout.addWidget(combo_box)
        h_layout.addWidget(clear_button)

        layout.addLayout(h_layout)

        return combo_box


class ModelSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setObjectName("fit_model_editor")
        self.setEnabled(True)
        self.setFixedWidth(380)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the main layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Add the widgets to the main layout
        self.spectral_range = SpectralRange(self)
        self.baseline = Baseline(self)
        self.normalization = Normalization(self)
        self.fitting = Fitting(self)
        main_layout.addWidget(self.spectral_range)
        main_layout.addWidget(self.baseline)
        main_layout.addWidget(self.normalization)
        main_layout.addWidget(self.fitting)

        HLayout = QHBoxLayout()
        HLayout.setSpacing(0)
        HLayout.setContentsMargins(0, 0, 0, 0)

        self.save_button = QPushButton(
            text="Save Model",
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save the fit model as a JSON file",
        )
        self.save_button.setIconSize(QSize(20, 20))

        self.fit_button = QPushButton("Fit")

        HLayout.addWidget(self.save_button)
        HLayout.addWidget(self.fit_button)

        main_layout.addLayout(HLayout)

        scroll_area.setWidget(container)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)


class ModelSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fit_models = []
        self.initUI()

    def initUI(self):
        h_layout = QHBoxLayout(self)
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel("Select a model:")

        self.combo_box = QComboBox()
        self.combo_box.setPlaceholderText("Select a model for fitting")

        self.apply_button = QPushButton("Apply Model")

        self.load_button = QPushButton("Load Model")

        h_layout.addWidget(label)
        h_layout.addWidget(self.combo_box)
        h_layout.addWidget(self.apply_button)
        h_layout.addWidget(self.load_button)

        h_layout.setStretch(1, 1)

        self.setLayout(h_layout)


class ModelBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.model_settings = ModelSettings(self)
        self.peak_table = PeaksTable(self)
        self.limits_chbox = QCheckBox("Limits")
        self.expr_chbox = QCheckBox("Expressions")
        self.limits_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.expr_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.model_selector = ModelSelector(self)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.peak_table)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.limits_chbox)
        hbox_layout.addWidget(self.expr_chbox)
        hbox_layout.addWidget(self.model_selector)

        vbox_layout.addLayout(hbox_layout)

        layout = QHBoxLayout(self)
        layout.addWidget(self.model_settings)
        layout.addLayout(vbox_layout)

    def set_spinbox_value(self, spinbox, value):
        if value is None:
            spinbox.clear()
        else:
            spinbox.setValue(value)

    def update_model(self, model):

        set_spinbox_value = self.set_spinbox_value

        # Spectral range
        spectral_range = self.model_settings.spectral_range
        set_spinbox_value(spectral_range.range_min, model['range_min'])
        set_spinbox_value(spectral_range.range_max, model['range_max'])

        # Baseline
        baseline = self.model_settings.baseline
        m_baseline = model['baseline']
        baseline.radio_semi_auto.setChecked(m_baseline['mode'] == "Semi-Auto")
        baseline.radio_linear.setChecked(m_baseline['mode'] == "Linear")
        baseline.radio_polynomial.setChecked(m_baseline['mode'] == "Polynomial")
        baseline.attached.setChecked(m_baseline['attached'])
        set_spinbox_value(baseline.spin_poly_order, m_baseline['order_max'])
        set_spinbox_value(baseline.spin_sigma, m_baseline['sigma'])
        baseline.slider.setValue(m_baseline['coef'])

        # Normalization
        normalization = self.model_settings.normalization
        set_spinbox_value(normalization.range_min, model['normalize_range_min'])
        set_spinbox_value(normalization.range_max, model['normalize_range_max'])
        normalization.normalize.setChecked(model['normalize'])


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    model_builder = ModelBuilder()
    model_builder.show()
    sys.exit(app.exec())
