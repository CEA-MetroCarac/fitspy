from pathlib import Path
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import (QMainWindow, QAbstractItemView, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit, QListWidget,
    QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)

from fitspy.components.plot import Toolbar, ViewOptions
from fitspy.components.settings import StatusBar, ModelBuilder, FitSettings
from fitspy.components.files import MapsList, SpectrumList

project_root = Path(__file__).resolve().parent.parent
icons = project_root / 'resources' / 'iconpack'

class MenuBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.actionManual = QAction(
            self,
            icon=QIcon(str(icons / "manual.png")),
            toolTip="Manual",
        )
        self.actionDarkMode = QAction(
            self,
            icon=QIcon(str(icons / "dark.png")),
            toolTip="Dark Mode",
        )
        self.actionLightMode = QAction(
            self,
            icon=QIcon(str(icons / "light-mode.svg")),
            toolTip="Light Mode",
        )
        self.actionAbout = QAction(
            self,
            icon=QIcon(str(icons / "about.png")),
            toolTip="About",
        )
        self.actionOpen = QAction(
            self,
            icon=QIcon(str(icons / "icons8-folder-96.png")),
            toolTip="Open spectra data, saved work or Excel file",
        )
        self.actionSave = QAction(
            self,
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save current work",
        )
        self.actionClear_env = QAction(
            self,
            icon=QIcon(str(icons / "clear.png")),
            toolTip="Clear the environment",
        )

        self.setObjectName("menuBar")
        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(16777215, 50))
        self.setMovable(True)
        self.setIconSize(QSize(30, 30))
        self.setFloatable(False)

        actions = [
            self.actionOpen, self.actionSave, self.actionClear_env,
            None,  # Separator
            QWidget(self),  # Spacer
            self.actionDarkMode, self.actionLightMode,
            None,  # Separator
            self.actionManual, self.actionAbout,
        ]

        for action in actions:
            if action is None:
                self.addSeparator()
            elif isinstance(action, QWidget):
                action.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.addWidget(action)
            else:
                self.addAction(action)

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        if not self.objectName():
            self.setObjectName("MainWindow")
        self.resize(1553, 1019)

        self.centralwidget = QWidget(self, enabled=True, baseSize=QSize(0, 0))
        self.verticalLayout_15 = QVBoxLayout(self.centralwidget, spacing=0)
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)

        self.menuBar = MenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.menuBar)

        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)

        self.central = QWidget()
        self.central.setObjectName("central")
        self.gridLayout_5 = QGridLayout(self.central)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.splitter = QSplitter(self.central)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(10)
        self.upper_frame = QFrame(self.splitter)
        self.upper_frame.setObjectName("upper_frame")
        self.horizontalLayout_27 = QHBoxLayout(self.upper_frame)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(3, 0, 3, 3)
        self.Upper_zone = QHBoxLayout()
        self.Upper_zone.setSpacing(0)
        self.Upper_zone.setObjectName("Upper_zone")
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, -1, 10, -1)
        self.spectre_view_frame_ = QFrame(self.upper_frame)
        self.spectre_view_frame_.setObjectName("spectre_view_frame_")
        self.spectre_view_frame_.setFrameShape(QFrame.Shape.StyledPanel)
        self.spectre_view_frame_.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.spectre_view_frame_)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.QVBoxlayout = QVBoxLayout()
        self.QVBoxlayout.setSpacing(6)
        self.QVBoxlayout.setObjectName("QVBoxlayout")

        self.verticalLayout_16.addLayout(self.QVBoxlayout)

        self.verticalLayout_26.addWidget(self.spectre_view_frame_)

        self.toolbar = Toolbar()

        self.verticalLayout_26.addWidget(self.toolbar)

        self.verticalLayout_26.setStretch(0, 75)
        self.verticalLayout_26.setStretch(1, 25)

        self.Upper_zone.addLayout(self.verticalLayout_26)

        self.widget_7 = QWidget(self.upper_frame)
        self.widget_7.setObjectName("widget_7")
        self.widget_7.setMinimumSize(QSize(300, 0))
        self.widget_7.setMaximumSize(QSize(320, 16777215))
        self.verticalLayout_13 = QVBoxLayout(self.widget_7)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(2, 0, 2, 0)
        self.horizontalLayout_69 = QHBoxLayout()
        self.horizontalLayout_69.setObjectName("horizontalLayout_69")
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_69.addItem(self.horizontalSpacer_21)

        self.measurement_sites = QFrame(self.widget_7)
        self.measurement_sites.setObjectName("measurement_sites")
        self.measurement_sites.setMinimumSize(QSize(320, 330))
        self.measurement_sites.setMaximumSize(QSize(320, 330))
        self.measurement_sites.setFrameShape(QFrame.Shape.StyledPanel)
        self.measurement_sites.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.measurement_sites)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)

        self.horizontalLayout_69.addWidget(self.measurement_sites)

        self.verticalLayout_13.addLayout(self.horizontalLayout_69)

        self.horizontalLayout_50 = QHBoxLayout()
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_50.addItem(self.horizontalSpacer_18)

        self.verticalLayout_13.addLayout(self.horizontalLayout_50)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_13.addItem(self.verticalSpacer_5)

        self.view_options = ViewOptions()

        self.verticalLayout_13.addWidget(self.view_options)

        self.Upper_zone.addWidget(self.widget_7)

        self.Upper_zone.setStretch(0, 75)

        self.horizontalLayout_27.addLayout(self.Upper_zone)

        self.splitter.addWidget(self.upper_frame)
        self.bottom_widget_2 = QWidget(self.splitter)
        self.bottom_widget_2.setObjectName("bottom_widget_2")
        self.verticalLayout_25 = QVBoxLayout(self.bottom_widget_2)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(3, 3, 3, 0)
        self.tabWidget_2 = QTabWidget(self.bottom_widget_2)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setEnabled(True)

        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 428, 356))
        self.verticalLayout_38 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_38.setSpacing(10)
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.btn_cosmis_ray = QPushButton(self.scrollAreaWidgetContents_3)
        self.btn_cosmis_ray.setObjectName("btn_cosmis_ray")
        self.btn_cosmis_ray.setMinimumSize(QSize(80, 0))
        self.btn_cosmis_ray.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_18.addWidget(self.btn_cosmis_ray)

        self.horizontalSpacer_56 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_56)

        self.label_99 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_99.setObjectName("label_99")

        self.horizontalLayout_18.addWidget(self.label_99)

        self.cbb_xaxis_unit2 = QComboBox(self.scrollAreaWidgetContents_3)
        self.cbb_xaxis_unit2.setObjectName("cbb_xaxis_unit2")

        self.horizontalLayout_18.addWidget(self.cbb_xaxis_unit2)

        self.verticalLayout_38.addLayout(self.horizontalLayout_18)

        font = QFont()
        font.setBold(True)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_36 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_36.setSpacing(5)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(2, 2, 2, 2)
        self.label_54 = QLabel(self.groupBox_4)
        self.label_54.setObjectName("label_54")
        self.label_54.setFont(font)

        self.verticalLayout_36.addWidget(self.label_54)

        self.horizontalLayout_58 = QHBoxLayout()
        self.horizontalLayout_58.setSpacing(5)
        self.horizontalLayout_58.setObjectName("horizontalLayout_58")
        self.horizontalLayout_58.setContentsMargins(2, 2, 2, 2)
        self.label_61 = QLabel(self.groupBox_4)
        self.label_61.setObjectName("label_61")

        self.horizontalLayout_58.addWidget(self.label_61)

        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_58.addItem(self.horizontalSpacer_30)

        self.range_min = QLineEdit(self.groupBox_4)
        self.range_min.setObjectName("range_min")

        self.horizontalLayout_58.addWidget(self.range_min)

        self.label_62 = QLabel(self.groupBox_4)
        self.label_62.setObjectName("label_62")

        self.horizontalLayout_58.addWidget(self.label_62)

        self.range_max = QLineEdit(self.groupBox_4)
        self.range_max.setObjectName("range_max")

        self.horizontalLayout_58.addWidget(self.range_max)

        self.range_apply = QPushButton(self.groupBox_4)
        self.range_apply.setObjectName("range_apply")

        self.horizontalLayout_58.addWidget(self.range_apply)

        self.verticalLayout_36.addLayout(self.horizontalLayout_58)

        self.verticalLayout_38.addWidget(self.groupBox_4)

        self.label_59 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_59.setObjectName("label_59")

        self.verticalLayout_38.addWidget(self.label_59)

        self.baseline = QGroupBox(self.scrollAreaWidgetContents_3)
        self.baseline.setObjectName("baseline")
        self.verticalLayout_6 = QVBoxLayout(self.baseline)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.label_52 = QLabel(self.baseline)
        self.label_52.setObjectName("label_52")
        self.label_52.setFont(font)

        self.verticalLayout_6.addWidget(self.label_52)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setSpacing(5)
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(2, 2, 2, 2)
        self.rbtn_linear = QRadioButton(self.baseline)
        self.rbtn_linear.setObjectName("rbtn_linear")
        self.rbtn_linear.setChecked(True)

        self.horizontalLayout_37.addWidget(self.rbtn_linear)

        self.rbtn_polynomial = QRadioButton(self.baseline)
        self.rbtn_polynomial.setObjectName("rbtn_polynomial")

        self.horizontalLayout_37.addWidget(self.rbtn_polynomial)

        self.degre = QSpinBox(self.baseline)
        self.degre.setObjectName("degre")
        self.degre.setMinimum(1)

        self.horizontalLayout_37.addWidget(self.degre)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_37.addItem(self.horizontalSpacer_32)

        self.label_37 = QLabel(self.baseline)
        self.label_37.setObjectName("label_37")

        self.horizontalLayout_37.addWidget(self.label_37)

        self.noise = QDoubleSpinBox(self.baseline)
        self.noise.setObjectName("noise")
        self.noise.setDecimals(0)
        self.noise.setValue(5.000000000000000)

        self.horizontalLayout_37.addWidget(self.noise)

        self.horizontalLayout_37.setStretch(0, 25)
        self.horizontalLayout_37.setStretch(1, 25)

        self.verticalLayout_6.addLayout(self.horizontalLayout_37)

        self.horizontalLayout_57 = QHBoxLayout()
        self.horizontalLayout_57.setSpacing(5)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.horizontalLayout_57.setContentsMargins(2, 2, 2, 2)
        self.cb_attached = QCheckBox(self.baseline)
        self.cb_attached.setObjectName("cb_attached")
        self.cb_attached.setChecked(True)

        self.horizontalLayout_57.addWidget(self.cb_attached)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_57.addItem(self.horizontalSpacer_22)

        self.btn_undo_baseline = QPushButton(self.baseline)
        self.btn_undo_baseline.setObjectName("btn_undo_baseline")

        self.horizontalLayout_57.addWidget(self.btn_undo_baseline)

        self.sub_baseline = QPushButton(self.baseline)
        self.sub_baseline.setObjectName("sub_baseline")

        self.horizontalLayout_57.addWidget(self.sub_baseline)

        self.verticalLayout_6.addLayout(self.horizontalLayout_57)

        self.verticalLayout_38.addWidget(self.baseline)

        self.label_60 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_60.setObjectName("label_60")

        self.verticalLayout_38.addWidget(self.label_60)

        self.peaks = QGroupBox(self.scrollAreaWidgetContents_3)
        self.peaks.setObjectName("peaks")
        self.verticalLayout_34 = QVBoxLayout(self.peaks)
        self.verticalLayout_34.setSpacing(5)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(2, 2, 2, 2)
        self.label_57 = QLabel(self.peaks)
        self.label_57.setObjectName("label_57")
        self.label_57.setFont(font)

        self.verticalLayout_34.addWidget(self.label_57)

        self.horizontalLayout_56 = QHBoxLayout()
        self.horizontalLayout_56.setSpacing(5)
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")
        self.horizontalLayout_56.setContentsMargins(2, 2, 2, 2)
        self.label_41 = QLabel(self.peaks)
        self.label_41.setObjectName("label_41")

        self.horizontalLayout_56.addWidget(self.label_41)

        self.horizontalSpacer_31 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_56.addItem(self.horizontalSpacer_31)

        self.cbb_fit_models = QComboBox(self.peaks)
        self.cbb_fit_models.setObjectName("cbb_fit_models")

        self.horizontalLayout_56.addWidget(self.cbb_fit_models)

        self.clear_peaks = QPushButton(self.peaks)
        self.clear_peaks.setObjectName("clear_peaks")

        self.horizontalLayout_56.addWidget(self.clear_peaks)

        self.horizontalLayout_56.setStretch(2, 65)

        self.verticalLayout_34.addLayout(self.horizontalLayout_56)

        self.verticalLayout_38.addWidget(self.peaks)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_38.addItem(self.verticalSpacer)

        self.fit_model_editor = ModelBuilder()

        self.tabWidget_2.addTab(self.fit_model_editor, "")
        self.collect_fit_data = QWidget()
        self.collect_fit_data.setObjectName("collect_fit_data")
        self.verticalLayout_32 = QVBoxLayout(self.collect_fit_data)
        self.verticalLayout_32.setSpacing(6)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_62 = QHBoxLayout()
        self.horizontalLayout_62.setSpacing(5)
        self.horizontalLayout_62.setObjectName("horizontalLayout_62")
        self.horizontalLayout_62.setContentsMargins(5, 5, 5, 5)
        self.scrollArea_9 = QScrollArea(self.collect_fit_data)
        self.scrollArea_9.setObjectName("scrollArea_9")
        self.scrollArea_9.setMinimumSize(QSize(430, 100))
        self.scrollArea_9.setMaximumSize(QSize(430, 16777215))
        self.scrollArea_9.setWidgetResizable(True)
        self.scrollAreaWidgetContents_9 = QWidget()
        self.scrollAreaWidgetContents_9.setObjectName("scrollAreaWidgetContents_9")
        self.scrollAreaWidgetContents_9.setGeometry(QRect(0, 0, 322, 354))
        self.verticalLayout_80 = QVBoxLayout(self.scrollAreaWidgetContents_9)
        self.verticalLayout_80.setSpacing(10)
        self.verticalLayout_80.setObjectName("verticalLayout_80")
        self.verticalLayout_80.setContentsMargins(10, 10, 10, 10)
        self.btn_collect_results = QPushButton(self.scrollAreaWidgetContents_9)
        self.btn_collect_results.setObjectName("btn_collect_results")
        self.btn_collect_results.setMinimumSize(QSize(140, 40))
        self.btn_collect_results.setMaximumSize(QSize(140, 40))
        self.btn_collect_results.setFont(font)
        self.btn_collect_results.setIconSize(QSize(16, 22))

        self.verticalLayout_80.addWidget(self.btn_collect_results)

        self.label_56 = QLabel(self.scrollAreaWidgetContents_9)
        self.label_56.setObjectName("label_56")

        self.verticalLayout_80.addWidget(self.label_56)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.btn_split_fname_2 = QPushButton(self.scrollAreaWidgetContents_9)
        self.btn_split_fname_2.setObjectName("btn_split_fname_2")
        self.btn_split_fname_2.setMinimumSize(QSize(40, 0))
        self.btn_split_fname_2.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_49.addWidget(self.btn_split_fname_2)

        self.cbb_split_fname_2 = QComboBox(self.scrollAreaWidgetContents_9)
        self.cbb_split_fname_2.setObjectName("cbb_split_fname_2")
        self.cbb_split_fname_2.setMinimumSize(QSize(120, 0))
        self.cbb_split_fname_2.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_49.addWidget(self.cbb_split_fname_2)

        self.ent_col_name_2 = QLineEdit(self.scrollAreaWidgetContents_9)
        self.ent_col_name_2.setObjectName("ent_col_name_2")

        self.horizontalLayout_49.addWidget(self.ent_col_name_2)

        self.btn_add_col_2 = QPushButton(self.scrollAreaWidgetContents_9)
        self.btn_add_col_2.setObjectName("btn_add_col_2")
        self.btn_add_col_2.setMinimumSize(QSize(60, 0))
        self.btn_add_col_2.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_49.addWidget(self.btn_add_col_2)

        self.horizontalLayout_49.setStretch(2, 40)
        self.horizontalLayout_49.setStretch(3, 20)

        self.verticalLayout_80.addLayout(self.horizontalLayout_49)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_80.addItem(self.verticalSpacer_13)

        self.groupBox_df_manip_3 = QGroupBox(self.scrollAreaWidgetContents_9)
        self.groupBox_df_manip_3.setObjectName("groupBox_df_manip_3")
        self.groupBox_df_manip_3.setMinimumSize(QSize(0, 200))
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_df_manip_3)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.horizontalLayout_65 = QHBoxLayout()
        self.horizontalLayout_65.setObjectName("horizontalLayout_65")
        self.ent_filter_query_3 = QLineEdit(self.groupBox_df_manip_3)
        self.ent_filter_query_3.setObjectName("ent_filter_query_3")

        self.horizontalLayout_65.addWidget(self.ent_filter_query_3)

        self.btn_add_filter_3 = QPushButton(self.groupBox_df_manip_3)
        self.btn_add_filter_3.setObjectName("btn_add_filter_3")
        icon21 = QIcon()
        icon21.addFile(":/icon/iconpack/filter.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_add_filter_3.setIcon(icon21)

        self.horizontalLayout_65.addWidget(self.btn_add_filter_3)

        self.verticalLayout_31.addLayout(self.horizontalLayout_65)

        self.filter_listbox_2 = QListWidget(self.groupBox_df_manip_3)
        self.filter_listbox_2.setObjectName("filter_listbox_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.filter_listbox_2.sizePolicy().hasHeightForWidth())
        self.filter_listbox_2.setSizePolicy(sizePolicy6)
        self.filter_listbox_2.setMinimumSize(QSize(0, 100))

        self.verticalLayout_31.addWidget(self.filter_listbox_2)

        self.horizontalLayout_66 = QHBoxLayout()
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_66.addItem(self.horizontalSpacer_19)

        self.btn_remove_filters_3 = QPushButton(self.groupBox_df_manip_3)
        self.btn_remove_filters_3.setObjectName("btn_remove_filters_3")
        icon22 = QIcon()
        icon22.addFile(":/icon/iconpack/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_remove_filters_3.setIcon(icon22)

        self.horizontalLayout_66.addWidget(self.btn_remove_filters_3)

        self.btn_apply_filters_3 = QPushButton(self.groupBox_df_manip_3)
        self.btn_apply_filters_3.setObjectName("btn_apply_filters_3")
        icon23 = QIcon()
        icon23.addFile(":/icon/iconpack/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_apply_filters_3.setIcon(icon23)

        self.horizontalLayout_66.addWidget(self.btn_apply_filters_3)

        self.verticalLayout_31.addLayout(self.horizontalLayout_66)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_31.addItem(self.verticalSpacer_7)

        self.verticalLayout_80.addWidget(self.groupBox_df_manip_3)

        self.horizontalLayout_138 = QHBoxLayout()
        self.horizontalLayout_138.setObjectName("horizontalLayout_138")

        self.verticalLayout_80.addLayout(self.horizontalLayout_138)

        self.scrollArea_9.setWidget(self.scrollAreaWidgetContents_9)

        self.horizontalLayout_62.addWidget(self.scrollArea_9)

        self.verticalLayout_37 = QVBoxLayout()
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(15, -1, -1, -1)
        self.layout_df_table = QVBoxLayout()
        self.layout_df_table.setObjectName("layout_df_table")

        self.verticalLayout_37.addLayout(self.layout_df_table)

        self.groupBox_3 = QGroupBox(self.collect_fit_data)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_36 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_36.setSpacing(9)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(3, 3, 3, 3)
        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_36.addItem(self.horizontalSpacer_20)

        self.btn_view_df_2 = QPushButton(self.groupBox_3)
        self.btn_view_df_2.setObjectName("btn_view_df_2")
        self.btn_view_df_2.setMinimumSize(QSize(30, 0))
        self.btn_view_df_2.setMaximumSize(QSize(30, 16777215))
        self.btn_view_df_2.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_view_df_2)

        self.btn_save_fit_results = QPushButton(self.groupBox_3)
        self.btn_save_fit_results.setObjectName("btn_save_fit_results")
        self.btn_save_fit_results.setMinimumSize(QSize(30, 0))
        self.btn_save_fit_results.setMaximumSize(QSize(30, 16777215))
        self.btn_save_fit_results.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_save_fit_results)

        self.btn_open_fit_results = QPushButton(self.groupBox_3)
        self.btn_open_fit_results.setObjectName("btn_open_fit_results")
        self.btn_open_fit_results.setMaximumSize(QSize(30, 16777215))
        # self.btn_open_fit_results.setIcon(icon18)
        self.btn_open_fit_results.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_open_fit_results)

        self.verticalLayout_37.addWidget(self.groupBox_3)

        self.horizontalLayout_62.addLayout(self.verticalLayout_37)

        self.verticalLayout_32.addLayout(self.horizontalLayout_62)

        self.tabWidget_2.addTab(self.collect_fit_data, "")
        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")

        self.horizontalLayout_61.addLayout(self.horizontalLayout_60)

        self.fit_settings = FitSettings()

        self.tabWidget_2.addTab(self.fit_settings, "")

        self.verticalLayout_25.addWidget(self.tabWidget_2)

        self.splitter.addWidget(self.bottom_widget_2)

        self.gridLayout_5.addWidget(self.splitter, 1, 2, 1, 1)

        self.sidebar = QFrame(self.central)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Raised)
        self.sidebar.setLineWidth(0)
        self.verticalLayout_17 = QVBoxLayout(self.sidebar)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(3, 3, 3, 3)
        self.groupBox = QGroupBox(self.sidebar)
        self.groupBox.setObjectName("groupBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(20)
        sizePolicy8.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy8)
        self.groupBox.setMinimumSize(QSize(290, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_64 = QLabel(self.groupBox)
        self.label_64.setObjectName("label_64")

        self.verticalLayout_2.addWidget(self.label_64)

        self.maps_listbox = QListWidget(self.groupBox)
        self.maps_listbox.setObjectName("maps_listbox")
        self.maps_listbox.setMinimumSize(QSize(270, 0))

        self.verticalLayout_2.addWidget(self.maps_listbox)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_4)

        self.btn_remove_map = QPushButton(self.groupBox)
        self.btn_remove_map.setObjectName("btn_remove_map")
        self.btn_remove_map.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_29.addWidget(self.btn_remove_map)

        self.btn_view_wafer = QPushButton(self.groupBox)
        self.btn_view_wafer.setObjectName("btn_view_wafer")
        self.btn_view_wafer.setMaximumSize(QSize(70, 16777215))
        self.btn_view_wafer.setIconSize(QSize(22, 22))

        self.horizontalLayout_29.addWidget(self.btn_view_wafer)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(70, 16777215))
        self.pushButton_3.setIconSize(QSize(22, 22))

        self.horizontalLayout_29.addWidget(self.pushButton_3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_29)

        self.verticalLayout_17.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.sidebar)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(290, 0))
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 5, 5, 5)

        sel_all_icon = QIcon(str(icons / 'select-all.png'))
        self.btn_sel_all = QPushButton(self.groupBox_2)
        self.btn_sel_all.setIcon(sel_all_icon)
        self.btn_sel_all.setIconSize(QSize(22, 22))
        self.btn_sel_all.setMaximumSize(QSize(30, 16777215))
        self.btn_sel_all.setObjectName("btn_sel_all")
        self.btn_sel_all.setToolTip("Select all spectre")

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalSpacer_52 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_52)

        self.btn_init = QPushButton(self.groupBox_2)
        self.btn_init.setObjectName("btn_init")
        self.btn_init.setMinimumSize(QSize(70, 0))
        self.btn_init.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_8.addWidget(self.btn_init)

        self.btn_show_stats = QPushButton(self.groupBox_2)
        self.btn_show_stats.setObjectName("btn_show_stats")
        self.btn_show_stats.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_8.addWidget(self.btn_show_stats)

        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.spectra_listbox = QListWidget(self.groupBox_2)
        self.spectra_listbox.setObjectName("spectra_listbox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.spectra_listbox.sizePolicy().hasHeightForWidth())
        self.spectra_listbox.setSizePolicy(sizePolicy9)
        self.spectra_listbox.setMinimumSize(QSize(270, 0))
        self.spectra_listbox.setDragEnabled(False)
        self.spectra_listbox.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_10.addWidget(self.spectra_listbox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.item_count_label = QLabel(self.groupBox_2)
        self.item_count_label.setObjectName("item_count_label")

        self.horizontalLayout.addWidget(self.item_count_label)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.verticalLayout_10.addLayout(self.horizontalLayout)

        self.verticalLayout_17.addWidget(self.groupBox_2)

        self.verticalLayout_17.setStretch(0, 30)
        self.verticalLayout_17.setStretch(1, 65)

        # # Create the sidebar content
        # self.maps_list = MapsList()
        # self.spectrum_list = SpectrumList()

        # self.sidebar = QWidget()
        # self.sidebar_layout = QVBoxLayout(self.sidebar)
        # self.sidebar_layout.addWidget(self.maps_list)
        # self.sidebar_layout.addWidget(self.spectrum_list)

        # # Create the main content (placeholder for your main content widget)
        # self.main_content = QWidget()  # Replace with your actual main content widget

        # # Create a splitter to separate the sidebar and the main content
        # self.main_splitter = QSplitter(Qt.Horizontal)
        # self.main_splitter.addWidget(self.main_content)
        # self.main_splitter.addWidget(self.sidebar)  

        # self.main_splitter.setStretchFactor(0, 1)  # Main content takes up remaining space
        # self.main_splitter.setStretchFactor(1, 0)

        # # Add the splitter to the main layout
        # self.gridLayout_5.addWidget(self.main_splitter, 1, 3, 1, 1)
        self.gridLayout_5.addWidget(self.sidebar, 1, 3, 1, 1)


        self.tab_plot_settings = QWidget()
        self.tab_plot_settings.setObjectName("tab_plot_settings")

        self.horizontalLayout_71 = QHBoxLayout()
        self.horizontalLayout_71.setObjectName("horizontalLayout_71")

        self.horizontalLayout_89 = QHBoxLayout()
        self.horizontalLayout_89.setObjectName("horizontalLayout_89")


        self.tab_more_options = QWidget()
        self.tab_more_options.setObjectName("tab_more_options")
        self.verticalLayout_4 = QVBoxLayout(self.tab_more_options)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_8 = QScrollArea(self.tab_more_options)
        self.scrollArea_8.setObjectName("scrollArea_8")
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollAreaWidgetContents_8 = QWidget()
        self.scrollAreaWidgetContents_8.setObjectName("scrollAreaWidgetContents_8")
        self.scrollAreaWidgetContents_8.setGeometry(QRect(0, 0, 249, 267))
        self.cb_legend_visible = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_legend_visible.setObjectName("cb_legend_visible")
        self.cb_legend_visible.setChecked(True)


        self.cb_show_err_bar_plot = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_show_err_bar_plot.setObjectName("cb_show_err_bar_plot")
        self.cb_show_err_bar_plot.setChecked(True)


        self.cb_wafer_stats = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_wafer_stats.setObjectName("cb_wafer_stats")
        self.cb_wafer_stats.setChecked(True)

        self.cb_join_for_point_plot = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_join_for_point_plot.setObjectName("cb_join_for_point_plot")

        self.spb_trendline_oder = QDoubleSpinBox(self.scrollAreaWidgetContents_8)
        self.spb_trendline_oder.setObjectName("spb_trendline_oder")
        self.spb_trendline_oder.setDecimals(0)
        self.spb_trendline_oder.setMinimum(1.000000000000000)
        self.spb_trendline_oder.setMaximum(10.000000000000000)


        self.label_18 = QLabel(self.scrollAreaWidgetContents_8)
        self.label_18.setObjectName("label_18")


        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)


        self.line_3 = QFrame(self.scrollAreaWidgetContents_8)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.legends_loc = QHBoxLayout()
        self.legends_loc.setObjectName("legends_loc")
        self.label_17 = QLabel(self.scrollAreaWidgetContents_8)
        self.label_17.setObjectName("label_17")

        self.legends_loc.addWidget(self.label_17)

        self.cbb_legend_loc = QComboBox(self.scrollAreaWidgetContents_8)
        self.cbb_legend_loc.setObjectName("cbb_legend_loc")

        self.legends_loc.addWidget(self.cbb_legend_loc)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.legends_loc.addItem(self.horizontalSpacer_35)

        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName("main_layout")

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalSpacer_48 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_48)

        self.line_2 = QFrame(self.scrollAreaWidgetContents_8)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)

        self.verticalLayout_4.addWidget(self.scrollArea_8)

        self.tab_multi_axes = QWidget()
        self.tab_multi_axes.setObjectName("tab_multi_axes")

        self.verticalLayout_15.addWidget(self.central)

        self.setCentralWidget(self.centralwidget)
        

        self.retranslateUi()

        self.tabWidget_2.setCurrentIndex(0)

        self.statusBar = StatusBar()
        self.setStatusBar(self.statusBar)

    def retranslateUi(self):
        self.setWindowTitle("Fitspy")
        self.btn_cosmis_ray.setToolTip("Detect cosmis ray based on the loaded spectra")
        self.btn_cosmis_ray.setText("Spike removal")
        self.label_99.setText("X-axis unit:")
        self.groupBox_4.setTitle("")
        self.label_54.setText("Spectral range:")
        self.label_61.setText("X max/min:")
        self.label_62.setText("/")
        self.range_apply.setToolTip("Extract the spectral windows range.\n"
" Hold 'Ctrl' and press 'Extract' button to apply to all spectra")
        self.range_apply.setText("Extract")
        self.label_59.setText("")
        self.baseline.setTitle("")
        self.label_52.setText("Baseline:")
        self.rbtn_linear.setText("Linear")
        self.rbtn_polynomial.setText("Poly")
        self.label_37.setToolTip("Number of nearby points considered to smoothing the noise")
        self.label_37.setText("Smoothing")
        self.cb_attached.setText("Attached")
        self.btn_undo_baseline.setToolTip("To remove all baseline points and undo the baseline subtraction")
        self.btn_undo_baseline.setText("Undo baseline")
        self.sub_baseline.setToolTip("To subtract the evaluated baseline from the spectrum. \n"
" Hold 'Ctrl' and press 'Subtract' button to apply to all spectra")
        self.sub_baseline.setText("Subtract")
        self.label_60.setText("")
        self.peaks.setTitle("")
        self.label_57.setText("Peaks:")
        self.label_41.setText("Peak model:")
        self.clear_peaks.setToolTip("Clear all the current peak models. \n"
" Hold 'Ctrl' and press 'Clear peaks' button to apply to all spectra")
        self.clear_peaks.setText("Clear peaks")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.fit_model_editor), "Fit model builder")
        self.btn_collect_results.setToolTip("To gather all the best fit results in a dataframe for visualization")
        self.btn_collect_results.setText(" Collect fit results")
        self.label_56.setText("Add new column(s) from file name:")
        self.btn_split_fname_2.setToolTip("Split the file name of spectrum to several parts")
        self.btn_split_fname_2.setText("Split")
        self.cbb_split_fname_2.setToolTip("Select file name part")
        self.cbb_split_fname_2.setPlaceholderText("")
        self.ent_col_name_2.setPlaceholderText("type column name")
        self.btn_add_col_2.setToolTip("Add a new column containing the selected part")
        self.btn_add_col_2.setText("Add")
        self.groupBox_df_manip_3.setTitle("Data filtering:")
        self.ent_filter_query_3.setPlaceholderText("Enter query expression (? : see Help menu)")
        self.btn_add_filter_3.setToolTip("Add filter(s) to dataframe")
        self.btn_add_filter_3.setText("Add filter(s)")
        self.btn_remove_filters_3.setToolTip("Remove filters from the list")
        self.btn_remove_filters_3.setText("Remove filter")
        self.btn_apply_filters_3.setToolTip("Apply selected filters to selected dataframe")
        self.btn_apply_filters_3.setText("Apply filter(s)")
        self.groupBox_3.setTitle("")
        self.btn_view_df_2.setToolTip("View collected fit results")
        self.btn_view_df_2.setText("")
        self.btn_save_fit_results.setToolTip("Save all fit results in an Excel file")
        self.btn_save_fit_results.setText("")
        self.btn_open_fit_results.setToolTip("Open fit results (format Excel) to view/plot")
        self.btn_open_fit_results.setText("")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.collect_fit_data), "Collect fit data")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.fit_settings), "More settings")
        self.groupBox.setTitle("")
        self.label_64.setText("Maps:")
        self.btn_remove_map.setText("")
        self.btn_view_wafer.setText("")
        self.pushButton_3.setText("")
        self.groupBox_2.setTitle("")
        self.btn_init.setToolTip("Reinitialize to RAW spectrum (Hold Ctrl to reinit all spectra)")
        self.btn_init.setText("Reinitialize")
        self.btn_show_stats.setToolTip("Show fitting statistique results")
        self.btn_show_stats.setText("Stats")
        self.item_count_label.setText("0 points")