from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QDockWidget, QWidget, QVBoxLayout, QLabel

class Map2DPlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(300, 300)

        self.dock_widget = QDockWidget("Measurement sites", self)
        self.dock_widget.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)

        self.dock_container = QWidget()
        self.dock_layout = QVBoxLayout(self.dock_container)

        self.placeholder_label = QLabel("2D Map Plot will be here")
        self.dock_layout.addWidget(self.placeholder_label)

        self.dock_widget.setWidget(self.dock_container)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    def onDockWidgetTopLevelChanged(self, floating):
        if floating:
            self.dock_widget.resize(600, 600)
        else:
            self.dock_widget.resize(300, 300)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = QMainWindow()
    main.setCentralWidget(QLabel("Central Widget"))
    map2d_plot = Map2DPlot(main)
    main.setCentralWidget(map2d_plot)
    main.show()
    sys.exit(app.exec())