# EACH ROW IN THE TABLE WILL HAVE THE FOLLOWING COLUMNS:
# Delete column with the option to select multiple rows and delete them all at once or delete all
# Prefix: colored text, no edit
# Label, editable
# model, combo box, editable
# x0, editable, spin box
# Ampli, editable, spin box
# FWHM, editable, spin box

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