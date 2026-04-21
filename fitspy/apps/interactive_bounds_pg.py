"""
Class dedicated to the interactive bounds with pyqtgraph
"""
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

from fitspy.core.utils import closest_index
from fitspy.apps.interactive_bounds import set_tmp_params, CMAP
from fitspy.apps.pyside.utils import convert_color_pg


class InteractiveBounds(QtCore.QObject):

    def __init__(self, ax, spectrum, peak_model_name,
                 cmap=None, bind_func=None, enable_add_peak=False):
        super().__init__()

        self.ax = ax
        self.spectrum = spectrum
        self.peak_model_name = peak_model_name
        self.cmap = cmap or CMAP
        self.bind_func = bind_func
        self.enable_add_peak = enable_add_peak

        self.bboxes = []

        self.ax.vb.scene().installEventFilter(self)
        self.ax.vb.scene().sigMouseMoved.connect(self.on_move)

    def set_cmap(self, cmap):
        self.cmap = cmap

    def add_bbox(self, k, peak_model, is_visible=False):
        bbox = BBox(self.ax, self.spectrum, peak_model, is_visible=is_visible)
        bbox.set_color(self.cmap(k % self.cmap.N))
        bbox.update()
        self.bboxes.append(bbox)

    def update(self):
        self.bboxes = []
        for k, peak_model in enumerate(self.spectrum.peak_models):
            self.add_bbox(k, peak_model)

    def set_visible(self, status):
        for bbox in self.bboxes:
            for item in bbox.items:
                item.setVisible(status)

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:

            mouse_point = self.ax.vb.mapSceneToView(event.scenePos())
            x, y = mouse_point.x(), mouse_point.y()
            self.active_bbox = None

            for bbox in reversed(self.bboxes):
                if bbox.contains(x, y):
                    self.active_bbox = bbox
                    bbox.start_drag(x, y)
                    self.ax.vb.setMouseEnabled(x=False, y=False)
                    return True

            if event.button() == QtCore.Qt.MouseButton.LeftButton and self.enable_add_peak:
                self.spectrum.add_peak_model(self.peak_model_name, x)
                k = len(self.spectrum.peak_models) - 1
                self.add_bbox(k, self.spectrum.peak_models[-1], is_visible=True)

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            if self.active_bbox:
                self.active_bbox.stop_drag()
                self.active_bbox = None
                self.ax.vb.setMouseEnabled(x=True, y=True)
                if self.bind_func is not None:
                    self.bind_func()
                return True

        return False

    def on_move(self, pos):
        if not hasattr(self, "active_bbox") or self.active_bbox is None:
            return

        buttons = QtWidgets.QApplication.mouseButtons()
        if buttons == QtCore.Qt.MouseButton.NoButton:
            self.active_bbox.stop_drag()
            self.active_bbox = None
            self.ax.vb.setMouseEnabled(x=True, y=True)
            return

        mouse_point = self.ax.vb.mapSceneToView(pos)
        self.active_bbox.on_move(mouse_point.x())


class BBox:

    def __init__(self, ax, spectrum, peak_model, is_visible=True, color='b', ratio=0.5):

        self.ax = ax
        self.spectrum = spectrum
        self.peak_model = peak_model
        self.color = color
        self.ratio = ratio

        self.x = spectrum.x
        self.y = spectrum.y

        params = peak_model.param_hints

        self.ampli = params['ampli']['value']
        self.x0 = params['x0']['value']
        self.dx0 = [self.x0 - params['x0']['min'], params['x0']['max'] - self.x0]

        if 'fwhm_l' in params:
            self.fwhm = [params['fwhm_l']['value'], params['fwhm_r']['value']]
            self.dfwhm = [params['fwhm_l']['max'], params['fwhm_r']['max']]
            self.symetric = False
        else:
            self.fwhm = [params['fwhm']['value'], params['fwhm']['value']]
            self.dfwhm = [params['fwhm']['max']] * 2
            self.symetric = True

        pen = pg.mkPen(self.color)
        brush = pg.mkBrush(self.color)

        self.profile_fwhm = pg.PlotDataItem([], [], pen=pen)

        self.vline = pg.PlotDataItem([self.x0, self.x0], [0, self.ampli], pen=pen)

        # rectangles
        self.rect_x0 = QtWidgets.QGraphicsRectItem()
        self.rect_x0.setBrush(brush)
        self.rect_x0.setOpacity(0.3)

        self.rect_x0_inner = QtWidgets.QGraphicsRectItem()
        self.rect_x0_inner.setBrush(brush)
        self.rect_x0_inner.setOpacity(0.3)

        self.rect_fwhm = QtWidgets.QGraphicsRectItem()
        self.rect_fwhm.setBrush(brush)
        self.rect_fwhm.setOpacity(0.3)

        self.items = [self.profile_fwhm, self.vline,
                      self.rect_x0, self.rect_x0_inner, self.rect_fwhm]

        for item in self.items:
            item.setVisible(is_visible)
            self.ax.vb.addItem(item)

        self.update_display()

    def set_color(self, color):
        self.color = convert_color_pg(color)
        pen = pg.mkPen(self.color)
        brush = pg.mkBrush(self.color)
        for item in self.items:
            item.setPen(pen)
            item.setBrush(brush)

    def start_drag(self, x, y):
        self.last_x = x
        self.dragging = None

        if self.contains_rect(self.rect_x0_inner, x, y):
            self.dragging = 'all'

        elif self.contains_rect(self.rect_x0, x, y):
            self.dragging = 'dx0[0]' if x < self.x0 else 'dx0[1]'

        elif self.contains_rect(self.rect_fwhm, x, y):
            self.dragging = 'dfwhm[0]' if x < self.x0 else 'dfwhm[1]'

    def stop_drag(self):
        self.dragging = None

    def on_move(self, x):
        if not self.dragging:
            return

        dx = x - self.last_x
        self.last_x = x

        if self.dragging == 'all':
            self.x0 += dx
            ind = closest_index(self.x, self.x0)
            self.ampli = self.y[ind]

        elif self.dragging == 'dx0[0]':
            self.dx0[0] = max(0, self.dx0[0] - dx)

        elif self.dragging == 'dx0[1]':
            self.dx0[1] = max(0, self.dx0[1] + dx)

        elif self.dragging == 'dfwhm[0]':
            self.dfwhm[0] = max(0, self.dfwhm[0] - dx)
            if self.symetric:
                self.dfwhm[1] = self.dfwhm[0]

        elif self.dragging == 'dfwhm[1]':
            self.dfwhm[1] = max(0, self.dfwhm[1] + dx)
            if self.symetric:
                self.dfwhm[0] = self.dfwhm[1]

        self.update()

    def contains(self, x, y):
        return (self.contains_rect(self.rect_x0, x, y) or
                self.contains_rect(self.rect_fwhm, x, y))

    def contains_rect(self, rect, x, y):
        scene_pos = self.ax.vb.mapViewToScene(QtCore.QPointF(x, y))
        local_pos = rect.mapFromScene(scene_pos)
        return rect.rect().contains(local_pos)

    def update_params(self):
        self.peak_model.set_param_hint('ampli', value=self.ampli)
        self.peak_model.set_param_hint('x0', value=self.x0)
        self.peak_model.set_param_hint('x0', min=self.x0 - self.dx0[0])
        self.peak_model.set_param_hint('x0', max=self.x0 + self.dx0[1])
        if 'fwhm_l' in self.peak_model.param_hints.keys():
            self.peak_model.set_param_hint('fwhm_l', value=self.fwhm[0])
            self.peak_model.set_param_hint('fwhm_r', value=self.fwhm[1])
            self.peak_model.set_param_hint('fwhm_l', max=self.dfwhm[0])
            self.peak_model.set_param_hint('fwhm_r', max=self.dfwhm[1])
        else:
            self.peak_model.set_param_hint('fwhm', value=self.fwhm[0])
            self.peak_model.set_param_hint('fwhm', max=self.dfwhm[0])

    def update_display(self):
        self.vline.setData([self.x0, self.x0], [0, self.ampli])

        w = self.dx0[0] + self.dx0[1]
        h = self.ratio * self.ampli
        self.rect_x0.setRect(self.x0 - self.dx0[0], 0, w, h)
        self.rect_x0_inner.setRect(self.x0 - 0.5 * self.dx0[0], 0, 0.5 * w, h)
        self.rect_fwhm.setRect(self.x0 - 0.5 * self.dfwhm[0], self.ratio * self.ampli,
                               0.5 * (self.dfwhm[0] + self.dfwhm[1]), (1 - self.ratio) * self.ampli)

    def update_profile_fwhm(self):
        x = self.spectrum.x
        mask = (self.x0 - 0.5 * self.dfwhm[0] <= x) & (x <= self.x0 + 0.5 * self.dfwhm[1])
        with set_tmp_params(self.peak_model, self.dfwhm):
            tmp_params = self.peak_model.make_params()
            y = self.peak_model.eval(tmp_params, x=x[mask])
            self.profile_fwhm.setData(x[mask], y)

    def update(self):
        self.update_params()
        self.update_display()
        self.update_profile_fwhm()


if __name__ == "__main__":
    from pathlib import Path
    from fitspy.core.spectrum import Spectrum
    from fitspy.apps.pyside.components.plot.backend_manager import MplLikeAxes

    app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(show=True)
    win.setBackground('w')

    plot = win.addPlot()
    vb = plot.getViewBox()
    vb.setMenuEnabled(False)
    ax = MplLikeAxes(plot)

    DATA = Path(__file__).parents[2] / "examples" / "data"
    fname = DATA / 'spectra_2' / 'spectrum_2_1.txt'

    spectrum = Spectrum()
    spectrum.load_profile(fname=fname)

    ax.plot(spectrum.x, spectrum.y)

    ib = InteractiveBounds(ax, spectrum, 'Gaussian', enable_add_peak=True)

    app.exec()
