from PySide6.QtWidgets import QWidget, QVBoxLayout, QDoubleSpinBox
from PySide6.QtCore import Signal

class FloatInput(QWidget):
    valueChanged = Signal(float)

    def __init__(self,default=0 , min_value=-999.0, max_value=999.0, decimals=2, step=1.0):
        super().__init__()
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.decimals = decimals
        self.step = step
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.floatSpinBox = QDoubleSpinBox()
        self.floatSpinBox.setRange(self.min_value, self.max_value)
        self.floatSpinBox.setDecimals(self.decimals)
        self.floatSpinBox.setSingleStep(self.step)  # Set the step size
        layout.addWidget(self.floatSpinBox)
        self.setLayout(layout)

        self.floatSpinBox.valueChanged.connect(self.valueChanged.emit)
        self.setValue(self.default)

    def setValue(self, value):
        self.floatSpinBox.setValue(value)

    def value(self):
        return self.floatSpinBox.value()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    default_widget = FloatInput()
    default_widget.show()
    app.exec()