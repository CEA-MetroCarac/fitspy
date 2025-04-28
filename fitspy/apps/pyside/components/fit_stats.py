from PySide6.QtWidgets import QVBoxLayout, QTextBrowser, QWidget
from PySide6.QtCore import Qt

class FitStats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fit Statistics")
        self.setGeometry(100, 100, 400, 400)
        self.setWindowFlag(Qt.Window)
        self.layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.layout.addWidget(self.text_browser)
        self.setLayout(self.layout)

    def set_text(self, text):
        self.text_browser.setText(text)