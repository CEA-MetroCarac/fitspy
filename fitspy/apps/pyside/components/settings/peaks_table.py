from matplotlib.colors import rgb2hex
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QPushButton, QLineEdit, QCheckBox,
                               QHeaderView, QWidget, QHBoxLayout)
from PySide6.QtGui import QIcon

from fitspy import PEAK_MODELS
from fitspy.core.utils import get_model_params
from fitspy.apps.pyside import DEFAULTS
from fitspy.apps.pyside.utils import get_icon_path
from fitspy.apps.pyside.components.settings.generic_table import GenericTable
from fitspy.apps.pyside.components.custom_widgets import DoubleSpinBox, ComboBox


def model_params():
    return get_model_params(PEAK_MODELS)


def is_bound_param(param):
    return "MIN |" and "| MAX" in param


def extract_param_name(param):
    return param.split("|")[1].strip().lower()


def cmap():
    return DEFAULTS["peaks_cmap"]


class SpinBoxGroupWithExpression(QWidget):
    showToast = Signal(str, str, str)

    def __init__(self, min_value=None, value=None, max_value=None, expr=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.spin_box_layout = QHBoxLayout()
        self.min_spin_box = DoubleSpinBox(empty_value=float("inf"))
        self.value_spin_box = DoubleSpinBox(empty_value=float("inf"))
        self.max_spin_box = DoubleSpinBox(empty_value=float("inf"))

        for sb in (self.min_spin_box, self.value_spin_box, self.max_spin_box):
            sb.setMinimumWidth(75)

        self.min_spin_box.editingFinished.connect(self._validate_bounds)
        self.max_spin_box.valueChanged.connect(self._validate_bounds)
        self.value_spin_box.editingFinished.connect(self._validate_value)

        self._previous_value = value if value is not None else float("inf")

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

    def _validate_bounds(self):
        min_val = self.min_spin_box.value()
        max_val = self.max_spin_box.value()

        if min_val > max_val:
            # Reset to previous valid bounds
            if self.sender() == self.min_spin_box:
                self.min_spin_box.setValue(max_val)
            else:
                self.max_spin_box.setValue(min_val)
            self.showToast.emit(
                "WARNING",
                "Invalid bounds",
                "Minimum value must be less than maximum value.",
            )
            return False
        return True

    def _validate_value(self):
        if not self._validate_bounds():
            self.value_spin_box.setValue(self._previous_value)
            return

        min_val = self.min_spin_box.value()
        max_val = self.max_spin_box.value()
        current_val = self.value_spin_box.value()

        if not (min_val <= current_val <= max_val):
            self.value_spin_box.setValue(self._previous_value)
            self.showToast.emit(
                "WARNING",
                "Value out of bounds",
                f"Value {current_val} must be between {min_val} and "
                f"{max_val}.",
            )
        else:
            self._previous_value = current_val

    def get_values(self):
        return {
            "min": self.min_spin_box.value(),
            "value": self.value_spin_box.value(),
            "max": self.max_spin_box.value(),
            "expr": self.expr_edit.text(),
        }

    def set_values(self, min_value, value, max_value, expr):
        self.min_spin_box.setValue(min_value)
        self.value_spin_box.setValue(value)
        self.max_spin_box.setValue(max_value)
        self.expr_edit.setText(expr)

    def show_expr(self, show):
        self.expr_edit.setVisible(show)

    def show_bounds(self, show):
        self.min_spin_box.setVisible(show)
        self.max_spin_box.setVisible(show)

    def blockSignals(self, b):
        self.min_spin_box.blockSignals(b)
        self.value_spin_box.blockSignals(b)
        self.max_spin_box.blockSignals(b)
        self.expr_edit.blockSignals(b)


class CenteredCheckBox(QWidget):
    def __init__(self, checked=False, callback=None, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.checkbox = QCheckBox()
        self.checkbox.setChecked(checked)
        self.layout.addWidget(self.checkbox)
        self.layout.setAlignment(self.checkbox, Qt.AlignCenter)

        if callback:
            self.checkbox.stateChanged.connect(callback)

    def __getattr__(self, name):
        return getattr(self.checkbox, name)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)

    def blockSignals(self, b):
        self.checkbox.blockSignals(b)


class PeaksTable(QWidget):
    peakSelected = Signal(int)
    peaksChanged = Signal(dict)
    showToast = Signal(str, str, str)

    def __init__(self, params_order=None, parent=None):
        super().__init__(parent)
        if params_order is None:
            params_order = ['Prefix', 'Label', 'Model',
                            'x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']
        self.params_order = params_order
        self.initUI()
        self.show_bounds_state = None  # FIXME: bool instead ? What for show_bounds_state=True ?
        self.show_expr_state = None

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        columns = {"Prefix": QLabel, "Label": QLineEdit, "Model": ComboBox}
        self.table = GenericTable(columns=columns)
        self.table.horizontalHeader().setMinimumSectionSize(75)
        self.table.widgetsChanged.connect(self.emit_peaks_changed)
        self.show_bounds(True)
        main_layout.addWidget(self.table)
        self.table.rowsDeleted.connect(self.emit_peaks_changed)
        self.table.rowsDeleted.connect(self.update_prefix_colors)
        self.table.itemSelectionChanged.connect(
            lambda: self.peakSelected.emit(
                self.table.get_selected_rows()[0]
                if self.table.get_selected_rows()
                else -1
            )
        )
        self.setLayout(main_layout)

    @property
    def row_count(self):
        return self.table.row_count

    def get_peaks(self):
        def get_widget_value(row, column_name):
            # case insensitive search
            column_names = [col_name.lower() for col_name in self.table.columns]
            widget = self.table.cellWidget(row, column_names.index(column_name.lower()))

            if isinstance(widget, SpinBoxGroupWithExpression):
                return widget.get_values()
            elif isinstance(widget, CenteredCheckBox):
                return widget.isChecked()
            elif hasattr(widget, "value"):
                return widget.value()
            elif hasattr(widget, "currentText"):
                return widget.currentText()
            else:
                return widget.text()

        peaks = {"peak_models": {}, "peak_labels": []}
        peak_models = peaks["peak_models"]
        peak_labels = peaks["peak_labels"]

        for row in range(self.table.rowCount()):
            label = get_widget_value(row, "Label")
            model_name = get_widget_value(row, "Model")

            peak_labels.append(label)

            if row not in peak_models:
                peak_models[row] = {}
            if model_name not in peak_models[row]:
                peak_models[row][model_name] = {}

            params = model_params()

            for param in params[model_name]:
                if is_bound_param(param):
                    param_name = param.split(" | ")[1].lower()
                    param_dict = get_widget_value(row, param)
                    peak_models[row][model_name][param_name] = {
                        "min": param_dict["min"],
                        "max": param_dict["max"],
                        "value": param_dict["value"],
                        "vary": not get_widget_value(row, f"{param_name}_fixed"),
                        "expr": param_dict["expr"],
                    }
        return peaks

    def emit_peaks_changed(self):
        self.update_columns_based_on_model()
        self.peaksChanged.emit(self.get_peaks())

    def create_spin_box_group_with_expr(self, min=None, value=None, max=None, expr="",
                                        param_name=None):

        if param_name in ['fwhm', 'fwhm_l', 'fwhm_r']:
            min = 0
            value = self.fwhm
            max = 1.5 * value

        elif param_name == 'alpha':
            min = 0
            value = 0.5
            max = 1

        if min is None or value is None or max is None:
            raise ValueError("min, value, and max cannot be None")

        widget = SpinBoxGroupWithExpression(min, value, max, expr)
        widget.show_bounds(self.show_bounds_state)
        widget.showToast.connect(self.showToast)
        widget.show_expr(self.show_expr_state)
        return widget

    def update_columns_based_on_model(self):
        required_columns = ["Prefix", "Label", "Model"]

        cellWidget = self.table.cellWidget

        # Getting additional required columns based on used models
        for row in range(self.table.rowCount()):
            model_name = cellWidget(row, self.table.get_column_index("Model")).currentText()
            parameters = model_params().get(model_name, [])
            required_columns.extend(parameters)

        # Remove unnecessary columns
        for column in list(self.table.columns.keys()):
            if column not in required_columns:
                self.table.remove_column(column)

        # Add missing columns
        for column in required_columns:
            if column not in self.table.columns:
                if "MIN" in column and "MAX" in column:
                    self.table.add_column(column, SpinBoxGroupWithExpression)
                elif column.endswith("_fixed"):
                    self.table.add_column(column, CenteredCheckBox)
                else:
                    self.table.add_column(column, QLabel)

        # Update each row
        for row in range(self.table.rowCount()):
            model_name = cellWidget(row, self.table.get_column_index("Model")).currentText()
            parameters = model_params().get(model_name, [])

            # Set widgets for required parameters
            for param in parameters:
                col = self.table.get_column_index(param)
                widget = cellWidget(row, col)
                if widget is None or isinstance(widget, QWidget) and not widget.children():
                    if is_bound_param(param):
                        if not isinstance(widget, SpinBoxGroupWithExpression):
                            widget = self.create_spin_box_group_with_expr(
                                param_name=extract_param_name(param)
                            )
                            self.table.setCellWidget(row, col, widget)
                    elif param.endswith("_fixed"):
                        if not isinstance(widget, CenteredCheckBox):
                            widget = CenteredCheckBox()
                            self.table.setCellWidget(row, col, widget)

            # Remove widgets for parameters not required by the model
            for column in self.table.columns:
                if column not in ["Prefix", "Label", "Model"] + parameters:
                    col_index = self.table.get_column_index(column)
                    self.table.setCellWidget(row, col_index, QWidget())

        self.table.resizeRowsToContents()

    def clear(self):
        self.table.clear()

    def add_row(self, show_bounds, show_expr, **params):
        self.show_bounds_state = show_bounds
        self.show_expr_state = show_expr
        prefix = QPushButton(text=params["prefix"], icon=QIcon(get_icon_path("close.png")),
                             toolTip="Delete peak")
        color = rgb2hex(cmap()(self.row_count % cmap().N))
        prefix.setStyleSheet(f"color: {color};")
        prefix.clicked.connect(lambda: self.table.remove_widget_row(prefix))

        label = QLineEdit(params["label"])

        model_names = list(PEAK_MODELS.keys())
        model_combo = ComboBox()
        model_combo.addItems(model_names)
        model_combo.setCurrentText(params["model_name"])

        row_widgets = {"Prefix": prefix, "Label": label, "Model": model_combo}

        model_name = params["model_name"]
        parameters = model_params().get(model_name, [])
        for param in parameters:
            # Getting min, value, max and expr values
            if is_bound_param(param):
                param_name = extract_param_name(param)
                min_value = params.get(f"{param_name}_min")
                value = params.get(f"{param_name}")
                max_value = params.get(f"{param_name}_max")
                expr = params.get(f"{param_name}_expr")
                widget = self.create_spin_box_group_with_expr(min_value, value, max_value, expr)
                widget.show_bounds(show_bounds)
                widget.show_expr(show_expr)
                row_widgets[param] = widget
            elif param.endswith("_fixed"):
                checked = params.get(param, False)
                widget = CenteredCheckBox(checked)
                row_widgets[param] = widget

        # Ensure all columns are added to the table
        for column in row_widgets.keys():
            if column not in self.table.columns:
                if is_bound_param(column):
                    self.table.add_column(column, SpinBoxGroupWithExpression)
                elif column.endswith("_fixed"):
                    self.table.add_column(column, CenteredCheckBox)
                else:
                    self.table.add_column(column, type(row_widgets[column]))

        if self.params_order:
            self.reorder_params(self.params_order)
            self.params_order = None

        self.table.add_row(**row_widgets)
        self.update_columns_based_on_model()

    def update_prefix_colors(self):
        for row in range(self.table.rowCount()):
            prefix = self.table.cellWidget(row, self.table.get_column_index("Prefix"))
            color = rgb2hex(cmap()(row % cmap().N))
            prefix.setStyleSheet(f"color: {color};")

    def show_bounds(self, show):
        for row in range(self.table.rowCount()):
            for column_name in self.table.columns:
                if is_bound_param(column_name):
                    widget = self.table.cellWidget(row, self.table.get_column_index(column_name))
                    if isinstance(widget, SpinBoxGroupWithExpression):
                        widget.show_bounds(show)
        self.show_bounds_state = show
        self.table.set_header_labels(show_bounds=show)
        if show:
            self.table.set_header_resize_mode(QHeaderView.ResizeToContents)
        else:
            self.table.set_header_resize_mode(QHeaderView.Stretch)

    def show_expr(self, show):
        for row in range(self.table.rowCount()):
            for column_name in self.table.columns:
                if is_bound_param(column_name):
                    widget = self.table.cellWidget(row, self.table.get_column_index(column_name))
                    if isinstance(widget, SpinBoxGroupWithExpression):
                        widget.show_expr(show)
            self.table.resizeRowsToContents()
        self.show_expr_state = show

    def reorder_params(self, order):
        # Expand non basic items into full parameter columns.
        new_order = []
        for item in order:
            if item in ["Prefix", "Label", "Model"]:
                new_order.append(item)
            else:
                new_order.append(f"MIN | {item} | MAX")
                new_order.append(f"{item}_fixed")
        self.params_order = order
        self.table.set_column_order(new_order)
