from models.plot_model import PlotModel

class PlotController():
    def __init__(self, view, settings):
        super().__init__()
        self.view = view
        self.model = PlotModel(settings)

    def setup_actions(self, settings_controller):
        if self.view.canvas and self.view.toolbar:
            self.view.canvas.mpl_connect('button_press_event', self.press_event)

        self.model.axChanged.connect(self.view.display_figure)
        self.model.canvasChanged.connect(self.view.update_canvas)
        self.model.extendFiles.connect(settings_controller.extend_files)

    def set_settings(self, settings):
        for key, value in settings.items():
            self.model.settings[key] = value

            if key == "outliers":
                self.model.outliers_calc()

        # print("Settings updated"+str(self.model.settings))
        self.update_fig(self.model.selected_files)

    def press_event(self, event):
        if event.button == 1:
            print("Left click")
            if self.view.toolbar.baseline_mode.isChecked():
                print("Baseline activated")
                self.model.add_baseline_point(event.xdata, event.ydata)
            elif self.view.toolbar.fitting_mode.isChecked():
                print("Fitting activated")
                pass
        elif event.button == 3:
            print("Right click")
            if self.view.toolbar.baseline_mode.isChecked():
                print("Baseline deactivated")
                self.model.del_baseline_point(event.xdata, event.ydata)
            elif self.view.toolbar.fitting_mode.isChecked():
                print("Fitting deactivated")
                pass

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