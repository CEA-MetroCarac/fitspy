from models.plot_model import PlotModel

class PlotController():
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = PlotModel()

    def setup_actions(self, settings_controller):
        self.model.figureChanged.connect(self.view.display_figure)
        self.model.extendFiles.connect(settings_controller.extend_files)

    def update_fig(self, selected_files):
        self.model.update_fig(selected_files)

    def spectra_map_init(self, file):
        self.model.spectra_map_init(file)

    def frame_map_init(self, spectra_map):
        print("Frame map creation")
        self.view.frame_map_init(spectra_map)

    def spectrum_init(self, file):
        print("Spectrum creation")
        self.model.spectrum_init(file)