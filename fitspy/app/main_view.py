from pathlib import Path
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import (QMainWindow, QAbstractItemView, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit, QListWidget,
    QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)

from fitspy.components.settings import StatusBar, ModelBuilder

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
            objectName="actionManual",
        )
        self.actionDarkMode = QAction(
            self,
            icon=QIcon(str(icons / "dark.png")),
            toolTip="Dark Mode",
            objectName="actionDarkMode",
        )
        self.actionLightMode = QAction(
            self,
            icon=QIcon(str(icons / "light-mode.svg")),
            toolTip="Light Mode",
            objectName="actionLightMode",
        )
        self.actionAbout = QAction(
            self,
            icon=QIcon(str(icons / "about.png")),
            toolTip="About",
            objectName="actionAbout",
        )
        self.actionOpen = QAction(
            self,
            icon=QIcon(str(icons / "icons8-folder-96.png")),
            toolTip="Open spectra data, saved work or Excel file",
            objectName="actionOpen",
        )
        self.actionSave = QAction(
            self,
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save current work",
            objectName="actionSave",
        )
        self.actionClear_env = QAction(
            self,
            icon=QIcon(str(icons / "clear.png")),
            toolTip="Clear the environment",
            objectName="actionClear_env",
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

        self.centralwidget = QWidget(self, objectName="centralwidget", enabled=True, baseSize=QSize(0, 0))
        self.verticalLayout_15 = QVBoxLayout(self.centralwidget, spacing=0, objectName="verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)

        self.menuBar = MenuBar()
        self.addToolBar(Qt.TopToolBarArea, self.menuBar)

        self.Upper_zone_3 = QHBoxLayout()
        self.Upper_zone_3.setSpacing(0)
        self.Upper_zone_3.setObjectName("Upper_zone_3")
        self.QVBoxlayout_2 = QVBoxLayout()
        self.QVBoxlayout_2.setSpacing(6)
        self.QVBoxlayout_2.setObjectName("QVBoxlayout_2")

        self.bottom_frame_3 = QHBoxLayout()
        self.bottom_frame_3.setSpacing(10)
        self.bottom_frame_3.setObjectName("bottom_frame_3")
        self.bottom_frame_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.bottom_frame_3.setContentsMargins(2, 2, 2, 2)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_24)



        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_16)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_25)

        self.bottom_frame_3.setStretch(0, 50)
        self.bottom_frame_3.setStretch(1, 25)
        self.bottom_frame_3.setStretch(9, 2)

        
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, 0, 316, 448))
        self.verticalLayout_74 = QVBoxLayout(self.scrollAreaWidgetContents_7)
        self.verticalLayout_74.setObjectName("verticalLayout_74")
        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_74.addItem(self.verticalSpacer_12)

        self.view_options_box_2 = QGroupBox(self.scrollAreaWidgetContents_7)
        self.view_options_box_2.setObjectName("view_options_box_2")
        self.view_options_box_2.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_7 = QGridLayout(self.view_options_box_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.cb_residual_3 = QCheckBox(self.view_options_box_2)
        self.cb_residual_3.setObjectName("cb_residual_3")
        self.cb_residual_3.setChecked(False)

        self.gridLayout_7.addWidget(self.cb_residual_3, 1, 1, 1, 1)

        self.cb_filled_3 = QCheckBox(self.view_options_box_2)
        self.cb_filled_3.setObjectName("cb_filled_3")
        self.cb_filled_3.setChecked(True)

        self.gridLayout_7.addWidget(self.cb_filled_3, 0, 2, 1, 1)

        self.cb_bestfit_3 = QCheckBox(self.view_options_box_2)
        self.cb_bestfit_3.setObjectName("cb_bestfit_3")
        self.cb_bestfit_3.setChecked(True)

        self.gridLayout_7.addWidget(self.cb_bestfit_3, 0, 1, 1, 1)

        self.cb_legend_3 = QCheckBox(self.view_options_box_2)
        self.cb_legend_3.setObjectName("cb_legend_3")
        self.cb_legend_3.setEnabled(True)
        self.cb_legend_3.setChecked(False)

        self.gridLayout_7.addWidget(self.cb_legend_3, 0, 0, 1, 1)

        self.cb_raw_3 = QCheckBox(self.view_options_box_2)
        self.cb_raw_3.setObjectName("cb_raw_3")
        self.cb_raw_3.setChecked(False)

        self.gridLayout_7.addWidget(self.cb_raw_3, 1, 0, 1, 1)

        self.cb_colors_3 = QCheckBox(self.view_options_box_2)
        self.cb_colors_3.setObjectName("cb_colors_3")
        self.cb_colors_3.setChecked(True)

        self.gridLayout_7.addWidget(self.cb_colors_3, 1, 2, 1, 1)

        self.cb_peaks_3 = QCheckBox(self.view_options_box_2)
        self.cb_peaks_3.setObjectName("cb_peaks_3")
        self.cb_peaks_3.setChecked(False)

        self.gridLayout_7.addWidget(self.cb_peaks_3, 0, 3, 1, 1)

        self.cb_normalize_3 = QCheckBox(self.view_options_box_2)
        self.cb_normalize_3.setObjectName("cb_normalize_3")

        self.gridLayout_7.addWidget(self.cb_normalize_3, 1, 3, 1, 1)

        self.verticalLayout_74.addWidget(self.view_options_box_2)



        self.Upper_zone_3.setStretch(0, 75)

        self.horizontalLayout_72 = QHBoxLayout()
        self.horizontalLayout_72.setSpacing(5)
        self.horizontalLayout_72.setObjectName("horizontalLayout_72")
        self.horizontalLayout_72.setContentsMargins(-1, 5, 5, 5)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 428, 375))
        self.fit_model_builder = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.fit_model_builder.setSpacing(10)
        self.fit_model_builder.setObjectName("fit_model_builder")
        self.fit_model_builder.setContentsMargins(10, 10, 10, 10)

        self.horizontalSpacer_57 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)


        self.label_22 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_22.setObjectName("label_22")


        self.cbb_xaxis_unit = QComboBox(self.scrollAreaWidgetContents_4)
        self.cbb_xaxis_unit.setObjectName("cbb_xaxis_unit")

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_40 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_40.setSpacing(5)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(2, 2, 2, 2)

        self.horizontalLayout_74 = QHBoxLayout()
        self.horizontalLayout_74.setSpacing(5)
        self.horizontalLayout_74.setObjectName("horizontalLayout_74")
        self.horizontalLayout_74.setContentsMargins(2, 2, 2, 2)
        self.label_66 = QLabel(self.groupBox_5)
        self.label_66.setObjectName("label_66")

        self.horizontalLayout_74.addWidget(self.label_66)

        self.horizontalSpacer_34 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_74.addItem(self.horizontalSpacer_34)

        self.range_min_2 = QLineEdit(self.groupBox_5)
        self.range_min_2.setObjectName("range_min_2")

        self.horizontalLayout_74.addWidget(self.range_min_2)

        self.label_67 = QLabel(self.groupBox_5)
        self.label_67.setObjectName("label_67")

        self.horizontalLayout_74.addWidget(self.label_67)

        self.range_max_2 = QLineEdit(self.groupBox_5)
        self.range_max_2.setObjectName("range_max_2")

        self.horizontalLayout_74.addWidget(self.range_max_2)

        self.range_apply_2 = QPushButton(self.groupBox_5)
        self.range_apply_2.setObjectName("range_apply_2")

        self.horizontalLayout_74.addWidget(self.range_apply_2)

        self.verticalLayout_40.addLayout(self.horizontalLayout_74)

        self.fit_model_builder.addWidget(self.groupBox_5)

        self.label_68 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_68.setObjectName("label_68")

        self.fit_model_builder.addWidget(self.label_68)

        self.baseline_2 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.baseline_2.setObjectName("baseline_2")
        self.verticalLayout_41 = QVBoxLayout(self.baseline_2)
        self.verticalLayout_41.setSpacing(5)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(2, 2, 2, 2)

        self.horizontalLayout_75 = QHBoxLayout()
        self.horizontalLayout_75.setSpacing(5)
        self.horizontalLayout_75.setObjectName("horizontalLayout_75")
        self.horizontalLayout_75.setContentsMargins(2, 2, 2, 2)
        self.rbtn_linear_2 = QRadioButton(self.baseline_2)
        self.rbtn_linear_2.setObjectName("rbtn_linear_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.rbtn_linear_2.sizePolicy().hasHeightForWidth())
        self.rbtn_linear_2.setSizePolicy(sizePolicy3)
        self.rbtn_linear_2.setChecked(True)

        self.horizontalLayout_75.addWidget(self.rbtn_linear_2)

        self.rbtn_polynomial_2 = QRadioButton(self.baseline_2)
        self.rbtn_polynomial_2.setObjectName("rbtn_polynomial_2")
        sizePolicy3.setHeightForWidth(self.rbtn_polynomial_2.sizePolicy().hasHeightForWidth())
        self.rbtn_polynomial_2.setSizePolicy(sizePolicy3)

        self.horizontalLayout_75.addWidget(self.rbtn_polynomial_2)

        self.degre_2 = QSpinBox(self.baseline_2)
        self.degre_2.setObjectName("degre_2")
        self.degre_2.setMinimum(1)

        self.horizontalLayout_75.addWidget(self.degre_2)

        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_75.addItem(self.horizontalSpacer_36)

        self.label_70 = QLabel(self.baseline_2)
        self.label_70.setObjectName("label_70")

        self.horizontalLayout_75.addWidget(self.label_70)

        self.noise_2 = QDoubleSpinBox(self.baseline_2)
        self.noise_2.setObjectName("noise_2")
        self.noise_2.setDecimals(0)
        self.noise_2.setValue(5.000000000000000)

        self.horizontalLayout_75.addWidget(self.noise_2)

        self.horizontalLayout_75.setStretch(0, 25)
        self.horizontalLayout_75.setStretch(1, 25)

        self.verticalLayout_41.addLayout(self.horizontalLayout_75)

        self.horizontalLayout_76 = QHBoxLayout()
        self.horizontalLayout_76.setSpacing(5)
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.horizontalLayout_76.setContentsMargins(2, 2, 2, 2)
        self.cb_attached_3 = QCheckBox(self.baseline_2)
        self.cb_attached_3.setObjectName("cb_attached_3")
        sizePolicy3.setHeightForWidth(self.cb_attached_3.sizePolicy().hasHeightForWidth())
        self.cb_attached_3.setSizePolicy(sizePolicy3)
        self.cb_attached_3.setChecked(True)

        self.horizontalLayout_76.addWidget(self.cb_attached_3)

        self.horizontalSpacer_37 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_76.addItem(self.horizontalSpacer_37)

        self.btn_undo_baseline_2 = QPushButton(self.baseline_2)
        self.btn_undo_baseline_2.setObjectName("btn_undo_baseline_2")

        self.horizontalLayout_76.addWidget(self.btn_undo_baseline_2)

        self.sub_baseline_2 = QPushButton(self.baseline_2)
        self.sub_baseline_2.setObjectName("sub_baseline_2")

        self.horizontalLayout_76.addWidget(self.sub_baseline_2)

        self.verticalLayout_41.addLayout(self.horizontalLayout_76)

        self.fit_model_builder.addWidget(self.baseline_2)

        self.label_71 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_71.setObjectName("label_71")

        self.fit_model_builder.addWidget(self.label_71)

        self.peaks_2 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.peaks_2.setObjectName("peaks_2")
        self.verticalLayout_42 = QVBoxLayout(self.peaks_2)
        self.verticalLayout_42.setSpacing(5)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(2, 2, 2, 2)

        self.horizontalLayout_77 = QHBoxLayout()
        self.horizontalLayout_77.setSpacing(5)
        self.horizontalLayout_77.setObjectName("horizontalLayout_77")
        self.horizontalLayout_77.setContentsMargins(2, 2, 2, 2)
        self.label_73 = QLabel(self.peaks_2)
        self.label_73.setObjectName("label_73")

        self.horizontalLayout_77.addWidget(self.label_73)

        self.horizontalSpacer_38 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_77.addItem(self.horizontalSpacer_38)

        self.cbb_fit_models_2 = QComboBox(self.peaks_2)
        self.cbb_fit_models_2.setObjectName("cbb_fit_models_2")

        self.horizontalLayout_77.addWidget(self.cbb_fit_models_2)

        self.clear_peaks_2 = QPushButton(self.peaks_2)
        self.clear_peaks_2.setObjectName("clear_peaks_2")

        self.horizontalLayout_77.addWidget(self.clear_peaks_2)

        self.horizontalLayout_77.setStretch(2, 65)

        self.verticalLayout_42.addLayout(self.horizontalLayout_77)

        self.fit_model_builder.addWidget(self.peaks_2)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_83 = QHBoxLayout()

        self.fit_model_builder.addItem(self.verticalSpacer_15)
        

        self.verticalLayout_43 = QVBoxLayout()
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 731, 265))
        self.verticalLayout_44 = QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_44.setObjectName("verticalLayout_44")
        self.verticalLayout_312 = QVBoxLayout()
        self.verticalLayout_312.setObjectName("verticalLayout_312")
        self.horizontalLayout_79 = QHBoxLayout()
        self.horizontalLayout_79.setObjectName("horizontalLayout_79")
        self.peak_table1_2 = QHBoxLayout()
        self.peak_table1_2.setObjectName("peak_table1_2")

        self.horizontalLayout_79.addLayout(self.peak_table1_2)

        self.horizontalLayout_80 = QHBoxLayout()
        self.horizontalLayout_80.setObjectName("horizontalLayout_80")

        self.horizontalLayout_79.addLayout(self.horizontalLayout_80)

        self.verticalLayout_312.addLayout(self.horizontalLayout_79)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_312.addItem(self.verticalSpacer_16)

        self.verticalLayout_44.addLayout(self.verticalLayout_312)

        self.horizontalLayout_81 = QHBoxLayout()
        self.horizontalLayout_81.setSpacing(5)
        self.horizontalLayout_81.setObjectName("horizontalLayout_81")

        self.verticalLayout_45 = QVBoxLayout()
        self.verticalLayout_45.setObjectName("verticalLayout_45")
        self.horizontalLayout_82 = QHBoxLayout()
        self.horizontalLayout_82.setSpacing(5)
        self.horizontalLayout_82.setObjectName("horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(5, 2, 5, 2)

        self.horizontalSpacer_51 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_82.addItem(self.horizontalSpacer_51)

        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_82.addItem(self.horizontalSpacer_39)

        self.verticalLayout_45.addLayout(self.horizontalLayout_82)

        self.horizontalSpacer_42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_81.addLayout(self.verticalLayout_45)

        self.verticalLayout_43.addLayout(self.horizontalLayout_81)

        self.verticalLayout_43.setStretch(0, 85)
        self.verticalLayout_43.setStretch(1, 15)

        self.collect_fit_data_2 = QWidget()
        self.collect_fit_data_2.setObjectName("collect_fit_data_2")
        self.verticalLayout_47 = QVBoxLayout(self.collect_fit_data_2)
        self.verticalLayout_47.setSpacing(6)
        self.verticalLayout_47.setObjectName("verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_94 = QHBoxLayout()
        self.horizontalLayout_94.setSpacing(5)
        self.horizontalLayout_94.setObjectName("horizontalLayout_94")
        self.horizontalLayout_94.setContentsMargins(5, 5, 5, 5)
        
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName("scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 322, 144))
        self.verticalLayout_81 = QVBoxLayout(self.scrollAreaWidgetContents_11)
        self.verticalLayout_81.setSpacing(10)
        self.verticalLayout_81.setObjectName("verticalLayout_81")
        self.verticalLayout_81.setContentsMargins(10, 10, 10, 10)

        self.label_83 = QLabel(self.scrollAreaWidgetContents_11)
        self.label_83.setObjectName("label_83")

        self.verticalLayout_81.addWidget(self.label_83)

        self.horizontalLayout_95 = QHBoxLayout()
        self.horizontalLayout_95.setObjectName("horizontalLayout_95")
        self.btn_split_fname = QPushButton(self.scrollAreaWidgetContents_11)
        self.btn_split_fname.setObjectName("btn_split_fname")
        self.btn_split_fname.setMinimumSize(QSize(40, 0))
        self.btn_split_fname.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_95.addWidget(self.btn_split_fname)

        self.cbb_split_fname = QComboBox(self.scrollAreaWidgetContents_11)
        self.cbb_split_fname.setObjectName("cbb_split_fname")
        self.cbb_split_fname.setMinimumSize(QSize(120, 0))
        self.cbb_split_fname.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_95.addWidget(self.cbb_split_fname)

        self.ent_col_name = QLineEdit(self.scrollAreaWidgetContents_11)
        self.ent_col_name.setObjectName("ent_col_name")

        self.horizontalLayout_95.addWidget(self.ent_col_name)

        self.btn_add_col = QPushButton(self.scrollAreaWidgetContents_11)
        self.btn_add_col.setObjectName("btn_add_col")
        self.btn_add_col.setMinimumSize(QSize(60, 0))
        self.btn_add_col.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_95.addWidget(self.btn_add_col)

        self.horizontalLayout_95.setStretch(2, 40)
        self.horizontalLayout_95.setStretch(3, 20)

        self.verticalLayout_81.addLayout(self.horizontalLayout_95)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_81.addItem(self.verticalSpacer_18)

        self.horizontalLayout_139 = QHBoxLayout()
        self.horizontalLayout_139.setObjectName("horizontalLayout_139")

        self.verticalLayout_81.addLayout(self.horizontalLayout_139)

        self.verticalLayout_55 = QVBoxLayout()
        self.verticalLayout_55.setObjectName("verticalLayout_55")
        self.verticalLayout_55.setContentsMargins(15, -1, -1, -1)
        self.layout_df_table2 = QVBoxLayout()
        self.layout_df_table2.setObjectName("layout_df_table2")

        self.verticalLayout_55.addLayout(self.layout_df_table2)

        self.groupBox_6 = QGroupBox(self.collect_fit_data_2)
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_98 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_98.setSpacing(9)
        self.horizontalLayout_98.setObjectName("horizontalLayout_98")
        self.horizontalLayout_98.setContentsMargins(3, 3, 3, 3)
        self.horizontalSpacer_46 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_98.addItem(self.horizontalSpacer_46)

        self.btn_view_df_5 = QPushButton(self.groupBox_6)
        self.btn_view_df_5.setObjectName("btn_view_df_5")
        self.btn_view_df_5.setMinimumSize(QSize(30, 0))
        self.btn_view_df_5.setMaximumSize(QSize(30, 16777215))
        icon16 = QIcon()
        icon16.addFile(":/icon/iconpack/view11.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_view_df_5.setIcon(icon16)
        self.btn_view_df_5.setIconSize(QSize(22, 22))

        self.horizontalLayout_98.addWidget(self.btn_view_df_5)

        self.btn_save_fit_results_3 = QPushButton(self.groupBox_6)
        self.btn_save_fit_results_3.setObjectName("btn_save_fit_results_3")
        self.btn_save_fit_results_3.setMinimumSize(QSize(30, 0))
        self.btn_save_fit_results_3.setMaximumSize(QSize(30, 16777215))
        icon17 = QIcon()
        icon17.addFile(":/icon/iconpack/save12.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_save_fit_results_3.setIcon(icon17)
        self.btn_save_fit_results_3.setIconSize(QSize(22, 22))

        self.horizontalLayout_98.addWidget(self.btn_save_fit_results_3)

        self.btn_open_fit_results_3 = QPushButton(self.groupBox_6)
        self.btn_open_fit_results_3.setObjectName("btn_open_fit_results_3")
        sizePolicy3.setHeightForWidth(self.btn_open_fit_results_3.sizePolicy().hasHeightForWidth())
        self.btn_open_fit_results_3.setSizePolicy(sizePolicy3)
        self.btn_open_fit_results_3.setMaximumSize(QSize(30, 16777215))
        icon18 = QIcon()
        icon18.addFile(":/icon/iconpack/opened-folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_open_fit_results_3.setIcon(icon18)
        self.btn_open_fit_results_3.setIconSize(QSize(22, 22))

        self.horizontalLayout_98.addWidget(self.btn_open_fit_results_3)

        self.verticalLayout_55.addWidget(self.groupBox_6)

        self.horizontalLayout_94.addLayout(self.verticalLayout_55)

        self.verticalLayout_47.addLayout(self.horizontalLayout_94)

        self.fit_settings_3 = QWidget()
        self.fit_settings_3.setObjectName("fit_settings_3")
        self.fit_settings_3.setEnabled(True)
        self.label_74 = QLabel(self.fit_settings_3)
        self.label_74.setObjectName("label_74")
        self.label_74.setGeometry(QRect(20, 10, 121, 31))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.label_74.setFont(font1)
        self.layoutWidget_2 = QWidget(self.fit_settings_3)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(20, 50, 381, 224))
        self.verticalLayout_48 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_48.setObjectName("verticalLayout_48")
        self.verticalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_83 = QHBoxLayout()
        self.horizontalLayout_83.setObjectName("horizontalLayout_83")
        self.label_51 = QLabel(self.layoutWidget_2)
        self.label_51.setObjectName("label_51")

        self.horizontalLayout_83.addWidget(self.label_51)

        self.cb_fit_negative_2 = QCheckBox(self.layoutWidget_2)
        self.cb_fit_negative_2.setObjectName("cb_fit_negative_2")

        self.horizontalLayout_83.addWidget(self.cb_fit_negative_2)

        self.verticalLayout_48.addLayout(self.horizontalLayout_83)

        self.horizontalLayout_84 = QHBoxLayout()
        self.horizontalLayout_84.setObjectName("horizontalLayout_84")
        self.label_75 = QLabel(self.layoutWidget_2)
        self.label_75.setObjectName("label_75")

        self.horizontalLayout_84.addWidget(self.label_75)

        self.max_iteration_2 = QSpinBox(self.layoutWidget_2)
        self.max_iteration_2.setObjectName("max_iteration_2")
        self.max_iteration_2.setMaximum(10000)
        self.max_iteration_2.setValue(200)

        self.horizontalLayout_84.addWidget(self.max_iteration_2)

        self.verticalLayout_48.addLayout(self.horizontalLayout_84)

        self.horizontalLayout_85 = QHBoxLayout()
        self.horizontalLayout_85.setObjectName("horizontalLayout_85")
        self.label_76 = QLabel(self.layoutWidget_2)
        self.label_76.setObjectName("label_76")

        self.horizontalLayout_85.addWidget(self.label_76)

        self.cbb_fit_methods_2 = QComboBox(self.layoutWidget_2)
        self.cbb_fit_methods_2.setObjectName("cbb_fit_methods_2")

        self.horizontalLayout_85.addWidget(self.cbb_fit_methods_2)

        self.verticalLayout_48.addLayout(self.horizontalLayout_85)

        self.horizontalLayout_87 = QHBoxLayout()
        self.horizontalLayout_87.setObjectName("horizontalLayout_87")
        self.label_78 = QLabel(self.layoutWidget_2)
        self.label_78.setObjectName("label_78")

        self.horizontalLayout_87.addWidget(self.label_78)

        self.xtol_2 = QLineEdit(self.layoutWidget_2)
        self.xtol_2.setObjectName("xtol_2")
        self.xtol_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_87.addWidget(self.xtol_2)

        self.verticalLayout_48.addLayout(self.horizontalLayout_87)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_48.addItem(self.verticalSpacer_17)

        self.l_defaut_folder_model_3 = QLineEdit(self.fit_settings_3)
        self.l_defaut_folder_model_3.setObjectName("l_defaut_folder_model_3")
        self.l_defaut_folder_model_3.setGeometry(QRect(160, 320, 481, 21))
        self.btn_refresh_model_folder_3 = QPushButton(self.fit_settings_3)
        self.btn_refresh_model_folder_3.setObjectName("btn_refresh_model_folder_3")
        self.btn_refresh_model_folder_3.setGeometry(QRect(650, 320, 75, 23))

        self.horizontalLayout_103 = QHBoxLayout()
        self.horizontalLayout_103.setObjectName("horizontalLayout_103")

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_103.addItem(self.horizontalSpacer_9)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")

        self.listbox_layout = QVBoxLayout()
        self.listbox_layout.setObjectName("listbox_layout")

        self.horizontalLayout_104 = QHBoxLayout()
        self.horizontalLayout_104.setObjectName("horizontalLayout_104")

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_104.addItem(self.horizontalSpacer_23)

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

        self.bottom_frame = QHBoxLayout()
        self.bottom_frame.setSpacing(10)
        self.bottom_frame.setObjectName("bottom_frame")
        self.bottom_frame.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.bottom_frame.setContentsMargins(2, 2, 2, 2)
        self.toolbar_frame = QHBoxLayout()
        self.toolbar_frame.setObjectName("toolbar_frame")

        self.bottom_frame.addLayout(self.toolbar_frame)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame.addItem(self.horizontalSpacer_7)

        self.rdbtn_baseline = QRadioButton(self.upper_frame)
        self.rdbtn_baseline.setObjectName("rdbtn_baseline")
        self.rdbtn_baseline.setChecked(True)

        self.bottom_frame.addWidget(self.rdbtn_baseline)

        self.rdbtn_peak = QRadioButton(self.upper_frame)
        self.rdbtn_peak.setObjectName("rdbtn_peak")
        self.rdbtn_peak.setChecked(False)

        self.bottom_frame.addWidget(self.rdbtn_peak)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame.addItem(self.horizontalSpacer_15)

        self.rsquared_1 = QLabel(self.upper_frame)
        self.rsquared_1.setObjectName("rsquared_1")
        self.rsquared_1.setMinimumSize(QSize(80, 0))
        self.rsquared_1.setMaximumSize(QSize(80, 16777215))

        self.bottom_frame.addWidget(self.rsquared_1)

        self.label_63 = QLabel(self.upper_frame)
        self.label_63.setObjectName("label_63")
        self.label_63.setMinimumSize(QSize(20, 0))
        self.label_63.setMaximumSize(QSize(20, 16777215))

        self.bottom_frame.addWidget(self.label_63)

        self.sb_dpi_spectra = QSpinBox(self.upper_frame)
        self.sb_dpi_spectra.setObjectName("sb_dpi_spectra")
        self.sb_dpi_spectra.setMinimum(100)
        self.sb_dpi_spectra.setMaximum(200)
        self.sb_dpi_spectra.setSingleStep(10)

        self.bottom_frame.addWidget(self.sb_dpi_spectra)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame.addItem(self.horizontalSpacer_8)

        self.bottom_frame.setStretch(0, 50)
        self.bottom_frame.setStretch(1, 25)
        self.bottom_frame.setStretch(9, 2)

        self.verticalLayout_26.addLayout(self.bottom_frame)

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

        self.view_options_box = QGroupBox(self.widget_7)
        self.view_options_box.setObjectName("view_options_box")
        self.view_options_box.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_6 = QGridLayout(self.view_options_box)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.cb_residual = QCheckBox(self.view_options_box)
        self.cb_residual.setObjectName("cb_residual")
        self.cb_residual.setChecked(False)

        self.gridLayout_6.addWidget(self.cb_residual, 1, 1, 1, 1)

        self.cb_filled = QCheckBox(self.view_options_box)
        self.cb_filled.setObjectName("cb_filled")
        self.cb_filled.setChecked(True)

        self.gridLayout_6.addWidget(self.cb_filled, 0, 2, 1, 1)

        self.cb_bestfit = QCheckBox(self.view_options_box)
        self.cb_bestfit.setObjectName("cb_bestfit")
        self.cb_bestfit.setChecked(True)

        self.gridLayout_6.addWidget(self.cb_bestfit, 0, 1, 1, 1)

        self.cb_legend = QCheckBox(self.view_options_box)
        self.cb_legend.setObjectName("cb_legend")
        self.cb_legend.setEnabled(True)
        self.cb_legend.setChecked(False)

        self.gridLayout_6.addWidget(self.cb_legend, 0, 0, 1, 1)

        self.cb_raw = QCheckBox(self.view_options_box)
        self.cb_raw.setObjectName("cb_raw")
        self.cb_raw.setChecked(False)

        self.gridLayout_6.addWidget(self.cb_raw, 1, 0, 1, 1)

        self.cb_colors = QCheckBox(self.view_options_box)
        self.cb_colors.setObjectName("cb_colors")
        self.cb_colors.setChecked(True)

        self.gridLayout_6.addWidget(self.cb_colors, 1, 2, 1, 1)

        self.cb_peaks = QCheckBox(self.view_options_box)
        self.cb_peaks.setObjectName("cb_peaks")
        self.cb_peaks.setChecked(False)

        self.gridLayout_6.addWidget(self.cb_peaks, 0, 3, 1, 1)

        self.cb_normalize = QCheckBox(self.view_options_box)
        self.cb_normalize.setObjectName("cb_normalize")

        self.gridLayout_6.addWidget(self.cb_normalize, 1, 3, 1, 1)

        self.verticalLayout_13.addWidget(self.view_options_box)

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
        sizePolicy3.setHeightForWidth(self.rbtn_linear.sizePolicy().hasHeightForWidth())
        self.rbtn_linear.setSizePolicy(sizePolicy3)
        self.rbtn_linear.setChecked(True)

        self.horizontalLayout_37.addWidget(self.rbtn_linear)

        self.rbtn_polynomial = QRadioButton(self.baseline)
        self.rbtn_polynomial.setObjectName("rbtn_polynomial")
        sizePolicy3.setHeightForWidth(self.rbtn_polynomial.sizePolicy().hasHeightForWidth())
        self.rbtn_polynomial.setSizePolicy(sizePolicy3)

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
        sizePolicy3.setHeightForWidth(self.cb_attached.sizePolicy().hasHeightForWidth())
        self.cb_attached.setSizePolicy(sizePolicy3)
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

        

        

        

       

        

        self.save_model = QPushButton(
            self,
            text="Save Model",
            icon=QIcon(str(icons / "save.png")),
            toolTip="Save the fit model as a JSON file",
            objectName="save_model",
        )
        self.horizontalLayout_83.addWidget(self.save_model)
        self.fit_model_builder.addItem(self.horizontalLayout_83)


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
        self.btn_view_df_2.setIcon(icon16)
        self.btn_view_df_2.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_view_df_2)

        self.btn_save_fit_results = QPushButton(self.groupBox_3)
        self.btn_save_fit_results.setObjectName("btn_save_fit_results")
        self.btn_save_fit_results.setMinimumSize(QSize(30, 0))
        self.btn_save_fit_results.setMaximumSize(QSize(30, 16777215))
        self.btn_save_fit_results.setIcon(icon17)
        self.btn_save_fit_results.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_save_fit_results)

        self.btn_open_fit_results = QPushButton(self.groupBox_3)
        self.btn_open_fit_results.setObjectName("btn_open_fit_results")
        sizePolicy3.setHeightForWidth(self.btn_open_fit_results.sizePolicy().hasHeightForWidth())
        self.btn_open_fit_results.setSizePolicy(sizePolicy3)
        self.btn_open_fit_results.setMaximumSize(QSize(30, 16777215))
        self.btn_open_fit_results.setIcon(icon18)
        self.btn_open_fit_results.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_open_fit_results)

        self.verticalLayout_37.addWidget(self.groupBox_3)

        self.horizontalLayout_62.addLayout(self.verticalLayout_37)

        self.verticalLayout_32.addLayout(self.horizontalLayout_62)

        self.tabWidget_2.addTab(self.collect_fit_data, "")
        self.fit_settings = QWidget()
        self.fit_settings.setObjectName("fit_settings")
        self.fit_settings.setEnabled(True)
        self.groupBox_8 = QGroupBox(self.fit_settings)
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_8.setGeometry(QRect(780, 30, 376, 110))
        self.verticalLayout_28 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.horizontalLayout_61 = QHBoxLayout()
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")
        self.radioButton_3 = QRadioButton(self.groupBox_8)
        self.radioButton_3.setObjectName("radioButton_3")
        sizePolicy3.setHeightForWidth(self.radioButton_3.sizePolicy().hasHeightForWidth())
        self.radioButton_3.setSizePolicy(sizePolicy3)
        self.radioButton_3.setChecked(True)

        self.horizontalLayout_61.addWidget(self.radioButton_3)

        self.label_45 = QLabel(self.groupBox_8)
        self.label_45.setObjectName("label_45")

        self.horizontalLayout_61.addWidget(self.label_45)

        self.horizontalLayout_60 = QHBoxLayout()
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")
        self.radioButton_2 = QRadioButton(self.groupBox_8)
        self.radioButton_2.setObjectName("radioButton_2")
        sizePolicy3.setHeightForWidth(self.radioButton_2.sizePolicy().hasHeightForWidth())
        self.radioButton_2.setSizePolicy(sizePolicy3)

        self.horizontalLayout_60.addWidget(self.radioButton_2)

        self.label_44 = QLabel(self.groupBox_8)
        self.label_44.setObjectName("label_44")

        self.horizontalLayout_60.addWidget(self.label_44)

        self.lineEdit_32 = QLineEdit(self.groupBox_8)
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.lineEdit_32.setMinimumSize(QSize(20, 0))

        self.horizontalLayout_60.addWidget(self.lineEdit_32)

        self.horizontalLayout_61.addLayout(self.horizontalLayout_60)

        self.verticalLayout_28.addLayout(self.horizontalLayout_61)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_28.addItem(self.verticalSpacer_11)

        self.horizontalLayout_64 = QHBoxLayout()
        self.horizontalLayout_64.setObjectName("horizontalLayout_64")
        self.label_47 = QLabel(self.groupBox_8)
        self.label_47.setObjectName("label_47")

        self.horizontalLayout_64.addWidget(self.label_47)

        self.comboBox_14 = QComboBox(self.groupBox_8)
        self.comboBox_14.setObjectName("comboBox_14")

        self.horizontalLayout_64.addWidget(self.comboBox_14)

        self.lineEdit_34 = QLineEdit(self.groupBox_8)
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.lineEdit_34.setMinimumSize(QSize(20, 0))

        self.horizontalLayout_64.addWidget(self.lineEdit_34)

        self.verticalLayout_28.addLayout(self.horizontalLayout_64)

        self.layoutWidget = QWidget(self.fit_settings)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 50, 411, 220))
        self.verticalLayout_29 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_55 = QHBoxLayout()
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.label_23 = QLabel(self.layoutWidget)
        self.label_23.setObjectName("label_23")

        self.horizontalLayout_55.addWidget(self.label_23)

        self.cb_fit_negative = QCheckBox(self.layoutWidget)
        self.cb_fit_negative.setObjectName("cb_fit_negative")

        self.horizontalLayout_55.addWidget(self.cb_fit_negative)

        self.verticalLayout_29.addLayout(self.horizontalLayout_55)

        self.horizontalLayout_59 = QHBoxLayout()
        self.horizontalLayout_59.setObjectName("horizontalLayout_59")
        self.label_25 = QLabel(self.layoutWidget)
        self.label_25.setObjectName("label_25")

        self.horizontalLayout_59.addWidget(self.label_25)

        self.max_iteration = QSpinBox(self.layoutWidget)
        self.max_iteration.setObjectName("max_iteration")
        self.max_iteration.setMaximum(10000)
        self.max_iteration.setValue(200)

        self.horizontalLayout_59.addWidget(self.max_iteration)

        self.verticalLayout_29.addLayout(self.horizontalLayout_59)

        self.horizontalLayout_63 = QHBoxLayout()
        self.horizontalLayout_63.setObjectName("horizontalLayout_63")
        self.label_27 = QLabel(self.layoutWidget)
        self.label_27.setObjectName("label_27")

        self.horizontalLayout_63.addWidget(self.label_27)

        self.cbb_fit_methods = QComboBox(self.layoutWidget)
        self.cbb_fit_methods.setObjectName("cbb_fit_methods")

        self.horizontalLayout_63.addWidget(self.cbb_fit_methods)

        self.verticalLayout_29.addLayout(self.horizontalLayout_63)

        self.horizontalLayout_68 = QHBoxLayout()
        self.horizontalLayout_68.setObjectName("horizontalLayout_68")
        self.label_55 = QLabel(self.layoutWidget)
        self.label_55.setObjectName("label_55")

        self.horizontalLayout_68.addWidget(self.label_55)

        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_68.addItem(self.horizontalSpacer_41)

        self.xtol = QLineEdit(self.layoutWidget)
        self.xtol.setObjectName("xtol")
        self.xtol.setMaximumSize(QSize(60, 16777215))
        self.xtol.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_68.addWidget(self.xtol)

        self.verticalLayout_29.addLayout(self.horizontalLayout_68)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_29.addItem(self.verticalSpacer_14)

        self.label_53 = QLabel(self.fit_settings)
        self.label_53.setObjectName("label_53")
        self.label_53.setGeometry(QRect(10, 10, 121, 31))
        self.label_53.setFont(font1)
        self.layoutWidget1 = QWidget(self.fit_settings)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 320, 715, 33))
        self.horizontalLayout_45 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.btn_default_folder_model = QPushButton(self.layoutWidget1)
        self.btn_default_folder_model.setObjectName("btn_default_folder_model")

        self.horizontalLayout_45.addWidget(self.btn_default_folder_model)

        self.horizontalSpacer_40 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_40)

        self.l_defaut_folder_model = QLineEdit(self.layoutWidget1)
        self.l_defaut_folder_model.setObjectName("l_defaut_folder_model")
        self.l_defaut_folder_model.setMinimumSize(QSize(500, 0))
        self.l_defaut_folder_model.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_45.addWidget(self.l_defaut_folder_model)

        self.btn_refresh_model_folder = QPushButton(self.layoutWidget1)
        self.btn_refresh_model_folder.setObjectName("btn_refresh_model_folder")

        self.horizontalLayout_45.addWidget(self.btn_refresh_model_folder)

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

        self.btn_remove_wafer = QPushButton(self.groupBox)
        self.btn_remove_wafer.setObjectName("btn_remove_wafer")
        self.btn_remove_wafer.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_29.addWidget(self.btn_remove_wafer)

        self.btn_view_wafer = QPushButton(self.groupBox)
        self.btn_view_wafer.setObjectName("btn_view_wafer")
        self.btn_view_wafer.setMaximumSize(QSize(70, 16777215))
        self.btn_view_wafer.setIcon(icon16)
        self.btn_view_wafer.setIconSize(QSize(22, 22))

        self.horizontalLayout_29.addWidget(self.btn_view_wafer)

        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setMaximumSize(QSize(70, 16777215))
        self.pushButton_3.setIcon(icon17)
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
        sizePolicy3.setHeightForWidth(self.btn_init.sizePolicy().hasHeightForWidth())
        self.btn_init.setSizePolicy(sizePolicy3)
        self.btn_init.setMinimumSize(QSize(70, 0))
        self.btn_init.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_8.addWidget(self.btn_init)

        self.btn_show_stats = QPushButton(self.groupBox_2)
        self.btn_show_stats.setObjectName("btn_show_stats")
        sizePolicy3.setHeightForWidth(self.btn_show_stats.sizePolicy().hasHeightForWidth())
        self.btn_show_stats.setSizePolicy(sizePolicy3)
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
        self.view_options_box_2.setTitle("View options:")
        self.cb_residual_3.setText("residual")
        self.cb_filled_3.setText("filled")
        self.cb_bestfit_3.setText("best-fit")
        self.cb_legend_3.setToolTip("To display or remove the legend of the plot")
        self.cb_legend_3.setText("legend")
        self.cb_raw_3.setText("raw")
        self.cb_colors_3.setText("colors")
        self.cb_peaks_3.setText("peaks")
        self.cb_normalize_3.setText("normalized")
        self.label_22.setText("X-axis unit:")
        self.groupBox_5.setTitle("")
        self.label_66.setText("X max/min:")
        self.label_67.setText("/")
        self.range_apply_2.setToolTip("Extract the spectral windows range.\n"
" Hold 'Ctrl' and press 'Extract' button to apply to all spectra")
        self.range_apply_2.setText("Extract")
        self.label_68.setText("")
        self.baseline_2.setTitle("")
        self.rbtn_linear_2.setText("Linear")
        self.rbtn_polynomial_2.setText("Poly")
        self.label_70.setToolTip("Number of nearby points considered to smoothing the noise")
        self.label_70.setText("Smoothing")
        self.cb_attached_3.setText("Attached")
        self.btn_undo_baseline_2.setToolTip("To remove all baseline points and undo the baseline subtraction")
        self.btn_undo_baseline_2.setText("Undo baseline")
        self.sub_baseline_2.setToolTip("To subtract the evaluated baseline from the spectrum. \n"
" Hold 'Ctrl' and press 'Subtract' button to apply to all spectra")
        self.sub_baseline_2.setText("Subtract")
        self.label_71.setText("")
        self.peaks_2.setTitle("")
        self.label_73.setText("Peak model:")
        self.clear_peaks_2.setToolTip("Clear all the current peak models. \n"
" Hold 'Ctrl' and press 'Clear peaks' button to apply to all spectra")
        self.clear_peaks_2.setText("Clear peaks")
        self.label_83.setText("Add new column(s) from file name:")
        self.btn_split_fname.setToolTip("Split the file name of spectrum to several parts")
        self.btn_split_fname.setText("Split")
        self.cbb_split_fname.setToolTip("Select file name part")
        self.cbb_split_fname.setPlaceholderText("")
        self.ent_col_name.setPlaceholderText("type column name")
        self.btn_add_col.setToolTip("Add a new column containing the selected part")
        self.btn_add_col.setText("Add")
        self.groupBox_6.setTitle("")
        self.btn_view_df_5.setToolTip("View collected fit results")
        self.btn_view_df_5.setText("")
        self.btn_save_fit_results_3.setToolTip("Save all fit results in an Excel file")
        self.btn_save_fit_results_3.setText("")
        self.btn_open_fit_results_3.setToolTip("Open fit results (format Excel) to view/plot")
        self.btn_open_fit_results_3.setText("")
        self.label_74.setText("Fit settings:")
        self.label_51.setText("Fit negative values:")
        self.cb_fit_negative_2.setText("")
        self.label_75.setText("Maximumn iterations :")
        self.max_iteration_2.setPrefix("")
        self.label_76.setText("Fit method")
        self.label_78.setText("x-tolerence")
        self.xtol_2.setText("0.0001")
        self.btn_refresh_model_folder_3.setText("refresh")
        self.rdbtn_baseline.setText("baseline")
        self.rdbtn_peak.setText("peaks")
        self.rsquared_1.setText("R2=0 ")
        self.label_63.setText("DPI:")
        self.view_options_box.setTitle("View options:")
        self.cb_residual.setText("residual")
        self.cb_filled.setText("filled")
        self.cb_bestfit.setText("best-fit")
        self.cb_legend.setToolTip("To display or remove the legend of the plot")
        self.cb_legend.setText("legend")
        self.cb_raw.setText("raw")
        self.cb_colors.setText("colors")
        self.cb_peaks.setText("peaks")
        self.cb_normalize.setText("normalized")
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
        self.groupBox_8.setTitle("Peak position correction :")
        self.radioButton_3.setText("")
        self.label_45.setText("No")
        self.radioButton_2.setText("")
        self.label_44.setText("Peak  shift (cm-1) :")
        self.lineEdit_32.setToolTip("Type the different between experimental and theoretical values")
        self.label_47.setText("Reference peak :")
        self.lineEdit_34.setToolTip("Type the theoretical values")
        self.label_23.setText("Fit negative values:")
        self.cb_fit_negative.setText("")
        self.label_25.setText("Maximumn iterations :")
        self.max_iteration.setPrefix("")
        self.label_27.setText("Fit method")
        self.label_55.setText("x-tolerence")
        self.xtol.setText("0.0001")
        self.label_53.setText("Fit settings:")
        self.btn_default_folder_model.setText("Model Folder")
        self.btn_refresh_model_folder.setText("refresh")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.fit_settings), "More settings")
        self.groupBox.setTitle("")
        self.label_64.setText("Maps:")
        self.btn_remove_wafer.setText("")
        self.btn_view_wafer.setText("")
        self.pushButton_3.setText("")
        self.groupBox_2.setTitle("")
        self.btn_init.setToolTip("Reinitialize to RAW spectrum (Hold Ctrl to reinit all spectra)")
        self.btn_init.setText("Reinitialize")
        self.btn_show_stats.setToolTip("Show fitting statistique results")
        self.btn_show_stats.setText("Stats")
        self.item_count_label.setText("0 points")