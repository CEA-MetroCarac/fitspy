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

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)  # 8 columns
        self.table_widget.setHorizontalHeaderLabels(["Label", "Model", "X0", "fix X0", "Fwhm", "fix Fwhm", "Ampli", "Fix Ampli"])
        self.table_widget.setShowGrid(False)

        self.table_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        # for row in range(10):
        #     # Label (text input)
        #     label_item = QTableWidgetItem(f"Label {row + 1}")
        #     self.table_widget.setItem(row, 0, label_item)

        #     # Model (combo box)
        #     model_combo = QComboBox()
        #     model_combo.addItems(["Model 1", "Model 2", "Model 3"])  # Example items
        #     self.table_widget.setCellWidget(row, 1, model_combo)

        #     # X0 (float input)
        #     x0_input = QLineEdit()
        #     x0_input.setText(f"{row + 1}.0")
        #     self.table_widget.setCellWidget(row, 2, x0_input)

        #     # fix X0 (checkbox)
        #     fix_x0_checkbox = QCheckBox()
        #     fix_x0_widget = QWidget()
        #     fix_x0_layout = QHBoxLayout(fix_x0_widget)
        #     fix_x0_layout.addWidget(fix_x0_checkbox)
        #     fix_x0_layout.setAlignment(fix_x0_checkbox, Qt.AlignCenter)
        #     fix_x0_layout.setContentsMargins(0, 0, 0, 0)
        #     self.table_widget.setCellWidget(row, 3, fix_x0_widget)

        #     # Fwhm (float input)
        #     fwhm_input = QLineEdit()
        #     fwhm_input.setText(f"{row + 1}.0")
        #     self.table_widget.setCellWidget(row, 4, fwhm_input)

        #     # fix Fwhm (checkbox)
        #     fix_fwhm_checkbox = QCheckBox()
        #     fix_fwhm_widget = QWidget()
        #     fix_fwhm_layout = QHBoxLayout(fix_fwhm_widget)
        #     fix_fwhm_layout.addWidget(fix_fwhm_checkbox)
        #     fix_fwhm_layout.setAlignment(fix_fwhm_checkbox, Qt.AlignCenter)
        #     fix_fwhm_layout.setContentsMargins(0, 0, 0, 0)
        #     self.table_widget.setCellWidget(row, 5, fix_fwhm_widget)

        #     # Ampli (float input)
        #     ampli_input = QLineEdit()
        #     ampli_input.setText(f"{row + 1}.0")
        #     self.table_widget.setCellWidget(row, 6, ampli_input)

        #     # Fix Ampli (checkbox)
        #     fix_ampli_checkbox = QCheckBox()
        #     fix_ampli_widget = QWidget()
        #     fix_ampli_layout = QHBoxLayout(fix_ampli_widget)
        #     fix_ampli_layout.addWidget(fix_ampli_checkbox)
        #     fix_ampli_layout.setAlignment(fix_ampli_checkbox, Qt.AlignCenter)
        #     fix_ampli_layout.setContentsMargins(0, 0, 0, 0)
        #     self.table_widget.setCellWidget(row, 7, fix_ampli_widget)

        self.table_widget.resizeColumnsToContents()
        # self.table_widget.setColumnWidth(2, 50)  # X0
        # self.table_widget.setColumnWidth(4, 50)  # Fwhm
        # self.table_widget.setColumnWidth(6, 50)  # Ampli

        # Create a scroll area and set the table widget as its widget
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table_widget)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def add_row(self, label, model_items, x0_value, fwhm_value, ampli_value):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)

        # Label (text input)
        label_item = QTableWidgetItem(label)
        self.table_widget.setItem(row, 0, label_item)

        # Model (combo box)
        model_combo = QComboBox()
        model_combo.addItems(model_items)
        self.table_widget.setCellWidget(row, 1, model_combo)

        # X0 (float input)
        x0_input = QLineEdit()
        x0_input.setText(str(x0_value))
        x0_input.setFixedWidth(50)
        self.table_widget.setCellWidget(row, 2, x0_input)

        # fix X0 (checkbox)
        fix_x0_checkbox = QCheckBox()
        fix_x0_widget = QWidget()
        fix_x0_layout = QHBoxLayout(fix_x0_widget)
        fix_x0_layout.addWidget(fix_x0_checkbox)
        fix_x0_layout.setAlignment(fix_x0_checkbox, Qt.AlignCenter)
        fix_x0_layout.setContentsMargins(0, 0, 0, 0)
        self.table_widget.setCellWidget(row, 3, fix_x0_widget)

        # Fwhm (float input)
        fwhm_input = QLineEdit()
        fwhm_input.setText(str(fwhm_value))
        fwhm_input.setFixedWidth(60)  # Set fixed width for float input
        self.table_widget.setCellWidget(row, 4, fwhm_input)

        # fix Fwhm (checkbox)
        fix_fwhm_checkbox = QCheckBox()
        fix_fwhm_widget = QWidget()
        fix_fwhm_layout = QHBoxLayout(fix_fwhm_widget)
        fix_fwhm_layout.addWidget(fix_fwhm_checkbox)
        fix_fwhm_layout.setAlignment(fix_fwhm_checkbox, Qt.AlignCenter)
        fix_fwhm_layout.setContentsMargins(0, 0, 0, 0)
        self.table_widget.setCellWidget(row, 5, fix_fwhm_widget)

        # Ampli (float input)
        ampli_input = QLineEdit()
        ampli_input.setText(str(ampli_value))
        ampli_input.setFixedWidth(60)  # Set fixed width for float input
        self.table_widget.setCellWidget(row, 6, ampli_input)

        # Fix Ampli (checkbox)
        fix_ampli_checkbox = QCheckBox()
        fix_ampli_widget = QWidget()
        fix_ampli_layout = QHBoxLayout(fix_ampli_widget)
        fix_ampli_layout.addWidget(fix_ampli_checkbox)
        fix_ampli_layout.setAlignment(fix_ampli_checkbox, Qt.AlignCenter)
        fix_ampli_layout.setContentsMargins(0, 0, 0, 0)
        self.table_widget.setCellWidget(row, 7, fix_ampli_widget)

        # Adjust column widths
        self.table_widget.resizeColumnsToContents()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    peaks_table = PeaksTable()
    peaks_table.add_row("Label 1", ["Model 1", "Model 2", "Model 3"], 1.0, 1.0, 1.0)
    peaks_table.add_row("Label 2", ["Model 1", "Model 2", "Model 3"], 2.0, 2.0, 2.0)

    peaks_table.show()
    app.exec()