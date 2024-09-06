from pathlib import Path
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QMainWindow, QCheckBox, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter,
    QTabWidget, QVBoxLayout, QWidget)

from .components import MenuBar
from .components.plot import SpectraPlot, Map2DPlot, Toolbar, ViewOptions
from .components.settings import StatusBar, ModelBuilder, FitSettings
from .components.files import MapsList, SpectrumList

project_root = Path(__file__).resolve().parent.parent
icons = project_root / 'resources' / 'iconpack'

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Fitspy")
        self.resize(1500, 900)

        self.centralwidget = QWidget(self, enabled=True, baseSize=QSize(0, 0))
        self.verticalLayout_15 = QVBoxLayout(self.centralwidget, spacing=0)
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)

        self.menuBar = MenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.menuBar)

        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)

        self.central = QWidget()
        self.gridLayout_5 = QGridLayout(self.central)
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.splitter = QSplitter(self.central)
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(10)
        self.upper_frame = QFrame(self.splitter)
        self.horizontalLayout_27 = QHBoxLayout(self.upper_frame)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.Upper_zone = QHBoxLayout()
        self.Upper_zone.setSpacing(0)
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setContentsMargins(0, -1, 10, -1)

        self.spectra_plot = SpectraPlot()
        self.verticalLayout_26.addWidget(self.spectra_plot)

        self.toolbar = Toolbar()
        self.verticalLayout_26.addWidget(self.toolbar)

        self.verticalLayout_26.setStretch(0, 100)

        self.Upper_zone.addLayout(self.verticalLayout_26)

        self.widget_7 = QWidget(self.upper_frame)
        self.widget_7.setMinimumSize(QSize(300, 0))
        self.widget_7.setMaximumSize(QSize(320, 16777215))
        self.verticalLayout_13 = QVBoxLayout(self.widget_7)
        self.verticalLayout_13.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_69 = QHBoxLayout()

        self.measurement_sites = Map2DPlot()  # This is a second QMainWIndow as a dock widget
        self.horizontalLayout_69.addWidget(self.measurement_sites)

        self.verticalLayout_13.addLayout(self.horizontalLayout_69)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_50.addItem(self.horizontalSpacer_18)

        self.verticalLayout_13.addLayout(self.horizontalLayout_50)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)


        self.view_options = ViewOptions()

        self.verticalLayout_13.addWidget(self.view_options)

        self.Upper_zone.addWidget(self.widget_7)

        self.horizontalLayout_27.addLayout(self.Upper_zone)

        self.splitter.addWidget(self.upper_frame)
        self.bottom_widget_2 = QWidget(self.splitter)
        self.verticalLayout_25 = QVBoxLayout(self.bottom_widget_2)
        self.verticalLayout_25.setContentsMargins(3, 3, 3, 0)
        self.tabWidget_2 = QTabWidget(self.bottom_widget_2)
        self.tabWidget_2.setEnabled(True)

        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 428, 356))

        self.fit_model_editor = ModelBuilder()
        self.tabWidget_2.addTab(self.fit_model_editor, "Fit Model Builder")

        self.fit_settings = FitSettings()
        self.tabWidget_2.addTab(self.fit_settings, "More Settings")

        self.verticalLayout_25.addWidget(self.tabWidget_2)

        self.splitter.addWidget(self.bottom_widget_2)

        self.gridLayout_5.addWidget(self.splitter, 1, 2, 1, 1)

        self.maps_list = MapsList()
        self.spectrum_list = SpectrumList()

        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.addWidget(self.maps_list)
        self.sidebar_layout.addWidget(self.spectrum_list)
        self.sidebar.setMaximumWidth(250)

        self.main_content = QWidget()

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.splitter)
        self.main_splitter.addWidget(self.sidebar)  

        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 0)
        self.main_splitter.setSizes([self.width() - self.sidebar.width(), self.sidebar.width()])

        self.gridLayout_5.addWidget(self.main_splitter, 1, 3, 1, 1)


        self.tab_plot_settings = QWidget()

        self.horizontalLayout_71 = QHBoxLayout()

        self.horizontalLayout_89 = QHBoxLayout()


        self.tab_more_options = QWidget()
        self.verticalLayout_4 = QVBoxLayout(self.tab_more_options)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_8 = QScrollArea(self.tab_more_options)
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, 0, 249, 267))
        self.cb_legend_visible = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_legend_visible.setChecked(True)

        self.cb_show_err_bar_plot = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_show_err_bar_plot.setChecked(True)

        self.cb_wafer_stats = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_wafer_stats.setChecked(True)

        self.cb_join_for_point_plot = QCheckBox(self.scrollAreaWidgetContents_8)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.line_3 = QFrame(self.scrollAreaWidgetContents_8)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.legends_loc = QHBoxLayout()
        self.label_17 = QLabel(self.scrollAreaWidgetContents_8)

        self.legends_loc.addWidget(self.label_17)

        self.cbb_legend_loc = QComboBox(self.scrollAreaWidgetContents_8)

        self.legends_loc.addWidget(self.cbb_legend_loc)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.legends_loc.addItem(self.horizontalSpacer_35)

        self.main_layout = QHBoxLayout()

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalSpacer_48 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_48)

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)

        self.verticalLayout_4.addWidget(self.scrollArea_8)

        self.tab_multi_axes = QWidget()

        self.verticalLayout_15.addWidget(self.central)

        self.setCentralWidget(self.centralwidget)

        self.statusBar = StatusBar()
        self.setStatusBar(self.statusBar)