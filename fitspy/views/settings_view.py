from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QPalette, QPen, QBrush
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

        # Create and set layout for this widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Select Files button
        self.select_files = QPushButton("Select Files")
        layout.addWidget(self.select_files)

        # Remove Selected button
        self.remove_selected = QPushButton("Remove Selected")
        layout.addWidget(self.remove_selected)

        # Remove All button
        self.remove_all = QPushButton("Remove All")
        layout.addWidget(self.remove_all)

        self.file_list = FileDropListWidget()
        layout.addWidget(self.file_list)
