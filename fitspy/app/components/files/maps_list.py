from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from fitspy.core import get_icon_path
from .dragndrop_list import DragNDropList


class MapsList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.title_label = QLabel("Maps:")
        self.count_label = QLabel("")

        self.deselect_btn = QPushButton(
            icon=QIcon(get_icon_path("deselect.png")),
            toolTip="Deselect all. Go back to default spectrum list.",
        )
        self.deselect_btn.setIconSize(QSize(20, 20))
        self.rm_btn = QPushButton(icon=QIcon(get_icon_path("remove.png")))
        self.rm_btn.setIconSize(QSize(20, 20))

        self.list = DragNDropList(selection_mode=QListWidget.SingleSelection)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        title_layout = QHBoxLayout()

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.count_label)
        title_layout.addStretch()  # horizontal spacer
        title_layout.addWidget(self.deselect_btn)
        title_layout.addWidget(self.rm_btn)

        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.list)

        self.setLayout(main_layout)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    maps_list = MapsList()
    maps_list.show()

    app.exec()
