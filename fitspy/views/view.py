from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QDockWidget, QWidget, QWidgetAction, QCheckBox, QHBoxLayout
from .settings_view import SettingsView
from .plot_view import PlotView

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(1000, 500)
        self.setWindowTitle("Fitspy")
        statusBar = self.statusBar()
        # statusBar.showMessage(self.windowTitle())

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.createActions()
        self.createMenuBar()

        self.plot_area = PlotView()
        layout.addWidget(self.plot_area)

        self.main_settings_dock = QDockWidget("Main Settings", self)
        self.settings_view = SettingsView()
        self.main_settings_dock.setWidget(self.settings_view)
        self.main_settings_dock.setFloating(False)

        self.setCentralWidget(central_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.main_settings_dock)

    def createActions(self):
        self.actNew = QAction(QIcon("icons/new.png"), "&New NOT IMPLEMENTED", self)
        self.actNew.setShortcut("Ctrl+N")
        self.actNew.setStatusTip("New document")

        self.actOpenFiles = QAction(QIcon("icons/open.png"), "&Open File(s)", self)
        self.actOpenFiles.setStatusTip("Open file(s)")

        self.actOpenFolder = QAction(QIcon("icons/open.png"), "&Open Folder", self)
        self.actOpenFolder.setShortcut("Ctrl+O")
        self.actOpenFolder.setStatusTip("Open folder")

        self.actSave = QAction(QIcon("icons/save.png"), "&Save NOT IMPLEMENTED", self)
        self.actSave.setShortcut("Ctrl+S")
        self.actSave.setStatusTip("Save File")

        self.actExit = QAction(QIcon("icons/exit.png"), "Exit", self)
        self.actExit.setShortcut("Alt+F4")
        self.actExit.setStatusTip("Exit")

        self.actToggleFigureSettings = QAction("Plot Fit", self, checkable=True)
        self.actToggleFigureSettings.setStatusTip("Toggle Plot Fit")
        # self.actToggleFigureSettings.triggered.connect(self.toggle_figure_settings)

    def createMenuBar(self):
        menuBar = self.menuBar()

        self.file = menuBar.addMenu("&File")
        self.file.addAction(self.actNew)
        self.file.addSeparator()
        self.file.addAction(self.actOpenFiles)
        self.file.addAction(self.actOpenFolder)
        self.file.addAction(self.actSave)
        self.file.addSeparator()
        self.file.addAction(self.actExit)

        self.figure_menu = menuBar.addMenu("&Figure Settings")
        # TODO Factor out the creation of QWidgetActions

        # Create a QWidgetAction with a QCheckBox for "Plot Fit"
        figureSettingsAction1 = QWidgetAction(self)
        self.togglePlotFit = QCheckBox("Plot Fit", self)
        self.togglePlotFit.setChecked(True)  # Initial state
        figureSettingsAction1.setStatusTip("Toggle Plot Fit")
        figureSettingsAction1.setDefaultWidget(self.togglePlotFit)
        self.figure_menu.addAction(figureSettingsAction1)

        # Create a QWidgetAction with a QCheckBox for "Plot Negative Values"
        figureSettingsAction2 = QWidgetAction(self)
        self.togglePlotNegValues = QCheckBox("Plot Negative Values", self)
        self.togglePlotNegValues.setChecked(True)  # Initial state
        figureSettingsAction2.setStatusTip("Toggle Plot Negative Values")
        figureSettingsAction2.setDefaultWidget(self.togglePlotNegValues)
        self.figure_menu.addAction(figureSettingsAction2)

        # Create a QWidgetAction with a QCheckBox for "Plot Outliers"
        figureSettingsAction3 = QWidgetAction(self)
        self.togglePlotOutliers = QCheckBox("Plot Outliers", self)
        self.togglePlotOutliers.setChecked(True)  # Initial state
        figureSettingsAction3.setStatusTip("Toggle Plot Outliers")
        figureSettingsAction3.setDefaultWidget(self.togglePlotOutliers)
        self.figure_menu.addAction(figureSettingsAction3)

        # Create a QWidgetAction with a QCheckBox for "Plot Outliers Limit"
        figureSettingsAction4 = QWidgetAction(self)
        self.togglePlotOutliersLimit = QCheckBox("Plot Outliers Limit", self)
        self.togglePlotOutliersLimit.setChecked(True)
        figureSettingsAction4.setStatusTip("Toggle Plot Outliers Limit")
        figureSettingsAction4.setDefaultWidget(self.togglePlotOutliersLimit)
        self.figure_menu.addAction(figureSettingsAction4)

        # Create a QWidgetAction with a QCheckBox for "Plot Noise Level"
        figureSettingsAction5 = QWidgetAction(self)    
        self.togglePlotNoiseLevel = QCheckBox("Plot Noise Level", self)
        self.togglePlotNoiseLevel.setChecked(True)
        figureSettingsAction5.setStatusTip("Toggle Plot Noise Level")
        figureSettingsAction5.setDefaultWidget(self.togglePlotNoiseLevel)
        self.figure_menu.addAction(figureSettingsAction5)

        # Create a QWidgetAction with a QCheckBox for "Plot Baseline"
        figureSettingsAction6 = QWidgetAction(self)
        self.togglePlotBaseline = QCheckBox("Plot Baseline", self)
        self.togglePlotBaseline.setChecked(True)
        figureSettingsAction6.setStatusTip("Toggle Plot Baseline")
        figureSettingsAction6.setDefaultWidget(self.togglePlotBaseline)
        self.figure_menu.addAction(figureSettingsAction6)

        # Create a QWidgetAction with a QCheckBox for "Plot Background"
        figureSettingsAction7 = QWidgetAction(self)
        self.togglePlotBackground = QCheckBox("Plot Background", self)
        self.togglePlotBackground.setChecked(True)
        figureSettingsAction7.setStatusTip("Toggle Plot Background")
        figureSettingsAction7.setDefaultWidget(self.togglePlotBackground)
        self.figure_menu.addAction(figureSettingsAction7)

        # Create a QWidgetAction with a QCheckBox for "Plot Residual"
        figureSettingsAction8 = QWidgetAction(self)
        self.togglePlotResidual = QCheckBox("Plot Residual", self)
        self.togglePlotResidual.setChecked(True)
        figureSettingsAction8.setStatusTip("Toggle Plot Residual")
        figureSettingsAction8.setDefaultWidget(self.togglePlotResidual)
        self.figure_menu.addAction(figureSettingsAction8)

        # Create a QWidgetAction with a QCheckBox for "Show Peaks Labels"
        figureSettingsAction9 = QWidgetAction(self)
        self.toggleShowPeaksLabels = QCheckBox("Show Peaks Labels", self)
        self.toggleShowPeaksLabels.setChecked(True)
        figureSettingsAction9.setStatusTip("Toggle Show Peaks Labels")
        figureSettingsAction9.setDefaultWidget(self.toggleShowPeaksLabels)
        self.figure_menu.addAction(figureSettingsAction9)

        # Create a float input for coef residual
        figureSettingsAction10 = QWidgetAction(self)
        label = QLabel("Residual coef:")
        self.residualCoeff = QLineEdit(self)
        self.residualCoeff.setText("1")
        self.residualCoeff.setFixedWidth(30)  # Set a fixed width

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 2)
        layout.addWidget(label)
        layout.addWidget(self.residualCoeff)

        widget = QWidget()
        widget.setLayout(layout)
        figureSettingsAction10.setDefaultWidget(widget)
        self.figure_menu.addAction(figureSettingsAction10)
        # figureSettingsAction9 = QWidgetAction(self)
        # self.coefResidual = QDoubleSpinBox(self)
        # self.coefResidual.setRange(0, 1)
        # self.coefResidual.setSingleStep(0.1)
        # self.coefResidual.setValue(0.5)
        # self.coefResidual.setToolTip("Coefficient for residual")
        # figureSettingsAction9.setDefaultWidget(self.coefResidual)
        # self.figure_menu.addAction(figureSettingsAction9)