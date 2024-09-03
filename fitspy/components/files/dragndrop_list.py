from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QPainter, QPalette

class DragAndDropList(QListWidget):
    filesDropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSelectionRectVisible(True)
        self.drag_active = False

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drag_active = True
            self.viewport().update()
        else:
            super().dragMoveEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.drag_active = False
        self.viewport().update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
            self.filesDropped.emit(file_paths)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
        self.drag_active = False
        self.viewport().update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.save()

            if self.drag_active:
                painter.setPen(self.palette().color(QPalette.Highlight))
                text = "Release to load file(s)"
            else:
                painter.setPen(self.palette().color(QPalette.Disabled, QPalette.Text))
                text = "Drag and Drop File(s) Here"

            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, text)

            painter.restore()