from PySide6.QtWidgets import QWidget, QVBoxLayout, QDoubleSpinBox

class FloatInput(QWidget):
    def __init__(self, min_value=-999.0, max_value=999.0, decimals=2, step=1.0):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.decimals = decimals
        self.step = step  # Add step as an instance variable
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.floatSpinBox = QDoubleSpinBox()
        self.floatSpinBox.setRange(self.min_value, self.max_value)
        self.floatSpinBox.setDecimals(self.decimals)
        self.floatSpinBox.setSingleStep(self.step)  # Set the step size
        layout.addWidget(self.floatSpinBox)
        self.setLayout(layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    default_widget = FloatInput()
    default_widget.show()
    app.exec()