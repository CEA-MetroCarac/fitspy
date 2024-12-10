from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from fitspy.core import get_icon_path
from .dragndrop_list import DragAndDropList


class SpectrumList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.title_label = QLabel("Spectrum:")
        self.count_label = QLabel("")

        self.sel_all = QPushButton(icon=QIcon(get_icon_path("select-all.png")))
        self.sel_all.setIconSize(QSize(20, 20))
        self.rm_btn = QPushButton(icon=QIcon(get_icon_path("remove.png")))
        self.rm_btn.setIconSize(QSize(20, 20))
        self.save_btn = QPushButton(
            icon=QIcon(get_icon_path("save.png")),
            toolTip="Save results of selected spectra",
        )
        self.save_btn.setIconSize(QSize(20, 20))

        self.list = DragAndDropList()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        title_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        combined_layout = QVBoxLayout()

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.count_label)
        title_layout.addStretch()  # horizontal spacer

        button_layout.addWidget(self.sel_all)
        button_layout.addWidget(self.rm_btn)
        button_layout.addWidget(self.save_btn)

        combined_layout.addLayout(title_layout)
        combined_layout.addLayout(button_layout)

        main_layout.addLayout(combined_layout)
        main_layout.addWidget(self.list)

        self.setLayout(main_layout)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    spectrum_list = SpectrumList()
    spectrum_list.show()

    app.exec()
