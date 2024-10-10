from PySide6.QtWidgets import (
    QLabel, QGroupBox, QVBoxLayout, QPushButton, QComboBox, QLineEdit,
    QCheckBox, QHeaderView, QWidget
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from matplotlib.colors import rgb2hex
import matplotlib.cm as cm
from fitspy import PEAK_MODELS
from fitspy.core import get_icon_path

from .generic_table import GenericTable
from .custom_spinbox import DoubleSpinBox


class PeaksTable(QGroupBox):
    peaksChanged = Signal(dict)
    showToast = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.cmap = cm.get_cmap("tab10")

    def initUI(self):
        self.setTitle("Peak table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.table = GenericTable(
            columns={
                "Prefix": QLabel,
                "Label": QLineEdit,
                "Model": QComboBox,
                "x0_min": DoubleSpinBox,
                "x0": DoubleSpinBox,
                "x0_max": DoubleSpinBox,
                "x0_vary": QCheckBox,
                "Ampli_min": DoubleSpinBox,
                "Ampli": DoubleSpinBox,
                "Ampli_max": DoubleSpinBox,
                "Ampli_vary": QCheckBox,
                "FWHM_min": DoubleSpinBox,
                "FWHM": DoubleSpinBox,
                "FWHM_max": DoubleSpinBox,
                "FWHM_vary": QCheckBox
            }
        )
        self.show_bounds(False)
        main_layout.addWidget(self.table)
        self.table.rowsDeleted.connect(self.emit_peaks_changed)
        self.table.rowsDeleted.connect(self.update_prefix_colors)
        self.setLayout(main_layout)

    @property
    def row_count(self):
        return self.table.row_count
    
    def get_peaks(self):
        def get_widget_value(row, column_name):
            widget = self.table.cellWidget(row, self.table.get_column_index(column_name))

            if isinstance(widget, QWidget):
                layout = widget.layout()
                if layout is not None and layout.count() == 1:
                    widget = layout.itemAt(0).widget() 
            if isinstance(widget, QCheckBox):
                return widget.isChecked()
            elif hasattr(widget, 'value'):
                return widget.value()
            elif hasattr(widget, 'currentText'):
                return widget.currentText()
            else:
                return widget.text()

        peaks = {
            'peak_models': {},
            'peak_labels': []
        }
        peak_models = peaks['peak_models']
        peak_labels = peaks['peak_labels']

        for row in range(self.table.rowCount()):
            label = get_widget_value(row, "Label")
            model_name = get_widget_value(row, "Model")

            peak_labels.append(label)

            if row not in peak_models:
                peak_models[row] = {}
            if model_name not in peak_models[row]:
                peak_models[row][model_name] = {}

            peak_models[row][model_name]['ampli'] = {
                'min': get_widget_value(row, "Ampli_min"),
                'max': get_widget_value(row, "Ampli_max"),
                'value': get_widget_value(row, "Ampli"),
                'vary': get_widget_value(row, "Ampli_vary"),
                'expr': None # TODO Expr
            }
            peak_models[row][model_name]['x0'] = {
                'min': get_widget_value(row, "x0_min"),
                'max': get_widget_value(row, "x0_max"),
                'value': get_widget_value(row, "x0"),
                'vary': get_widget_value(row, "x0_vary"),
                'expr': None # TODO Expr
            }
            peak_models[row][model_name]['fwhm'] = {
                'min': get_widget_value(row, "FWHM_min"),
                'max': get_widget_value(row, "FWHM_max"),
                'value': get_widget_value(row, "FWHM"),
                'vary': get_widget_value(row, "FWHM_vary"),
                'expr': None # TODO Expr
            }
        return peaks
    
    def emit_peaks_changed(self):
        peaks = self.get_peaks()
        
        # if there is a peak with incorrect bounds, show a warning and return
        for peak in peaks['peak_models'].values():
            for model in peak.values():
                for param in model.values():
                    if param['min'] > param['max']:
                        self.showToast.emit("WARNING", "Invalid bounds", "Minimum value must be less than maximum value.")
                        return
                    if not (param['min'] <= param['value'] <= param['max']):
                        self.showToast.emit("WARNING", "Value out of bounds", f"Value {param['value']} must be between {param['min']} and {param['max']}.")
                        return

        self.peaksChanged.emit(peaks)

    def clear(self):
        self.table.clear()

    def add_row(self, **params):
        def create_spin_box(value=None):
            spin_box = DoubleSpinBox(empty_value=float("inf"))
            spin_box.setMinimumWidth(60)
            if value:
                spin_box.setValue(value)
            spin_box.editingFinished.connect(self.emit_peaks_changed)
            return spin_box

        def create_checkbox(checked=False):
            checkbox = QCheckBox()
            checkbox.setChecked(checked)
            checkbox.stateChanged.connect(self.emit_peaks_changed)
            return checkbox

        prefix_btn = QPushButton(
            text=params["prefix"],
            icon=QIcon(get_icon_path('close.png')),
            toolTip="Delete peak"
        )
        color = rgb2hex(self.cmap(self.row_count % self.cmap.N))
        prefix_btn.setStyleSheet(f"color: {color};")
        prefix_btn.clicked.connect(lambda: self.table.remove_widget_row(prefix_btn))

        label_edit = QLineEdit(params["label"])
        label_edit.editingFinished.connect(self.emit_peaks_changed)

        model_names = list(PEAK_MODELS.keys())
        model_combo = QComboBox()
        model_combo.addItems(model_names)
        model_combo.setCurrentText(params["model_name"])
        model_combo.currentIndexChanged.connect(self.emit_peaks_changed)

        x0_min_spin = create_spin_box(params["x0_min"])
        x0_spin = create_spin_box(params["x0"])
        x0_max_spin = create_spin_box(params["x0_max"])
        x0_vary_checkbox = create_checkbox(params["x0_vary"])

        ampli_min_spin = create_spin_box(params["ampli_min"])
        ampli_spin = create_spin_box(params["ampli"])
        ampli_max_spin = create_spin_box(params["ampli_max"])
        ampli_vary_checkbox = create_checkbox(params["ampli_vary"])

        fwhm_min_spin = create_spin_box(params["fwhm_min"])
        fwhm_spin = create_spin_box(params["fwhm"])
        fwhm_max_spin = create_spin_box(params["fwhm_max"])
        fwhm_vary_checkbox = create_checkbox(params["fwhm_vary"])

        row_widgets = {
            "Prefix": prefix_btn,
            "Label": label_edit,
            "Model": model_combo,
            "x0_min": x0_min_spin,
            "x0": x0_spin,
            "x0_max": x0_max_spin,
            "x0_vary": x0_vary_checkbox,
            "Ampli_min": ampli_min_spin,
            "Ampli": ampli_spin,
            "Ampli_max": ampli_max_spin,
            "Ampli_vary": ampli_vary_checkbox,
            "FWHM_min": fwhm_min_spin,
            "FWHM": fwhm_spin,
            "FWHM_max": fwhm_max_spin,
            "FWHM_vary": fwhm_vary_checkbox
        }

        self.table.add_row(**row_widgets)

    def update_prefix_colors(self):
        for row in range(self.table.rowCount()):
            prefix_btn = self.table.cellWidget(row, self.table.get_column_index("Prefix"))
            color = rgb2hex(self.cmap(row % self.cmap.N))
            prefix_btn.setStyleSheet(f"color: {color};")

    def show_bounds(self, show):
        columns_to_toggle = ["x0_min", "x0_max", "Ampli_min", "Ampli_max", "FWHM_min", "FWHM_max"]
        
        for column in columns_to_toggle:
            column_index = self.table.get_column_index(column)
            self.table.setColumnHidden(column_index, not show)

        header = self.table.horizontalHeader()
        if show:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)