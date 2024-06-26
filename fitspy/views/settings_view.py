from PySide6.QtWidgets import QListWidget, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class FileDropListWidget(QListWidget):
    filesDropped = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.DragDrop)
        self.setSelectionMode(QListWidget.ExtendedSelection)

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
            for file_path in file_paths:
                self.addItem(file_path)
            self.filesDropped.emit(file_paths)  # Emit the signal with the list of dropped file paths
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        # Create and set layout for this widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Select Files button
        self.select_files = QPushButton("Select Files")
        layout.addWidget(self.select_files)
        # self.select_files.clicked.connect(self.load_files)

        # Remove Selected button
        self.remove_selected = QPushButton("Remove Selected")
        layout.addWidget(self.remove_selected)

        # Remove All button
        self.remove_all = QPushButton("Remove All")
        layout.addWidget(self.remove_all)

        self.file_list = FileDropListWidget()
        layout.addWidget(self.file_list)
