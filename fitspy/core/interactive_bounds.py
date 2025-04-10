"""
module description
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from fitspy.core.utils import closest_index
from fitspy.core.models import gaussian


class InteractiveBounds:

    def __init__(self, ax, x, y, cmap):
        self.ax = ax
        self.x = x
        self.y = y
        self.cmap = cmap

        self.bboxes = []
        self.canvas = self.ax.get_figure().canvas

        self.cid = self.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        # bbox selection or creation
        if event.button == 1:
            in_bbox = False
            for bbox in self.bboxes:
                if bbox.rect_x0.contains_point((event.x, event.y)) or \
                        bbox.rect_fwhm.contains_point((event.x, event.y)):
                    bbox.connect()
                    in_bbox = True
                else:
                    bbox.disconnect()
            if not in_bbox:
                bbox = BBox(self.ax, self.x, self.y,
                            event.xdata, dx0=[20, 20], dfwhm=[30, 30])
                bbox.set_color(self.cmap(len(self.bboxes)))
                bbox.update_display()
                self.bboxes.append(bbox)

        # bbox deletion
        elif event.button == 3:
            for k, bbox in enumerate(self.bboxes):
                if bbox.rect_x0.contains_point((event.x, event.y)) or \
                        bbox.rect_fwhm.contains_point((event.x, event.y)):
                    bbox.delete()
                    self.bboxes.pop(k)
            for k, bbox in enumerate(self.bboxes):
                bbox.set_color(self.cmap(k))

            self.canvas.draw_idle()


class BBox:

    def __init__(self, ax, x, y, x0, dx0, dfwhm, color='blue', ratio=0.1):

        self.ax = ax
        self.x = x
        self.y = y

        self.cids = None
        self.canvas = self.ax.get_figure().canvas
        self.connect()

        self.x0 = x0
        self.dx0 = dx0
        self.dfwhm = dfwhm
        self.color = color
        self.ratio = ratio
        self.symetric = True

        self.dragging = {'move': False, 'press_x': None}
        self.dx = np.min(np.diff(x))

        height = self.y[closest_index(self.x, self.x0)]
        width_x0, height_x0 = dx0[0] + dx0[1], ratio * height
        width_fwhm, height_fwhm = 0.5 * (dfwhm[0] + dfwhm[1]), (1 - ratio) * height

        self.tmp = None
        self.line = Line2D([x0, x0], [0, height])
        self.rect_x0 = Rectangle((x0 - dx0[0], 0), width_x0, height_x0, alpha=0.5)
        self.rect_fwhm = Rectangle((x0 - dfwhm[0], ratio * height), width_fwhm, height_fwhm,
                                   alpha=0.2)

        self.ax.add_line(self.line)
        self.ax.add_patch(self.rect_x0)
        self.ax.add_patch(self.rect_fwhm)

        self.canvas.draw_idle()

    def delete(self):
        self.line.remove()
        self.rect_x0.remove()
        self.rect_fwhm.remove()
        self.tmp.remove()

    def connect(self):
        self.cids = []
        self.cids.append(self.canvas.mpl_connect('button_press_event', self.on_press))
        self.cids.append(self.canvas.mpl_connect('motion_notify_event', self.on_motion))
        self.cids.append(self.canvas.mpl_connect('scroll_event', self.on_scroll))
        self.cids.append(self.canvas.mpl_connect('button_release_event', self.on_release))

    def disconnect(self):
        [self.canvas.mpl_disconnect(cid) for cid in self.cids]
        self.cids.clear()

    def set_color(self, color):
        self.color = color
        self.line.set_color(color)
        self.rect_x0.set_facecolor(color)
        self.rect_fwhm.set_facecolor(color)
        if self.tmp is not None:
            self.tmp.set_color(color)

    def update_display(self):
        height = self.y[closest_index(self.x, self.x0)]

        self.line.set_xdata([self.x0, self.x0])
        self.line.set_ydata([0, height])

        self.rect_x0.set_x(self.x0 - self.dx0[0])
        self.rect_x0.set_width(self.dx0[0] + self.dx0[1])
        self.rect_x0.set_height(self.ratio * height)

        self.rect_fwhm.set_x(self.x0 - 0.5 * self.dfwhm[0])
        self.rect_fwhm.set_y(self.ratio * height)
        self.rect_fwhm.set_width(0.5 * (self.dfwhm[0] + self.dfwhm[1]))
        self.rect_fwhm.set_height((1 - self.ratio) * height)

        if self.tmp is not None:
            self.tmp.remove()
        mask = (self.x0 - 0.5 * self.dfwhm[0] <= self.x) & (self.x <= self.x0 + 0.5 * self.dfwhm[1])
        x = self.x[mask]
        y = gaussian(x, height, self.dfwhm[0], self.x0)
        self.tmp, = self.ax.plot(x, y, c=self.color, lw=0.5)

        self.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax:
            return

        self.dragging['press_x'] = event.xdata
        self.dragging['move'] = self.rect_x0.contains_point((event.x, event.y))

    def on_motion(self, event):
        if not self.dragging['move'] or event.inaxes != self.ax:
            return

        dx = event.xdata - self.dragging['press_x']
        self.dragging['press_x'] = event.xdata

        if self.dragging['move']:
            self.x0 += dx

        self.update_display()

    def on_scroll(self, event):
        if event.inaxes != self.ax:
            return

        dx = self.dx if event.button == 'up' else -self.dx
        k = int(event.xdata > self.x0)

        if self.rect_x0.contains_point((event.x, event.y)):
            self.dx0[k] = max(0, self.dx0[k] + dx)
        elif self.rect_fwhm.contains_point((event.x, event.y)):
            self.dfwhm[k] = max(0, self.dfwhm[k] + dx)
            if self.symetric:
                self.dfwhm[1 - k] = self.dfwhm[k]
        else:
            return

        self.update_display()

    def on_release(self, _):
        self.dragging['move'] = False
        print(self.x0, self.dx0, self.dfwhm)


if __name__ == "__main__":
    import matplotlib
    import numpy as np
    from fitspy.core.models import lorentzian, gaussian, lorentzian_asym

    cmap = matplotlib.colormaps['tab10']

    x = np.linspace(0, 600, 250)
    y = lorentzian(x, ampli=200, fwhm=30, x0=200)
    y += gaussian(x, ampli=120, fwhm=70, x0=300)
    y += lorentzian_asym(x, ampli=300, fwhm_l=40, fwhm_r=20, x0=500)

    _, ax = plt.subplots()
    ax.plot(x, y)

    # bbox = BoundingBox(ax, x, y, x0=300, dx0=[20, 20], dfwhm=[30, 30], color='blue')
    # bbox.update_display()
    # plt.show()

    bboxes = InteractiveBounds(ax, x, y, cmap)
    plt.show()
