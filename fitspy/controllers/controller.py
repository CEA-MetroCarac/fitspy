from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow
from views.view import View

class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Fitspy")
        self.view = View()
        # self.model = Model()
        self.setCentralWidget(self.view)

        self.setupActions()

        statusBar = self.statusBar()
        statusBar.showMessage(self.windowTitle())   # Définition du message initial

    def setupActions(self):
        self.view.actNew.triggered.connect(self.newDocument)
        # self.view.actOpen.triggered.connect(self.open_file)
        # self.view.actSave.triggered.connect(self.save_file)
        self.view.actExit.triggered.connect(self.close)
        self.view.togglePlotFit.stateChanged.connect(self.toggle_plot_fit)
        self.view.togglePlotNegValues.stateChanged.connect(self.toggle_plot_neg_values)
        self.view.togglePlotOutliers.stateChanged.connect(self.toggle_plot_outliers)
        self.view.togglePlotOutliersLimit.stateChanged.connect(self.toggle_plot_outliers_limits)
        self.view.togglePlotNoiseLevel.stateChanged.connect(self.toggle_plot_noise_level)
        self.view.togglePlotBaseline.stateChanged.connect(self.toggle_plot_baseline)
        self.view.togglePlotBackground.stateChanged.connect(self.toggle_plot_background)
        self.view.togglePlotResidual.stateChanged.connect(self.toggle_plot_residuals)
        self.view.toggleShowPeaksLabels.stateChanged.connect(self.toggle_show_peaks_labels)
        self.view.title.textChanged.connect(self.update_title)
        self.view.residualCoeff.textChanged.connect(self.update_residual_coeff)
        self.view.xLabel.textChanged.connect(self.update_x_label)
        self.view.yLabel.textChanged.connect(self.update_y_label)


    def newDocument(self):
        print("New document is requested")

    def toggle_plot_fit(self, state):
        # TODO use model self.model.toggle_plot_fit(state)
        if state == 2:  # Qt.Checked
            print("Plot Fit is checked")
        else:
            print("Plot Fit is unchecked")
        
    def toggle_plot_neg_values(self, state):
        if state == 2:
            print("Plot Neg Values is checked")
        else:
            print("Plot Neg Values is unchecked")

    def toggle_plot_outliers(self, state):
        if state == 2:
            print("Plot Outliers is checked")
        else:
            print("Plot Outliers is unchecked")

    def toggle_plot_outliers_limits(self, state):
        if state == 2:
            print("Plot Outliers Limits is checked")
        else:
            print("Plot Outliers Limits is unchecked")

    def toggle_plot_noise_level(self, state):
        if state == 2:
            print("Plot Noise Level is checked")
        else:
            print("Plot Noise Level is unchecked")

    def toggle_plot_baseline(self, state):
        if state == 2:
            print("Plot Baseline is checked")
        else:
            print("Plot Baseline is unchecked")

    def toggle_plot_background(self, state):
        if state == 2:
            print("Plot Background is checked")
        else:
            print("Plot Background is unchecked")

    def toggle_plot_residuals(self, state):
        if state == 2:
            print("Plot Residuals is checked")
        else:
            print("Plot Residuals is unchecked")
    
    def toggle_show_peaks_labels(self, state):
        if state == 2:
            print("Show Peaks Labels is checked")
        else:
            print("Show Peaks Labels is unchecked")
            
    def update_title(self, text):
        print("Title is changed to", text)
        
    def update_residual_coeff(self, text):
        print("Residual coefficient is changed to", text)

    def update_x_label(self, text):
        print("X label is changed to", text)
    
    def update_y_label(self, text):
        print("Y label is changed to", text)
