"""
Classes dedicated to spectra fitting
"""
# import os
import warnings
# import itertools
# import csv
# from copy import deepcopy
# from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.widgets import RangeSlider
# from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
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

# MODELS = {"Gaussian": gaussian,
#           "Lorentzian": lorentzian,
#           "PseudoVoigt": pseudovoigt,
#           "GaussianAsym": gaussian_asym,
#           "LorentzianAsym": lorentzian_asym}
#
# BKG_MODELS = ['None', 'Constant', 'Linear', 'Parabolic', 'Exponential']
#
# KEYS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']


class BaseLine:
    """
    Class dedicated to spectrum baseline manipulation

    Attributes
    ----------
    points: list of 2 lists
        List of the (x,y) baseline points coordinates
    order_max: int
        Maximum order of the baseline polynomial evaluation
    distance: float
        Minimum distance between baseline point to consider when doing automatic
        detection with 'Spectrum.auto_baseline'
    sigma: float
        Smoothing coefficient related to a gaussian filtering when defining
        baseline attached points to the spectrum
    """

    def __init__(self):
        self.points = [[], []]
        self.mode = "Linear"
        self.order_max = 1
        self.distance = 100
        self.sigma = None

    def add_point(self, x, y):
        """ Add point in the baseline """
        self.points[0].append(x)
        self.points[1].append(y)

        # reordering
        inds = np.argsort(self.points[0])
        self.points[0] = [self.points[0][ind] for ind in inds]
        self.points[1] = [self.points[1][ind] for ind in inds]

    def attach_points(self, x, y, sigma=None):
        """Return baseline points attached to (x,y) 'spectrum' profile coords"""
        assert x.size == y.size, 'x and y should have the same size'
        self.sigma = sigma
        points = [[], []]
        inds = [closest_index(x, x0) for x0 in self.points[0]]
        if sigma is not None and sigma > 0:
            y = gaussian_filter1d(y, sigma=sigma)
        points[0] = [x[ind] for ind in inds]
        points[1] = [y[ind] for ind in inds]
        return points

    def load_baseline(self, fname):
        """ Load baseline from 'fname' with 1 header line and 2 (x,y) columns"""
        dfr = pd.read_csv(fname, sep=r'\s+|\t|,|;| ', engine='python',
                          skiprows=1, usecols=[0, 1], names=['x', 'y'])
        x = dfr['x'].to_numpy()
        y = dfr['y'].to_numpy()

        inds = np.argsort(x)
        self.points[0] = [x[ind] for ind in inds]
        self.points[1] = [y[ind] for ind in inds]

    def eval(self, x, y=None, sigma=None):
        """ Evaluate the baseline on a 'x' support and a 'y' attached profile
            possibily smoothed with a gaussian filter """

        # use the original points or the attached points to an y-profile
        points = self.points if y is None else self.attach_points(x, y, sigma)

        if len(points[1]) == 1:
            return points[1] * np.ones_like(x)

        if self.mode == 'Linear':
            func_interp = interp1d(points[0], points[1],
                                   fill_value="extrapolate")
            return func_interp(x)

        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                order = min(self.order_max, len(points[0]) - 1)
                coefs = np.polyfit(points[0], points[1], order)
            return np.polyval(coefs, x)

    def plot(self, ax, x=None, y=None, sigma=None):
        """
        Plot the baseline and its related points

        Parameters
        ----------
        ax: Matplotlib.Axes
            Axis to work with
        x: iterable of floats, optional
            Support to consider for the baseline plotting.
            If None, create a support from the baseline extrema points
        y: iterable of floats, optional
            Values for baseline points attachment (if provided), sharing the
            same x coordinates
        sigma: float, optional
            Smoothing gaussian filter coefficient applied to 'y'
        """
        if len(self.points[0]) == 0:
            return

        # use the original points or the attached points to an y-profile
        points = self.points if y is None else self.attach_points(x, y, sigma)

        if x is None:
            if len(points[0]) > 1:
                x = np.linspace(points[0][0], points[0][-1], 100)
            else:
                x = points[0][0]

        ax.plot(x, self.eval(x, y, sigma), 'g')
        ax.plot(self.points[0], self.points[1], 'ko--', mfc='none')
        ax.plot(points[0], points[1], 'go', mfc='none')
