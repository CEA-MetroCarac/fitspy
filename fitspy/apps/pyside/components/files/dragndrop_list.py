from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QPainter, QPalette, QColor


class CustomQListWidgetItem(QListWidgetItem):
    def __init__(self, text, original_text):
        super().__init__(text)
        self.original_text = original_text

    def text(self):
        return self.original_text


class DragNDropList(QListWidget):
    filesDropped = Signal(list)

    def __init__(self, parent=None, selection_mode=QListWidget.ExtendedSelection):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(selection_mode)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionRectVisible(True)
        self.drag_active = False
        self.format_function = None

    def set_format_function(self, format_function):
        self.format_function = format_function

    def get_all_fnames(self):
        return [self.item(i).text() for i in range(self.count())]

    def get_selected_fnames(self):
        return [item.text() for item in self.selectedItems()]

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

    def addItem(self, item):
        if isinstance(item, str):
            display_text = self.format_function(item) if self.format_function else item
            item = CustomQListWidgetItem(display_text, item)
        super().addItem(item)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.save()

            if self.drag_active:
                painter.setPen(self.palette().color(QPalette.Highlight))
                text = "Release to load file(s)"
            else:
                painter.setPen(
                    self.palette().color(QPalette.Disabled, QPalette.Text)
                )
                text = "Drag and Drop File(s) Here"

            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, text)

            painter.restore()

    def colorize_items(self, fnames=None, color=None):
        if fnames is None:
            fnames = self.get_all_fnames()

        for i in range(self.count()):
            item = self.item(i)
            if item.text() in fnames:
                if color is None:
                    item.setBackground(Qt.transparent)
                    item.setForeground(Qt.NoBrush)
                else:
                    bg_color = QColor(color)
                    item.setBackground(bg_color)
                    
                    # Calculate luminance to determine if text should be black or white
                    luminance = (0.299 * bg_color.red() + 
                                0.587 * bg_color.green() + 
                                0.114 * bg_color.blue()) / 255
                    item.setForeground(Qt.black if luminance > 0.5 else Qt.white)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.remove_selected_files(self)  # defined after instantiation
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = DragNDropList()
    obj.show()
    sys.exit(app.exec())
