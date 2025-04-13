from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QHeaderView, QWidget

from fitspy import BKG_MODELS
from fitspy.core.utils import get_model_params
from fitspy.apps.pyside.components.settings.generic_table import GenericTable
from fitspy.apps.pyside.components.settings.peaks_table import (SpinBoxGroupWithExpression,
                                                                CenteredCheckBox)


def model_params():
    return get_model_params(BKG_MODELS)


class BkgTable(QWidget):
    bkgChanged = Signal(dict)
    showToast = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bkg_model = list(model_params().keys())[0]
        self.initUI()
        self.show_bounds_state = True
        self.show_expr_state = False

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.table = GenericTable(columns={})
        self.show_bounds(True)
        main_layout.addWidget(self.table)
        self.add_row(False, False, model_name=self.bkg_model)
        self.setLayout(main_layout)

    @property
    def row_count(self):
        return self.table.row_count

    def get_bkg_model(self):
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

        bkg_model = {"bkg_model": {self.bkg_model: {}}}

        for row in range(self.table.rowCount()):
            params = model_params()[self.bkg_model]
            for param in params:
                if "MIN |" and "| MAX" in param:
                    param_name = param.split(" | ")[1].lower()
                    param_dict = get_widget_value(row, param)
                    bkg_model["bkg_model"][self.bkg_model][param_name] = {
                        "min": param_dict["min"],
                        "max": param_dict["max"],
                        "value": param_dict["value"],
                        "vary": not get_widget_value(row, f"{param_name}_fixed"),
                        "expr": param_dict["expr"]}

        return bkg_model

    def emit_bkg_changed(self):
        bkg_model = self.get_bkg_model()

        # if there is a peak with incorrect bounds, show a warning and return
        for param in bkg_model["bkg_model"][self.bkg_model].values():
            if param["min"] > param["max"]:
                self.showToast.emit(
                    "WARNING",
                    "Invalid bounds",
                    "Minimum value must be less than maximum value.")
                return
            if not (param["min"] <= param["value"] <= param["max"]):
                self.showToast.emit(
                    "WARNING",
                    "Value out of bounds",
                    f"Value {param['value']} must be between {param['min']} and {param['max']}.")
                return

        self.bkgChanged.emit(bkg_model)

    def create_spin_box_group_with_expr(self, min_value=-float("inf"), value=0,
                                        max_value=float("inf"), expr=""):
        widget = SpinBoxGroupWithExpression(min_value, value, max_value, expr)
        widget.min_spin_box.editingFinished.connect(self.emit_bkg_changed)
        widget.value_spin_box.editingFinished.connect(self.emit_bkg_changed)
        widget.max_spin_box.editingFinished.connect(self.emit_bkg_changed)
        widget.expr_edit.editingFinished.connect(self.emit_bkg_changed)
        widget.show_bounds(self.show_bounds_state)
        widget.show_expr(self.show_expr_state)
        return widget

    def update_columns_based_on_model(self):
        # Get required columns for the selected bkg model
        required_columns = model_params().get(self.bkg_model, [])

        if not required_columns:
            self.clear()
            return

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
            parameters = model_params().get(self.bkg_model, [])
            for param in parameters:
                if "MIN |" in param and "| MAX" in param:
                    existing_widget = self.table.cellWidget(row, self.table.get_column_index(param))
                    if not isinstance(existing_widget, SpinBoxGroupWithExpression):
                        widget = self.create_spin_box_group_with_expr()
                        self.table.setCellWidget(row, self.table.get_column_index(param), widget)
                elif param.endswith("_fixed"):
                    existing_widget = self.table.cellWidget(row, self.table.get_column_index(param))
                    if not isinstance(existing_widget, CenteredCheckBox):
                        widget = CenteredCheckBox(callback=self.emit_bkg_changed)
                        self.table.setCellWidget(row, self.table.get_column_index(param), widget)

    def clear(self):
        """del all columns of self.table without deleting rows"""
        for column in list(self.table.columns.keys()):
            self.table.remove_column(column)
        self.bkgChanged.emit({"bkg_model": None})

    def add_row(self, show_bounds, show_expr, **params):
        self.show_bounds_state = show_bounds
        self.show_expr_state = show_expr

        row_widgets = {}

        model_name = params["model_name"]
        parameters = model_params().get(model_name, [])

        for param in parameters:
            # Getting min, value, max and expr values
            if "MIN |" in param and "| MAX" in param:
                param_key = param.split("|")[1].strip().lower()
                min_value = params.get(f"{param_key}_min")
                value = params.get(f"{param_key}")
                max_value = params.get(f"{param_key}_max")
                expr = params.get(f"{param_key}_expr")
                widget = self.create_spin_box_group_with_expr(min_value, value, max_value, expr)
                widget.show_bounds(show_bounds)
                widget.show_expr(show_expr)
                row_widgets[param] = widget
            elif param.endswith("_fixed"):
                checked = params.get(param, False)
                widget = CenteredCheckBox(checked, callback=self.emit_bkg_changed)
                row_widgets[param] = widget

        # Ensure all columns are added to the table
        for column in row_widgets.keys():
            if column not in self.table.columns:
                if "MIN |" in column and "| MAX" in column:
                    self.table.add_column(column, SpinBoxGroupWithExpression)
                elif column.endswith("_fixed"):
                    self.table.add_column(column, CenteredCheckBox)
                else:
                    self.table.add_column(column, type(row_widgets[column]))

        self.table.add_row(**row_widgets)
        self.update_columns_based_on_model()

    def update_row(self, param_hints, row=0):
        for param, hints in param_hints.items():
            min_max_col = f"MIN | {param} | MAX"
            fixed_col = f"{param}_fixed"

            # Update SpinBoxGroupWithExpression
            spin_widget = self.table.cellWidget(row, self.table.get_column_index(min_max_col))
            if isinstance(spin_widget, SpinBoxGroupWithExpression):
                spin_widget.set_values(min_value=hints.get("min", -float("inf")),
                                       value=hints.get("value", 0),
                                       max_value=hints.get("max", float("inf")),
                                       expr=hints.get("expr", ""))

            # Update CenteredCheckBox
            fixed_widget = self.table.cellWidget(row, self.table.get_column_index(fixed_col))
            if isinstance(fixed_widget, CenteredCheckBox):
                fixed_widget.setChecked(hints.get("fixed", False))

    def show_bounds(self, show):
        for row in range(self.table.rowCount()):
            for column_name in self.table.columns:
                if "MIN |" in column_name and "| MAX" in column_name:
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
                if "MIN |" in column_name and "| MAX" in column_name:
                    widget = self.table.cellWidget(row, self.table.get_column_index(column_name))
                    if isinstance(widget, SpinBoxGroupWithExpression):
                        widget.show_expr(show)
            self.table.resizeRowsToContents()
        self.show_expr_state = show


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = BkgTable()
    obj.show()
    sys.exit(app.exec())
