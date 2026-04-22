from PySide6.QtCore import Signal, QSignalBlocker
from PySide6.QtWidgets import (QLabel, QVBoxLayout,
                               QHeaderView, QWidget, QPushButton)
from PySide6.QtGui import QIcon

from fitspy import BKG_MODELS
from fitspy.core.utils import get_model_params
from fitspy.apps.pyside.utils import get_icon_path
from fitspy.apps.pyside.components.settings.generic_table import GenericTable
from fitspy.apps.pyside.components.custom_widgets import ComboBox
from fitspy.apps.pyside.components.settings.peaks_table import (SpinBoxGroupWithExpression,
                                                                CenteredCheckBox)


def model_params():
    return get_model_params(BKG_MODELS)

def is_bound_param(param):
    return "MIN |" and "| MAX" in param

def extract_param_name(param):
    return param.split("|")[1].strip().lower()

class BkgTable(QWidget):
    bkgsChanged = Signal(dict)
    showToast = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._bkg_model = list(model_params().keys())[0]
        self.initUI()
        self.show_bounds_state = True
        self.show_expr_state = False

    @property
    def bkg_model(self):
        return self._bkg_model

    @bkg_model.setter
    def bkg_model(self, model_name):
        if model_name not in model_params():
            return

        self._bkg_model = model_name

        if hasattr(self, "model_combo"):
            with QSignalBlocker(self.model_combo):
                self.model_combo.setCurrentText(model_name)

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)


        self.table = GenericTable(columns={})
        self.table.widgetsChanged.connect(self.emit_bkgs_changed)
        self.table.rowsDeleted.connect(self.emit_bkgs_changed)
        self.show_bounds(True)
        main_layout.addWidget(self.table)
        # self.add_row(False, False, model_name=self.bkg_model)
        self.setLayout(main_layout)

    def emit_bkgs_changed(self):
        self.update_columns_based_on_model()
        self.bkgsChanged.emit(self.get_bkgs())

    @property
    def row_count(self):
        return self.table.row_count

    def get_bkgs(self):
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

        # Legacy single-entry (first row) + multi-entry payload
        bkg_model = {}
        bkg_models = []

        # helper to read a given column value in a row
        def safe_get_widget_value(row, column_name):
            try:
                return get_widget_value(row, column_name)
            except Exception:
                return None

        for row in range(self.table.rowCount()):
            # Determine model name for this row
            model_name = safe_get_widget_value(row, "Model") or self.bkg_model

            params = model_params().get(model_name, [])
            param_hints = {}
            for param in params:
                if "MIN |" in param and "| MAX" in param:
                    param_name = param.split(" | ")[1].lower()
                    param_dict = safe_get_widget_value(row, param) or {"min": -float("inf"),
                                                                      "max": float("inf"),
                                                                      "value": 0,
                                                                      "expr": ""}
                    param_hints[param_name] = {
                        "min": param_dict["min"],
                        "max": param_dict["max"],
                        "value": param_dict["value"],
                        "vary": not (safe_get_widget_value(row, f"{param_name}_fixed") or False),
                        "expr": param_dict["expr"]}

            bkg_models.append({
                "id": f"b{row+1:02d}",
                "model_name": model_name,
                "order": row + 1,
                "param_hints": param_hints,
            })

            # fill legacy first-entry format for backwards compatibility
            if row == 0:
                bkg_model["bkg_model"] = {model_name: param_hints}

        bkg_model["bkg_models"] = bkg_models
        return bkg_model


    def create_spin_box_group_with_expr(self, min_value=-float("inf"), value=0,
                                        max_value=float("inf"), expr=""):
        widget = SpinBoxGroupWithExpression(min_value, value, max_value, expr)
        widget.min_spin_box.editingFinished.connect(self.emit_bkgs_changed)
        widget.value_spin_box.editingFinished.connect(self.emit_bkgs_changed)
        widget.max_spin_box.editingFinished.connect(self.emit_bkgs_changed)
        widget.expr_edit.editingFinished.connect(self.emit_bkgs_changed)
        widget.show_bounds(self.show_bounds_state)
        widget.show_expr(self.show_expr_state)
        return widget

    def update_columns_based_on_model(self):
        # Keep main combo in sync with property
        if hasattr(self, "model_combo") and self.model_combo.currentText() != self.bkg_model:
            with QSignalBlocker(self.model_combo):
                self.model_combo.setCurrentText(self.bkg_model)

        # Determine required columns as union of parameters used by each row's model
        required_columns = ["Prefix", "Model"]

        for row in range(self.table.rowCount()):
            # model widget may not exist yet
            try:
                model_widget = self.table.cellWidget(row, self.table.get_column_index("Model"))
                model_name = model_widget.currentText() if model_widget and hasattr(model_widget, "currentText") else self.bkg_model
            except Exception:
                model_name = self.bkg_model

            params = model_params().get(model_name, [])
            required_columns.extend(params)

        # Deduplicate while preserving order
        seen = set()
        required_columns = [x for x in required_columns if not (x in seen or seen.add(x))]

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

        # Update each row according to its own model
        for row in range(self.table.rowCount()):
            try:
                model_widget = self.table.cellWidget(row, self.table.get_column_index("Model"))
                model_name = model_widget.currentText() if model_widget and hasattr(model_widget, "currentText") else self.bkg_model
            except Exception:
                model_name = self.bkg_model

            parameters = model_params().get(model_name, [])

            for param in parameters:
                col_idx = self.table.get_column_index(param)
                existing_widget = self.table.cellWidget(row, col_idx)
                if "MIN |" in param and "| MAX" in param:
                    if not isinstance(existing_widget, SpinBoxGroupWithExpression):
                        widget = self.create_spin_box_group_with_expr()
                        self.table.setCellWidget(row, col_idx, widget)
                elif param.endswith("_fixed"):
                    if not isinstance(existing_widget, CenteredCheckBox):
                        widget = CenteredCheckBox(callback=self.emit_bkgs_changed)
                        self.table.setCellWidget(row, col_idx, widget)

            # Remove widgets for parameters not required by this row's model
            for column in list(self.table.columns.keys()):
                if column not in ["Prefix", "Model"] + parameters:
                    col_index = self.table.get_column_index(column)
                    # replace with empty widget
                    self.table.setCellWidget(row, col_index, QWidget())

    def clear(self):
        self.table.clear()

    def add_row(self, show_bounds, show_expr, **params):
        self.show_bounds_state = show_bounds
        self.show_expr_state = show_expr
        prefix = QPushButton(text=params["id"], icon=QIcon(get_icon_path("close.png")),
                             toolTip="Delete peak")
        # color = rgb2hex(cmap()(self.row_count % cmap().N))
        # prefix.setStyleSheet(f"color: {color};")
        prefix.clicked.connect(lambda: self.table.remove_widget_row(prefix))

        model_names = list(BKG_MODELS.keys())
        model_combo = ComboBox()
        model_combo.addItems(model_names)
        model_combo.setCurrentText(params["model_name"])

        row_widgets = {"Prefix": prefix, "Model": model_combo}

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

        # if self.params_order:
        #     self.reorder_params(self.params_order)
        #     self.params_order = None

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
