from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QAction

from .frame_map import FrameMap

class CustomNavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self.original_xlim = None
        self.original_ylim = None
        self.addSeparator()
        self.add_custom_buttons()

    def set_original_view_limits(self, xlim, ylim):
        self.original_xlim = xlim
        self.original_ylim = ylim

    def deactivate_modes(self):
        """Deactivate both baseline and fitting modes."""
        self.baseline_mode.setChecked(False)
        self.fitting_mode.setChecked(False) 

    def pan(self, *args):
        """Override pan to deactivate modes before panning."""
        self.deactivate_modes()
        super().pan(*args)

    def zoom(self, *args):
        """Override zoom to deactivate modes before zooming."""
        self.deactivate_modes()
        super().zoom(*args)

    def home(self, *args):
        if self.original_xlim and self.original_ylim:
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(self.original_xlim)
            ax.set_ylim(self.original_ylim)
            self.canvas.draw()
        else:
            super().home(*args)

    def add_custom_buttons(self):
        self.baseline_mode = QAction('Baseline points', self)
        self.baseline_mode.setCheckable(True)  # Make the action checkable
        self.baseline_mode.triggered.connect(lambda: self.on_mode_toggle(self.baseline_mode, self.fitting_mode))
        self.addAction(self.baseline_mode)

        self.fitting_mode = QAction('Peaks points', self)
        self.fitting_mode.setCheckable(True)
        self.fitting_mode.triggered.connect(lambda: self.on_mode_toggle(self.fitting_mode, self.baseline_mode))
        self.addAction(self.fitting_mode)

    def update_canvas(self, new_canvas):
        self.canvas = new_canvas
        self.set_original_view_limits(self.original_xlim, self.original_ylim)
        self.update()

    # TODO Move to controller once display_figure is fixed
    def on_mode_toggle(self, active_action, inactive_action):
        # Deactivate pan and zoom modes
        self._actions['pan'].setChecked(False)
        self._actions['zoom'].setChecked(False)

        # Ensure only one action is checked at a time
        if active_action.isChecked():
            active_action.setChecked(True)
            inactive_action.setChecked(False)
        else:
            active_action.setChecked(False)

    def on_mode1(self):
        print("Baseline activated")

    def on_mode2(self):
        print("Fitting activated")

    def on_press (self, event):
        if event.button == 1:  # Left click
            print("Left click")
            # get active mode
            if self.baseline_mode.isChecked():
                self.on_mode1()
            elif self.fitting_mode.isChecked():
                self.on_mode2()

class PlotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.fig = Figure(layout='tight')
        self.ax = self.fig.add_subplot(111)
        self.canvas = None
        self.toolbar = None
        self.original_xlim = None
        self.original_ylim = None
        self._init_canvas_and_toolbar()

    def _init_canvas_and_toolbar(self):
        fig = self.fig
        # Create and add new canvas and toolbar if they don't exist
        if self.canvas is None:
            self.canvas = FigureCanvas(fig)
            self.toolbar = CustomNavigationToolbar(self.canvas, self)
            self.toolbar.set_original_view_limits(self.original_xlim, self.original_ylim)

            self.layout.addWidget(self.toolbar)
            self.layout.addWidget(self.canvas)

    def frame_map_init(self, spectra_map):
        self.frame_map_window = FrameMap(spectra_map)
        self.frame_map_window.show()

    def display_figure(self, ax, xlim=None, ylim=None):
        if ax is not None:
            # set data of each line in ax to the corresponding line in self.ax
            self.ax.clear()

            for line in ax.lines:
                self.ax.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())

            self.canvas.draw()

            if xlim and ylim:
                self.set_view_limits(xlim, ylim)
            else:
                self.store_original_view_limits()

    def get_view_limits(self):
        """Get the current view limits of the plot."""
        ax = self.fig.gca()
        if not ax.has_data():
            return None, None
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        return xlim, ylim

    def set_view_limits(self, xlim, ylim):
        if hasattr(self, 'canvas') and self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            self.canvas.draw()

    def store_original_view_limits(self):
        if hasattr(self, 'canvas') and self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            self.original_xlim = ax.get_xlim()
            self.original_ylim = ax.get_ylim()
            print(f"Original view limits: {self.original_xlim}, {self.original_ylim}")

    def update_element_visibility(self):
        """Method to handle element visibility updates without full redraw."""
        # Use blitting to update element visibility without full redraw
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)