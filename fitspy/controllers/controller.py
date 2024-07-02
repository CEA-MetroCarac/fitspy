import toml
from views.view import View
from models.model import Model
from .settings_controller import SettingsController
from .plot_controller import PlotController

class Controller:
    def __init__(self):
        config = toml.load("fitspy/config.toml")

        self.view = View(config)
        self.model = Model()

        self.plot_controller = PlotController(self.view.plot_view, config)
        self.settings_controller = SettingsController(self.view.settings_view)

        self.plot_controller.setup_actions(self.settings_controller)
        self.settings_controller.setup_actions(self.plot_controller)

        self.setup_actions()

    def setup_actions(self):
        self.view.actOpenFiles.triggered.connect(self.settings_controller.load_files)
        self.view.actOpenFolder.triggered.connect(self.settings_controller.load_folder)
        self.view.actExit.triggered.connect(self.view.close)
        self.view.togglePlotFit.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('main_line'))
        self.view.togglePlotNegValues.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('negative_values'))
        self.view.togglePlotOutliers.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('outliers'))
        self.view.togglePlotOutliersLimit.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('outliers_limit'))
        self.view.togglePlotNoiseLevel.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('noise_level'))
        self.view.togglePlotBaseline.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('baseline'))
        self.view.togglePlotBackground.stateChanged.connect(lambda: self.plot_controller.toggle_element_visibility('background'))
        # self.view.togglePlotResidual.stateChanged.connect(self.model.toggle_plot_residuals)
        # self.view.toggleShowPeaksLabels.stateChanged.connect(self.model.toggle_show_peaks_labels)
        # self.view.residualCoeff.textChanged.connect(self.model.update_residual_coeff)
        self.view.settings_view.show_all.clicked.connect(self.settings_controller.select_all_files)
        self.settings_controller.selectionChanged.connect(self.update_fig)

    def update_fig(self, files):
        num_files = len(files)
        self.view.statusBar().showMessage(f"{num_files} spectra loaded")
        self.plot_controller.update_fig(files)