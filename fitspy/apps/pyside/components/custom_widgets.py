from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox, QComboBox
from PySide6.QtGui import QAction, QDragEnterEvent, QDragLeaveEvent, QDropEvent, QPainter, QPalette


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, empty_value=None):
        super().__init__(parent)
        self.empty_value = empty_value
        self.setMaximum(float("inf"))
        self.setMinimum(-float("inf"))
        self.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def wheelEvent(self, event):
        event.ignore()

    def handle_empty_text(self):
        if not self.text():
            if self.empty_value is None:
                self.clear()
            else:
                self.setValue(self.empty_value)

    def value(self):
        if self.text() == "":
            return None
        return super().value()

    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)

    def stepBy(self, steps):
        base = self.value() or 0
        new_value = base + steps * self.singleStep()
        self.setValue(new_value)

    def contextMenuEvent(self, event):
        menu = self.lineEdit().createStandardContextMenu()

        set_to_inf_action = QAction("Set to Max", self)
        set_to_inf_action.triggered.connect(self.set_to_max)
        menu.addAction(set_to_inf_action)

        set_to_default_action = QAction("Set to Default", self)
        set_to_default_action.triggered.connect(self.set_to_default)
        menu.addAction(set_to_default_action)

        menu.exec(event.globalPos())

    def set_to_max(self):
        self.setValue(float("inf"))

    def set_to_default(self):
        self.setValue(self.empty_value)

class SpinBox(QSpinBox):
    def __init__(self, parent=None, empty_value=None):
        super().__init__(parent)
        self.empty_value = empty_value
        self.setMaximum(999999999)
        self.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def wheelEvent(self, event):
        event.ignore()

    def handle_empty_text(self):
        if not self.text():
            if self.empty_value is None:
                self.clear()
            else:
                self.setValue(self.empty_value)

    def value(self):
        if self.text() == "":
            return None
        return super().value()

    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)
    
    def stepBy(self, steps):
        base = self.value() or 0
        new_value = base + steps * self.singleStep()
        self.setValue(new_value)

    def contextMenuEvent(self, event):
        menu = self.lineEdit().createStandardContextMenu()

        set_to_default_action = QAction("Set to Default", self)
        set_to_default_action.triggered.connect(self.set_to_default)
        menu.addAction(set_to_default_action)

        menu.exec(event.globalPos())

    def set_to_default(self):
        self.setValue(self.empty_value)


class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
    
    def wheelEvent(self, event):
        event.ignore()

class DragNDropCombo(ComboBox):
    itemAdded = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
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
            self.update()
        else:
            super().dragMoveEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.drag_active = False
        self.update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            fname = url.toLocalFile()
            if fname not in [self.itemText(i) for i in range(self.count())]:
                self.itemAdded.emit(fname)
        event.acceptProposedAction()
        self.drag_active = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self)
            painter.save()

            if self.drag_active:
                painter.setPen(self.palette().color(QPalette.Highlight))
                text = "Release to load file(s)"
            else:
                painter.setPen(self.palette().color(QPalette.Disabled, QPalette.Text))
                text = "Fitting Models: Drag and Drop File(s) Here"

            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, text)

            painter.restore()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = SpinBox()
    # obj = DoubleSpinBox()
    obj.show()
    sys.exit(app.exec())
