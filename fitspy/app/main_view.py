from pathlib import Path
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import (QMainWindow, QAbstractItemView, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit, QListWidget,
    QProgressBar, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QToolBar, QVBoxLayout, QWidget)


project_root = Path(__file__).resolve().parent.parent.parent
icons = project_root / 'fitspy' / 'resources' / 'iconpack'


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        if not self.objectName():
            self.setObjectName("MainWindow")
        self.resize(1553, 1019)
        self.actionOpen_dataframe_Excel = QAction(self)
        self.actionOpen_dataframe_Excel.setObjectName("actionOpen_dataframe_Excel")
        self.actionOpen_dataframe_CSV = QAction(self)
        self.actionOpen_dataframe_CSV.setObjectName("actionOpen_dataframe_CSV")
        self.actionOpen_saved_work_s = QAction(self)
        self.actionOpen_saved_work_s.setObjectName("actionOpen_saved_work_s")
        self.actionOpen_a_recipie = QAction(self)
        self.actionOpen_a_recipie.setObjectName("actionOpen_a_recipie")
        self.actionSave_all_graph_PNG = QAction(self)
        self.actionSave_all_graph_PNG.setObjectName("actionSave_all_graph_PNG")
        self.actionSave_all_graphs_to_pptx = QAction(self)
        self.actionSave_all_graphs_to_pptx.setObjectName("actionSave_all_graphs_to_pptx")
        self.open_df = QAction(self)
        self.open_df.setObjectName("open_df")
        
        self.actionManual = QAction(QIcon(str(icons / 'manual.png')), "Manual", self)
        self.actionManual.setObjectName("actionManual")
 
        self.actionDarkMode = QAction(QIcon(str(icons / 'dark.png')), "Dark Mode", self)
        self.actionDarkMode.setObjectName("actionDarkMode")

        self.actionLightMode = QAction(QIcon(str(icons / 'light-mode.svg')), "Light Mode", self)
        self.actionLightMode.setObjectName("actionLightMode")
        self.actionLightMode.setCheckable(False)
        self.actionLightMode.setChecked(False)

        self.actionAbout = QAction(QIcon(str(icons / 'about.png')), "About", self)
        self.actionAbout.setObjectName("actionAbout")

        self.actionOpen_wafer = QAction(self)
        self.actionOpen_wafer.setObjectName("actionOpen_wafer")
        self.action_reload = QAction(self)
        self.action_reload.setObjectName("action_reload")
        icon4 = QIcon()
        icon4.addFile(":/icon/iconpack/icons8-documents-folder-96.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_reload.setIcon(icon4)
        self.actionOpen_spectra = QAction(self)
        self.actionOpen_spectra.setObjectName("actionOpen_spectra")
        self.actionOpen_dfs = QAction(self)
        self.actionOpen_dfs.setObjectName("actionOpen_dfs")
        icon5 = QIcon()
        icon5.addFile(":/icon/iconpack/view.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_dfs.setIcon(icon5)
        self.actionOpen = QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        icon6 = QIcon()
        icon6.addFile(":/icon/iconpack/icons8-folder-96.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon6)
        self.actionOpen_2 = QAction(self)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionOpen_2.setIcon(icon6)
        self.actionSave = QAction(self)
        self.actionSave.setObjectName("actionSave")
        icon7 = QIcon()
        icon7.addFile(":/icon/iconpack/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon7)
        self.actionClear_WS = QAction(self)
        self.actionClear_WS.setObjectName("actionClear_WS")
        self.actionThem = QAction(self)
        self.actionThem.setObjectName("actionThem")
        icon8 = QIcon()
        icon8.addFile(":/icon/iconpack/dark-light.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionThem.setIcon(icon8)
        self.actionClear_env = QAction(self)
        self.actionClear_env.setObjectName("actionClear_env")
        icon9 = QIcon()
        icon9.addFile(":/icon/iconpack/clear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClear_env.setIcon(icon9)
        self.actionLogo = QAction(self)
        self.actionLogo.setObjectName("actionLogo")
        icon10 = QIcon()
        icon10.addFile(":/icon/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLogo.setIcon(icon10)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setBaseSize(QSize(0, 0))
        self.verticalLayout_15 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(5, 5, 5, 5)
        
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(1200, 900))
        self.tabWidget.setMaximumSize(QSize(2560, 1440))
        # self.plot_area = QMdiArea(self.centralwidget)
        
        self.tab_spectra = QWidget()
        self.tab_spectra.setObjectName("tab_spectra")
        self.horizontalLayout_131 = QHBoxLayout(self.tab_spectra)
        self.horizontalLayout_131.setObjectName("horizontalLayout_131")
        self.horizontalLayout_131.setContentsMargins(5, 5, 5, 5)
        self.splitter_3 = QSplitter(self.tab_spectra)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Vertical)
        self.splitter_3.setHandleWidth(10)
        self.upper_frame_3 = QFrame(self.splitter_3)
        self.upper_frame_3.setObjectName("upper_frame_3")
        self.horizontalLayout_105 = QHBoxLayout(self.upper_frame_3)
        self.horizontalLayout_105.setObjectName("horizontalLayout_105")
        self.horizontalLayout_105.setContentsMargins(3, 0, 3, 3)
        self.Upper_zone_3 = QHBoxLayout()
        self.Upper_zone_3.setSpacing(0)
        self.Upper_zone_3.setObjectName("Upper_zone_3")
        self.verticalLayout_62 = QVBoxLayout()
        self.verticalLayout_62.setObjectName("verticalLayout_62")
        self.verticalLayout_62.setContentsMargins(0, -1, 10, -1)
        self.spectre_view_frame_3 = QFrame(self.upper_frame_3)
        self.spectre_view_frame_3.setObjectName("spectre_view_frame_3")
        self.spectre_view_frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.spectre_view_frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_63 = QVBoxLayout(self.spectre_view_frame_3)
        self.verticalLayout_63.setObjectName("verticalLayout_63")
        self.verticalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.QVBoxlayout_2 = QVBoxLayout()
        self.QVBoxlayout_2.setSpacing(6)
        self.QVBoxlayout_2.setObjectName("QVBoxlayout_2")

        self.verticalLayout_63.addLayout(self.QVBoxlayout_2)


        self.verticalLayout_62.addWidget(self.spectre_view_frame_3)

        self.bottom_frame_3 = QHBoxLayout()
        self.bottom_frame_3.setSpacing(10)
        self.bottom_frame_3.setObjectName("bottom_frame_3")
        self.bottom_frame_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.bottom_frame_3.setContentsMargins(2, 2, 2, 2)
        self.toolbar_frame_3 = QHBoxLayout()
        self.toolbar_frame_3.setObjectName("toolbar_frame_3")

        self.bottom_frame_3.addLayout(self.toolbar_frame_3)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_24)

        self.rdbtn_baseline_2 = QRadioButton(self.upper_frame_3)
        self.rdbtn_baseline_2.setObjectName("rdbtn_baseline_2")
        self.rdbtn_baseline_2.setChecked(True)

        self.bottom_frame_3.addWidget(self.rdbtn_baseline_2)

        self.rdbtn_peak_2 = QRadioButton(self.upper_frame_3)
        self.rdbtn_peak_2.setObjectName("rdbtn_peak_2")
        self.rdbtn_peak_2.setChecked(False)

        self.bottom_frame_3.addWidget(self.rdbtn_peak_2)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_16)

        self.rsquared_2 = QLabel(self.upper_frame_3)
        self.rsquared_2.setObjectName("rsquared_2")

        self.bottom_frame_3.addWidget(self.rsquared_2)

        self.btn_copy_fig_3 = QPushButton(self.upper_frame_3)
        self.btn_copy_fig_3.setObjectName("btn_copy_fig_3")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_copy_fig_3.sizePolicy().hasHeightForWidth())
        self.btn_copy_fig_3.setSizePolicy(sizePolicy)
        self.btn_copy_fig_3.setMinimumSize(QSize(0, 0))
        self.btn_copy_fig_3.setMaximumSize(QSize(16777215, 16777215))
        icon11 = QIcon()
        icon11.addFile(":/icon/iconpack/copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_copy_fig_3.setIcon(icon11)
        self.btn_copy_fig_3.setIconSize(QSize(24, 24))

        self.bottom_frame_3.addWidget(self.btn_copy_fig_3)

        self.label_79 = QLabel(self.upper_frame_3)
        self.label_79.setObjectName("label_79")

        self.bottom_frame_3.addWidget(self.label_79)

        self.sb_dpi_spectra_2 = QSpinBox(self.upper_frame_3)
        self.sb_dpi_spectra_2.setObjectName("sb_dpi_spectra_2")
        self.sb_dpi_spectra_2.setMinimum(100)
        self.sb_dpi_spectra_2.setMaximum(200)
        self.sb_dpi_spectra_2.setSingleStep(10)

        self.bottom_frame_3.addWidget(self.sb_dpi_spectra_2)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.bottom_frame_3.addItem(self.horizontalSpacer_25)

        self.bottom_frame_3.setStretch(0, 50)
        self.bottom_frame_3.setStretch(1, 25)
        self.bottom_frame_3.setStretch(9, 2)

        self.verticalLayout_62.addLayout(self.bottom_frame_3)

        self.verticalLayout_62.setStretch(0, 75)
        self.verticalLayout_62.setStretch(1, 25)

        self.Upper_zone_3.addLayout(self.verticalLayout_62)

        self.widget_9 = QWidget(self.upper_frame_3)
        self.widget_9.setObjectName("widget_9")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy1)
        self.widget_9.setMinimumSize(QSize(300, 0))
        self.verticalLayout_64 = QVBoxLayout(self.widget_9)
        self.verticalLayout_64.setObjectName("verticalLayout_64")
        self.verticalLayout_64.setContentsMargins(2, 0, 2, 0)
        self.scrollArea_7 = QScrollArea(self.widget_9)
        self.scrollArea_7.setObjectName("scrollArea_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.scrollArea_7.sizePolicy().hasHeightForWidth())
        self.scrollArea_7.setSizePolicy(sizePolicy2)
        self.scrollArea_7.setMinimumSize(QSize(250, 450))
        self.scrollArea_7.setMaximumSize(QSize(350, 16777215))
        self.scrollArea_7.setWidgetResizable(True)
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

        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)

        self.verticalLayout_64.addWidget(self.scrollArea_7)


        self.Upper_zone_3.addWidget(self.widget_9)

        self.Upper_zone_3.setStretch(0, 75)

        self.horizontalLayout_105.addLayout(self.Upper_zone_3)

        self.splitter_3.addWidget(self.upper_frame_3)
        self.bottom_widget_4 = QWidget(self.splitter_3)
        self.bottom_widget_4.setObjectName("bottom_widget_4")
        self.verticalLayout_66 = QVBoxLayout(self.bottom_widget_4)
        self.verticalLayout_66.setObjectName("verticalLayout_66")
        self.verticalLayout_66.setContentsMargins(3, 3, 3, 0)
        self.tabWidget_3 = QTabWidget(self.bottom_widget_4)
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tabWidget_3.setEnabled(True)
        self.fit_model_editor_3 = QWidget()
        self.fit_model_editor_3.setObjectName("fit_model_editor_3")
        self.fit_model_editor_3.setEnabled(True)
        self.verticalLayout_46 = QVBoxLayout(self.fit_model_editor_3)
        self.verticalLayout_46.setSpacing(6)
        self.verticalLayout_46.setObjectName("verticalLayout_46")
        self.verticalLayout_46.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_72 = QHBoxLayout()
        self.horizontalLayout_72.setSpacing(5)
        self.horizontalLayout_72.setObjectName("horizontalLayout_72")
        self.horizontalLayout_72.setContentsMargins(-1, 5, 5, 5)
        self.widget_18 = QWidget(self.fit_model_editor_3)
        self.widget_18.setObjectName("widget_18")
        self.horizontalLayout_73 = QHBoxLayout(self.widget_18)
        self.horizontalLayout_73.setSpacing(6)
        self.horizontalLayout_73.setObjectName("horizontalLayout_73")
        self.horizontalLayout_73.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_4 = QScrollArea(self.widget_18)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollArea_4.setMinimumSize(QSize(430, 100))
        self.scrollArea_4.setMaximumSize(QSize(430, 16777215))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 428, 375))
        self.verticalLayout_39 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_39.setSpacing(10)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.btn_cosmis_ray_3 = QPushButton(self.scrollAreaWidgetContents_4)
        self.btn_cosmis_ray_3.setObjectName("btn_cosmis_ray_3")
        self.btn_cosmis_ray_3.setMinimumSize(QSize(80, 0))
        self.btn_cosmis_ray_3.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_17.addWidget(self.btn_cosmis_ray_3)

        self.horizontalSpacer_57 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_57)

        self.label_22 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_22.setObjectName("label_22")

        self.horizontalLayout_17.addWidget(self.label_22)

        self.cbb_xaxis_unit = QComboBox(self.scrollAreaWidgetContents_4)
        self.cbb_xaxis_unit.setObjectName("cbb_xaxis_unit")

        self.horizontalLayout_17.addWidget(self.cbb_xaxis_unit)


        self.verticalLayout_39.addLayout(self.horizontalLayout_17)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_40 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_40.setSpacing(5)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(2, 2, 2, 2)
        self.label_65 = QLabel(self.groupBox_5)
        self.label_65.setObjectName("label_65")
        font = QFont()
        font.setBold(True)
        self.label_65.setFont(font)

        self.verticalLayout_40.addWidget(self.label_65)

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


        self.verticalLayout_39.addWidget(self.groupBox_5)

        self.label_68 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_68.setObjectName("label_68")

        self.verticalLayout_39.addWidget(self.label_68)

        self.baseline_2 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.baseline_2.setObjectName("baseline_2")
        self.verticalLayout_41 = QVBoxLayout(self.baseline_2)
        self.verticalLayout_41.setSpacing(5)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(2, 2, 2, 2)
        self.label_69 = QLabel(self.baseline_2)
        self.label_69.setObjectName("label_69")
        self.label_69.setFont(font)

        self.verticalLayout_41.addWidget(self.label_69)

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


        self.verticalLayout_39.addWidget(self.baseline_2)

        self.label_71 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_71.setObjectName("label_71")

        self.verticalLayout_39.addWidget(self.label_71)

        self.peaks_2 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.peaks_2.setObjectName("peaks_2")
        self.verticalLayout_42 = QVBoxLayout(self.peaks_2)
        self.verticalLayout_42.setSpacing(5)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(2, 2, 2, 2)
        self.label_72 = QLabel(self.peaks_2)
        self.label_72.setObjectName("label_72")
        self.label_72.setFont(font)

        self.verticalLayout_42.addWidget(self.label_72)

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


        self.verticalLayout_39.addWidget(self.peaks_2)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_39.addItem(self.verticalSpacer_15)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.horizontalLayout_73.addWidget(self.scrollArea_4)

        self.verticalLayout_43 = QVBoxLayout()
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.peak_table_2 = QGroupBox(self.widget_18)
        self.peak_table_2.setObjectName("peak_table_2")
        self.horizontalLayout_78 = QHBoxLayout(self.peak_table_2)
        self.horizontalLayout_78.setObjectName("horizontalLayout_78")
        self.scrollArea_6 = QScrollArea(self.peak_table_2)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollArea_6.setWidgetResizable(True)
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

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)

        self.horizontalLayout_78.addWidget(self.scrollArea_6)


        self.verticalLayout_43.addWidget(self.peak_table_2)

        self.horizontalLayout_81 = QHBoxLayout()
        self.horizontalLayout_81.setSpacing(5)
        self.horizontalLayout_81.setObjectName("horizontalLayout_81")
        self.btn_fit_3 = QPushButton(self.widget_18)
        self.btn_fit_3.setObjectName("btn_fit_3")
        self.btn_fit_3.setMinimumSize(QSize(50, 50))
        self.btn_fit_3.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_81.addWidget(self.btn_fit_3)

        self.verticalLayout_45 = QVBoxLayout()
        self.verticalLayout_45.setObjectName("verticalLayout_45")
        self.horizontalLayout_82 = QHBoxLayout()
        self.horizontalLayout_82.setSpacing(5)
        self.horizontalLayout_82.setObjectName("horizontalLayout_82")
        self.horizontalLayout_82.setContentsMargins(5, 2, 5, 2)
        self.btn_copy_fit_model_2 = QPushButton(self.widget_18)
        self.btn_copy_fit_model_2.setObjectName("btn_copy_fit_model_2")
        icon12 = QIcon()
        icon12.addFile(":/icon/iconpack/copy10.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_copy_fit_model_2.setIcon(icon12)

        self.horizontalLayout_82.addWidget(self.btn_copy_fit_model_2)

        self.lbl_copied_fit_model_2 = QLabel(self.widget_18)
        self.lbl_copied_fit_model_2.setObjectName("lbl_copied_fit_model_2")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lbl_copied_fit_model_2.sizePolicy().hasHeightForWidth())
        self.lbl_copied_fit_model_2.setSizePolicy(sizePolicy4)
        self.lbl_copied_fit_model_2.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_82.addWidget(self.lbl_copied_fit_model_2)

        self.btn_paste_fit_model_2 = QPushButton(self.widget_18)
        self.btn_paste_fit_model_2.setObjectName("btn_paste_fit_model_2")
        self.btn_paste_fit_model_2.setMinimumSize(QSize(0, 0))
        self.btn_paste_fit_model_2.setMaximumSize(QSize(16777215, 40))
        icon13 = QIcon()
        icon13.addFile(":/icon/iconpack/copy_label.png.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_paste_fit_model_2.setIcon(icon13)

        self.horizontalLayout_82.addWidget(self.btn_paste_fit_model_2)

        self.horizontalSpacer_51 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_82.addItem(self.horizontalSpacer_51)

        self.save_model_2 = QPushButton(self.widget_18)
        self.save_model_2.setObjectName("save_model_2")
        icon14 = QIcon()
        icon14.addFile(":/icon/iconpack/save11.png", QSize(), QIcon.Normal, QIcon.Off)
        self.save_model_2.setIcon(icon14)

        self.horizontalLayout_82.addWidget(self.save_model_2)

        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_82.addItem(self.horizontalSpacer_39)

        self.cb_limits_2 = QCheckBox(self.widget_18)
        self.cb_limits_2.setObjectName("cb_limits_2")

        self.horizontalLayout_82.addWidget(self.cb_limits_2)

        self.cb_expr_2 = QCheckBox(self.widget_18)
        self.cb_expr_2.setObjectName("cb_expr_2")

        self.horizontalLayout_82.addWidget(self.cb_expr_2)


        self.verticalLayout_45.addLayout(self.horizontalLayout_82)

        self.cbb_fit_model_list_3 = QComboBox(self.widget_18)
        self.cbb_fit_model_list_3.setObjectName("cbb_fit_model_list_3")
        self.cbb_fit_model_list_3.setMinimumSize(QSize(400, 0))
        self.cbb_fit_model_list_3.setMaximumSize(QSize(400, 16777215))


        self.btn_apply_model_3 = QPushButton(self.widget_18)
        self.btn_apply_model_3.setObjectName("btn_apply_model_3")


        self.horizontalSpacer_42 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.btn_load_model_3 = QPushButton(self.widget_18)
        self.btn_load_model_3.setObjectName("btn_load_model_3")

        self.horizontalLayout_81.addLayout(self.verticalLayout_45)


        self.verticalLayout_43.addLayout(self.horizontalLayout_81)

        self.verticalLayout_43.setStretch(0, 85)
        self.verticalLayout_43.setStretch(1, 15)

        self.horizontalLayout_73.addLayout(self.verticalLayout_43)

        self.horizontalLayout_73.setStretch(0, 50)
        self.horizontalLayout_73.setStretch(1, 50)

        self.horizontalLayout_72.addWidget(self.widget_18)


        self.verticalLayout_46.addLayout(self.horizontalLayout_72)

        self.tabWidget_3.addTab(self.fit_model_editor_3, "")
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
        self.scrollArea_11 = QScrollArea(self.collect_fit_data_2)
        self.scrollArea_11.setObjectName("scrollArea_11")
        sizePolicy2.setHeightForWidth(self.scrollArea_11.sizePolicy().hasHeightForWidth())
        self.scrollArea_11.setSizePolicy(sizePolicy2)
        self.scrollArea_11.setMinimumSize(QSize(430, 100))
        self.scrollArea_11.setMaximumSize(QSize(430, 16777215))
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName("scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 322, 144))
        self.verticalLayout_81 = QVBoxLayout(self.scrollAreaWidgetContents_11)
        self.verticalLayout_81.setSpacing(10)
        self.verticalLayout_81.setObjectName("verticalLayout_81")
        self.verticalLayout_81.setContentsMargins(10, 10, 10, 10)
        self.btn_collect_results_3 = QPushButton(self.scrollAreaWidgetContents_11)
        self.btn_collect_results_3.setObjectName("btn_collect_results_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.btn_collect_results_3.sizePolicy().hasHeightForWidth())
        self.btn_collect_results_3.setSizePolicy(sizePolicy5)
        self.btn_collect_results_3.setMinimumSize(QSize(140, 40))
        self.btn_collect_results_3.setMaximumSize(QSize(140, 40))
        self.btn_collect_results_3.setFont(font)
        icon15 = QIcon()
        icon15.addFile(":/icon/iconpack/collect.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_collect_results_3.setIcon(icon15)
        self.btn_collect_results_3.setIconSize(QSize(16, 22))

        self.verticalLayout_81.addWidget(self.btn_collect_results_3)

        self.label_83 = QLabel(self.scrollAreaWidgetContents_11)
        self.label_83.setObjectName("label_83")

        self.verticalLayout_81.addWidget(self.label_83)

        self.horizontalLayout_95 = QHBoxLayout()
        self.horizontalLayout_95.setObjectName("horizontalLayout_95")
        self.btn_split_fname = QPushButton(self.scrollAreaWidgetContents_11)
        self.btn_split_fname.setObjectName("btn_split_fname")
        sizePolicy5.setHeightForWidth(self.btn_split_fname.sizePolicy().hasHeightForWidth())
        self.btn_split_fname.setSizePolicy(sizePolicy5)
        self.btn_split_fname.setMinimumSize(QSize(40, 0))
        self.btn_split_fname.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_95.addWidget(self.btn_split_fname)

        self.cbb_split_fname = QComboBox(self.scrollAreaWidgetContents_11)
        self.cbb_split_fname.setObjectName("cbb_split_fname")
        sizePolicy5.setHeightForWidth(self.cbb_split_fname.sizePolicy().hasHeightForWidth())
        self.cbb_split_fname.setSizePolicy(sizePolicy5)
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

        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_11)

        self.horizontalLayout_94.addWidget(self.scrollArea_11)

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
        sizePolicy5.setHeightForWidth(self.btn_view_df_5.sizePolicy().hasHeightForWidth())
        self.btn_view_df_5.setSizePolicy(sizePolicy5)
        self.btn_view_df_5.setMinimumSize(QSize(30, 0))
        self.btn_view_df_5.setMaximumSize(QSize(30, 16777215))
        icon16 = QIcon()
        icon16.addFile(":/icon/iconpack/view11.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_view_df_5.setIcon(icon16)
        self.btn_view_df_5.setIconSize(QSize(22, 22))

        self.horizontalLayout_98.addWidget(self.btn_view_df_5)

        self.btn_save_fit_results_3 = QPushButton(self.groupBox_6)
        self.btn_save_fit_results_3.setObjectName("btn_save_fit_results_3")
        sizePolicy5.setHeightForWidth(self.btn_save_fit_results_3.sizePolicy().hasHeightForWidth())
        self.btn_save_fit_results_3.setSizePolicy(sizePolicy5)
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

        self.tabWidget_3.addTab(self.collect_fit_data_2, "")
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

        self.horizontalLayout_86 = QHBoxLayout()
        self.horizontalLayout_86.setObjectName("horizontalLayout_86")
        self.label_77 = QLabel(self.layoutWidget_2)
        self.label_77.setObjectName("label_77")

        self.horizontalLayout_86.addWidget(self.label_77)

        self.cbb_cpu_number_2 = QComboBox(self.layoutWidget_2)
        self.cbb_cpu_number_2.setObjectName("cbb_cpu_number_2")

        self.horizontalLayout_86.addWidget(self.cbb_cpu_number_2)


        self.verticalLayout_48.addLayout(self.horizontalLayout_86)

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

        self.btn_open_fitspy_3 = QPushButton(self.layoutWidget_2)
        self.btn_open_fitspy_3.setObjectName("btn_open_fitspy_3")
        self.btn_open_fitspy_3.setMinimumSize(QSize(0, 30))
        self.btn_open_fitspy_3.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout_48.addWidget(self.btn_open_fitspy_3)

        self.l_defaut_folder_model_3 = QLineEdit(self.fit_settings_3)
        self.l_defaut_folder_model_3.setObjectName("l_defaut_folder_model_3")
        self.l_defaut_folder_model_3.setGeometry(QRect(160, 320, 481, 21))
        self.btn_default_folder_model_3 = QPushButton(self.fit_settings_3)
        self.btn_default_folder_model_3.setObjectName("btn_default_folder_model_3")
        self.btn_default_folder_model_3.setGeometry(QRect(20, 320, 121, 21))
        self.btn_refresh_model_folder_3 = QPushButton(self.fit_settings_3)
        self.btn_refresh_model_folder_3.setObjectName("btn_refresh_model_folder_3")
        self.btn_refresh_model_folder_3.setGeometry(QRect(650, 320, 75, 23))
        self.tabWidget_3.addTab(self.fit_settings_3, "")

        self.verticalLayout_66.addWidget(self.tabWidget_3)

        self.splitter_3.addWidget(self.bottom_widget_4)

        self.horizontalLayout_131.addWidget(self.splitter_3)


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


        self.tab_maps = QWidget()
        self.tab_maps.setObjectName("tab_maps")
        self.gridLayout_5 = QGridLayout(self.tab_maps)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(5, 5, 5, 5)
        self.splitter = QSplitter(self.tab_maps)
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

        self.btn_copy_fig = QPushButton(self.upper_frame)
        self.btn_copy_fig.setObjectName("btn_copy_fig")
        self.btn_copy_fig.setIcon(icon11)
        self.btn_copy_fig.setIconSize(QSize(24, 24))

        self.bottom_frame.addWidget(self.btn_copy_fig)

        self.label_63 = QLabel(self.upper_frame)
        self.label_63.setObjectName("label_63")
        sizePolicy4.setHeightForWidth(self.label_63.sizePolicy().hasHeightForWidth())
        self.label_63.setSizePolicy(sizePolicy4)
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
        sizePolicy1.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy1)
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
        sizePolicy5.setHeightForWidth(self.measurement_sites.sizePolicy().hasHeightForWidth())
        self.measurement_sites.setSizePolicy(sizePolicy5)
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
        self.fit_model_editor = QWidget()
        self.fit_model_editor.setObjectName("fit_model_editor")
        self.fit_model_editor.setEnabled(True)
        self.verticalLayout_14 = QVBoxLayout(self.fit_model_editor)
        self.verticalLayout_14.setSpacing(6)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(-1, 5, 5, 5)
        self.widget_17 = QWidget(self.fit_model_editor)
        self.widget_17.setObjectName("widget_17")
        self.horizontalLayout_44 = QHBoxLayout(self.widget_17)
        self.horizontalLayout_44.setSpacing(6)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_3 = QScrollArea(self.widget_17)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollArea_3.setMinimumSize(QSize(430, 100))
        self.scrollArea_3.setMaximumSize(QSize(430, 16777215))
        self.scrollArea_3.setWidgetResizable(True)
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

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.horizontalLayout_44.addWidget(self.scrollArea_3)

        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.peak_table = QGroupBox(self.widget_17)
        self.peak_table.setObjectName("peak_table")
        self.horizontalLayout_26 = QHBoxLayout(self.peak_table)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.scrollArea_5 = QScrollArea(self.peak_table)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 731, 246))
        self.verticalLayout_35 = QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.verticalLayout_311 = QVBoxLayout()
        self.verticalLayout_311.setObjectName("verticalLayout_311")
        self.horizontalLayout_53 = QHBoxLayout()
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.peak_table1 = QHBoxLayout()
        self.peak_table1.setObjectName("peak_table1")

        self.horizontalLayout_53.addLayout(self.peak_table1)

        self.horizontalLayout_54 = QHBoxLayout()
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")

        self.horizontalLayout_53.addLayout(self.horizontalLayout_54)


        self.verticalLayout_311.addLayout(self.horizontalLayout_53)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_311.addItem(self.verticalSpacer_6)


        self.verticalLayout_35.addLayout(self.verticalLayout_311)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)

        self.horizontalLayout_26.addWidget(self.scrollArea_5)


        self.verticalLayout_33.addWidget(self.peak_table)

        self.horizontalLayout_70 = QHBoxLayout()
        self.horizontalLayout_70.setObjectName("horizontalLayout_70")
        self.btn_fit = QPushButton(self.widget_17)
        self.btn_fit.setObjectName("btn_fit")
        self.btn_fit.setMinimumSize(QSize(50, 50))
        self.btn_fit.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_70.addWidget(self.btn_fit)

        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.horizontalLayout_51 = QHBoxLayout()
        self.horizontalLayout_51.setSpacing(5)
        self.horizontalLayout_51.setObjectName("horizontalLayout_51")
        self.horizontalLayout_51.setContentsMargins(5, 2, 5, 2)
        self.btn_copy_fit_model = QPushButton(self.widget_17)
        self.btn_copy_fit_model.setObjectName("btn_copy_fit_model")
        self.btn_copy_fit_model.setIcon(icon12)

        self.horizontalLayout_51.addWidget(self.btn_copy_fit_model)

        self.lbl_copied_fit_model = QLabel(self.widget_17)
        self.lbl_copied_fit_model.setObjectName("lbl_copied_fit_model")
        sizePolicy4.setHeightForWidth(self.lbl_copied_fit_model.sizePolicy().hasHeightForWidth())
        self.lbl_copied_fit_model.setSizePolicy(sizePolicy4)
        self.lbl_copied_fit_model.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_51.addWidget(self.lbl_copied_fit_model)

        self.btn_paste_fit_model = QPushButton(self.widget_17)
        self.btn_paste_fit_model.setObjectName("btn_paste_fit_model")
        self.btn_paste_fit_model.setMinimumSize(QSize(0, 0))
        self.btn_paste_fit_model.setMaximumSize(QSize(16777215, 40))
        self.btn_paste_fit_model.setIcon(icon13)

        self.horizontalLayout_51.addWidget(self.btn_paste_fit_model)

        self.horizontalSpacer_50 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_50)

        self.save_model = QPushButton(self.widget_17)
        self.save_model.setObjectName("save_model")
        self.save_model.setIcon(icon14)

        self.horizontalLayout_51.addWidget(self.save_model)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_51.addItem(self.horizontalSpacer_17)

        self.cb_limits = QCheckBox(self.widget_17)
        self.cb_limits.setObjectName("cb_limits")

        self.horizontalLayout_51.addWidget(self.cb_limits)

        self.cb_expr = QCheckBox(self.widget_17)
        self.cb_expr.setObjectName("cb_expr")

        self.horizontalLayout_51.addWidget(self.cb_expr)


        self.verticalLayout_22.addLayout(self.horizontalLayout_51)

        self.horizontalLayout_52 = QHBoxLayout()
        self.horizontalLayout_52.setSpacing(5)
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(5, 2, 5, 2)
        self.label_80 = QLabel(self.widget_17)
        self.label_80.setObjectName("label_80")

        self.horizontalLayout_52.addWidget(self.label_80)

        self.cbb_fit_model_list = QComboBox(self.widget_17)
        self.cbb_fit_model_list.setObjectName("cbb_fit_model_list")
        self.cbb_fit_model_list.setMinimumSize(QSize(400, 0))
        self.cbb_fit_model_list.setMaximumSize(QSize(400, 16777215))

        self.horizontalLayout_52.addWidget(self.cbb_fit_model_list)

        self.btn_apply_model = QPushButton(self.widget_17)
        self.btn_apply_model.setObjectName("btn_apply_model")
        sizePolicy3.setHeightForWidth(self.btn_apply_model.sizePolicy().hasHeightForWidth())
        self.btn_apply_model.setSizePolicy(sizePolicy3)
        self.btn_apply_model.setMinimumSize(QSize(0, 0))
        self.btn_apply_model.setMaximumSize(QSize(85, 32))

        self.horizontalLayout_52.addWidget(self.btn_apply_model)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_52.addItem(self.horizontalSpacer_6)

        self.btn_load_model = QPushButton(self.widget_17)
        self.btn_load_model.setObjectName("btn_load_model")
        self.btn_load_model.setMaximumSize(QSize(85, 16777215))

        self.horizontalLayout_52.addWidget(self.btn_load_model)


        self.verticalLayout_22.addLayout(self.horizontalLayout_52)


        self.horizontalLayout_70.addLayout(self.verticalLayout_22)


        self.verticalLayout_33.addLayout(self.horizontalLayout_70)

        self.verticalLayout_33.setStretch(0, 85)
        self.verticalLayout_33.setStretch(1, 15)

        self.horizontalLayout_44.addLayout(self.verticalLayout_33)

        self.horizontalLayout_44.setStretch(1, 60)

        self.horizontalLayout_9.addWidget(self.widget_17)


        self.verticalLayout_14.addLayout(self.horizontalLayout_9)

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
        sizePolicy2.setHeightForWidth(self.scrollArea_9.sizePolicy().hasHeightForWidth())
        self.scrollArea_9.setSizePolicy(sizePolicy2)
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
        sizePolicy5.setHeightForWidth(self.btn_collect_results.sizePolicy().hasHeightForWidth())
        self.btn_collect_results.setSizePolicy(sizePolicy5)
        self.btn_collect_results.setMinimumSize(QSize(140, 40))
        self.btn_collect_results.setMaximumSize(QSize(140, 40))
        self.btn_collect_results.setFont(font)
        self.btn_collect_results.setIcon(icon15)
        self.btn_collect_results.setIconSize(QSize(16, 22))

        self.verticalLayout_80.addWidget(self.btn_collect_results)

        self.label_56 = QLabel(self.scrollAreaWidgetContents_9)
        self.label_56.setObjectName("label_56")

        self.verticalLayout_80.addWidget(self.label_56)

        self.horizontalLayout_49 = QHBoxLayout()
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.btn_split_fname_2 = QPushButton(self.scrollAreaWidgetContents_9)
        self.btn_split_fname_2.setObjectName("btn_split_fname_2")
        sizePolicy5.setHeightForWidth(self.btn_split_fname_2.sizePolicy().hasHeightForWidth())
        self.btn_split_fname_2.setSizePolicy(sizePolicy5)
        self.btn_split_fname_2.setMinimumSize(QSize(40, 0))
        self.btn_split_fname_2.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_49.addWidget(self.btn_split_fname_2)

        self.cbb_split_fname_2 = QComboBox(self.scrollAreaWidgetContents_9)
        self.cbb_split_fname_2.setObjectName("cbb_split_fname_2")
        sizePolicy5.setHeightForWidth(self.cbb_split_fname_2.sizePolicy().hasHeightForWidth())
        self.cbb_split_fname_2.setSizePolicy(sizePolicy5)
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
        sizePolicy5.setHeightForWidth(self.btn_view_df_2.sizePolicy().hasHeightForWidth())
        self.btn_view_df_2.setSizePolicy(sizePolicy5)
        self.btn_view_df_2.setMinimumSize(QSize(30, 0))
        self.btn_view_df_2.setMaximumSize(QSize(30, 16777215))
        self.btn_view_df_2.setIcon(icon16)
        self.btn_view_df_2.setIconSize(QSize(22, 22))

        self.horizontalLayout_36.addWidget(self.btn_view_df_2)

        self.btn_save_fit_results = QPushButton(self.groupBox_3)
        self.btn_save_fit_results.setObjectName("btn_save_fit_results")
        sizePolicy5.setHeightForWidth(self.btn_save_fit_results.sizePolicy().hasHeightForWidth())
        self.btn_save_fit_results.setSizePolicy(sizePolicy5)
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
        sizePolicy5.setHeightForWidth(self.lineEdit_32.sizePolicy().hasHeightForWidth())
        self.lineEdit_32.setSizePolicy(sizePolicy5)
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
        sizePolicy5.setHeightForWidth(self.lineEdit_34.sizePolicy().hasHeightForWidth())
        self.lineEdit_34.setSizePolicy(sizePolicy5)
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

        self.horizontalLayout_67 = QHBoxLayout()
        self.horizontalLayout_67.setObjectName("horizontalLayout_67")
        self.label_26 = QLabel(self.layoutWidget)
        self.label_26.setObjectName("label_26")

        self.horizontalLayout_67.addWidget(self.label_26)

        self.cbb_cpu_number = QComboBox(self.layoutWidget)
        self.cbb_cpu_number.setObjectName("cbb_cpu_number")

        self.horizontalLayout_67.addWidget(self.cbb_cpu_number)


        self.verticalLayout_29.addLayout(self.horizontalLayout_67)

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

        self.btn_open_fitspy = QPushButton(self.layoutWidget)
        self.btn_open_fitspy.setObjectName("btn_open_fitspy")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.btn_open_fitspy.sizePolicy().hasHeightForWidth())
        self.btn_open_fitspy.setSizePolicy(sizePolicy7)
        self.btn_open_fitspy.setMinimumSize(QSize(100, 30))
        self.btn_open_fitspy.setMaximumSize(QSize(100, 30))

        self.verticalLayout_29.addWidget(self.btn_open_fitspy)

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

        self.sidebar = QFrame(self.tab_maps)
        self.sidebar.setObjectName("sidebar")
        sizePolicy1.setHeightForWidth(self.sidebar.sizePolicy().hasHeightForWidth())
        self.sidebar.setSizePolicy(sizePolicy1)
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
        sizePolicy5.setHeightForWidth(self.maps_listbox.sizePolicy().hasHeightForWidth())
        self.maps_listbox.setSizePolicy(sizePolicy5)
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
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
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

        self.tabWidget.addTab(self.tab_maps, "")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")

        self.tab_plot_settings = QWidget()
        self.tab_plot_settings.setObjectName("tab_plot_settings")
        self.verticalLayout = QVBoxLayout(self.tab_plot_settings)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.scrollArea = QScrollArea(self.tab_plot_settings)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 372, 490))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_115 = QHBoxLayout()
        self.horizontalLayout_115.setObjectName("horizontalLayout_115")
        self.label_96 = QLabel(self.scrollAreaWidgetContents)
        self.label_96.setObjectName("label_96")
        self.label_96.setMinimumSize(QSize(80, 0))
        self.label_96.setMaximumSize(QSize(80, 16777215))
        self.label_96.setFont(font)

        self.horizontalLayout_115.addWidget(self.label_96)

        self.cbb_plotstyle = QComboBox(self.scrollAreaWidgetContents)
        self.cbb_plotstyle.setObjectName("cbb_plotstyle")

        self.horizontalLayout_115.addWidget(self.cbb_plotstyle)

        self.label_93 = QLabel(self.scrollAreaWidgetContents)
        self.label_93.setObjectName("label_93")

        self.horizontalLayout_115.addWidget(self.label_93)

        self.cbb_palette = QComboBox(self.scrollAreaWidgetContents)
        self.cbb_palette.setObjectName("cbb_palette")

        self.horizontalLayout_115.addWidget(self.cbb_palette)


        self.verticalLayout_3.addLayout(self.horizontalLayout_115)

        self.horizontalLayout_71 = QHBoxLayout()
        self.horizontalLayout_71.setObjectName("horizontalLayout_71")
        self.label_82 = QLabel(self.scrollAreaWidgetContents)
        self.label_82.setObjectName("label_82")
        self.label_82.setMinimumSize(QSize(30, 0))
        self.label_82.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_71.addWidget(self.label_82)

        self.cbb_x_2 = QComboBox(self.scrollAreaWidgetContents)
        self.cbb_x_2.setObjectName("cbb_x_2")

        self.horizontalLayout_71.addWidget(self.cbb_x_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_71)

        self.horizontalLayout_88 = QHBoxLayout()
        self.horizontalLayout_88.setObjectName("horizontalLayout_88")
        self.label_84 = QLabel(self.scrollAreaWidgetContents)
        self.label_84.setObjectName("label_84")
        self.label_84.setMinimumSize(QSize(30, 0))
        self.label_84.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_88.addWidget(self.label_84)

        self.cbb_y_2 = QComboBox(self.scrollAreaWidgetContents)
        self.cbb_y_2.setObjectName("cbb_y_2")

        self.horizontalLayout_88.addWidget(self.cbb_y_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_88)

        self.horizontalLayout_89 = QHBoxLayout()
        self.horizontalLayout_89.setObjectName("horizontalLayout_89")
        self.label_85 = QLabel(self.scrollAreaWidgetContents)
        self.label_85.setObjectName("label_85")
        self.label_85.setMinimumSize(QSize(30, 0))
        self.label_85.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_89.addWidget(self.label_85)

        self.cbb_z_2 = QComboBox(self.scrollAreaWidgetContents)
        self.cbb_z_2.setObjectName("cbb_z_2")

        self.horizontalLayout_89.addWidget(self.cbb_z_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_89)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_107 = QHBoxLayout()
        self.horizontalLayout_107.setObjectName("horizontalLayout_107")
        self.label_91 = QLabel(self.scrollAreaWidgetContents)
        self.label_91.setObjectName("label_91")
        self.label_91.setFont(font)

        self.horizontalLayout_107.addWidget(self.label_91)

        self.lbl_plot_title = QLineEdit(self.scrollAreaWidgetContents)
        self.lbl_plot_title.setObjectName("lbl_plot_title")

        self.horizontalLayout_107.addWidget(self.lbl_plot_title)


        self.verticalLayout_3.addLayout(self.horizontalLayout_107)

        self.horizontalLayout_91 = QHBoxLayout()
        self.horizontalLayout_91.setObjectName("horizontalLayout_91")
        self.label_86 = QLabel(self.scrollAreaWidgetContents)
        self.label_86.setObjectName("label_86")

        self.horizontalLayout_91.addWidget(self.label_86)

        self.lbl_xlabel = QLineEdit(self.scrollAreaWidgetContents)
        self.lbl_xlabel.setObjectName("lbl_xlabel")

        self.horizontalLayout_91.addWidget(self.lbl_xlabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_91)

        self.horizontalLayout_92 = QHBoxLayout()
        self.horizontalLayout_92.setObjectName("horizontalLayout_92")
        self.label_87 = QLabel(self.scrollAreaWidgetContents)
        self.label_87.setObjectName("label_87")

        self.horizontalLayout_92.addWidget(self.label_87)

        self.lbl_ylabel = QLineEdit(self.scrollAreaWidgetContents)
        self.lbl_ylabel.setObjectName("lbl_ylabel")

        self.horizontalLayout_92.addWidget(self.lbl_ylabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_92)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_97 = QLabel(self.scrollAreaWidgetContents)
        self.label_97.setObjectName("label_97")
        self.label_97.setFont(font)

        self.horizontalLayout_19.addWidget(self.label_97)

        self.btn_get_limits = QPushButton(self.scrollAreaWidgetContents)
        self.btn_get_limits.setObjectName("btn_get_limits")

        self.horizontalLayout_19.addWidget(self.btn_get_limits)

        self.btn_clear_limits = QPushButton(self.scrollAreaWidgetContents)
        self.btn_clear_limits.setObjectName("btn_clear_limits")

        self.horizontalLayout_19.addWidget(self.btn_clear_limits)


        self.verticalLayout_3.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_102 = QHBoxLayout()
        self.horizontalLayout_102.setObjectName("horizontalLayout_102")
        self.label_89 = QLabel(self.scrollAreaWidgetContents)
        self.label_89.setObjectName("label_89")

        self.horizontalLayout_102.addWidget(self.label_89)

        self.xmin_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.xmin_2.setObjectName("xmin_2")

        self.horizontalLayout_102.addWidget(self.xmin_2)

        self.xmax_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.xmax_2.setObjectName("xmax_2")

        self.horizontalLayout_102.addWidget(self.xmax_2)

        self.label_90 = QLabel(self.scrollAreaWidgetContents)
        self.label_90.setObjectName("label_90")

        self.horizontalLayout_102.addWidget(self.label_90)

        self.ymin_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.ymin_2.setObjectName("ymin_2")

        self.horizontalLayout_102.addWidget(self.ymin_2)

        self.ymax_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.ymax_2.setObjectName("ymax_2")

        self.horizontalLayout_102.addWidget(self.ymax_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_102)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.horizontalLayout_93 = QHBoxLayout()
        self.horizontalLayout_93.setObjectName("horizontalLayout_93")
        self.label_88 = QLabel(self.scrollAreaWidgetContents)
        self.label_88.setObjectName("label_88")

        self.horizontalLayout_93.addWidget(self.label_88)

        self.lbl_zlabel = QLineEdit(self.scrollAreaWidgetContents)
        self.lbl_zlabel.setObjectName("lbl_zlabel")

        self.horizontalLayout_93.addWidget(self.lbl_zlabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_93)

        self.horizontalLayout_113 = QHBoxLayout()
        self.horizontalLayout_113.setObjectName("horizontalLayout_113")
        self.label_94 = QLabel(self.scrollAreaWidgetContents)
        self.label_94.setObjectName("label_94")

        self.horizontalLayout_113.addWidget(self.label_94)

        self.zmin_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.zmin_2.setObjectName("zmin_2")

        self.horizontalLayout_113.addWidget(self.zmin_2)

        self.zmax_2 = QLineEdit(self.scrollAreaWidgetContents)
        self.zmax_2.setObjectName("zmax_2")

        self.horizontalLayout_113.addWidget(self.zmax_2)

        self.horizontalSpacer_43 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_113.addItem(self.horizontalSpacer_43)


        self.verticalLayout_3.addLayout(self.horizontalLayout_113)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName("label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_124 = QHBoxLayout()
        self.horizontalLayout_124.setObjectName("horizontalLayout_124")
        self.label_98 = QLabel(self.scrollAreaWidgetContents)
        self.label_98.setObjectName("label_98")

        self.horizontalLayout_124.addWidget(self.label_98)

        self.lbl_wafersize = QLineEdit(self.scrollAreaWidgetContents)
        self.lbl_wafersize.setObjectName("lbl_wafersize")

        self.horizontalLayout_124.addWidget(self.lbl_wafersize)


        self.verticalLayout_3.addLayout(self.horizontalLayout_124)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_8)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

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
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents_8)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.cb_legend_visible = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_legend_visible.setObjectName("cb_legend_visible")
        self.cb_legend_visible.setChecked(True)

        self.verticalLayout_11.addWidget(self.cb_legend_visible)

        self.cb_show_err_bar_plot = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_show_err_bar_plot.setObjectName("cb_show_err_bar_plot")
        self.cb_show_err_bar_plot.setChecked(True)

        self.verticalLayout_11.addWidget(self.cb_show_err_bar_plot)

        self.cb_wafer_stats = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_wafer_stats.setObjectName("cb_wafer_stats")
        self.cb_wafer_stats.setChecked(True)

        self.verticalLayout_11.addWidget(self.cb_wafer_stats)

        self.cb_join_for_point_plot = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_join_for_point_plot.setObjectName("cb_join_for_point_plot")

        self.verticalLayout_11.addWidget(self.cb_join_for_point_plot)

        self.horizontalLayout_126 = QHBoxLayout()
        self.horizontalLayout_126.setObjectName("horizontalLayout_126")
        self.cb_trendline_eq = QCheckBox(self.scrollAreaWidgetContents_8)
        self.cb_trendline_eq.setObjectName("cb_trendline_eq")
        self.cb_trendline_eq.setChecked(True)

        self.horizontalLayout_126.addWidget(self.cb_trendline_eq)

        self.spb_trendline_oder = QDoubleSpinBox(self.scrollAreaWidgetContents_8)
        self.spb_trendline_oder.setObjectName("spb_trendline_oder")
        self.spb_trendline_oder.setDecimals(0)
        self.spb_trendline_oder.setMinimum(1.000000000000000)
        self.spb_trendline_oder.setMaximum(10.000000000000000)

        self.horizontalLayout_126.addWidget(self.spb_trendline_oder)

        self.label_18 = QLabel(self.scrollAreaWidgetContents_8)
        self.label_18.setObjectName("label_18")

        self.horizontalLayout_126.addWidget(self.label_18)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_126.addItem(self.horizontalSpacer_5)


        self.verticalLayout_11.addLayout(self.horizontalLayout_126)

        self.line_3 = QFrame(self.scrollAreaWidgetContents_8)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_3)

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


        self.verticalLayout_11.addLayout(self.legends_loc)

        self.line = QFrame(self.scrollAreaWidgetContents_8)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line)

        self.label_13 = QLabel(self.scrollAreaWidgetContents_8)
        self.label_13.setObjectName("label_13")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.label_13.setFont(font2)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_13)

        self.main_layout = QHBoxLayout()
        self.main_layout.setObjectName("main_layout")

        self.verticalLayout_11.addLayout(self.main_layout)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalSpacer_48 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_48)


        self.verticalLayout_11.addLayout(self.horizontalLayout_13)

        self.line_2 = QFrame(self.scrollAreaWidgetContents_8)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_11.addItem(self.verticalSpacer_3)

        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)

        self.verticalLayout_4.addWidget(self.scrollArea_8)

        self.tab_multi_axes = QWidget()
        self.tab_multi_axes.setObjectName("tab_multi_axes")
        self.verticalLayout_8 = QVBoxLayout(self.tab_multi_axes)
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.scrollArea_10 = QScrollArea(self.tab_multi_axes)
        self.scrollArea_10.setObjectName("scrollArea_10")
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_10 = QWidget()
        self.scrollAreaWidgetContents_10.setObjectName("scrollAreaWidgetContents_10")
        self.scrollAreaWidgetContents_10.setGeometry(QRect(0, 0, 362, 329))
        self.verticalLayout_9 = QVBoxLayout(self.scrollAreaWidgetContents_10)
        self.verticalLayout_9.setSpacing(5)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.label_12 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_12.setObjectName("label_12")

        self.verticalLayout_9.addWidget(self.label_12)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label100 = QLabel(self.scrollAreaWidgetContents_10)
        self.label100.setObjectName("label100")
        self.label100.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.label100)

        self.cbb_y2_2 = QComboBox(self.scrollAreaWidgetContents_10)
        self.cbb_y2_2.setObjectName("cbb_y2_2")
        self.cbb_y2_2.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_6.addWidget(self.cbb_y2_2)

        self.btn_add_y2 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_add_y2.setObjectName("btn_add_y2")

        self.horizontalLayout_6.addWidget(self.btn_add_y2)

        self.btn_remove_y2 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_remove_y2.setObjectName("btn_remove_y2")

        self.horizontalLayout_6.addWidget(self.btn_remove_y2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.lbl_y2label = QLineEdit(self.scrollAreaWidgetContents_10)
        self.lbl_y2label.setObjectName("lbl_y2label")

        self.horizontalLayout_2.addWidget(self.lbl_y2label)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.y2min_2 = QLineEdit(self.scrollAreaWidgetContents_10)
        self.y2min_2.setObjectName("y2min_2")

        self.horizontalLayout_3.addWidget(self.y2min_2)

        self.label_6 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_6.setObjectName("label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.y2max_2 = QLineEdit(self.scrollAreaWidgetContents_10)
        self.y2max_2.setObjectName("y2max_2")

        self.horizontalLayout_3.addWidget(self.y2max_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_11 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_11.setObjectName("label_11")
        self.label_11.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.label_11)

        self.cbb_y3_2 = QComboBox(self.scrollAreaWidgetContents_10)
        self.cbb_y3_2.setObjectName("cbb_y3_2")
        self.cbb_y3_2.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_10.addWidget(self.cbb_y3_2)

        self.btn_add_y3 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_add_y3.setObjectName("btn_add_y3")

        self.horizontalLayout_10.addWidget(self.btn_add_y3)

        self.btn_remove_y3 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_remove_y3.setObjectName("btn_remove_y3")

        self.horizontalLayout_10.addWidget(self.btn_remove_y3)


        self.verticalLayout_9.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_7.setObjectName("label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.lbl_y3label = QLineEdit(self.scrollAreaWidgetContents_10)
        self.lbl_y3label.setObjectName("lbl_y3label")

        self.horizontalLayout_4.addWidget(self.lbl_y3label)


        self.verticalLayout_9.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_9.setObjectName("label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.y3min_2 = QLineEdit(self.scrollAreaWidgetContents_10)
        self.y3min_2.setObjectName("y3min_2")

        self.horizontalLayout_5.addWidget(self.y3min_2)

        self.label_8 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_8.setObjectName("label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.y3max_2 = QLineEdit(self.scrollAreaWidgetContents_10)
        self.y3max_2.setObjectName("y3max_2")

        self.horizontalLayout_5.addWidget(self.y3max_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_9.addItem(self.verticalSpacer_20)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label100_2 = QLabel(self.scrollAreaWidgetContents_10)
        self.label100_2.setObjectName("label100_2")
        self.label100_2.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_11.addWidget(self.label100_2)

        self.cbb_y12 = QComboBox(self.scrollAreaWidgetContents_10)
        self.cbb_y12.setObjectName("cbb_y12")
        self.cbb_y12.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_11.addWidget(self.cbb_y12)

        self.btn_add_y12 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_add_y12.setObjectName("btn_add_y12")

        self.horizontalLayout_11.addWidget(self.btn_add_y12)

        self.btn_remove_y12 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_remove_y12.setObjectName("btn_remove_y12")

        self.horizontalLayout_11.addWidget(self.btn_remove_y12)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_10 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_10.setObjectName("label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.lbl_y12label = QLineEdit(self.scrollAreaWidgetContents_10)
        self.lbl_y12label.setObjectName("lbl_y12label")

        self.horizontalLayout_12.addWidget(self.lbl_y12label)


        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_14 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_14.setObjectName("label_14")
        self.label_14.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_14.addWidget(self.label_14)

        self.cbb_y13 = QComboBox(self.scrollAreaWidgetContents_10)
        self.cbb_y13.setObjectName("cbb_y13")
        self.cbb_y13.setMinimumSize(QSize(160, 0))

        self.horizontalLayout_14.addWidget(self.cbb_y13)

        self.btn_add_y13 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_add_y13.setObjectName("btn_add_y13")

        self.horizontalLayout_14.addWidget(self.btn_add_y13)

        self.btn_remove_y13 = QPushButton(self.scrollAreaWidgetContents_10)
        self.btn_remove_y13.setObjectName("btn_remove_y13")

        self.horizontalLayout_14.addWidget(self.btn_remove_y13)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_15 = QLabel(self.scrollAreaWidgetContents_10)
        self.label_15.setObjectName("label_15")

        self.horizontalLayout_15.addWidget(self.label_15)

        self.lbl_y3label_2 = QLineEdit(self.scrollAreaWidgetContents_10)
        self.lbl_y3label_2.setObjectName("lbl_y3label_2")

        self.horizontalLayout_15.addWidget(self.lbl_y3label_2)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)

        self.scrollArea_10.setWidget(self.scrollAreaWidgetContents_10)

        self.verticalLayout_8.addWidget(self.scrollArea_10)

        self.verticalLayout_15.addWidget(self.tabWidget)

        self.layout_statusbar = QHBoxLayout()
        self.layout_statusbar.setObjectName("layout_statusbar")
        self.layout_statusbar.setContentsMargins(5, 5, 5, 5)
        self.label_38 = QLabel(self.centralwidget)
        self.label_38.setObjectName("label_38")

        self.layout_statusbar.addWidget(self.label_38)

        self.label_19 = QLabel(self.centralwidget)
        self.label_19.setObjectName("label_19")

        self.layout_statusbar.addWidget(self.label_19)

        self.label_21 = QLabel(self.centralwidget)
        self.label_21.setObjectName("label_21")

        self.layout_statusbar.addWidget(self.label_21)

        self.ncpus = QSpinBox(self.centralwidget)
        self.ncpus.setObjectName("ncpus")
        self.ncpus.setMinimum(1)
        self.ncpus.setMaximum(64)

        self.layout_statusbar.addWidget(self.ncpus)

        self.horizontalSpacer_58 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_statusbar.addItem(self.horizontalSpacer_58)

        self.progressText = QLabel(self.centralwidget)
        self.progressText.setObjectName("progressText")

        self.layout_statusbar.addWidget(self.progressText)

        self.label_95 = QLabel(self.centralwidget)
        self.label_95.setObjectName("label_95")

        self.layout_statusbar.addWidget(self.label_95)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName("progressBar")
        sizePolicy5.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy5)
        self.progressBar.setMinimumSize(QSize(200, 10))
        self.progressBar.setMaximumSize(QSize(200, 10))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)

        self.layout_statusbar.addWidget(self.progressBar)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName("label_24")

        self.layout_statusbar.addWidget(self.label_24)


        self.verticalLayout_15.addLayout(self.layout_statusbar)

        self.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setMinimumSize(QSize(0, 0))
        self.toolBar.setMaximumSize(QSize(16777215, 50))
        self.toolBar.setMovable(True)
        self.toolBar.setIconSize(QSize(30, 30))
        self.toolBar.setFloatable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar_2 = QToolBar(self)
        self.toolBar_2.setObjectName("toolBar_2")
        self.toolBar_2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar_2)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_env)
        self.toolBar.addSeparator()
        self.toolBar_2.addAction(self.actionAbout)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionManual)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionDarkMode)
        self.toolBar_2.addAction(self.actionLightMode)
        self.toolBar_2.addSeparator()

        self.retranslateUi()

        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)

        

    def retranslateUi(self):
        self.setWindowTitle("SPECTROview (Spectroscopic Data Processing and Visualization)")
        self.actionOpen_dataframe_Excel.setText("Open data inline (Semilab)")
        self.actionOpen_dataframe_CSV.setText("Open data inline (Labspec6)")
        self.actionOpen_saved_work_s.setText("Open saved work(s)")
        self.actionOpen_a_recipie.setText("Open a recipie")
        self.actionSave_all_graph_PNG.setText("Save all graphs (PNG)")
        self.actionSave_all_graphs_to_pptx.setText("Save all graphs to pptx")
        self.open_df.setText("Open df")
        self.actionOpen_wafer.setText("Open hyperspectra : wafer, 2Dmap (CSV, txt)")
        self.action_reload.setText("Reload saved work")
        self.actionOpen_spectra.setText("Open spectra data (txt)")
        self.actionOpen_dfs.setText("Open dataframe (Excel)")
        self.actionOpen.setText("Open")
        self.actionOpen.setToolTip("Open spectra data, saved work or Excel file")
        self.actionOpen_2.setText("Open")
        self.actionSave.setText("Save")
        self.actionSave.setToolTip("Save current work")
        self.actionClear_WS.setText("Clear WS")
        self.actionThem.setText("Theme")
        self.actionClear_env.setText("Clear env")
        self.actionLogo.setText("zer")
        self.rdbtn_baseline_2.setText("baseline")
        self.rdbtn_peak_2.setText("peaks")
        self.rsquared_2.setText("R2")
        self.btn_copy_fig_3.setToolTip("Copy Figure to clipboard")
        self.btn_copy_fig_3.setText("")
        self.label_79.setText("DPI:")
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
        self.btn_cosmis_ray_3.setToolTip("Detect cosmis ray based on the loaded spectra")
        self.btn_cosmis_ray_3.setText("Spike removal")
        self.label_22.setText("X-axis unit:")
        self.groupBox_5.setTitle("")
        self.label_65.setText("Spectral range:")
        self.label_66.setText("X max/min:")
        self.label_67.setText("/")
        self.range_apply_2.setToolTip("Extract the spectral windows range.\n"
" Hold 'Ctrl' and press 'Extract' button to apply to all spectra")
        self.range_apply_2.setText("Extract")
        self.label_68.setText("")
        self.baseline_2.setTitle("")
        self.label_69.setText("Baseline:")
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
        self.label_72.setText("Peaks:")
        self.label_73.setText("Peak model:")
        self.clear_peaks_2.setToolTip("Clear all the current peak models. \n"
" Hold 'Ctrl' and press 'Clear peaks' button to apply to all spectra")
        self.clear_peaks_2.setText("Clear peaks")
        self.peak_table_2.setTitle("Peak table: ")
        self.btn_fit_3.setToolTip("Fit selected spectrum(s) with all parameters (range, baseline, peaks). \n"
" Hold 'Ctrl' and press 'Fit' button to apply to all spectra")
        self.btn_fit_3.setText("Fit")
        self.btn_copy_fit_model_2.setToolTip("Copy current fit parameters (range, baseline, peaks) of selected spectrum to Clipboard")
        self.btn_copy_fit_model_2.setText("Copy model")
        self.lbl_copied_fit_model_2.setText("")
        self.btn_paste_fit_model_2.setToolTip("Paste the copied fit model to the selected spectrum(s).\n"
" Hold 'Ctrl' and press 'Paste' button to paste fit model to all spectra, including spectra within different wafers")
        self.btn_paste_fit_model_2.setText("Paste model")
        self.save_model_2.setToolTip("Save the fit model as a JSON file")
        self.save_model_2.setText("Save Model")
        self.cb_limits_2.setToolTip("Show limits (max, min) of each parameters")
        self.cb_limits_2.setText("Limits")
        self.cb_expr_2.setToolTip("Show the expression of fit parameters")
        self.cb_expr_2.setText("Expression")
        self.cbb_fit_model_list_3.setPlaceholderText("Select a model for fitting")
        self.btn_apply_model_3.setText("Apply model")
        self.btn_load_model_3.setToolTip("Load a fit model if it is not in the default folder")
        self.btn_load_model_3.setText("Load model")
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.fit_model_editor_3), "Fit model builder")
        self.btn_collect_results_3.setToolTip("To gather all the best fit results in a dataframe for visualization")
        self.btn_collect_results_3.setText(" Collect fit results")
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
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.collect_fit_data_2), "Collect fit data")
        self.label_74.setText("Fit settings:")
        self.label_51.setText("Fit negative values:")
        self.cb_fit_negative_2.setText("")
        self.label_75.setText("Maximumn iterations :")
        self.max_iteration_2.setPrefix("")
        self.label_76.setText("Fit method")
        self.label_77.setText("Number of CPUs")
        self.label_78.setText("x-tolerence")
        self.xtol_2.setText("0.0001")
        self.btn_open_fitspy_3.setToolTip("Open FITSPY application")
        self.btn_open_fitspy_3.setText("Open FITSPY")
        self.btn_default_folder_model_3.setText("Model Folder:")
        self.btn_refresh_model_folder_3.setText("refresh")
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.fit_settings_3), "More settings")
        self.rdbtn_baseline.setText("baseline")
        self.rdbtn_peak.setText("peaks")
        self.rsquared_1.setText("R2=0 ")
        self.btn_copy_fig.setToolTip("Copy Figure to clipboard")
        self.btn_copy_fig.setText("")
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
        self.peak_table.setTitle("Peak table: ")
        self.btn_fit.setToolTip("Fit selected spectrum(s) with all parameters (range, baseline, peaks). \n"
" Hold 'Ctrl' and press 'Fit' button to apply to all spectra")
        self.btn_fit.setText("Fit")
        self.btn_copy_fit_model.setToolTip("Copy current fit parameters (range, baseline, peaks) of selected spectrum to Clipboard")
        self.btn_copy_fit_model.setText("Copy model")
        self.lbl_copied_fit_model.setText("")
        self.btn_paste_fit_model.setToolTip("Paste the copied fit model to the selected spectrum(s).\n"
" Hold 'Ctrl' and press 'Paste' button to paste fit model to all spectra, including spectra within different wafers")
        self.btn_paste_fit_model.setText("Paste model")
        self.save_model.setToolTip("Save the fit model as a JSON file")
        self.save_model.setText("Save Model")
        self.cb_limits.setToolTip("Show limits (max, min) of each parameters")
        self.cb_limits.setText("Limits")
        self.cb_expr.setToolTip("Show the expression of fit parameters")
        self.cb_expr.setText("Expression")
        self.label_80.setText("Select a model:")
        self.cbb_fit_model_list.setToolTip("Go to 'Settings' to specify a folder where fit models are stored ")
        self.cbb_fit_model_list.setPlaceholderText("Select a model for fitting")
        self.btn_apply_model.setToolTip("Hold \"Ctrl\" and click to apply fit model to all wafer")
        self.btn_apply_model.setText("Apply model")
        self.btn_load_model.setToolTip("Load a fit model if it is not in the default folder")
        self.btn_load_model.setText("Load model")
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
        self.label_26.setText("Number of CPUs")
        self.label_55.setText("x-tolerence")
        self.xtol.setText("0.0001")
        self.btn_open_fitspy.setText("open FITSPY")
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_maps), "Maps")