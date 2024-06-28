from models.plot_model import PlotModel

class PlotController():
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = PlotModel()
        self.setup_actions()

    def setup_actions(self):
        self.model.figureChanged.connect(self.view.display_figure)

    def update_fig(self, selected_files):
        self.model.update_fig(selected_files)

    def frame_map_init(self, spectra_map):
        print("Frame map creation")
        self.view.frame_map_init(spectra_map)