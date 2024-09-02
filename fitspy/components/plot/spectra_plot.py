from PySide6.QtWidgets import QFrame, QHBoxLayout

class SpectraPlot(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        layout = QHBoxLayout(self)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    spectra_plot = SpectraPlot()
    spectra_plot.show()
    sys.exit(app.exec())