from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout

project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class SpectrumList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.label = QLabel("Spectra:")

        self.button1 = QPushButton(icon=QIcon(str(icons / 'remove.png')))
        self.button2 = QPushButton(icon=QIcon(str(icons / 'save.png')))

        self.list_widget = QListWidget()

        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        title_layout.addWidget(self.label)
        title_layout.addStretch()  # Add horizontal spacer
        title_layout.addWidget(self.button1)
        title_layout.addWidget(self.button2)

        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    spectrum_list = SpectrumList()
    spectrum_list.show()

    app.exec()