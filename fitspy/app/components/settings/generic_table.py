from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QHeaderView, QPushButton, QSizePolicy, QAbstractItemView, QLineEdit, QComboBox, QSpinBox
from PySide6.QtCore import Qt, Signal

class GenericTable(QTableWidget):
    rowsDeleted = Signal(list)

    def __init__(self, columns, callbacks=None):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.columns = columns
        self.callbacks = callbacks or {}
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


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    columns = {
        "Prefix": QPushButton,
        "Label": QLineEdit,
        "Model": QComboBox,
        "x0": QSpinBox,
        "Ampli": QSpinBox,
        "fwhm": QSpinBox
    }

    def prefix_callback(row_widgets):
        print(f"Prefix clicked: {row_widgets['Prefix'].text()}")
        print(f"Label: {row_widgets['Label'].text()}")

    callbacks = {
        "Prefix": prefix_callback,
        "Label": lambda row_widgets: print(f"Label edited: {row_widgets['Label'].text()}"),
        "x0": lambda row_widgets: print(f"x0 {row_widgets['x0'].value()}"),
        "Ampli": lambda row_widgets: print(f"Ampli {row_widgets['Ampli'].value()}"),
    }

    peaks_table = GenericTable(columns, callbacks)

    rows_data = [
    {
        "Prefix": "m01_",
        "Label": "Label1",
        "Model": "Gaussian",
        "x0": 0,
        "Ampli": 0,
        "fwhm": 0
    },
    {
        "Prefix": "m02_",
        "Label": "Label2",
        "Model": "Laurentzian",
        "x0": 1,
        "Ampli": 1,
        "fwhm": 1
    }
]

    # Loop through the data and add rows to the table
    for row_data in rows_data:
        prefix_button = QPushButton(row_data["Prefix"])
        label_edit = QLineEdit(row_data["Label"])
        # label_edit.setReadOnly(True)
        model_combo = QComboBox()
        model_combo.addItem(row_data["Model"])
        x0_spin = QSpinBox()
        x0_spin.setValue(row_data["x0"])
        ampli_spin = QSpinBox()
        ampli_spin.setValue(row_data["Ampli"])
        fwhm_spin = QSpinBox()
        fwhm_spin.setValue(row_data["fwhm"])

        row_widgets = {
            "Prefix": prefix_button,
            "Label": label_edit,
            "Model": model_combo,
            "x0": x0_spin,
            "Ampli": ampli_spin,
            "fwhm": fwhm_spin
        }

        # Set the connections for the callbacks
        prefix_button.clicked.connect(lambda event, rw=row_widgets: callbacks["Prefix"](rw))
        label_edit.editingFinished.connect(lambda rw=row_widgets: callbacks["Label"](rw))
        x0_spin.valueChanged.connect(lambda value, rw=row_widgets: callbacks["x0"](rw))
        ampli_spin.valueChanged.connect(lambda value, rw=row_widgets: callbacks["Ampli"](rw))

        peaks_table.add_row(**row_widgets)

    # Create a button to toggle the visibility of the "Model" column
    toggle_button = QPushButton("Toggle Model Column")
    toggle_button.clicked.connect(lambda: peaks_table.toggle_column_visibility("Label"))

    # Set up the main window layout
    main_window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(peaks_table)
    layout.addWidget(toggle_button)
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)
    main_window.show()

    app.exec()
