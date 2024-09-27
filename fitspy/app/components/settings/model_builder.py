from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QRadioButton, QSlider, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QCheckBox, QLabel, QWidget, QComboBox, QSpacerItem, QSizePolicy

from superqt import QCollapsible
from fitspy import PEAK_MODELS, BKG_MODELS
from .custom_spinbox import SpinBox, DoubleSpinBox
from .peaks_table import PeaksTable
from .baseline_table import BaselineTable

project_root = Path(__file__).resolve().parent.parent.parent.parent
icons = project_root / 'resources' / 'iconpack'


class SpectralRange(QCollapsible):
    def __init__(self, parent=None):
        super().__init__("Spectral range", parent)
        self.initUI()

    def initUI(self):
        content_widget = QWidget()

        h_layout = QHBoxLayout(content_widget)
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("X min/max:")

        self.range_min = DoubleSpinBox()
        self.range_min.setDecimals(2)
        self.range_min.setRange(-9999.99, 9999.99)

        self.range_max = DoubleSpinBox()
        self.range_max.setDecimals(2)
        self.range_max.setRange(-9999.99, 9999.99)

        self.apply = QPushButton("Apply")

        slash_label = QLabel("/")
        slash_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        slash_label.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(label)
        h_layout.addWidget(self.range_min)
        h_layout.addWidget(slash_label)
        h_layout.addWidget(self.range_max)
        h_layout.addWidget(self.apply)
        self.setContent(content_widget)
        self.expand(animate=False)

class Baseline(QCollapsible):
    def __init__(self, parent=None):
        super().__init__("Baseline", parent)
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        vbox_layout = QVBoxLayout(content_widget)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.setSpacing(2)
        content_widget.setLayout(vbox_layout)

        self.HLayout1 = QHBoxLayout()
        self.HLayout1.setSpacing(5)
        self.HLayout1.setContentsMargins(0, 0, 0, 0)

        self.semi_auto = QRadioButton("Semi-Auto :")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)
        # self.slider.setValue(5)
        self.import_button = QPushButton("Import")

        self.HLayout1.addWidget(self.semi_auto)
        self.HLayout1.addWidget(self.slider)
        self.HLayout1.addWidget(self.import_button)

        self.HLayout2 = QHBoxLayout()
        self.HLayout2.setSpacing(5)
        self.HLayout2.setContentsMargins(0, 0, 0, 0)

        self.linear = QRadioButton("Linear")
        self.polynomial = QRadioButton("Polynomial")
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label_order = QLabel("Order:")
        self.order = SpinBox()

        self.HLayout2.addWidget(self.linear)
        self.HLayout2.addItem(spacer)
        self.HLayout2.addWidget(self.polynomial)
        self.HLayout2.addItem(spacer)
        self.HLayout2.addWidget(self.label_order)
        self.HLayout2.addWidget(self.order)

        self.HLayout3 = QHBoxLayout()
        self.HLayout3.setSpacing(5)
        self.HLayout3.setContentsMargins(0, 0, 0, 0)

        self.attached = QCheckBox("Attached")
        self.label_sigma = QLabel("Sigma (smoothing):")
        self.sigma = SpinBox()

        self.HLayout3.addWidget(self.attached)
        self.HLayout3.addItem(spacer)
        self.HLayout3.addWidget(self.label_sigma)
        self.HLayout3.addWidget(self.sigma)

        vbox_layout.addLayout(self.HLayout1)
        vbox_layout.addLayout(self.HLayout2)
        vbox_layout.addLayout(self.HLayout3)

        self.apply = QPushButton("Apply")
        vbox_layout.addWidget(self.apply)

        self.setContent(content_widget)
        self.expand(animate=False)

class Normalization(QCollapsible):
    def __init__(self, parent=None):
        super().__init__("Normalization", parent)
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        h_layout = QHBoxLayout(content_widget)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self.range_min = DoubleSpinBox()
        self.range_min.setDecimals(2)
        self.range_min.setRange(-9999.99, 9999.99)

        self.range_max = DoubleSpinBox()
        self.range_max.setDecimals(2)
        self.range_max.setRange(-9999.99, 9999.99)

        self.normalize = QCheckBox("Normalize")

        slash_label = QLabel("/")
        slash_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        slash_label.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(QLabel("X min/max:"))
        h_layout.addWidget(self.range_min)
        h_layout.addWidget(slash_label)
        h_layout.addWidget(self.range_max)
        h_layout.addWidget(self.normalize)

        self.setContent(content_widget)
        self.expand(animate=False)

class Fitting(QCollapsible):
    def __init__(self, parent=None):
        super().__init__("Fitting", parent)
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        vbox_layout = QVBoxLayout(content_widget)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.setSpacing(2)

        self.peak_model_combo = self.create_section(vbox_layout, "Peak model:", PEAK_MODELS.keys())
        self.bkg_model_combo = self.create_section(vbox_layout, "Background model:", BKG_MODELS.keys())

        self.setContent(content_widget)
        self.expand(animate=False)

    def create_section(self, layout, label_text, items=[]):
        label = QLabel(label_text)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        combo_box = QComboBox()
        combo_box.addItems(items)
        load_button = QPushButton("Load")

        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setStretch(2, 65)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(label)
        h_layout.addItem(spacer)
        h_layout.addWidget(combo_box)
        h_layout.addWidget(load_button)

        layout.addLayout(h_layout)

        return combo_box

class ModelSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setObjectName("fit_model_editor")
        self.setEnabled(True)
        self.setFixedWidth(346)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the main layout
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

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

        save_button = QPushButton(
            text="Save Model",
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save the fit model as a JSON file",
        )
        save_button.setIconSize(QSize(20, 20))
        fit_button = QPushButton("Fit")

        HLayout.addWidget(save_button)
        HLayout.addWidget(fit_button)

        main_layout.addLayout(HLayout)

        scroll_area.setWidget(container)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(scroll_area)

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

        apply = QPushButton("Apply Model")

        load_button = QPushButton("Load Model")

        h_layout.addWidget(label)
        h_layout.addWidget(combo_box)
        h_layout.addWidget(apply)
        h_layout.addWidget(load_button)

        h_layout.setStretch(1, 1)

        self.setLayout(h_layout)

class ModelBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.model_settings = ModelSettings(self)
        self.peaks_table = PeaksTable(self)
        self.bounds_chbox = QCheckBox("Bounds")
        self.expr_chbox = QCheckBox("Expressions")
        self.bounds_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.expr_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.model_selector = ModelSelector(self)
        self.baseline_table = BaselineTable(self)
        self.baseline_table.setMaximumWidth(150)

        vbox_layout = QVBoxLayout()
        vbox_layout.setSpacing(0)
        vbox_layout.addWidget(self.peaks_table)
        vbox_layout.setStretch(0, 1)

        hbox_layout = QHBoxLayout()
        hbox_layout.setSpacing(0)
        hbox_layout.addWidget(self.bounds_chbox)
        hbox_layout.addWidget(self.expr_chbox)
        hbox_layout.addWidget(self.model_selector)

        vbox_layout.addLayout(hbox_layout)

        layout = QHBoxLayout(self)
        layout.addWidget(self.model_settings)
        layout.addLayout(vbox_layout)
        layout.addWidget(self.baseline_table)

    def update_model(self, model):
        # Spectral range
        self.model_settings.spectral_range.range_min.setValue(model.get('range_min', 0))
        self.model_settings.spectral_range.range_max.setValue(model.get('range_max', 0))

        # Baseline
        baseline = model.get('baseline', {})
        self.model_settings.baseline.semi_auto.setAutoExclusive(False)
        self.model_settings.baseline.linear.setAutoExclusive(False)
        self.model_settings.baseline.polynomial.setAutoExclusive(False)
        self.model_settings.baseline.semi_auto.setChecked(baseline.get('mode', None) == "Semi-Auto")
        self.model_settings.baseline.linear.setChecked(baseline.get('mode', None) == "Linear")
        self.model_settings.baseline.polynomial.setChecked(baseline.get('mode', None) == "Polynomial")
        self.model_settings.baseline.semi_auto.setAutoExclusive(True)
        self.model_settings.baseline.linear.setAutoExclusive(True)
        self.model_settings.baseline.polynomial.setAutoExclusive(True)

        self.model_settings.baseline.attached.setChecked(baseline.get('attached', False))
        self.model_settings.baseline.order.setValue(baseline.get('order_max', 0))
        self.model_settings.baseline.sigma.setValue(baseline.get('sigma', 0))
        self.model_settings.baseline.slider.setValue(baseline.get('coef', 0))

        # Normalization
        self.model_settings.normalization.range_min.setValue(model.get('normalize_range_min', 0))
        self.model_settings.normalization.range_max.setValue(model.get('normalize_range_max', 0))
        self.model_settings.normalization.normalize.setChecked(model.get('normalize', False))

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    model_builder = ModelBuilder()
    model_builder.show()
    sys.exit(app.exec())
