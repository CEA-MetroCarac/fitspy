from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QCheckBox
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QPalette
from .settings import OverallSettings, BaselineSettings, NormalizationSettings, FittingSettings, ModelsSettings

class FileDropListWidget(QListWidget):
    filesDropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DropOnly)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSelectionRectVisible(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.filesDropped.emit(file_paths)  # Emit the signal with the list of dropped file paths
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:  # Check if the list is empty
            # Initialize a QPainter instance for drawing
            painter = QPainter(self.viewport())
            painter.save()

            # Set the pen color and font if needed
            painter.setPen(self.palette().color(QPalette.Disabled, QPalette.Text))

            # Draw the hint text in the center of the widget
            rect = self.rect()
            text = "Drag and Drop File(s) Here"
            painter.drawText(rect, Qt.AlignCenter, text)

            painter.restore()

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        buttons_layout = QHBoxLayout()

        self.open_file = QPushButton("Open Files")
        buttons_layout.addWidget(self.open_file)

        self.open_dir = QPushButton("Open Dir.")
        buttons_layout.addWidget(self.open_dir)

        self.remove_selected = QPushButton("Remove")
        buttons_layout.addWidget(self.remove_selected)

        self.remove_all = QPushButton("Remove All")
        buttons_layout.addWidget(self.remove_all)

        self.file_list = FileDropListWidget()

        self.show_all = QPushButton("Show All")
        self.auto_eval = QPushButton("Auto Eval")
        self.auto_eval_all = QPushButton("Auto Eval All")
        self.save_settings = QPushButton("Save Settings")
        self.reset = QPushButton("Reset")
        self.reset_all = QPushButton("Reset All")

        # First row of buttons
        first_row_layout = QHBoxLayout()
        first_row_layout.addWidget(self.show_all)
        first_row_layout.addWidget(self.auto_eval)
        first_row_layout.addWidget(self.auto_eval_all)

        # Second row of buttons
        second_row_layout = QHBoxLayout()
        second_row_layout.addWidget(self.save_settings)
        second_row_layout.addWidget(self.reset)
        second_row_layout.addWidget(self.reset_all)

        # Settings widgets
        self.overall_settings = OverallSettings()
        self.baseline_settings = BaselineSettings()
        self.normalization_settings = NormalizationSettings()
        self.fitting_settings = FittingSettings()
        self.models_settings = ModelsSettings()

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.file_list)
        layout.addLayout(first_row_layout)
        layout.addLayout(second_row_layout)
        layout.addWidget(self.overall_settings)
        layout.addWidget(self.baseline_settings)
        layout.addWidget(self.normalization_settings)
        layout.addWidget(self.fitting_settings)
        layout.addWidget(self.models_settings)
