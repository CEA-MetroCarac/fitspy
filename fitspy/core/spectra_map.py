"""
Class dedicated to handle 'Spectrum' objects from a 2D map managed by SpectraMap
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import RangeSlider
from parse import Parser

from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum
from fitspy.core.utils import closest_index, get_2d_map

POLICY = "{name}  X={x} Y={y}"
PARSER = Parser(POLICY)


class SpectraMap(Spectra):
    """
    Class dedicated to handle 'Spectrum' objects from a 2D map

    Attributes
    ----------
    fname: str
        Pathname associated to the loaded object
    arr0: numpy.ndarray
        Raw array with coordinates and intensities returned by fitspy.core.utils.get_2d_map()
    xy_map: tuple of 2 list
        Lists of x and y coordinates used in the 2D-map
    shape_map: tuple of 2 ints
        Shape associated to the 2D-map
    extent: iterable of 4 floats
        bounding box in data coordinates that the image will fill specified as
        (xmin, xmax, ymin, ymax)
    coords: list of list of 2 floats
        List containing the (x,y) coordinates for each spectrum in the 2D-map
    fnames_map: list of str
        List of the spectrum names related to the 2D-map
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
    marker: matplotlib.lines.Line2D
        Maker used in the 2D-map axis to set a spectrum position
    """

    def __init__(self):

        self.fname = None
        self.arr0 = None
        self.xy_map = None
        self.shape_map = None
        self.extent = None
        self.coords = None
        self.fnames_map = None
        self.intensity = None
        self.arr = None
        self.outliers_limit = None

        self.ax = None
        self.img = None
        self.cbar = None
        self.ax_slider = None
        self.slider = None
        self.xrange = None
        self.marker = None

    def create_map(self, fname, arr0=None):
        """ Create map """
        fname = os.path.normpath(fname)
        arr0 = get_2d_map(fname) if arr0 is None else arr0

        x_map = x = list(np.sort(np.unique(arr0[1:, 1])))
        y_map = y = list(np.sort(np.unique(arr0[1:, 0])))

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
        x = arr0[0][2:]
        inds = np.argsort(x)
        x = x[inds]

        # intensities
        intensity_map = np.nan * np.ones((len(x_map) * len(y_map), len(x)))

        coords = []
        fnames_map = []
        for vals in arr0[1:]:
            intensity = vals[2:][inds]
            ind_flat = x_map.index(vals[1]) + y_map.index(vals[0]) * len(x_map)
            intensity_map[ind_flat, :] = intensity
            coords.append([vals[1], vals[0]])

            # create the related spectrum object
            spectrum = Spectrum()
            spectrum.fname = POLICY.format(name=fname, x=vals[1], y=vals[0])
            spectrum.x = x
            spectrum.y = intensity
            spectrum.x0 = spectrum.x.copy()
            spectrum.y0 = spectrum.y.copy()
            self.append(spectrum)
            fnames_map.append(spectrum.fname)

        self.fname = fname
        self.arr0 = arr0
        self.xy_map = (x_map, y_map)
        self.shape_map = (len(self.xy_map[1]), len(self.xy_map[0]))
        self.extent = [xmin, xmax, ymin, ymax]
        self.intensity = intensity_map
        self.arr = np.sum(intensity_map, axis=1).reshape(self.shape_map)
        self.coords = coords
        self.fnames_map = fnames_map

    def get_spectrum(self, fname):
        """ Return the spectrum object related to 'fname' in the spectra map list """
        fname = os.path.normpath(fname)
        try:
            return self[self.fnames_map.index(fname)]
        except:
            print(f"{fname} not found in the spectra map list")
            return None

    @staticmethod
    def spectrum_coords(spectrum):
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

    def plot_map(self, ax, range_slider=None, cmap='viridis'):
        """ Plot the integrated spectra map intensities on 'ax' """
        ax.clear()
        self.ax = ax
        self.marker = None

        fig = self.ax.get_figure()
        # fig.subplots_adjust(top=0.92)
        # self.ax_slider = fig.add_axes([0.2, 0.92, 0.4, 0.05])

        # Y axis is inverted
        extent = [self.extent[0], self.extent[1], self.extent[3], self.extent[2]]
        self.img = self.ax.imshow(self.arr, extent=extent, origin='lower', cmap=cmap)

        if range_slider is not None:
            _min, _max = self[0].x0.min(), self[0].x0.max()
            range_slider.blockSignals(True)
            range_slider.setRange(_min, _max)
            range_slider.setValue((_min, _max))
            range_slider.blockSignals(False)
        else:
            fig.subplots_adjust(top=0.92)
            self.ax_slider = fig.add_axes([0.2, 0.92, 0.4, 0.05])
            self.cbar = plt.colorbar(self.img, ax=self.ax)
            self.xrange = (self[0].x0.min(), self[0].x0.max())
            self.slider = RangeSlider(self.ax_slider, "X-Range ",
                                      self.xrange[0], self.xrange[1],
                                      valinit=self.xrange)
            self.slider.on_changed(self.plot_map_update)

        fig.canvas.draw_idle()

    def plot_map_update(self, xrange=None, var='Intensity', label='',
                        vmin=None, vmax=None, cmap=None):
        """ 
        Update 'plot_map' with intensity or models parameter passed through
        'var' and 'label', and apply a custom colormap if provided.
        """
        if xrange is not None:
            self.xrange = xrange

        if 'Intensity' in var:
            imin = closest_index(self[0].x0, self.xrange[0])
            imax = closest_index(self[0].x0, self.xrange[1])
            arr = np.sum(self.intensity[:, imin:imax + 1], axis=1)
            self.arr = arr.reshape(self.shape_map)
        else:  # models parameter displaying
            self.arr = np.full((self.shape_map[0], self.shape_map[1]), np.nan)
            for spectrum in self:
                for j, lab in enumerate(spectrum.peak_labels):
                    if lab == label:
                        params = spectrum.peak_models[j].param_hints
                        if var in params.keys():
                            ind = self.spectrum_indices(spectrum)
                            self.arr[ind[0], ind[1]] = params[var]['value']

        self.img.set_data(self.arr)
        self.img.autoscale()

        if cmap is not None:
            self.img.set_cmap(cmap)
        if vmin is not None:
            self.img.norm.vmin = vmin
        if vmax is not None:
            self.img.norm.vmax = vmax
        if self.cbar is not None:
            self.cbar.update_normal(self.img)

        self.ax.get_figure().canvas.draw_idle()

    def set_marker(self, spectrum_id, canvas=None):
        """
        Set a marker on the plot.

        Parameters
        ----------
        spectrum_id: Spectrum object, str or a tuple of 2 floats
            a Spectrum object or its filename 'fname' or its (x, y) coordinates

        Returns
        -------
        None if spectrum_id is a spectrum object or a spectrum fname.
        A string corresponding to "{fname}  X={x}  Y={y}" if spectrum_id is a tuple (x, y).
        """
        if canvas is None:
            fig = self.ax.get_figure()
            canvas = fig.canvas

        if self.marker is not None:
            self.marker.remove()
            self.marker = None

        fname = None
        if isinstance(spectrum_id, tuple):
            x, y = spectrum_id
            x = self.xy_map[0][closest_index(self.xy_map[0], x)]
            y = self.xy_map[1][closest_index(self.xy_map[1], y)]
            fname = POLICY.format(name=self.fname, x=x, y=y)
        elif isinstance(spectrum_id, str):
            spectrum = self.get_spectrum(spectrum_id)
            x, y = self.spectrum_coords(spectrum)
        elif isinstance(spectrum_id, Spectrum):
            x, y = self.spectrum_coords(spectrum_id)
        else:
            raise IOError

        dx_ = np.pad(np.diff(self.xy_map[0]), pad_width=1, mode='edge')
        dx = 0.5 * (dx_[:-1] + dx_[1:])[closest_index(self.xy_map[0], x)]

        dy_ = np.pad(np.diff(self.xy_map[1]), pad_width=1, mode='edge')
        dy = 0.5 * (dy_[:-1] + dy_[1:])[closest_index(self.xy_map[1], y)]

        self.marker = Rectangle((x - dx / 2, y - dy / 2), dx, dy,
                                fill=False, edgecolor='r', linewidth=1.5)
        self.ax.add_patch(self.marker)

        canvas.draw_idle()
        return fname

    def export_to_csv(self, fname):
        """ Export 'arr' class attribute in a .csv file named 'fname' """
        if self.arr is not None:
            dfr = pd.DataFrame(self.arr)
            dfr.to_csv(fname, sep=';', header=False, index=False)

    @staticmethod
    def load_map(fname, arr0=None):
        """ Return a SpectraMap object from a .txt file issued either from the labspec file
            conversion or from the corresponding array 'arr0' previously saved and reloaded """
        spectra_map = SpectraMap()
        spectra_map.create_map(fname, arr0=arr0)
        return spectra_map
