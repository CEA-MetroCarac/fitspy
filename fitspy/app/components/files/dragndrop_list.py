from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QAbstractItemView
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QPainter, QPalette, QColor

class DragAndDropList(QListWidget):
    filesDropped = Signal(list)

    def __init__(self, parent=None, selection_mode=QListWidget.ExtendedSelection):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(selection_mode)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
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

    def colorize_items(self, fnames=None, color=None):
        if fnames is None:
            fnames = [self.item(i).text() for i in range(self.count())]

        for i in range(self.count()):
            item = self.item(i)
            if item.text() in fnames:
                if color is None:
                    item.setBackground(self.palette().base())
                else:
                    item.setBackground(QColor(color))