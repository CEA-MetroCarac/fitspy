from models.plot_model import PlotModel

class PlotController():
    def __init__(self, view, settings):
        super().__init__()
        self.view = view
        self.model = PlotModel(settings)

    def setup_actions(self, settings_controller):
        if self.view.canvas and self.view.toolbar:
            self.view.canvas.mpl_connect('button_press_event', self.view.toolbar.on_press)
            
        self.model.axChanged.connect(self.view.display_figure)
        self.model.elementVisibilityToggled.connect(self.view.update_element_visibility)
        self.model.extendFiles.connect(settings_controller.extend_files)

    def set_settings(self, settings):
        for key, value in settings.items():
            self.model.settings[key] = value

            if key == "outliers":
                self.model.outliers_calc()

        # print("Settings updated"+str(self.model.settings))
        self.update_fig(self.model.selected_files)

    def outliers_calc(self):
        self.model.outliers_calc()
        self.update_fig(self.model.selected_files)

    def toggle_element_visibility(self, element_key):
        self.model.toggle_element_visibility(element_key)

    def update_plot_element(self, element_key):
        self.model.update_plot_element(element_key)

    def spectra_map_init(self, file):
        self.model.spectra_map_init(file)

    def frame_map_init(self, spectra_map):
        print("Frame map creation")
        self.view.frame_map_init(spectra_map)

    def spectrum_init(self, file):
        print("Spectrum creation")
        self.model.spectrum_init(file)

    def update_fig(self, selected_files):
        xlim, ylim = self.view.get_view_limits()
        self.model.update_fig(selected_files, xlim, ylim)