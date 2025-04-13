from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTableWidget, QSizePolicy, QAbstractItemView, QHeaderView


class GenericTable(QTableWidget):
    rowsDeleted = Signal(list)
    widgetsChanged = Signal()

    def __init__(self, columns):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.columns = columns
        self.setColumnCount(len(columns))
        self.set_header_labels()
        self.row_count = 0

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.lastEditingWidget = None
        self.itemSelectionChanged.connect(self.handleSelectionChanged)

    def setDisabled(self, state):
        """Override setDisabled to keep scrollbars enabled while disabling cell widgets"""
        super().setEnabled(True)

        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                widget = self.cellWidget(row, col)
                if widget:
                    widget.setEnabled(not state)

    def setEnabled(self, state):
        self.setDisabled(not state)

    def set_header_resize_mode(self, mode):
        header = self.horizontalHeader()
        for col in range(self.columnCount()):
            header.setSectionResizeMode(col, mode)

    def clear(self):
        self.setRowCount(0)
        self.row_count = 0

    def add_row(self, **kwargs):
        self.insertRow(self.row_count)
        for col, header in enumerate(self.columns.keys()):
            widget = kwargs.get(header)
            self.setCellWidget(self.row_count, col, widget)
            # Register widget for multi-edit capabilities
            if widget:
                self.register_widget_for_multi_edit(self.row_count, col, widget)
        self.row_count += 1
        self.resizeRowsToContents()

    def add_column(self, column_name, widget_class):
        if column_name not in self.columns:
            self.columns[column_name] = widget_class
            self.setColumnCount(len(self.columns))
            self.set_header_labels()
            self.set_header_resize_mode(QHeaderView.ResizeToContents)

    def remove_column(self, column_name):
        if column_name in self.columns:
            column_index = self.get_column_index(column_name)
            self.removeColumn(column_index)
            del self.columns[column_name]
            self.setColumnCount(len(self.columns))
            self.set_header_labels()
            self.set_header_resize_mode(QHeaderView.Stretch)

    def set_header_labels(self, show_bounds=True):
        labels = list(self.columns.keys())
        labels = ['fixed' if '_fixed' in label else label for label in labels]
        if not show_bounds:
            labels = [label.replace('MIN |', '') for label in labels]
            labels = [label.replace('| MAX', '') for label in labels]
        self.setHorizontalHeaderLabels(labels)

    def get_column_index(self, column_name):
        return list(self.columns.keys()).index(column_name)

    def toggle_column_visibility(self, column_name):
        column_index = self.get_column_index(column_name)
        current_visibility = self.isColumnHidden(column_index)
        self.setColumnHidden(column_index, not current_visibility)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.delete_selected_rows()
        else:
            super().keyPressEvent(event)

    def delete_selected_rows(self):
        selected_rows = sorted(set(index.row() for index in self.selectedIndexes()), reverse=True)
        deleted_rows_data = []
        for row in selected_rows:
            row_data = {header: self.cellWidget(row, col)
                        for col, header in enumerate(self.columns.keys())}
            deleted_rows_data.append((row, row_data))
            self.removeRow(row)
            self.row_count -= 1
        self.rowsDeleted.emit(deleted_rows_data)

    def remove_widget_row(self, widget):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                if self.cellWidget(row, col) == widget:
                    row_data = {header: self.cellWidget(row, col)
                                for col, header in enumerate(self.columns.keys())}
                    self.removeRow(row)
                    self.row_count -= 1
                    self.rowsDeleted.emit([(row, row_data)])
                    return

    def set_column_order(self, order):
        current_columns = list(self.columns.keys())
        new_order = [col for col in order if col in current_columns]
        new_order += [col for col in current_columns if col not in new_order]

        # self.setHorizontalHeaderLabels(new_order)
        self.columns = {col: self.columns[col] for col in new_order}
        self.setColumnCount(len(self.columns))
        self.set_header_labels()
        # self.set_header_resize_mode(QHeaderView.ResizeToContents)

    def get_selected_rows(self):
        """Return list of selected row indices"""
        return sorted(set(index.row() for index in self.selectedIndexes()))

    def handleSelectionChanged(self):
        """Reset last editing widget when selection changes"""
        self.lastEditingWidget = None

    def propagate_edit(self, row, col, value):
        """Propagate an edit to all selected rows for the same column"""
        selected_rows = self.get_selected_rows()
        self.widgetsChanged.emit()

        if len(selected_rows) <= 1:
            return

        for other_row in selected_rows:
            if other_row != row:
                widget = self.cellWidget(other_row, col)
                if widget and widget != self.lastEditingWidget:
                    widget.blockSignals(True)
                    self.apply_value_to_widget(widget, value)
                    widget.blockSignals(False)

    def apply_value_to_widget(self, widget, value):
        """Apply a value to a widget based on its type"""
        if hasattr(widget, 'get_values') and hasattr(widget, 'set_values'):
            widget.set_values(value['min'], value['value'], value['max'], value['expr'])

        elif hasattr(widget, 'setChecked'):
            widget.setChecked(value)

        elif hasattr(widget, 'setCurrentText'):
            widget.setCurrentText(value)

        elif hasattr(widget, 'setText'):
            widget.setText(value)

        elif hasattr(widget, 'setValue'):
            widget.setValue(value)

    def register_widget_for_multi_edit(self, row, col, widget):
        """Connect appropriate signals based on widget type"""
        signal_connections = {
            'stateChanged': lambda w: (
                w.stateChanged,
                lambda state: self._handle_widget_change(row, col, w, w.isChecked())),
            'textChanged': lambda w: (
                w.textEdited,
                lambda text: self._handle_widget_change(row, col, w, text)),
            'currentTextChanged': lambda w: (
                w.currentTextChanged,
                lambda text: self._handle_widget_change(row, col, w, text)),
        }

        for signal_name, connector in signal_connections.items():
            if hasattr(widget, signal_name):
                signal, handler = connector(widget)
                signal.connect(handler)
                return

        # SpinBoxGroupWithExpression
        if hasattr(widget, 'get_values'):
            for child_name in ['value_spin_box', 'min_spin_box', 'max_spin_box', 'expr_edit']:
                if hasattr(widget, child_name):
                    child = getattr(widget, child_name)
                    signal = child.valueChanged if hasattr(child,
                                                           'valueChanged') else child.textChanged
                    signal.connect(
                        lambda: self._handle_widget_change(row, col, widget, widget.get_values()))

    def _handle_widget_change(self, row, col, widget, value):
        """Handle widget change and propagate to selected rows"""
        self.lastEditingWidget = widget
        self.propagate_edit(row, col, value)
