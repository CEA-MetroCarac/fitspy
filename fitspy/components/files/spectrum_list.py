from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from .dragndrop_list import DragAndDropList

project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'resources' / 'iconpack'

class SpectrumList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.title_label = QLabel("Spectrum:")
        self.count_label = QLabel("")

        self.sel_all = QPushButton(icon=QIcon(str(icons / 'select-all.png')))
        self.sel_all.setIconSize(QSize(20, 20))
        self.rm_btn = QPushButton(icon=QIcon(str(icons / 'remove.png')))
        self.rm_btn.setIconSize(QSize(20, 20))

        self.list = DragAndDropList()

        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.count_label)
        title_layout.addStretch()  # horizontal spacer
        title_layout.addWidget(self.sel_all)
        title_layout.addWidget(self.rm_btn)

        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.list)

        self.setLayout(main_layout)

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    spectrum_list = SpectrumList()
    spectrum_list.show()

    app.exec()