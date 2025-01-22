from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QSizePolicy, QGroupBox, QVBoxLayout, QHeaderView, QLineEdit

from fitspy.apps.pyside.components.settings.generic_table import GenericTable


class BaselineTable(QGroupBox):
    baselinePointsChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Baseline table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.setMaximumWidth(150)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.table = GenericTable(columns={"X": QLineEdit, "Y": QLineEdit})
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        self.table.rowsDeleted.connect(self.emit_baseline_point_changed)
        self.setLayout(main_layout)

    def emit_baseline_point_changed(self):
        points = self.get_points()
        self.baselinePointsChanged.emit(points)

    def set_points(self, points):
        self.table.clear()
        for x, y in zip(points[0], points[1]):
            self.add_row(x, y)

    def add_row(self, x, y):
        x_edit = QLineEdit(f"{x:.2f}")  # Only 2 decimals
        y_edit = QLineEdit(f"{y:.2f}")

        row_widgets = {"X": x_edit, "Y": y_edit}

        x_edit.editingFinished.connect(self.emit_baseline_point_changed)
        y_edit.editingFinished.connect(self.emit_baseline_point_changed)

        self.table.add_row(**row_widgets)

    def get_points(self):
        points = []
        for row in range(self.table.rowCount()):
            x_widget = self.table.cellWidget(row, self.table.get_column_index("X"))
            y_widget = self.table.cellWidget(row, self.table.get_column_index("Y"))
            x_value = float(x_widget.text())
            y_value = float(y_widget.text())
            points.append((x_value, y_value))

        # Sort points by the X values
        points.sort(key=lambda point: point[0])

        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]

        return [x_values, y_values]


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = BaselineTable()
    obj.show()
    sys.exit(app.exec())
