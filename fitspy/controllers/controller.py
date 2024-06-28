from views.view import View
from models.model import Model
from .settings_controller import SettingsController
from .plot_controller import PlotController

class Controller:
    def __init__(self):
        self.view = View()
        self.model = Model()
        self.plot_controller = PlotController(self.view.plot_view)
        self.settings_controller = SettingsController(self.view.settings_view, self.plot_controller)
        self.setup_actions()

    def setup_actions(self):
        self.view.actOpenFiles.triggered.connect(self.settings_controller.load_files)
        self.view.actOpenFolder.triggered.connect(self.settings_controller.load_folder)
        self.view.actExit.triggered.connect(self.view.close)
        self.view.togglePlotFit.stateChanged.connect(self.model.toggle_plot_fit)
        self.view.togglePlotNegValues.stateChanged.connect(self.model.toggle_plot_neg_values)
        self.view.togglePlotOutliers.stateChanged.connect(self.model.toggle_plot_outliers)
        self.view.togglePlotOutliersLimit.stateChanged.connect(self.model.toggle_plot_outliers_limits)
        self.view.togglePlotNoiseLevel.stateChanged.connect(self.model.toggle_plot_noise_level)
        self.view.togglePlotBaseline.stateChanged.connect(self.model.toggle_plot_baseline)
        self.view.togglePlotBackground.stateChanged.connect(self.model.toggle_plot_background)
        self.view.togglePlotResidual.stateChanged.connect(self.model.toggle_plot_residuals)
        self.view.toggleShowPeaksLabels.stateChanged.connect(self.model.toggle_show_peaks_labels)
        self.view.residualCoeff.textChanged.connect(self.model.update_residual_coeff)
        self.view.settings_view.show_all.clicked.connect(self.settings_controller.select_all_files)
        self.settings_controller.selectionChanged.connect(self.plot_controller.update_fig)