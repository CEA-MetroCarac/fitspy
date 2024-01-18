"""
Class dedicated to spectrum baseline manipulation
"""
import warnings
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d

from fitspy.utils import closest_index


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
        self.attached = True

    def add_point(self, x, y):
        """ Add point in the baseline """
        self.points[0].append(x)
        self.points[1].append(y)

        # reordering
        inds = np.argsort(self.points[0])
        self.points[0] = [self.points[0][ind] for ind in inds]
        self.points[1] = [self.points[1][ind] for ind in inds]

    def attach_points(self, x, y):
        """Return baseline points attached to (x,y) 'spectrum' profile coords"""
        assert x.size == y.size, 'x and y should have the same size'
        points = [[], []]
        inds = [closest_index(x, x0) for x0 in self.points[0]]
        if self.sigma is not None and self.sigma > 0:
            y = gaussian_filter1d(y, sigma=self.sigma)
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

    def eval(self, x, y=None):
        """ Evaluate the baseline on a 'x' support and a 'y' attached profile
            possibly smoothed with a gaussian filter """

        # use the original points or the attached points to an y-profile
        points = self.points if y is None else self.attach_points(x, y)

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

    def plot(self, ax, x=None, y=None, label=None, show_all=True):
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
        show_all: bool, optional
            Activation key to display the primary baseline components (before
            attachment)
        """
        if len(self.points[0]) == 0:
            return

        # use the original points or the attached points to an y-profile
        points = self.points if y is None else self.attach_points(x, y)

        if x is None:
            if len(points[0]) > 1:
                x = np.linspace(points[0][0], points[0][-1], 100)
            else:
                x = points[0][0]

        ax.plot(x, self.eval(x, y), 'g', label=label)
        if show_all:
            ax.plot(self.points[0], self.points[1], 'ko--', mfc='none')
            ax.plot(points[0], points[1], 'go', mfc='none')
