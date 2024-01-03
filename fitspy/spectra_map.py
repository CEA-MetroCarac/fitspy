"""
Classes dedicated to spectra fitting
"""
# import os
# import warnings
# import itertools
# import csv
# from copy import deepcopy
# from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
# from scipy.signal import find_peaks
# from scipy.interpolate import interp1d
# from scipy.ndimage import gaussian_filter1d
# from lmfit import Model, report_fit, fit_report, Parameters
# from lmfit.model import ModelResult
# from lmfit.models import ConstantModel, LinearModel, ParabolicModel, \
#     ExponentialModel  # pylint:disable=unused-import

from fitspy.utils import closest_index
# from fitspy.utils import closest_index, fileparts, check_or_rename
# from fitspy.utils import save_to_json, load_from_json
# from fitspy.models import gaussian, lorentzian, gaussian_asym, lorentzian_asym
# from fitspy.models import pseudovoigt
# from fitspy.app.utils import convert_dict_from_tk_variables
# from fitspy.app.utils import dict_has_tk_variable
from fitspy.spectra import Spectra
from fitspy.spectrum import Spectrum


# MODELS = {"Gaussian": gaussian,
#           "Lorentzian": lorentzian,
#           "PseudoVoigt": pseudovoigt,
#           "GaussianAsym": gaussian_asym,
#           "LorentzianAsym": lorentzian_asym}
#
# BKG_MODELS = ['None', 'Constant', 'Linear', 'Parabolic', 'Exponential']
#
# KEYS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']


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
    arr: numpy.ndarray(((len(shape_map[0]) * len(shape_map[1]), n))
        Array of spectra intensities (n-values) associated to the xy_map coords
    ax: Matplotlib.pyplot.axis
        Axis associated to the 2D-map displaying
    img: Matplotlib.image.AxesImage
        Image related to the 2D-map displaying
    cbar: Matplotlib.pyplot.colorbar
        Colorbar associated to the spectra 2D-map displaying
    xrange: tuple of 2 floats
        Range of intensity to consider in the 2D-map displaying
    slider: Matplotlib.widgets.RangeSlider
        Slider associated to the intensity integration range in the 2D-map
        displaying
    """

    def __init__(self):

        self.fname = None
        self.xy_map = None
        self.shape_map = None
        self.extent = None
        self.coords = None
        self.arr = None

        self.ax = None
        self.img = None
        self.cbar = None
        self.slider = None
        self.xrange = None

    def create_map(self, fname):
        """ Create map from .txt file issued from labspec files conversion """

        self.fname = fname
        dfr = pd.read_csv(fname, sep='\t', header=None)
        arr = dfr.to_numpy()

        x_map = x = list(np.sort(np.unique(arr[1:, 1])))
        y_map = y = list(np.sort(np.unique(arr[1:, 0])))

        # grid range associated to 'arr' to be consistent with the tools axis
        extent = [x[0] - 0.5 * (x[1] - x[0]), x[-1] + 0.5 * (x[-1] - x[-2]),
                  y[-1] + 0.5 * (y[-1] - y[-2]), y[0] - 0.5 * (y[1] - y[0])]

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
            spectrum.fname = f"{fname}  X={vals[1]}  Y={vals[0]}"
            intensity = vals[2:][inds]
            spectrum.x = x
            spectrum.y = intensity
            spectrum.x0 = spectrum.x.copy()
            spectrum.y0 = spectrum.y.copy()
            ind_flat = x_map.index(vals[1]) + y_map.index(vals[0]) * len(x_map)
            intensity_map[ind_flat, :] = intensity
            self.append(spectrum)
            coords.append([vals[1], vals[0]])

        self.xy_map = (x_map, y_map)
        self.shape_map = (len(self.xy_map[1]), len(self.xy_map[0]))
        self.extent = extent
        self.arr = intensity_map
        self.coords = coords

    def plot_map(self, ax):
        """ Plot the integrated spectra map intensities on 'ax' """

        self.ax = ax

        fig = self.ax.get_figure()
        fig.subplots_adjust(top=0.92)
        ax_slider = fig.add_axes([0.2, 0.92, 0.4, 0.05])

        arr = np.sum(self.arr, axis=1).reshape(self.shape_map)

        self.img = self.ax.imshow(arr, extent=self.extent)

        self.cbar = plt.colorbar(self.img, ax=self.ax)

        self.xrange = (self[0].x0.min(), self[0].x0.max())
        self.slider = RangeSlider(ax_slider, "Range ",
                                  self.xrange[0], self.xrange[1],
                                  valinit=self.xrange)
        self.slider.on_changed(self.plot_map_update)
        fig.canvas.draw()

    def plot_map_update(self, xrange=None):
        """ Update 'plot_map' """

        if xrange is not None:
            self.xrange = xrange

        imin = closest_index(self[0].x0, self.xrange[0])
        imax = closest_index(self[0].x0, self.xrange[1])

        arr = np.sum(self.arr[:, imin:imax + 1], axis=1).reshape(self.shape_map)

        self.img.set_data(arr)
        self.img.autoscale()
        self.cbar.update_normal(self.img)
        self.ax.get_figure().canvas.draw()

    @staticmethod
    def load_map(fname):
        """ Return a SpectraMap object from .txt file issued from labspec files
            conversion """
        spectra_map = SpectraMap()
        spectra_map.create_map(fname)
        return spectra_map
