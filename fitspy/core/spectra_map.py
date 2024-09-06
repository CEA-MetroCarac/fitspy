"""
Class dedicated to handle 'Spectrum' objects from a 2D map managed by SpectraMap
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
from parse import Parser

from fitspy.core import Spectra, Spectrum, closest_index, get_2d_map

POLICY = "{name}  X={x}  Y={y}"
PARSER = Parser(POLICY)


class SpectraMap(Spectra):
    """
    Class dedicated to handle 'Spectrum' objects from a 2D map

    Attributes
    ----------
    fname: str
        Pathname associated to the loaded object
    xy_map: tuple of 2 list
        Lists of x and y coordinates used in the 2D-map
    shape_map: tuple of 2 ints
        Shape associated to the 2D-map
    extent: iterable of 4 floats
        bounding box in data coordinates that the image will fill specified as
        (xmin, xmax, ymin, ymax)
    coords: list of list of 2 floats
        List containing the (x,y) coordinates for each spectrum in the 2D-map
    intensity: numpy.ndarray(((len(shape_map[0]) * len(shape_map[1]), n))
        Array of spectra intensities (n-values) associated to the xy_map coords
    arr: numpy.ndarray((len(shape_map[0]), len(shape_map[1]))
        Array associated to the xy_map coords
    ax: Matplotlib.pyplot.axis
        Axis associated to the 2D-map displaying
    img: Matplotlib.image.AxesImage
        Image related to the 2D-map displaying
    cbar: Matplotlib.pyplot.colorbar
        Colorbar associated to the spectra 2D-map displaying
    ax_slider: Matplotlib.pyplot.axis
        Axis associated to the RangeSlider object
    slider: Matplotlib.widgets.RangeSlider
        Slider associated to the intensity integration range or to a model
        parameter in the 2D-map displaying
    xrange: tuple of 2 floats
        Range of intensity to consider in the 2D-map displaying
    """

    def __init__(self):

        self.fname = None
        self.xy_map = None
        self.shape_map = None
        self.extent = None
        self.coords = None
        self.intensity = None
        self.arr = None
        self.outliers_limit = None

        self.ax = None
        self.img = None
        self.cbar = None
        self.ax_slider = None
        self.slider = None
        self.xrange = None

    def create_map(self, fname):
        """ Create map """

        arr = get_2d_map(fname)

        x_map = x = list(np.sort(np.unique(arr[1:, 1])))
        y_map = y = list(np.sort(np.unique(arr[1:, 0])))

        # grid range associated to 'arr' to be consistent with the tools axis
        xmin = ymin = -0.5
        xmax = ymax = 0.5
        if len(x) > 1:
            xmin = x[0] - 0.5 * (x[1] - x[0])
            xmax = x[-1] + 0.5 * (x[-1] - x[-2])
        if len(y) > 1:
            ymin = y[-1] + 0.5 * (y[-1] - y[-2])
            ymax = y[0] - 0.5 * (y[1] - y[0])

        # wavelengths
        x = arr[0][2:]
        inds = np.argsort(x)
        x = x[inds]

        # intensities
        intensity_map = np.nan * np.ones((len(x_map) * len(y_map), len(x)))

        coords = []
        for vals in arr[1:]:
            # create the related spectrum object
            spectrum = Spectrum()
            spectrum.fname = POLICY.format(name=fname, x=vals[1], y=vals[0])
            intensity = vals[2:][inds]
            spectrum.x = x
            spectrum.y = intensity
            spectrum.x0 = spectrum.x.copy()
            spectrum.y0 = spectrum.y.copy()
            ind_flat = x_map.index(vals[1]) + y_map.index(vals[0]) * len(x_map)
            intensity_map[ind_flat, :] = intensity
            self.append(spectrum)
            coords.append([vals[1], vals[0]])

        self.fname = fname
        self.xy_map = (x_map, y_map)
        self.shape_map = (len(self.xy_map[1]), len(self.xy_map[0]))
        self.extent = [xmin, xmax, ymin, ymax]
        self.intensity = intensity_map
        self.arr = np.sum(intensity_map, axis=1).reshape(self.shape_map)
        self.coords = coords

    def spectrum_coords(self, spectrum):
        """ Return the (x, y) map coordinates associated with 'spectrum' """
        res = PARSER.parse(spectrum.fname)
        x = float(res.named['x'])
        y = float(res.named['y'])
        return x, y

    def spectrum_indices(self, spectrum):
        """ Return the (i, j) map indices associated with 'spectrum' """
        x, y = self.spectrum_coords(spectrum)
        j = self.xy_map[0].index(x)
        i = self.xy_map[1].index(y)
        return i, j

    def plot_map(self, ax):
        """ Plot the integrated spectra map intensities on 'ax' """

        self.ax = ax

        fig = self.ax.get_figure()
        fig.subplots_adjust(top=0.92)
        self.ax_slider = fig.add_axes([0.2, 0.92, 0.4, 0.05])

        self.img = self.ax.imshow(self.arr, extent=self.extent)

        self.cbar = plt.colorbar(self.img, ax=self.ax)

        self.xrange = (self[0].x0.min(), self[0].x0.max())
        self.slider = RangeSlider(self.ax_slider, "X-Range ",
                                  self.xrange[0], self.xrange[1],
                                  valinit=self.xrange)
        self.slider.on_changed(self.plot_map_update)
        fig.canvas.draw()

    def plot_map_update(self, xrange=None, var='Intensity', label='',
                        vmin=None, vmax=None):
        """ Update 'plot_map' with intensity or models parameter passed through
            'var' and 'label'"""
        if xrange is not None:
            self.xrange = xrange

        if 'Intensity' in var:
            imin = closest_index(self[0].x0, self.xrange[0])
            imax = closest_index(self[0].x0, self.xrange[1])
            arr = np.sum(self.intensity[:, imin:imax + 1], axis=1)
            self.arr = arr.reshape(self.shape_map)
        else:  # models parameter displaying
            self.arr = np.nan * np.zeros((self.shape_map[0], self.shape_map[1]))
            for spectrum in self:
                for j, lab in enumerate(spectrum.peak_labels):
                    if lab == label:
                        params = spectrum.peak_models[j].param_hints
                        if var in params.keys():
                            ind = self.spectrum_indices(spectrum)
                            self.arr[ind[0], ind[1]] = params[var]['value']

        self.img.set_data(self.arr)
        self.img.autoscale()
        if vmin is not None:
            self.img.norm.vmin = vmin
        if vmax is not None:
            self.img.norm.vmax = vmax
        self.cbar.update_normal(self.img)
        self.ax.get_figure().canvas.draw()

    def export_to_csv(self, fname):
        """ Export 'arr' class attribute in a .csv file named 'fname' """
        if self.arr is not None:
            dfr = pd.DataFrame(self.arr)
            dfr.to_csv(fname, sep=';', header=False, index=False)

    @staticmethod
    def load_map(fname):
        """ Return a SpectraMap object from .txt file issued from labspec files
            conversion """
        spectra_map = SpectraMap()
        spectra_map.create_map(fname)
        return spectra_map