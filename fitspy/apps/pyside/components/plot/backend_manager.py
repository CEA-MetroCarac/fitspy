"""
Class dedicated to use pyqtgraph with the same syntax as matplotlib
"""
import math
import pyqtgraph as pg

from PySide6.QtCore import Qt

COLORS = set('rgbcmykw')
MARKERS = set('os^v<>dpx+.')
LINESTYLES = {'--': Qt.DashLine, '-.': Qt.DashDotLine, ':': Qt.DotLine, '-': Qt.SolidLine}


def parser(fmt=None, **kwargs):
    fmt = fmt or ''
    fmt_color = next((c for c in fmt if c in COLORS), None)
    fmt_marker = next((c for c in fmt if c in MARKERS), None)
    fmt_linestyle = next((ls for ls in LINESTYLES.keys() if ls in fmt), '-' if fmt_color else None)

    color = kwargs.pop('color', kwargs.pop('c', fmt_color))
    if isinstance(color, tuple) and max(color) <= 1:
        color = tuple(int(c * 255) for c in color)

    linewidth = kwargs.pop('linewidth', kwargs.pop('lw', 1))
    linestyle = kwargs.pop('linestyle', kwargs.pop('ls', fmt_linestyle))

    pg_kwargs = {'symbol': kwargs.pop('marker', fmt_marker),
                 'symbolPen': kwargs.pop('markeredgecolor', kwargs.pop('mec', None)),
                 'symbolBrush': kwargs.pop('markerfacecolor', kwargs.pop('mfc', color)),
                 'symbolSize': 2 * kwargs.pop('markersize', kwargs.pop('ms', 4)),
                 'name': kwargs.pop('label', None)}

    return color, linewidth, linestyle, pg_kwargs


class MplLikeAxes:
    def __init__(self, plot_item):
        self.plot_item = plot_item

        self._color_cycle = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        self._cycle_index = 0
        self.vb = self.plot_item.vb
        self._legend = pg.LegendItem(offset=(-10, 10))
        self._legend.setParentItem(self.plot_item)

        self._items = []
        self._lines = []

    def next_color(self):
        color = self._color_cycle[self._cycle_index % len(self._color_cycle)]
        self._cycle_index += 1
        return color

    def set_prop_cycle(self, cycler=None):
        if cycler is None:
            self._cycle_index = 0
        else:
            self._color_cycle = cycler
            self._cycle_index = 0

    def plot(self, x, y=None, fmt=None, **kwargs):
        if y is None:
            y = x
            x = list(range(len(y)))

        color, linewidth, linestyle, pg_kwargs = parser(fmt, **kwargs)

        pen = None
        if linestyle is not None or pg_kwargs['symbol'] is None:
            pen = pg.mkPen(color=color, width=linewidth)
            pen.setStyle(LINESTYLES.get(linestyle, Qt.SolidLine))

        item = self.plot_item.plot(x, y, pen=pen, **pg_kwargs)
        line = item.curve
        self._items.append(item)
        self._lines.append(line)
        self.draw_idle()
        return line, item

    def legend(self, loc=None):
        self._legend.clear()
        for item in self._items:
            name = item.opts.get('name', None)
            if name and name not in ["Spectrum", "_nolegend_"]:
                self._legend.addItem(item, name)

    def clear(self):
        self.plot_item.clear()
        self._items = []
        self._lines = []

    def draw_idle(self):
        self.plot_item.update()

    def set_title(self, title):
        self.plot_item.setTitle(title)

    def set_xlabel(self, label):
        self.plot_item.setLabel('bottom', label)

    def set_ylabel(self, label):
        self.plot_item.setLabel('left', label)

    def get_xlim(self):
        return self.vb.viewRange()[0]

    def get_ylim(self):
        return self.vb.viewRange()[1]

    def set_xlim(self, xmin, xmax):
        self.plot_item.setXRange(xmin, xmax, padding=0)

    def set_ylim(self, bottom=None, top=None):
        ymin, ymax = self.plot_item.viewRange()[1]
        if bottom is not None:
            ymin = bottom
        if top is not None:
            ymax = top
        self.plot_item.setYRange(ymin, ymax, padding=0)

    def has_data(self):
        return bool(self.plot_item.listDataItems())

    def hlines(self, y, xmin, xmax, **kwargs):
        color = kwargs.get('colors', 'r')
        width = kwargs.get('linewidth', 1)
        pen = pg.mkPen(color=color, width=width)
        line = pg.InfiniteLine(pos=y, angle=0, pen=pen)
        self.plot_item.addItem(line)
        self._lines.append(line)
        return line

    def axvline(self, x, **kwargs):
        pen = kwargs.get('color', 'r')
        width = kwargs.get('lw', 1)
        style = kwargs.get('ls', ':')
        if style == ':':
            pen_style = Qt.DashLine
        else:
            pen_style = Qt.SolidLine
        line = pg.InfiniteLine(pos=x, angle=90, pen=pg.mkPen(pen, width=width, style=pen_style))
        self.plot_item.addItem(line)
        self._lines.append(line)
        return line

    def annotate(self, text, xy, **kwargs):
        x, y = xy

        xytext = kwargs.get('xytext', (0, 0))
        textcoords = kwargs.get('textcoords', 'offset points')
        if textcoords == 'offset points':
            offset_x, offset_y = xytext
        elif textcoords == 'data':
            offset_x, offset_y = xytext
        else:
            offset_x, offset_y = xytext

        ha = kwargs.get('ha', 'center')
        va = kwargs.get('va', 'bottom')
        anchor = {
            ('center', 'bottom'): (0.5, 0),
            ('center', 'center'): (0.5, 0.5),
            ('center', 'top'): (0.5, 1.5),
            ('left', 'bottom'): (0, 0),
            ('left', 'center'): (0, 0.5),
            ('left', 'top'): (0, 1),
            ('right', 'bottom'): (1, 0),
            ('right', 'center'): (1, 0.5),
            ('right', 'top'): (1, 1.5),
        }.get((ha, va), (0.5, 0))  # fallback

        fill, border = None, None
        if 'bbox' in kwargs:
            fill = pg.mkBrush(kwargs['bbox']['facecolor'])
            border = pg.mkPen(kwargs['bbox']['edgecolor'])

        color = kwargs.get('color', 'k')
        item = pg.TextItem(text=text, color=color, anchor=anchor, fill=fill, border=border)
        item.setPos(x + offset_x, y + offset_y)
        self.plot_item.addItem(item)
        self._lines.append(item)

        arrowprops = kwargs.get('arrowprops')
        if arrowprops:
            arrow = pg.ArrowItem(pos=(x + offset_x, y + offset_y),
                                 angle=0, tipAngle=30, headLen=10, brush=arrowprops.get('fc', 'k'))
            dx = x - (x + offset_x)
            dy = y - (y + offset_y)
            arrow.setStyle(angle=math.degrees(math.atan2(dy, dx)))
            self.plot_item.addItem(arrow)
            self._lines.append(arrow)

        return item

    # def set_xscale(self, scale, orientation='bottom'):
    #     if scale == "log":
    #         self.plot_item.setAxisItems({orientation: pg.LogAxisItem(orientation=orientation)})
    #     elif scale == "linear":
    #         self.plot_item.setAxisItems({orientation: pg.AxisItem(orientation=orientation)})
    #     else:
    #         raise ValueError("scale must be 'linear' or 'log'")
    #
    # def set_yscale(self, scale):
    #     self.set_xscale(scale, orientation='left')


if __name__ == "__main__":
    kwargs = {'c': 'k', 'lw': 0.5, 'marker': 'o', 'ms': 1}
    print(parser(fmt=None, **kwargs))
