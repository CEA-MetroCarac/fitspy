from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def handle_empty_text(self, text):
        if not text:
            self.clear()

    def value(self):
        if self.text() == '':
            return None
        return super().value()
    
    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)

class SpinBox(QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def handle_empty_text(self, text):
        if not text:
            self.clear()

    def value(self):
        if self.text() == '':
            return None
        return super().value()
    
    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)