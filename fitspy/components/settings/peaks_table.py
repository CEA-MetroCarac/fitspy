from PySide6.QtWidgets import QAbstractItemView, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QCheckBox, QScrollArea, QComboBox
from PySide6.QtCore import Qt

class PeaksTable(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setTitle("Peak table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create a scroll area and set the table widget as its widget
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        # scroll_area.setWidget(self.table_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    # def add_row(self, label, model_items, x0_value, fwhm_value, ampli_value):

# if __name__ == "__main__":
#     from PySide6.QtWidgets import QApplication

#     app = QApplication([])

#     peaks_table = PeaksTable()
#     peaks_table.add_row("Label 1", ["Model 1", "Model 2", "Model 3"], 1.0, 1.0, 1.0)
#     peaks_table.add_row("Label 2", ["Model 1", "Model 2", "Model 3"], 2.0, 2.0, 2.0)

#     peaks_table.show()
#     app.exec()