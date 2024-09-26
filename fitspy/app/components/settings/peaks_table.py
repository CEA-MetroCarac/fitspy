from pathlib import Path
from PySide6.QtWidgets import (
    QLabel, QGroupBox, QVBoxLayout, QPushButton, QDoubleSpinBox, QComboBox, QLineEdit, QHeaderView, QSizePolicy
)
from PySide6.QtGui import QIcon
from matplotlib.colors import rgb2hex
import matplotlib.cm as cm
from fitspy import PEAK_MODELS

from .generic_table import GenericTable

project_root = Path(__file__).resolve().parent.parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class PeaksTable(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.cmap = cm.get_cmap("tab10")

    def initUI(self):
        self.setTitle("Peak table")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.table = GenericTable(
            columns={
                "Prefix": QLabel,
                "Label": QLineEdit,
                "Model": QComboBox,
                "x0_min": QDoubleSpinBox,
                "x0": QDoubleSpinBox,
                "x0_max": QDoubleSpinBox,
                "Ampli_min": QDoubleSpinBox,
                "Ampli": QDoubleSpinBox,
                "Ampli_max": QDoubleSpinBox,
                "FWHM_min": QDoubleSpinBox,
                "FWHM": QDoubleSpinBox,
                "FWHM_max": QDoubleSpinBox
            }
        )
        self.show_bounds(False)
        main_layout.addWidget(self.table)
        self.table.rowsDeleted.connect(self.emit_peaks_changed)
        self.setLayout(main_layout)

    @property
    def row_count(self):
        return self.table.row_count
    
    def get_peaks(self):
        pass
        peaks = {}
        for row in range(self.table.rowCount()):
            prefix_widget = self.table.cellWidget(row, self.table.get_column_index("Prefix"))
            label_widget = self.table.cellWidget(row, self.table.get_column_index("Label"))
            model_widget = self.table.cellWidget(row, self.table.get_column_index("Model"))
            x0_widget = self.table.cellWidget(row, self.table.get_column_index("x0"))
            ampli_widget = self.table.cellWidget(row, self.table.get_column_index("Ampli"))
            fwhm_widget = self.table.cellWidget(row, self.table.get_column_index("FWHM"))
            peaks[prefix_widget.text()] = {
                "label": label_widget.text(),
                "model": model_widget.currentText(),
                "x0": x0_widget.value(),
                "ampli": ampli_widget.value(),
                "fwhm": fwhm_widget.value()
            }
    
    def emit_peaks_changed(self):
        peaks = self.get_peaks()
        # TODO emit signal with peaks to update plot
        print(peaks)

    def clear(self):
        self.table.clear()

    def add_row(self, prefix, label, model_name, x0, ampli, fwhm):
        def create_spin_box(value=None):
            spin_box = QDoubleSpinBox()
            spin_box.setMaximum(float("inf"))
            spin_box.setMinimumWidth(60)
            if value:
                spin_box.setValue(value)
            return spin_box
        
        prefix_button = QPushButton(
            text=prefix,
            icon=QIcon(str(icons / 'close.png')),
            toolTip="Delete peak"
        )
        color = rgb2hex(self.cmap(self.row_count % self.cmap.N))
        prefix_button.setStyleSheet(f"color: {color};")
        prefix_button.clicked.connect(lambda: self.table.remove_widget_row(prefix_button))

        label_edit = QLineEdit(label)

        model_names = list(PEAK_MODELS.keys())
        model_combo = QComboBox()
        model_combo.addItems(model_names)
        model_combo.setCurrentText(model_name)

        x0_min_spin = create_spin_box()
        x0_spin = create_spin_box(x0)
        x0_max_spin = create_spin_box()

        ampli_min_spin = create_spin_box()
        ampli_spin = create_spin_box(ampli)
        ampli_max_spin = create_spin_box()

        fwhm_min_spin = create_spin_box()
        fwhm_spin = create_spin_box(fwhm)
        fwhm_max_spin = create_spin_box()

        row_widgets = {
            "Prefix": prefix_button,
            "Label": label_edit,
            "Model": model_combo,
            "x0_min": x0_min_spin,
            "x0": x0_spin,
            "x0_max": x0_max_spin,
            "Ampli_min": ampli_min_spin,
            "Ampli": ampli_spin,
            "Ampli_max": ampli_max_spin,
            "FWHM_min": fwhm_min_spin,
            "FWHM": fwhm_spin,
            "FWHM_max": fwhm_max_spin
        }

        self.table.add_row(**row_widgets)

    def show_bounds(self, show):
        columns_to_toggle = ["x0_min", "x0_max", "Ampli_min", "Ampli_max", "FWHM_min", "FWHM_max"]
        
        for column in columns_to_toggle:
            column_index = self.table.get_column_index(column)
            self.table.setColumnHidden(column_index, not show)

        header = self.table.horizontalHeader()
        if show:
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
        else:
            header.setSectionResizeMode(QHeaderView.Stretch)