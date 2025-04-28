from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QMainWindow, QFrame, QGridLayout, QHBoxLayout, QSplitter, QTabWidget,
                               QVBoxLayout, QWidget, QMessageBox)

from fitspy.apps.pyside.components import MenuBar, About
from fitspy.apps.pyside.components.plot import SpectraPlot, Map2DPlot, Toolbar
from fitspy.apps.pyside.components.settings import StatusBox, ModelBuilder, MoreSettings
from fitspy.apps.pyside.components.files import MapsList, SpectrumList

project_root = Path(__file__).resolve().parent.parent
icons = project_root / "resources" / "iconpack"


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Fitspy")
        self.resize(1500, 900)

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(5, 5, 0, 0)

        self.menuBar = MenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.menuBar)

        self.central = QWidget()
        self.gridLayout = QGridLayout(self.central)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.init_splitter()
        self.init_sidebar()

        self.gridLayout.addWidget(self.main_splitter)

        self.verticalLayout.addWidget(self.central)
        self.setCentralWidget(self.centralwidget)

    def init_splitter(self):
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setStyleSheet(
            """
        QSplitter::handle:hover {
            background: #999999;
        }
    """
        )

        self.init_upper_frame()
        self.init_bottom_widget()

        self.splitter.addWidget(self.upper_frame)
        self.splitter.addWidget(self.bottom_widget)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setStyleSheet(
            """
        QSplitter::handle:hover {
            background: #999999;
        }
    """
        )
        self.main_splitter.addWidget(self.splitter)

    def init_upper_frame(self):
        self.upper_frame = QFrame()
        self.horizontalLayout_27 = QHBoxLayout(self.upper_frame)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)

        self.Upper_zone = QHBoxLayout()
        self.Upper_zone.setSpacing(0)

        self.init_spectra_plot()
        self.init_2dmap()

        self.horizontalLayout_27.addLayout(self.Upper_zone)

    def init_bottom_widget(self):
        self.bottom_widget = QWidget()
        self.verticalLayout_25 = QVBoxLayout(self.bottom_widget)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)

        self.tabWidget_2 = QTabWidget()
        self.tabWidget_2.setEnabled(True)

        self.fit_model_editor = ModelBuilder()
        self.fit_stats = self.fit_model_editor.fit_stats
        self.tabWidget_2.addTab(self.fit_model_editor, "Model")

        self.more_settings = MoreSettings()
        self.tabWidget_2.addTab(self.more_settings, "More settings")

        self.verticalLayout_25.addWidget(self.tabWidget_2)

    def init_spectra_plot(self):
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setContentsMargins(0, -1, 10, -1)

        self.spectra_plot = SpectraPlot()
        self.verticalLayout_26.addWidget(self.spectra_plot)

        self.toolbar = Toolbar(self.spectra_plot.canvas)
        self.verticalLayout_26.addWidget(self.toolbar)

        self.verticalLayout_26.setStretch(0, 100)
        self.Upper_zone.addLayout(self.verticalLayout_26)

    def init_2dmap(self):
        self.widget_7 = QWidget()
        self.widget_7.setMinimumSize(QSize(300, 0))
        self.widget_7.setMaximumSize(QSize(320, 16777215))

        self.verticalLayout_13 = QVBoxLayout(self.widget_7)
        self.verticalLayout_13.setContentsMargins(2, 0, 2, 0)

        self.measurement_sites = Map2DPlot()
        self.verticalLayout_13.addWidget(self.measurement_sites)

        self.Upper_zone.addWidget(self.widget_7)

    def init_sidebar(self):
        self.maps_list = MapsList()
        self.spectrum_list = SpectrumList()
        self.statusBox = StatusBox()

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.addWidget(self.maps_list, 4)
        self.sidebar_layout.addWidget(self.spectrum_list, 6)
        self.sidebar_layout.addWidget(self.statusBox, 0)

        self.main_splitter.addWidget(self.sidebar)

        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 0)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit Confirmation', 'Are you sure you want to exit ?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def about(self):
        dialog = About(self)
        dialog.exec_()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = MainView()
    # obj = MenuBar()
    # obj = MapsList()
    # obj = SpectrumList()
    # obj = StatusBox()
    obj.show()
    sys.exit(app.exec())
