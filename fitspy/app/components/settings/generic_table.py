from PySide6.QtWidgets import QTableWidget, QSizePolicy, QCheckBox, QWidget, QHBoxLayout, QAbstractItemView
from PySide6.QtCore import Qt, Signal

class GenericTable(QTableWidget):
    rowsDeleted = Signal(list)

    def __init__(self, columns):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.columns = columns
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(list(columns.keys()))
        self.row_count = 0

        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def clear(self):
        self.setRowCount(0)
        self.row_count = 0

    def add_row(self, **kwargs):
        self.insertRow(self.row_count)
        for col, header in enumerate(self.columns.keys()):
            widget = kwargs.get(header, self.columns[header]())
            
            if isinstance(widget, QCheckBox):
                container = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(widget)
                layout.setAlignment(widget, Qt.AlignCenter)
                container.setLayout(layout)
                widget = container
            
            self.setCellWidget(self.row_count, col, widget)
        self.row_count += 1

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
            row_data = {
                header: self.cellWidget(row, col)
                for col, header in enumerate(self.columns.keys())
            }
            deleted_rows_data.append((row, row_data))
            self.removeRow(row)
            self.row_count -= 1
        self.rowsDeleted.emit(deleted_rows_data)

    def remove_widget_row(self, widget):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                if self.cellWidget(row, col) == widget:
                    row_data = {
                        header: self.cellWidget(row, col)
                        for col, header in enumerate(self.columns.keys())
                    }
                    self.removeRow(row)
                    self.row_count -= 1
                    self.rowsDeleted.emit([(row, row_data)])
                    return