from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QRadioButton, QSlider, QVBoxLayout, QHBoxLayout, QScrollArea,
                               QPushButton, QCheckBox, QLabel, QWidget, QSpacerItem,
                               QSizePolicy, QButtonGroup, QTabWidget)
from superqt import QCollapsible

from fitspy import PEAK_MODELS, BKG_MODELS
from fitspy.apps.pyside.utils import get_icon_path
from fitspy.apps.pyside.components import FitStats
from fitspy.apps.pyside.components.custom_widgets import SpinBox, DoubleSpinBox, DragNDropCombo
from fitspy.apps.pyside.components.settings.peaks_table import PeaksTable
from fitspy.apps.pyside.components.settings.bkg_table import BkgTable
from fitspy.apps.pyside.components.settings.baseline_table import BaselineTable


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
        self.range_max = DoubleSpinBox()

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

        self.none = QRadioButton("None")
        self.semi_auto = QRadioButton("Semi-Auto :")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10)
        self.slider.wheelEvent = lambda event: event.ignore()
        self.import_btn = QPushButton("Import")

        self.HLayout1.addWidget(self.none)
        self.HLayout1.addWidget(self.semi_auto)
        self.HLayout1.addWidget(self.slider)
        self.HLayout1.addWidget(self.import_btn)

        self.HLayout2 = QHBoxLayout()
        self.HLayout2.setSpacing(5)
        self.HLayout2.setContentsMargins(0, 0, 0, 0)

        self.linear = QRadioButton("Linear")
        self.polynomial = QRadioButton("Polynomial")
        self.label_order = QLabel("Order:")
        self.order = SpinBox()

        self.HLayout2.addWidget(self.linear)
        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HLayout2.addItem(spacer1)
        self.HLayout2.addWidget(self.polynomial)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HLayout2.addItem(spacer2)
        self.HLayout2.addWidget(self.label_order)
        self.HLayout2.addWidget(self.order)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.none)
        self.button_group.addButton(self.semi_auto)
        self.button_group.addButton(self.linear)
        self.button_group.addButton(self.polynomial)

        self.HLayout3 = QHBoxLayout()
        self.HLayout3.setSpacing(5)
        self.HLayout3.setContentsMargins(0, 0, 0, 0)

        self.attached = QCheckBox("Attached")
        self.label_sigma = QLabel("Sigma (smoothing):")
        self.sigma = SpinBox()

        self.HLayout3.addWidget(self.attached)
        spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.HLayout3.addItem(spacer3)
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
        self.range_max = DoubleSpinBox()

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
    loadPeakModel = Signal(object)
    loadBkgModel = Signal(object)

    def __init__(self, parent=None):
        super().__init__("Fitting", parent)
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        vbox_layout = QVBoxLayout(content_widget)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.setSpacing(2)

        self.peak_model = self.create_section(vbox_layout, "Peak model:",
                                              PEAK_MODELS.keys(), model_type="peak")
        self.bkg_model = self.create_section(vbox_layout, "BKG model:",
                                             BKG_MODELS.keys(), model_type="bkg")

        self.setContent(content_widget)
        self.expand(animate=False)

    def create_section(self, layout, label_text, items=[], model_type="peak"):
        label = QLabel(label_text)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        combo_box = DragNDropCombo()
        combo_box.addItems(items)
        add = QPushButton("Add Model", icon=QIcon(get_icon_path("add.png")),
                          toolTip="Load .txt/.py file and add it to the list of models")

        if model_type == "peak":
            add.clicked.connect(lambda: self.loadPeakModel.emit(None))
            combo_box.itemAdded.connect(lambda fname: self.loadPeakModel.emit(fname))
        elif model_type == "bkg":
            add.clicked.connect(lambda: self.loadBkgModel.emit(None))
            combo_box.itemAdded.connect(lambda fname: self.loadBkgModel.emit(fname))

        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(label)
        h_layout.addItem(spacer)
        h_layout.addWidget(combo_box)
        h_layout.addWidget(add)
        h_layout.setStretch(2, 1)

        layout.addLayout(h_layout)

        return combo_box

    def update_combo_boxes(self):
        """Refresh the items in peak_model and bkg_model combo boxes."""
        self.peak_model.blockSignals(True)
        self.peak_model.clear()
        self.peak_model.addItems(PEAK_MODELS.keys())
        self.peak_model.blockSignals(False)

        self.bkg_model.blockSignals(True)
        self.bkg_model.clear()
        self.bkg_model.addItems(BKG_MODELS.keys())
        self.bkg_model.blockSignals(False)


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
        self.container = QWidget()
        main_layout = QVBoxLayout(self.container)
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

        self.save = QPushButton(text="Save Model(s)",
                                icon=QIcon(get_icon_path("save.png")),
                                toolTip="Save selected fit models in a JSON file")
        self.save.setIconSize(QSize(20, 20))

        self.fit = QPushButton(text="Apply Model",
                               toolTip="Preprocess+fit the selected spectra with current model")

        HLayout.addWidget(self.fit)
        HLayout.addWidget(self.save)

        main_layout.addLayout(HLayout)

        scroll_area.setWidget(self.container)

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
        h_layout.setSpacing(2)
        h_layout.setContentsMargins(1, 1, 1, 1)

        self.combo_box = DragNDropCombo()

        self.set = QPushButton(
            "Set Model",
            icon=QIcon(get_icon_path("apply.png")),
            toolTip="Set the first model of file to selection, no preprocessing/fitting",
        )

        self.add = QPushButton("Add Model", icon=QIcon(get_icon_path("add.png")),
                               toolTip="Load .json file and add it to the list of models")

        h_layout.addWidget(self.combo_box)
        h_layout.addWidget(self.set)
        h_layout.addWidget(self.add)

        h_layout.setStretch(0, 1)
        h_layout.setStretch(1, 0)
        h_layout.setStretch(2, 0)
        h_layout.setStretch(3, 0)
        h_layout.setStretch(4, 0)

        self.setLayout(h_layout)

    def setDisabled(self, state):
        """Override setDisabled to keep preview checkbox enabled"""
        self.combo_box.setDisabled(state)
        self.set.setDisabled(state)
        self.add.setDisabled(state)

    def setEnabled(self, state):
        self.setDisabled(not state)


class ModelBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.model_settings = ModelSettings(self)
        self.baseline_table = BaselineTable(self)
        self.setupTabWidget()

        self.bounds_chbox = QCheckBox("Bounds")
        self.bounds_chbox.setChecked(True)
        self.expr_chbox = QCheckBox("Expressions")
        self.bounds_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.expr_chbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.model_selector = ModelSelector(self)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.bounds_chbox)
        hbox_layout.addWidget(self.expr_chbox)
        hbox_layout.addWidget(self.model_selector)

        vbox_layout = QVBoxLayout()
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.setSpacing(0)
        vbox_layout.addWidget(self.tab_widget)
        vbox_layout.addLayout(hbox_layout)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        layout.addWidget(self.model_settings)
        layout.addLayout(vbox_layout)
        layout.addWidget(self.baseline_table)

    def setupTabWidget(self):
        self.tab_widget = QTabWidget()
        tab_content = QWidget()
        self.peaks_table = PeaksTable(parent=self)
        self.bkg_table = BkgTable(parent=self)
        self.fit_stats = FitStats(self)

        vbox_layout = QVBoxLayout()
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.setSpacing(0)
        vbox_layout.addWidget(self.peaks_table)
        vbox_layout.setStretch(0, 1)
        tab_content.setLayout(vbox_layout)

        self.tab_widget.addTab(tab_content, "Peaks")
        self.tab_widget.addTab(self.bkg_table, "Background")
        self.tab_widget.addTab(self.fit_stats, "Fit statistics")

    def update_model(self, model):
        # Spectral range
        self.model_settings.spectral_range.range_min.setValue(model.get("range_min", 0))
        self.model_settings.spectral_range.range_max.setValue(model.get("range_max", 0))

        # Baseline
        baseline = self.model_settings.baseline
        baseline_model = model.get("baseline", {})

        baseline.none.setChecked(baseline_model.get("mode", None) is None)
        baseline.semi_auto.setChecked(baseline_model.get("mode", None) == "Semi-Auto")
        baseline.linear.setChecked(baseline_model.get("mode", None) == "Linear")
        baseline.polynomial.setChecked(baseline_model.get("mode", None) == "Polynomial")

        baseline.attached.setChecked(baseline_model.get("attached", False))
        baseline.order.setValue(baseline_model.get("order_max", 0))
        baseline.sigma.setValue(baseline_model.get("sigma", 0))
        baseline.slider.setValue(baseline_model.get("coef", 0))

        # Normalization
        normalization = self.model_settings.normalization
        normalization.normalize.blockSignals(True)
        normalization.range_min.setValue(model.get("normalize_range_min", 0))
        normalization.range_max.setValue(model.get("normalize_range_max", 0))
        normalization.normalize.setChecked(model.get("normalize", False))
        normalization.normalize.blockSignals(False)

        # Fitting
        bkg_model = next(iter(model.get("bkg_model") or {}), "None")
        self.model_settings.fitting.bkg_model.setCurrentText(bkg_model)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = ModelBuilder()
    # obj = SpectralRange()
    # obj = Baseline()
    # obj = Normalization()
    # obj = Fitting()
    # obj = ModelSettings()
    obj.show()
    sys.exit(app.exec())
