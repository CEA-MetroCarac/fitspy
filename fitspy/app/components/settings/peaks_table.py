from PySide6.QtWidgets import (
    QLabel, QGroupBox, QVBoxLayout, QPushButton, QComboBox, QLineEdit,
    QCheckBox, QHeaderView, QWidget, QHBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

from matplotlib.colors import rgb2hex
import matplotlib.cm as cm
from fitspy import PEAK_MODELS
from fitspy.core import get_icon_path

from .generic_table import GenericTable
from .custom_spinbox import DoubleSpinBox


class SpinBoxGroupWithExpression(QWidget):
    def __init__(self, min_value=None, value=None, max_value=None, expr=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.spin_box_layout = QHBoxLayout()
        self.min_spin_box = DoubleSpinBox(empty_value=float("inf"))
        self.value_spin_box = DoubleSpinBox(empty_value=float("inf"))
        self.max_spin_box = DoubleSpinBox(empty_value=float("inf"))

        min_width = 55
        self.min_spin_box.setMinimumWidth(min_width)
        self.value_spin_box.setMinimumWidth(min_width)
        self.max_spin_box.setMinimumWidth(min_width)

        if min_value is not None:
            self.min_spin_box.setValue(min_value)
        if value is not None:
            self.value_spin_box.setValue(value)
        if max_value is not None:
            self.max_spin_box.setValue(max_value)

        self.spin_box_layout.addWidget(self.min_spin_box)
        self.spin_box_layout.addWidget(self.value_spin_box)
        self.spin_box_layout.addWidget(self.max_spin_box)

        self.expr_edit = QLineEdit()
        if expr is not None:
            self.expr_edit.setText(expr)

        self.layout.addLayout(self.spin_box_layout)
        self.layout.addWidget(self.expr_edit)

    def get_values(self):
        return {
            'min': self.min_spin_box.value(),
            'value': self.value_spin_box.value(),
            'max': self.max_spin_box.value(),
            'expr': self.expr_edit.text()
        }

    def show_expr(self, show):
        self.expr_edit.setVisible(show)

    def show_bounds(self, show):
        self.min_spin_box.setVisible(show)
        self.max_spin_box.setVisible(show)


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
                "MIN | X0 | MAX": SpinBoxGroupWithExpression,
                "x0_vary": QCheckBox,
                "MIN | Ampli | MAX": SpinBoxGroupWithExpression,
                "Ampli_vary": QCheckBox,
                "MIN | FWHM | MAX": SpinBoxGroupWithExpression,
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

            if isinstance(widget, SpinBoxGroupWithExpression):
                return widget.get_values()
            elif isinstance(widget, QWidget):
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

            ampli = get_widget_value(row, "MIN | Ampli | MAX")
            x0 = get_widget_value(row, "MIN | X0 | MAX")
            fwhm = get_widget_value(row, "MIN | FWHM | MAX")

            peak_models[row][model_name]['ampli'] = {
                'min': ampli['min'],
                'max': ampli['max'],
                'value': ampli['value'],
                'vary': get_widget_value(row, "Ampli_vary"),
                'expr': ampli['expr']
            }
            peak_models[row][model_name]['x0'] = {
                'min': x0['min'],
                'max': x0['max'],
                'value': x0['value'],
                'vary': get_widget_value(row, "x0_vary"),
                'expr': x0['expr']
            }
            peak_models[row][model_name]['fwhm'] = {
                'min': fwhm['min'],
                'max': fwhm['max'],
                'value': fwhm['value'],
                'vary': get_widget_value(row, "FWHM_vary"),
                'expr': fwhm['expr']
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

    def add_row(self, show_bounds, show_expr, **params):
        def create_spin_box_group_with_expr(min_value=None, value=None, max_value=None, expr=None):
            widget = SpinBoxGroupWithExpression(min_value, value, max_value, expr)
            widget.min_spin_box.editingFinished.connect(self.emit_peaks_changed)
            widget.value_spin_box.editingFinished.connect(self.emit_peaks_changed)
            widget.max_spin_box.editingFinished.connect(self.emit_peaks_changed)
            widget.expr_edit.editingFinished.connect(self.emit_peaks_changed)
            widget.show_bounds(show_bounds)
            widget.show_expr(show_expr)
            return widget

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

        x0_widget = create_spin_box_group_with_expr(params["x0_min"], params["x0"], params["x0_max"])
        x0_vary_checkbox = create_checkbox(params["x0_vary"])

        ampli_widget = create_spin_box_group_with_expr(params["ampli_min"], params["ampli"], params["ampli_max"])
        ampli_vary_checkbox = create_checkbox(params["ampli_vary"])

        fwhm_widget = create_spin_box_group_with_expr(params["fwhm_min"], params["fwhm"], params["fwhm_max"])
        fwhm_vary_checkbox = create_checkbox(params["fwhm_vary"])

        row_widgets = {
            "Prefix": prefix_btn,
            "Label": label_edit,
            "Model": model_combo,
            "MIN | X0 | MAX": x0_widget,
            "x0_vary": x0_vary_checkbox,
            "MIN | Ampli | MAX": ampli_widget,
            "Ampli_vary": ampli_vary_checkbox,
            "MIN | FWHM | MAX": fwhm_widget,
            "FWHM_vary": fwhm_vary_checkbox
        }

        self.table.add_row(**row_widgets)
        self.table.resizeRowsToContents()

    def update_prefix_colors(self):
        for row in range(self.table.rowCount()):
            prefix_btn = self.table.cellWidget(row, self.table.get_column_index("Prefix"))
            color = rgb2hex(self.cmap(row % self.cmap.N))
            prefix_btn.setStyleSheet(f"color: {color};")

    def show_bounds(self, show):
        for row in range(self.table.rowCount()):
            for column_name in ["MIN | X0 | MAX", "MIN | Ampli | MAX", "MIN | FWHM | MAX"]:
                widget = self.table.cellWidget(row, self.table.get_column_index(column_name))
                if isinstance(widget, SpinBoxGroupWithExpression):
                    widget.show_bounds(show)

        header = self.table.horizontalHeader()
        if show:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)

    def show_expr(self, show):
        for row in range(self.table.rowCount()):
            for column_name in ["MIN | X0 | MAX", "MIN | Ampli | MAX", "MIN | FWHM | MAX"]:
                widget = self.table.cellWidget(row, self.table.get_column_index(column_name))
                if isinstance(widget, SpinBoxGroupWithExpression):
                    widget.show_expr(show)
            self.table.resizeRowsToContents()