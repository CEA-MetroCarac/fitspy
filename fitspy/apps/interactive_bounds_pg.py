"""
module description
"""

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

from fitspy.core.utils import closest_index


class InteractiveBounds(QtCore.QObject):

    def __init__(self, spectrum, plot_widget, model=None, bind_func=None):
        super().__init__()

        self.spectrum = spectrum
        self.plot_widget = plot_widget
        self.model = model
        self.bind_func = bind_func

        self.bboxes = []

        self.plot_widget.scene().installEventFilter(self)
        self.plot_widget.scene().sigMouseMoved.connect(self.on_move)

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:

            pos = event.scenePos()
            mouse_point = self.plot_widget.getViewBox().mapSceneToView(pos)

            x = mouse_point.x()
            y = mouse_point.y()

            self.active_bbox = None

            for bbox in reversed(self.bboxes):
                if bbox.contains(x, y):
                    self.active_bbox = bbox
                    bbox.start_drag(x)
                    self.plot_widget.getViewBox().setMouseEnabled(x=False, y=False)
                    return True

            if event.button() == QtCore.Qt.MouseButton.RightButton:
                if self.model:
                    self.spectrum.add_peak_model(self.model, x)
                    bbox = BBox(self.plot_widget, self.spectrum, self.spectrum.peak_models[-1])
                    self.bboxes.append(bbox)

        return False

    def on_move(self, pos):
        if not hasattr(self, "active_bbox") or self.active_bbox is None:
            return

        buttons = QtWidgets.QApplication.mouseButtons()
        if buttons == QtCore.Qt.MouseButton.NoButton:
            self.active_bbox.stop_drag()
            self.active_bbox = None
            self.plot_widget.getViewBox().setMouseEnabled(x=True, y=True)
            return

        mouse_point = self.plot_widget.getViewBox().mapSceneToView(pos)
        self.active_bbox.on_move(mouse_point.x())

    def update(self):
        for bbox in self.bboxes:
            bbox.remove()
        self.bboxes = []
        for peak_model in self.spectrum.peak_models:
            bbox = BBox(self.plot_widget, self.spectrum, peak_model)
            self.bboxes.append(bbox)


class BBox:

    def __init__(self, plot_widget, spectrum, peak_model, color=(0, 0, 255, 80)):

        self.plot_widget = plot_widget
        self.spectrum = spectrum
        self.peak_model = peak_model

        self.view = plot_widget.getViewBox()

        self.x = spectrum.x
        self.y = spectrum.y

        params = peak_model.param_hints

        self.ampli = params['ampli']['value']
        self.x0 = params['x0']['value']
        self.dx0 = [self.x0 - params['x0']['min'], params['x0']['max'] - self.x0]

        if 'fwhm_l' in params:
            self.dfwhm = [params['fwhm_l']['max'], params['fwhm_r']['max']]
            self.symetric = False
        else:
            self.dfwhm = [params['fwhm']['max']] * 2
            self.symetric = True

        self.color = color

        pen = pg.mkPen(color[:3])
        brush = pg.mkBrush(color)

        self.line = pg.PlotDataItem([self.x0, self.x0], [0, self.ampli], pen=pen)

        # rectangles
        self.rect_x0 = QtWidgets.QGraphicsRectItem()
        self.rect_x0.setBrush(brush)

        self.rect_x0_inner = QtWidgets.QGraphicsRectItem()
        self.rect_x0_inner.setBrush(brush)

        self.rect_fwhm = QtWidgets.QGraphicsRectItem()
        self.rect_fwhm.setBrush(brush)

        self.plot_widget.addItem(self.line)
        self.view.addItem(self.rect_x0)
        self.view.addItem(self.rect_x0_inner)
        self.view.addItem(self.rect_fwhm)

        self.update_display()

    def start_drag(self, x):
        self.last_x = x
        self.dragging = None

        if self.contains_rect(self.rect_x0_inner, x, 0):
            self.dragging = 'all'

        elif self.contains_rect(self.rect_x0, x, 0):
            self.dragging = 'dx0[0]' if x < self.x0 else 'dx0[1]'

        elif self.contains_rect(self.rect_fwhm, x, 0):
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

        self.update_display()

    def contains(self, x, y):
        return (self.contains_rect(self.rect_x0_inner, x, y) or
                self.contains_rect(self.rect_x0, x, y) or
                self.contains_rect(self.rect_fwhm, x, y))

    def contains_rect(self, rect, x, y):
        vb = self.plot_widget.getViewBox()
        scene_pos = vb.mapViewToScene(QtCore.QPointF(x, y))
        local_pos = rect.mapFromScene(scene_pos)
        return rect.rect().contains(local_pos)

    def update_display(self):
        ratio = 0.5

        self.line.setData([self.x0, self.x0], [0, self.ampli])

        x = self.x0 - self.dx0[0]
        w = self.dx0[0] + self.dx0[1]
        h = ratio * self.ampli

        self.rect_x0.setRect(x, 0, w, h)
        self.rect_x0_inner.setRect(self.x0 - 0.5 * self.dx0[0], 0, 0.5 * w, h)
        self.rect_fwhm.setRect(self.x0 - self.dfwhm[0], ratio * self.ampli,
                               0.5 * (self.dfwhm[0] + self.dfwhm[1]), (1 - ratio) * self.ampli)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(show=True)
    win.setBackground('w')

    plot = win.addPlot()
    plot.getViewBox().setMenuEnabled(False)

    from fitspy.core.spectrum import Spectrum
    from pathlib import Path

    DATA = Path(__file__).parents[2] / "examples" / "data"
    fname = DATA / 'spectra_2' / 'spectrum_2_1.txt'

    spectrum = Spectrum()
    spectrum.load_profile(fname=fname)

    plot.plot(spectrum.x, spectrum.y)

    ib = InteractiveBounds(spectrum, plot, model='Gaussian')

    app.exec()
