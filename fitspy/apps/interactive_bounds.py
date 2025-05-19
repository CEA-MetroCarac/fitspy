"""
module description
"""
import contextlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from fitspy.core.utils import closest_index

CMAP = matplotlib.colormaps['tab10']


@contextlib.contextmanager
def set_tmp_params(model, dfwhm=None):
    try:
        if dfwhm:
            if 'fwhm_l' in model.param_hints.keys():
                original_fwhm_l = model.param_hints['fwhm_l']['value']
                original_fwhm_r = model.param_hints['fwhm_r']['value']
                model.set_param_hint('fwhm_l', value=dfwhm[0])
                model.set_param_hint('fwhm_r', value=dfwhm[1])
            else:
                original_fwhm = model.param_hints['fwhm']['value']
                model.set_param_hint('fwhm', value=dfwhm[0])

        original_expr = {key: val.get('expr', '') for key, val in model.param_hints.items()}
        for key in model.param_hints:
            model.param_hints[key]['expr'] = ''

        yield model

    finally:
        if dfwhm:
            if 'fwhm_l' in model.param_hints.keys():
                model.set_param_hint('fwhm_l', value=original_fwhm_l)
                model.set_param_hint('fwhm_r', value=original_fwhm_r)
            else:
                model.set_param_hint('fwhm', value=original_fwhm)

        for key in model.param_hints:
            model.param_hints[key]['expr'] = original_expr.get(key, '')


class InteractiveBounds:

    def __init__(self, spectrum, ax, cmap=None, model=None, bind_func=None):
        self.spectrum = spectrum
        self.ax = ax
        self.cmap = cmap or CMAP
        self.model = model

        self.bboxes = []

        self.canvas = self.ax.get_figure().canvas
        self.canvas.mpl_connect('button_press_event', self.on_press)
        if bind_func is not None:
            self.canvas.mpl_connect('button_release_event', lambda _: bind_func())

    def update(self):
        self.bboxes = []
        for k, peak_model in enumerate(self.spectrum.peak_models):
            bbox = BBox(self.ax, self.spectrum, peak_model)
            bbox.set_color(self.cmap(k % self.cmap.N))
            bbox.update()
            self.bboxes.append(bbox)

    def interact_with_bbox(self, event):
        [bbox.disconnect() for bbox in self.bboxes]
        interact = False
        for bbox in reversed(self.bboxes):
            if bbox.rect_x0.contains(event)[0] or bbox.rect_fwhm.contains(event)[0]:
                bbox.connect()
                interact = True
                break
        return interact

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        if event.button == 3:

            interact = self.interact_with_bbox(event)

            if self.model and not interact:
                self.spectrum.add_peak_model(self.model, event.xdata)
                bbox = BBox(self.ax, self.spectrum, self.spectrum.peak_models[-1])
                bbox.set_color(self.cmap(len(self.bboxes) % self.cmap.N))
                bbox.update()
                self.bboxes.append(bbox)


class BBox:

    def __init__(self, ax, spectrum, peak_model, color='blue', ratio=0.5):

        self.ax = ax
        self.spectrum = spectrum
        self.x = spectrum.x
        self.y = spectrum.y
        self.dx = spectrum.dx()
        self.peak_model = peak_model
        self.color = color
        self.ratio = ratio

        params = self.peak_model.param_hints
        ampli = params['ampli']['value']
        x0 = params['x0']['value']
        dx0 = [x0 - params['x0']['min'], params['x0']['max'] - x0]
        if 'fwhm_l' in params:
            fwhm = [params['fwhm_l']['value'], params['fwhm_r']['value']]
            dfwhm = [params['fwhm_l']['max'], params['fwhm_r']['max']]
            symetric = False
        else:
            fwhm = [params['fwhm']['value'], params['fwhm']['value']]
            dfwhm = [params['fwhm']['max'], params['fwhm']['max']]
            symetric = True

        self.ampli = ampli
        self.x0 = x0
        self.dx0 = dx0
        self.fwhm = fwhm
        self.dfwhm = dfwhm
        self.symetric = symetric

        self.cids = None
        self.canvas = self.ax.get_figure().canvas
        self.connect()

        self.dragging = {'move': None, 'press_x': None}

        height = ampli
        width_x0, height_x0 = dx0[0] + dx0[1], ratio * height
        width_fwhm, height_fwhm = 0.5 * (dfwhm[0] + dfwhm[1]), (1 - ratio) * height

        self.tmp = None
        self.line = Line2D([x0, x0], [0, height])
        self.rect_x0 = Rectangle((x0 - dx0[0], 0), width_x0, height_x0, alpha=0.3)
        self.rect_x0_inner = Rectangle((x0 - 0.5 * dx0[0], 0), 0.5 * width_x0, height_x0, alpha=0.3)
        self.rect_fwhm = Rectangle((x0 - dfwhm[0], ratio * height),
                                   width_fwhm, height_fwhm, alpha=0.3)
        # self.rect_fwhm_inner = Rectangle((x0 - 0.25 * dfwhm[0], ratio * height),
        #                                  0.5 * width_fwhm, height_fwhm, alpha=0.3)

        self.ax.add_line(self.line)
        self.ax.add_patch(self.rect_x0)
        self.ax.add_patch(self.rect_x0_inner)
        self.ax.add_patch(self.rect_fwhm)
        # self.ax.add_patch(self.rect_fwhm_inner)

        self.canvas.draw_idle()

    def remove(self):
        self.line.remove()
        self.rect_x0.remove()
        self.rect_x0_inner.remove()
        self.rect_fwhm.remove()
        # self.rect_fwhm_inner.remove()
        [x.remove() for x in self.tmp]

    def connect(self):
        self.cids = []
        self.cids.append(self.canvas.mpl_connect('button_press_event', self.on_press))
        self.cids.append(self.canvas.mpl_connect('motion_notify_event', self.on_motion))
        self.cids.append(self.canvas.mpl_connect('scroll_event', self.on_scroll))
        self.cids.append(self.canvas.mpl_connect('button_release_event', self.on_release))

    def disconnect(self):
        [self.canvas.mpl_disconnect(cid) for cid in self.cids]

    def set_color(self, color):
        self.color = color
        self.line.set_color(color)
        self.rect_x0.set_facecolor(color)
        self.rect_x0_inner.set_facecolor(color)
        self.rect_fwhm.set_facecolor(color)
        # self.rect_fwhm_inner.set_facecolor(color)
        if self.tmp is not None:
            self.tmp.set_color(color)

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

        self.line.set_xdata([self.x0, self.x0])
        self.line.set_ydata([0, self.ampli])

        self.rect_x0.set_x(self.x0 - self.dx0[0])
        self.rect_x0.set_width(self.dx0[0] + self.dx0[1])
        self.rect_x0.set_height(self.ratio * self.ampli)

        self.rect_x0_inner.set_x(self.x0 - 0.5 * self.dx0[0])
        self.rect_x0_inner.set_width(0.5 * (self.dx0[0] + self.dx0[1]))
        self.rect_x0_inner.set_height(self.ratio * self.ampli)

        self.rect_fwhm.set_x(self.x0 - 0.5 * self.dfwhm[0])
        self.rect_fwhm.set_y(self.ratio * self.ampli)
        self.rect_fwhm.set_width(0.5 * (self.dfwhm[0] + self.dfwhm[1]))
        self.rect_fwhm.set_height((1 - self.ratio) * self.ampli)

        # self.rect_fwhm_inner.set_x(self.x0 - 0.25 * self.dfwhm[0])
        # self.rect_fwhm_inner.set_y(self.ratio * self.ampli)
        # self.rect_fwhm_inner.set_width(0.25 * (self.dfwhm[0] + self.dfwhm[1]))
        # self.rect_fwhm_inner.set_height((1 - self.ratio) * self.ampli)

    def update_profiles(self):

        if self.tmp is not None:
            [x.remove() for x in self.tmp]
        self.tmp = []

        x = self.spectrum.x

        with set_tmp_params(self.peak_model):
            tmp_params = self.peak_model.make_params()
            y = self.peak_model.eval(tmp_params, x=x)
            self.tmp.append(self.ax.plot(x, y, c=self.color, lw=0.5)[0])

        mask = (self.x0 - 0.5 * self.dfwhm[0] <= x) & (x <= self.x0 + 0.5 * self.dfwhm[1])
        with set_tmp_params(self.peak_model, self.dfwhm):
            tmp_params = self.peak_model.make_params()
            y = self.peak_model.eval(tmp_params, x=x[mask])
            self.tmp.append(self.ax.plot(x[mask], y, c=self.color, lw=0.5)[0])

    def update(self):
        self.update_params()
        self.update_display()
        self.update_profiles()
        self.canvas.draw_idle()

    def on_press(self, event):

        self.dragging['press_x'] = event.xdata

        if self.rect_x0_inner.contains(event)[0]:
            self.dragging['move'] = 'all'
        elif self.rect_x0.contains(event)[0]:
            self.dragging['move'] = 'dx0[0]' if event.xdata < self.x0 else 'dx0[1]'
        elif self.rect_fwhm.contains(event)[0]:
            self.dragging['move'] = 'dfwhm[0]' if event.xdata < self.x0 else 'dfwhm[1]'
        else:
            pass

    def on_motion(self, event):
        if not self.dragging['move'] or event.inaxes != self.ax:
            return

        dx = event.xdata - self.dragging['press_x']
        self.dragging['press_x'] = event.xdata

        if self.dragging['move'] == 'all':
            self.x0 += dx
            ind = closest_index(self.spectrum.x, self.x0)
            self.ampli = self.spectrum.y[ind]

        elif self.dragging['move'] == 'dx0[0]':
            self.dx0[0] = max(0, self.dx0[0] - dx)

        elif self.dragging['move'] == 'dx0[1]':
            self.dx0[1] = max(0, self.dx0[1] + dx)

        elif self.dragging['move'] == 'dfwhm[0]':
            self.dfwhm[0] = max(0, self.dfwhm[0] - dx)
            if self.symetric:
                self.dfwhm[1] = self.dfwhm[0]

        elif self.dragging['move'] == 'dfwhm[1]':
            self.dfwhm[1] = max(0, self.dfwhm[1] + dx)
            if self.symetric:
                self.dfwhm[0] = self.dfwhm[1]

        self.update()

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return

        ind = closest_index(self.x, self.x0)
        dx = self.dx[ind] if event.button == 'up' else -self.dx[ind]
        k = int(event.xdata > self.x0)

        if self.rect_x0.contains(event)[0]:
            self.dx0[k] = max(0, self.dx0[k] + dx)
        elif self.rect_fwhm.contains(event)[0]:
            self.dfwhm[k] = max(0, self.dfwhm[k] + dx)
            if self.symetric:
                self.dfwhm[1 - k] = self.dfwhm[k]
        else:
            return

        self.update()

    def on_release(self, _):
        self.dragging['move'] = False


if __name__ == "__main__":
    from pathlib import Path
    from fitspy.core.spectrum import Spectrum

    DATA = Path(__file__).parents[2] / "examples" / "data"
    fname = DATA / 'spectra_2' / 'spectrum_2_1.txt'

    spectrum = Spectrum()
    spectrum.load_profile(fname=fname)

    _, ax = plt.subplots()
    ax.plot(spectrum.x, spectrum.y)
    inds = spectrum.inds_local_minima()
    for ind in inds:
        ax.axvline(spectrum.x[ind], ls=':', lw=0.3)

    bboxes = InteractiveBounds(spectrum, ax, model='Gaussian')
    plt.show()
