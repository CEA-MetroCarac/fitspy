from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QRadioButton, QSpinBox, QSpacerItem, QSizePolicy

class Toolbar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        placeholder_label = QLabel("Placeholder matplotlib toolbar")
        baseline_radio = QRadioButton("Baseline")
        peaks_radio = QRadioButton("Fitting")
        r2_label = QLabel("R2=0")
        dpi_label = QLabel("DPI:")
        dpi_input = QSpinBox()
        dpi_input.setRange(1, 300)
        dpi_input.setValue(100)

        spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        hbox.addWidget(placeholder_label)
        hbox.addItem(spacer1)
        hbox.addWidget(baseline_radio)
        hbox.addWidget(peaks_radio)
        hbox.addItem(spacer2)
        hbox.addWidget(r2_label)
        hbox.addWidget(dpi_label)
        hbox.addWidget(dpi_input)

        self.setLayout(hbox)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    toolbar = Toolbar()
    toolbar.show()

    sys.exit(app.exec())