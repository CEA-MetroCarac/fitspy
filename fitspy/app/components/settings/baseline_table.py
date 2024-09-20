from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QSizePolicy, QLineEdit, QScrollArea
from PySide6.QtCore import Qt, Signal

class BaselineTable(QGroupBox):
    baselinePointChanged = Signal(int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Baseline table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        header_layout = QHBoxLayout()
        x_label = QLabel("X")
        x_label.setAlignment(Qt.AlignCenter)
        y_label = QLabel("Y")
        y_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(x_label)
        header_layout.addWidget(y_label)
        main_layout.addLayout(header_layout)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.table = QWidget()
        self.table_layout = QVBoxLayout(self.table)
        self.table_layout.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.table)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def clear(self):
        """ Clear the table """
        while self.table_layout.count():
            item = self.table_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout = item.layout()
                if layout is not None:
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.deleteLater()
                    layout.deleteLater()

    def set_points(self, points):
        self.sort_and_update_table(points)

    def sort_and_update_table(self, points):
        self.clear()
        for i, (x, y) in enumerate(zip(points[0], points[1])):
            self.add_row(i, x, y)

    def add_row(self, index, x, y):
        row = QHBoxLayout()

        x = QLineEdit(f"{x:.2f}")  # Only 2 decimals
        y = QLineEdit(f"{y:.2f}")

        # Couldn't put in Controller
        x.editingFinished.connect(lambda: self.baselinePointChanged.emit(index, float(x.text()), float(y.text())))
        y.editingFinished.connect(lambda: self.baselinePointChanged.emit(index, float(x.text()), float(y.text())))

        row.addWidget(x)
        row.addWidget(y)

        self.table_layout.addLayout(row)