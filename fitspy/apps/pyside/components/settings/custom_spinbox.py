from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox
from PySide6.QtGui import QAction


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, empty_value=None):
        super().__init__(parent)
        self.empty_value = empty_value
        self.setMaximum(float("inf"))
        self.setMinimum(-float("inf"))
        self.lineEdit().textChanged.connect(self.handle_empty_text)

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
        self.lineEdit().textChanged.connect(self.handle_empty_text)

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


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = SpinBox()
    # obj = DoubleSpinBox()
    obj.show()
    sys.exit(app.exec())
