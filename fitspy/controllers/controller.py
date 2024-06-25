from views.view import View
from models.model import Model
from .settings_controller import SettingsController

class Controller:
    def __init__(self):
        # super().__init__()
        # self.resize(800, 600)
        # self.setWindowTitle("Fitspy")
        # self.view = View()
        
        # self.model = Model()
        # self.setCentralWidget(self.view)

        self.view = View()
        self.model = Model()

        self.settings_controller = SettingsController(self.view.settings_view)
        self.setupActions()

        # statusBar = self.statusBar()
        # statusBar.showMessage(self.windowTitle())   # Définition du message initial

    def setupActions(self):
        self.view.actNew.triggered.connect(self.newDocument)
        # self.view.actExit.triggered.connect(self.close)
        self.view.togglePlotFit.stateChanged.connect(self.model.toggle_plot_fit)
        self.view.togglePlotNegValues.stateChanged.connect(self.model.toggle_plot_neg_values)
        self.view.togglePlotOutliers.stateChanged.connect(self.model.toggle_plot_outliers)
        self.view.togglePlotOutliersLimit.stateChanged.connect(self.model.toggle_plot_outliers_limits)
        self.view.togglePlotNoiseLevel.stateChanged.connect(self.model.toggle_plot_noise_level)
        self.view.togglePlotBaseline.stateChanged.connect(self.model.toggle_plot_baseline)
        self.view.togglePlotBackground.stateChanged.connect(self.model.toggle_plot_background)
        self.view.togglePlotResidual.stateChanged.connect(self.model.toggle_plot_residuals)
        self.view.toggleShowPeaksLabels.stateChanged.connect(self.model.toggle_show_peaks_labels)
        self.view.title.textChanged.connect(self.model.update_title)
        self.view.residualCoeff.textChanged.connect(self.model.update_residual_coeff)
        self.view.xLabel.textChanged.connect(self.model.update_x_label)
        self.view.yLabel.textChanged.connect(self.model.update_y_label)


    def newDocument(self):
        print("New document is requested")