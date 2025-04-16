"""
Class dedicated to spectrum baseline manipulation
"""
from functools import lru_cache
import warnings
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from scipy import sparse
from scipy.linalg import cholesky

from fitspy.core.utils import closest_index


class BaseLine:
    """
    Class dedicated to spectrum baseline manipulation

    Attributes
    ----------
    points: list of 2 lists
        List of the (x,y) baseline points coordinates
    mode: str or None
        Mode used to determine the baseline, among None, 'Semi-Auto' (semi-automatic
        baseline determination), 'Linear' (piecewise linear decomposition based
        on users points definition) and 'Polynomial'. Default mode is None
    coef: int
        Smoothing coefficient used in the 'Semi-Auto' mode.
        The larger coef is, the smoother the resulting baseline
    order_max: int
        Maximum order of the baseline polynomial evaluation
    distance: float
        Minimum distance between baseline point to consider when doing automatic
        detection with 'Spectrum.auto_baseline'
    sigma: float
        Smoothing coefficient (standard deviation) related to a gaussian
        filtering when defining baseline attached points to the spectrum
    attached: bool
        Activation key for attach the baseline points to the spectrum
    is_subtracted: bool
        Key used to indicate whether the baseline has been subtracted from the
        spectrum
    y_eval: numpy.ndarray(n)
        The baseline profile resulting from the 'eval' function
    """

    def __init__(self):
        self.mode = None
        self.coef = 5
        self.points = [[], []]
        self.order_max = 1
        self.sigma = 0
        self.attached = True
        self.is_subtracted = False
        self.y_eval = None

    def reinit(self):
        """ Reinitialize the main attributes """
        self.mode = None
        self.points = [[], []]
        self.is_subtracted = False
        self.y_eval = None

    def add_point(self, x, y):
        """ Add point in the baseline """
        self.points[0].append(x)
        self.points[1].append(y)

        # reordering
        inds = np.argsort(self.points[0])
        self.points[0] = [self.points[0][ind] for ind in inds]
        self.points[1] = [self.points[1][ind] for ind in inds]

    def attached_points(self, x, y):
        """Return baseline points attached to (x,y) 'spectrum' profile coords"""
        assert x.size == y.size, 'x and y should have the same size'
        attached_points = [[], []]
        inds = [closest_index(x, x0) for x0 in self.points[0]]
        if self.sigma > 0:
            y = gaussian_filter1d(y, sigma=self.sigma)
        attached_points[0] = [x[ind] for ind in inds]
        attached_points[1] = [y[ind] for ind in inds]
        return attached_points

    def load_baseline(self, fname):
        """ Load baseline from 'fname' with 1 header line and 2 (x,y) columns"""
        dfr = pd.read_csv(fname, sep=r'\s+|\t|,|;| ', engine='python',
                          skiprows=1, usecols=[0, 1], names=['x', 'y'])
        x = dfr['x'].to_numpy()
        y = dfr['y'].to_numpy()

        inds = np.argsort(x)
        self.points[0] = [x[ind] for ind in inds]
        self.points[1] = [y[ind] for ind in inds]

    def eval(self, x, y, attached=False):
        """ Evaluate the baseline on a 'x' support and a 'y' profile
            possibly smoothed with a gaussian filter """
        assert self.mode in [None, 'Semi-Auto', 'Linear', 'Polynomial']

        if self.mode is None:
            self.y_eval = None

        elif self.mode == 'Semi-Auto':
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                mask = np.zeros_like(y, dtype=bool)
                mask[::max(1, mask.size // 1024)] = True
                mask[y <= 0] = False
                self.y_eval = arpls(y=y[mask],
                                    edge_padding=100,
                                    differentiation_order=2,
                                    smoothing_factor=10 ** self.coef,
                                    cvg_tolerance=0.05,
                                    max_iterations=10)
                if False in mask:
                    func_interp = interp1d(x[mask], self.y_eval,
                                           fill_value="extrapolate")
                    self.y_eval = func_interp(x)

        else:
            points = self.points if not attached else self.attached_points(x, y)

            if len(points[1]) == 0:
                self.y_eval = None

            elif len(points[1]) == 1:
                self.y_eval = points[1] * np.ones_like(x)

            elif self.mode == 'Linear':
                func_interp = interp1d(points[0], points[1],
                                       fill_value="extrapolate")
                self.y_eval = func_interp(x)

            else:  # self.mode == 'Polynomial'
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    order = min(self.order_max, len(points[0]) - 1)
                    coefs = np.polyfit(points[0], points[1], order)
                    self.y_eval = np.polyval(coefs, x)

        return self.y_eval

    def plot(self, ax, x, y, attached=False, label="Baseline", show_all=True):
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
        label: str, optional
            Label displays in the figure
        show_all: bool, optional
            Activation key to display the primary baseline components (before
            attachment)
        """
        if self.mode is None:
            return

        if self.mode != 'Semi-Auto' and len(self.points[0]) == 0:
            return

        # use the original points or the attached points to an y-profile
        points = self.points if not attached else self.attached_points(x, y)

        ax.plot(x, self.eval(x, y, attached=attached), 'g', label=label)
        if show_all:
            ax.plot(self.points[0], self.points[1], 'ko--', mfc='none')
            ax.plot(points[0], points[1], 'go', mfc='none')


def arpls_origin(y, coef=4, ratio=0.05, itermax=10):
    r"""
    Asymmetrically Reweighted Penalized Least Squares smoothing extracted from:
    https://irfpy.irf.se/projects/ica/_modules/irfpy/ica/baseline.html#arpls

    Original article
    ----------------

    Sung-June Baek, Aaron Park, Young-Jin Ahna and Jaebum Choo,
    Analyst, 2015, 140, 250 (2015), https://doi.org/10.1039/C4AN01061B

    Parameters
    ----------
    y: numpy.ndarray(n)
        input data (i.e. spectrum intensity)
    coef: float, optional
        parameter that can be adjusted by user.
        The larger coef is, the smoother the resulting background, y_smooth
    ratio: float, optional
        wheighting deviations: 0 < ratio < 1, smaller values allow less negative
        values
    itermax: int, optional
        number of iterations to perform

    Returns
    -------
    y_smooth: numpy.ndarray(n)
        the fitted background
    """
    # pylint:disable=invalid-name, unused-variable

    N = len(y)
    D = sparse.eye(N, format='csc')
    # workaround: numpy.diff( ,2) does not work with sparse matrix
    D = D[1:] - D[:-1]
    D = D[1:] - D[:-1]

    H = 10 ** coef * D.T * D
    w = np.ones(N)
    for i in range(itermax):
        W = sparse.diags(w, 0, shape=(N, N))
        WH = sparse.csc_matrix(W + H)
        C = sparse.csc_matrix(cholesky(WH.todense()))
        y_smooth = sparse.linalg.spsolve(C, sparse.linalg.spsolve(C.T, w * y))
        d = y - y_smooth
        dn = d[d < 0]
        m = np.mean(dn)
        s = np.std(dn)
        wt = 1. / (1 + np.exp(2 * (d - (2 * s - m)) / s))
        if np.linalg.norm(w - wt) / np.linalg.norm(w) < ratio:
            break
        w = wt

    return y_smooth


def arpls(y, edge_padding=100, differentiation_order=2, smoothing_factor=1E4,
          cvg_tolerance=0.05, max_iterations=10):
    """
    Fits a baseline signal to the given spectrum using the Asymmetrically Reweighted Penalized
    Least Squares algorithm.

    This method iteratively fits a smooth baseline to a given spectrum by minimizing the effect
    of noise while preserving the original signal's characteristics.
    The ARPLS algorithm adjusts the baseline by asymmetrically penalizing negative deviations,
    making it particularly robust for spectral data with varying baseline shapes.

    optimized code from:
    https://stackoverflow.com/questions/78907548/trying-to-optimize-my-arpls-implementation

    Parameters
    ----------
    y: numpy.ndarray
        The 1D spectrum input array.
    edge_padding: int
        Number of points to pad on both ends of the spectrum to improve baseline fitting at the
        edges. Padding is done using edge values to minimize boundary effects.
    differentiation_order: int
        The order of the difference operator used in penalization.
        An order of 1 enforces a linear baseline (smoothing the first derivative), while an order
        of 2 enforces a quadratic baseline (smoothing the second derivative).
        Higher orders allow for more complex baseline shapes.
    smoothing_factor: float
        Controls the smoothness of the resulting baseline.
        Larger values suppress small fluctuations, which may lead to a smoother, but less sensitive
        baseline.
    cvg_tolerance: float
        Convergence criterion based on the change in weights between iterations
        Must be a value between 0 and 1. Smaller values allow less negative deviations, promoting
        a more accurate baseline fitting.
    max_iterations: int
        Maximum number of iterations to perform.
        The algorithm iteratively refines the baseline until the convergence criterion is met or
        the maximum number of iterations is reached.

    Returns
    -------
    y_smooth: numpy.ndarray(n)
        The fitted baseline signal array of the same length as the input spectrum (after removing
        padding).
    """
    y = np.pad(y, pad_width=edge_padding, mode="edge")
    weights, penalties, diagonal, diagonal_index = generate_penalties(y.shape[0],
                                                                      differentiation_order,
                                                                      smoothing_factor)

    for _ in range(max_iterations):
        penalties.data[diagonal_index] = diagonal + weights
        baseline = sparse.linalg.spsolve(penalties, weights * y,
                                         permc_spec="NATURAL", use_umfpack=False)
        residuals = y - baseline
        negative_residuals = residuals[residuals < 0]
        if not negative_residuals.size:
            break

        nr_mean = negative_residuals.mean(dtype=np.float64)
        nr_deviation = negative_residuals.std(dtype=np.float64)

        exponents = 2 * (residuals - (2 * nr_deviation - nr_mean)) / nr_deviation
        exponents.clip(-500, 500, out=exponents)
        updated_weights = 1.0 / (1.0 + np.exp(exponents, dtype=np.float64))

        if (np.linalg.norm(weights - updated_weights) / np.linalg.norm(weights)) < cvg_tolerance:
            break

        weights[:] = updated_weights

    y_smooth = baseline[edge_padding:-edge_padding]

    return y_smooth


@lru_cache(maxsize=2)
def generate_penalties(shape, differentiation_order, smoothing_factor):
    """ Generates the initial weights and smoothness penalty matrix """

    weights = np.ones(shape, dtype=np.float32)

    differences = sparse.csr_array(sparse.eye(shape, dtype=np.float64, format="csr"))
    for _ in range(differentiation_order):
        differences = sparse.csr_array(differences[1:] - differences[:-1])

    penalties = sparse.csc_array(smoothing_factor * (differences.T @ differences))
    penalties = sparse.coo_array(penalties.tocoo())
    penalties.sum_duplicates()

    diagonal_indices = np.where(penalties.row == penalties.col)[0]
    diagonal = penalties.data[diagonal_indices]
    penalties = sparse.csr_array(penalties.tocsr())

    return weights, penalties, diagonal, diagonal_indices


if __name__ == "__main__":
    from pathlib import Path
    import matplotlib.pyplot as plt
    from fitspy.core.spectrum import Spectrum
    from fitspy.core.spectra_map import SpectraMap
    import time

    DATA = Path(__file__).parents[2] / "examples" / "data"

    spectrum = Spectrum()
    spectrum.load_profile(fname=DATA / 'spectra_2' / 'spectrum_2_1.txt')
    x, y = spectrum.x, spectrum.y

    n = 100
    t0 = time.time()
    [arpls_origin(y) for _ in range(n)]
    t1 = time.time()
    [arpls(y) for _ in range(n)]
    t2 = time.time()

    _, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(x, arpls_origin(y), label='original')
    ax.plot(x, arpls(y), label=f'optimized (x{round((t1 - t0) / (t2 - t1))})')
    plt.legend()
    plt.show()

    # PERFORMANCES ON A FULL 2D-MAP

    # fname = DATA / "2D_maps" / "ordered_map.txt"
    # spectramap = SpectraMap()
    # spectramap.create_map(fname=DATA / "2D_maps" / "ordered_map.txt")
    # t0 = time.time()
    # for spectrum in spectramap:
    #     spectrum.baseline.mode = 'Semi-Auto'
    #     spectrum.eval_baseline()
    # print(f"TCPU: {time.time() - t0}")
    #
    # _, ax = plt.subplots()
    # ax.plot(spectrum.x, spectrum.y)
    # ax.plot(spectrum.x, spectrum.baseline.y_eval)
    # plt.show()
