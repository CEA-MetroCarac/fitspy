from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout

class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Fitspy")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        wip_label = QLabel("Work in Progress")
        font = wip_label.font()
        font.setPointSize(16)
        font.setBold(True)
        wip_label.setFont(font)

        text_label = QLabel("Fitspy is a Python application for processing and analyzing spectral data.")
        text_label.setWordWrap(True)

        layout.addWidget(wip_label)
        layout.addWidget(text_label)

        self.setLayout(layout)