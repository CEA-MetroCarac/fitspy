"""
Classes dedicated to spectra fitting
"""
import os
import warnings
import itertools
import csv
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider
from scipy.signal import find_peaks
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from lmfit import Model, report_fit, fit_report, Parameters
from lmfit.model import ModelResult
from lmfit.models import ConstantModel, LinearModel, ParabolicModel, \
    GaussianModel, ExponentialModel  # pylint:disable=unused-import

from fitspy.utils import closest_index, fileparts, check_or_rename
from fitspy.utils import save_to_json, load_from_json
from fitspy.models import gaussian, lorentzian, gaussian_asym, lorentzian_asym
from fitspy.models import pseudovoigt
from fitspy.app.utils import convert_dict_from_tk_variables
from fitspy.app.utils import dict_has_tk_variable

MODELS = {"Gaussian": gaussian,
          "Lorentzian": lorentzian,
          "PseudoVoigt": pseudovoigt,
          "GaussianAsym": gaussian_asym,
          "LorentzianAsym": lorentzian_asym}

BKG_MODELS = ['None', 'Constant', 'Linear', 'Parabolic', 'Gaussian',
              'Exponential']

KEYS = ['x0', 'ampli', 'fwhm', 'fwhm_l', 'fwhm_r', 'alpha']


def fit(params):
    """ Fitting function used in multiprocessing """
    x, y, models, method, fit_negative, max_ite = params
    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y
    spectrum.models = deepcopy(models)
    spectrum.fit(fit_method=method, fit_negative=fit_negative, max_ite=max_ite)
    return spectrum.result_fit.dumps()


def fit_mp(spectra, models,
           fit_method=None, fit_negative=None, max_ite=None, ncpus=None):
    """ Multiprocessing fit function applied to spectra """

    ncpus = ncpus or os.cpu_count()
    ncpus = min(ncpus, os.cpu_count())

    args = []
    for spectrum in spectra:
        x, y = spectrum.x, spectrum.y
        args.append((x, y, models, fit_method, fit_negative, max_ite))

    with ProcessPoolExecutor(max_workers=ncpus) as executor:
        results = tuple(executor.map(fit, args))

    for result_fit_json, spectrum in zip(results, spectra):
        spectrum.models = deepcopy(models)
        spectrum.fit_method = fit_method
        spectrum.fit_negative = fit_negative
        spectrum.max_ite = max_ite
        # dummy ModelResult that will be overwritten hereafter
        modres = ModelResult(Model(gaussian), Parameters())
        spectrum.result_fit = modres.loads(result_fit_json)
        spectrum.reassign_params()


class Spectrum:
    """
    Class dedicated to spectrum processing

    Attributes
    ----------
    fname: str
        Filename associated to spectrum to handle
    range_min, range_max: floats
        Range associated to the spectrum support to work with
    norm_mode: str
        Mode used for the spectrum normalization ('Maximum' or 'Attractor')
    norm_position_ref: float
        Reference position associated to the 'Attractor' mode during the
        normalization
    x0, y0: numpy.array((n))
        Arrays related to spectrum raw support and intensity (resp.)
    x, y: numpy.array((n))
        Arrays related to spectrum modified support and intensity (resp.)
    peaks: list of ints
        Indices of peaks
    peaks_params: dict
        Dictionary passed to scipy.signal.find_peaks for peaks determination.
        Could be a dictionary with Tkinter.Variable as values.
    models: list of lmfit.Model
        List of the lmfit models
    models_labels: list of str
        List of labels associated to the models. Default is ['1', '2', '3', ...]
    models_index: itertools.count
        Counter used for models indexing when creating a lmfit.Model
    bkg_model: str
        Background model to fit with the composite peaks models among :
        [None, 'Constant', 'Linear', 'Parabolic', 'Gaussian', 'Exponential']
    fit_method: str
        Method used for fitting. See lmfit.Model.fit().
        Default method is 'leastsq'.
    fit_negative: bool
        Activation keyword to take into account negative values when fitting.
        Default is False.
    max_ite: int
        Maximum number of iteration associated to the fitting process.
        An iteration consists in evaluating all the 'free' parameters once.
        Default is 200.
    result_fit: lmfit.ModelResult
        Object resulting from lmfit fitting
    baseline: Baseline object
        Baseline associated to the spectrum (to be removed)
    baseline_history: list of list
        Concatenation list of all baselines applied to the spectrum. Each item
        of the list consist in the max order of the baseline polynome and the
        (x, y) baseline points coordinates
    """

    def __init__(self):

        self.fname = None
        self.range_min = None
        self.range_max = None
        self.norm_mode = None
        self.norm_position_ref = None
        self.x0 = None
        self.y0 = None
        self.x = None
        self.y = None
        self.peaks = None
        self.peaks_params = {'distance': 20, 'prominence': None,
                             'width': None, 'height': None, 'threshold': None}
        self.models = []
        self.models_labels = []
        self.models_index = itertools.count(start=1)
        self.bkg_model = None
        self.fit_method = 'leastsq'
        self.fit_negative = False
        self.max_ite = 200
        self.result_fit = None

        self.baseline = BaseLine()
        self.baseline_history = []

    def set_attributes(self, dict_attrs, **fit_kwargs):
        """Set attributes from a dictionary (obtained from a .json reloading)"""

        for key, val in dict_attrs.items():
            if key != 'models':
                setattr(self, key, val)

        for key in ['fit_method', 'fit_negative', 'max_ite']:
            if key in fit_kwargs:
                setattr(self, key, fit_kwargs[key])

        self.models = []
        for _, dict_model in dict_attrs['models'].items():
            for model_name, param_hints in dict_model.items():
                index = next(self.models_index)
                ind_vars = ['x']
                pfx = f'm{index:02d}_'
                model_func = MODELS[model_name]
                model = Model(model_func, independent_vars=ind_vars, prefix=pfx)
                model.param_hints = param_hints
                self.models.append(model)

        # to make 'old' models still working
        if "models_labels" not in dict_attrs.keys():
            self.models_labels = list(map(str, range(1, len(self.models) + 1)))

    def preprocess(self):
        """ Preprocess the spectrum: call successively load_profile(),
        substract_baseline() and normalize() """

        self.load_profile(self.fname)
        for baseline_histo in self.baseline_history:
            self.baseline.mode = baseline_histo[0]
            self.baseline.order_max = baseline_histo[1]
            self.baseline.points = baseline_histo[2]
            if len(baseline_histo) == 4:
                self.baseline.sigma = baseline_histo[3]
            self.substract_baseline(add_to_history=False)
        self.baseline = BaseLine()
        self.normalize()

    def load_profile(self, fname):
        """ Load profile from 'fname' with 1 header line and 2 (x,y) columns"""

        # raw profile loading
        if self.x0 is None:
            self.fname = fname
            dfr = pd.read_csv(self.fname, sep=r'\s+|\t|,|;| ', engine='python',
                              skiprows=1, usecols=[0, 1], names=['x0', 'y0'])
            x0 = dfr['x0'].to_numpy()
            y0 = dfr['y0'].to_numpy()

            # reordering
            inds = np.argsort(x0)
            self.x0 = x0[inds]
            self.y0 = y0[inds]

        # (re)initialization or cropping
        if self.range_min is None:
            self.range_min = self.x0.min()
            self.range_max = self.x0.max()
            self.x = self.x0.copy()
            self.y = self.y0.copy()
        else:
            ind_min = closest_index(self.x0, self.range_min)
            ind_max = closest_index(self.x0, self.range_max)
            self.x = self.x0[ind_min:ind_max + 1].copy()
            self.y = self.y0[ind_min:ind_max + 1].copy()

    def normalize(self):
        """
        Normalize spectrum according to the 'Maximum' value or the nearest
        'Attractor' value from reference position, assuming that the baseline
        has been correctly defined (y_min value ~ 0)
        """
        if self.norm_mode == 'Maximum':
            self.y *= 100. / self.y.max()
        elif self.norm_mode == 'Attractor':
            ind = closest_index(self.x[self.peaks], self.norm_position_ref)
            self.y *= 100. / self.y[self.peaks][ind]

    def peaks_calculation(self):
        """ Calculate peaks positions ordered wrt decreasing intensities """

        if dict_has_tk_variable(self.peaks_params):
            peaks_params = convert_dict_from_tk_variables(self.peaks_params)
        else:
            peaks_params = self.peaks_params

        peaks, _ = find_peaks(self.y, **peaks_params)
        inds = np.argsort(self.y[peaks])
        self.peaks = peaks[inds[::-1]].astype(int).tolist()

    @staticmethod
    def create_model(model_name, index, ampli, x0,
                     fwhm=2, fwhm_l=2, fwhm_r=2, alpha=0.5):
        """
        Create a 'lmfit' model

        Parameters
        ----------
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'PseudoVoigt',
            'GaussianAsym', 'LorentzianAsym'
        index: int
            Index used to create the model 'prefix'
        ampli, x0: floats
            Paramaters associated to the model
        fwhm, fwhm_l, fwhm_r: floats, optional
            Optional parameters passed to the model.
            Default values are 2.
        alpha: float, optional
            Optional parameter passed to the 'PseudoVoigt' model.
            Default values is 0.5.
        Returns
        -------
        model: lmfit.Model
        """
        ind_vars = ['x']
        pfx = f'm{index:02d}_'
        model = Model(MODELS[model_name], independent_vars=ind_vars, prefix=pfx)

        kwargs_ampli = {'min': 0, 'max': np.inf, 'vary': True, 'expr': None}
        kwargs_fwhm = {'min': 0, 'max': 200, 'vary': True, 'expr': None}
        kwargs_x0 = {'min': x0 - 20, 'max': x0 + 20, 'vary': True, 'expr': None}
        kwargs_alpha = {'min': 0, 'max': 1, 'vary': True, 'expr': None}

        model.set_param_hint("ampli", value=ampli, **kwargs_ampli)
        model.set_param_hint("x0", value=x0, **kwargs_x0)

        if 'Asym' not in model_name:
            model.set_param_hint("fwhm", value=fwhm, **kwargs_fwhm)
        else:
            model.set_param_hint("fwhm_l", value=fwhm_l, **kwargs_fwhm)
            model.set_param_hint("fwhm_r", value=fwhm_r, **kwargs_fwhm)

        if "PseudoVoigt" in model_name:
            model.set_param_hint("alpha", value=alpha, **kwargs_alpha)

        return model

    def reassign_params(self):
        """ Reassign fitted 'params' to the 'models' """
        for model in self.models:
            for key in model.param_names:
                param = self.result_fit.params[key]
                model.set_param_hint(key[4:],  # remove prefix 'mXX_'
                                     value=param.value,
                                     min=param.min, max=param.max)

    def add_model(self, model_name, ind=None):
        """
        Add model (=peak) passing model_name and indice position or parameters

        Parameters
        ----------
        ind: int
            indice related to x-position for x0 peak localization
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'GaussianAsym',
            'LorentzianAsym'
        """
        dx = self.x[1] - self.x[0]
        index = next(self.models_index)
        model = self.create_model(model_name, index,
                                  ampli=self.y[ind], x0=self.x[ind],
                                  fwhm=dx, fwhm_l=dx, fwhm_r=dx)
        self.models.append(model)
        self.models_labels.append(f"{index}")

    def del_model(self, i):
        """ Delete the ith-model """
        del self.models[i]
        del self.models_labels[i]

    def reorder(self, key="x0", reverse=False):
        """ Return increasing or decreasing ordered models list from 'key' """
        vals = [model.param_hints[key]["value"] for model in self.models]
        inds = np.argsort(vals)
        if reverse:
            inds = inds[::-1]
        return [self.models[i] for i in inds]

    @staticmethod
    def get_model_name(model):
        """ from model class attribute return the function name associated
            Ex: Model('LorentzianAsym'...) -> 'lorentzian_asym' """
        name_fun = model.name.split(',')[0][6:]
        names = list(MODELS.keys())
        names_fun = [x.__name__ for x in MODELS.values()]
        ind = names_fun.index(name_fun)
        return names[ind]

    def remove_models(self):
        """ Remove all the models """
        self.models = []
        self.models_labels = []
        self.models_index = itertools.count(start=1)
        self.result_fit = None

    def fit(self, fit_method=None, fit_negative=None, max_ite=None,
            report=False, **kwargs):
        """ Fit the Spectrum models """
        # update class attributes
        if fit_method is not None:
            self.fit_method = fit_method
        if fit_negative is not None:
            self.fit_negative = fit_negative
        if max_ite is not None:
            self.max_ite = max_ite

        x, y = self.x, self.y
        weights = np.ones_like(x)
        if not self.fit_negative:
            weights[y < 0] = 0

        # composite model creation
        comp_model = self.models[0]
        if len(self.models) > 1:
            for model in self.models[1:]:
                comp_model += model

        # background model addition
        if self.bkg_model is not None:
            comp_model += eval(self.bkg_model + 'Model()')

        params = comp_model.make_params()

        # maximum function evaluation from max_ite
        # consider a minimum of 2 ite to avoid instabilities when fitting 1 by 1
        nvarys = 0  # number of 'free' parameters
        for _, val in comp_model.param_hints.items():
            nvarys += val['vary']
        max_nfev = max(2, self.max_ite) * nvarys

        self.result_fit = comp_model.fit(y, params, x=x, weights=weights,
                                         method=self.fit_method,
                                         max_nfev=max_nfev,
                                         # fit_kws={'xtol': 1.e-2},
                                         **kwargs)
        self.reassign_params()

        if report:
            report_fit(self.result_fit)

    def auto_baseline(self):
        """ Calculate 'baseline.points' considering 'baseline.distance'"""
        peaks, _ = find_peaks(-self.y, distance=self.baseline.distance)
        self.baseline.points[0] = list(self.x[peaks])
        self.baseline.points[1] = list(self.y[peaks])

    def substract_baseline(self, attached=True, sigma=None,
                           add_to_history=True):
        """ Substract the baseline to the spectrum """
        # substract baseline
        self.y -= self.baseline.eval(x=self.x,
                                     y=self.y if attached else None,
                                     sigma=sigma)

        # add baseline points in history
        if add_to_history:
            self.baseline_history.append([self.baseline.mode,
                                          self.baseline.order_max,
                                          self.baseline.points,
                                          self.baseline.sigma])

    def auto_peaks(self, model_name):
        """ Create automatically 'model_name' peak-models in the limit of
            5% of the maximum intensity peaks and nmax_nfev=400 """
        self.remove_models()
        self.peaks_calculation()
        y = y0 = self.y.copy()
        is_ok = True
        while is_ok:
            index = next(self.models_index)
            ind = np.argmax(y)
            dx = self.x[1] - self.x[0]
            model = self.create_model(model_name, index,
                                      ampli=self.y[ind], x0=self.x[ind],
                                      fwhm=dx, fwhm_l=dx, fwhm_r=dx)
            self.models.append(model)
            self.models_labels.append(index)
            self.fit()
            is_ok = self.result_fit.success
            y = y0 - self.result_fit.best_fit
            if y.max() < 0.05 * y0.max():
                is_ok = False

    def plot(self, ax, show_peaks=True, show_negative_values=False):
        """ Plot the spectrum with the fitted models and Return the profiles """
        lines = []
        x, y = self.x, self.y
        ax.plot(x, y, 'ko-', lw=0.5, ms=1)

        peaks = self.peaks
        if show_peaks and peaks is not None:
            ax.plot(x[peaks], y[peaks], 'go', ms=4, label="Attractors")

        if show_negative_values:
            ax.plot(x[y < 0], y[y < 0], 'ro', ms=4, label="Negative values")

        if self.result_fit is not None:
            ax.plot(x, self.result_fit.best_fit, 'b', label="Fitted profile")
        if len(self.models) > 0:
            ax.set_prop_cycle(None)
            for model in self.models:
                # remove temporarily 'expr' that can be related to another model
                param_hints_orig = deepcopy(model.param_hints)
                for key, _ in model.param_hints.items():
                    model.param_hints[key]['expr'] = ''
                params = model.make_params()
                # rassign 'expr'
                model.param_hints = param_hints_orig

                line, = ax.plot(x, model.eval(params, x=x))
                lines.append(line)

        return lines

    def plot_residual(self, ax, factor=1):
        """ Plot the residual x factor obtained after fitting """
        if self.result_fit is not None:
            ax.plot(self.x, factor * self.result_fit.residual, 'r',
                    label=f"residual (x{factor})")
            ax.legend()

    def save(self, fname_json=None):
        """ Return a 'dict_attrs' dictionary from the spectrum attributes and
            Save it if a 'fname_json' is given """

        excluded_keys = ['x0', 'y0', 'x', 'y',
                         'models', 'models_index', 'result_fit', 'baseline']
        dict_attrs = {}
        for key, val in vars(self).items():
            if key in excluded_keys:  # pass (x,y) coords and objects
                continue
            if isinstance(val, dict) and dict_has_tk_variable(val):
                val = convert_dict_from_tk_variables(val)
            dict_attrs[key] = val

        models = {}
        for i, model in enumerate(self.models):
            model_name = self.get_model_name(model)
            models[i] = {}
            models[i][model_name] = model.param_hints
        dict_attrs['models'] = models

        if fname_json is not None:
            save_to_json(fname_json, dict_attrs)

        return dict_attrs

    @staticmethod
    def load(fname_json):
        """ Return a Spectrum object created from a .json file reloading """

        dict_attrs = load_from_json(fname_json)

        spectrum = Spectrum()
        spectrum.set_attributes(dict_attrs)
        spectrum.preprocess()

        return spectrum


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


class Spectra(list):
    """
    Class dedicated to handle 'Spectrum' objects contained in a list

    Attributes
    ----------
    spectra_maps: list of SpectraMap objects

    Parameters
    ----------
    spectra_list: list of Spectrum objects, optional
    """

    def __init__(self, spectra_list=None):

        if spectra_list is not None:
            super().__init__(spectra_list)

        self.spectra_maps = []

    @property
    def fnames(self):
        """ Return all the fnames related to spectra AND spectra maps """
        return [spectrum.fname for spectrum in self.all]

    @property
    def all(self):
        """ Return all the spectra related to spectra AND spectra maps """
        spectra_all = []
        spectra_all.extend(self)
        for spectra_map in self.spectra_maps:
            spectra_all.extend(spectra_map)
        return spectra_all

    def get_objects(self, fname):
        """ Return spectrum and parent (spectra or spectra map)
            related to 'fname' """

        fnames = [spectrum.fname for spectrum in self]
        if fname in fnames:
            return self[fnames.index(fname)], self

        for spectra_map in self.spectra_maps:
            fnames = [spectrum.fname for spectrum in spectra_map]
            if fname in fnames:
                return spectra_map[fnames.index(fname)], spectra_map

        print(f"{fname} not found in spectra")
        return None, None

    def save_results(self, dirname_res, fnames=None):
        """
        Save spectra results (peaks parameters and statistics) in .csv files

        Parameters
        ----------
        dirname_res: str
            Dirname where to save the .csv files
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        """
        if fnames is None:
            fnames = self.fnames

        def write_params(fname_params, labels, models):
            with open(fname_params, 'w', newline='') as fid:
                writer = csv.writer(fid, delimiter=';')
                writer.writerow(['label', 'model'] + KEYS)
                for label, model in zip(labels, models):
                    vals = [label, Spectrum.get_model_name(model)]
                    for key in KEYS:
                        params = model.param_hints
                        if key in params.keys():
                            vals.append(params[key]['value'])
                        else:
                            vals.append('')
                    writer.writerow(vals)

        for fname in fnames:
            for spectrum in self.all:
                if spectrum.fname == fname:
                    _, name, _ = fileparts(fname)

                    # results saving
                    fname_params = os.path.join(dirname_res, name + '.csv')
                    fname_params = check_or_rename(fname_params)
                    labels, models = spectrum.models_labels, spectrum.models
                    if len(models) > 0:
                        write_params(fname_params, labels, models)

                    # statistics saving
                    fname_stats = os.path.join(dirname_res, name + '_stats.txt')
                    fname_stats = check_or_rename(fname_stats)
                    if spectrum.result_fit is not None:
                        with open(fname_stats, 'w') as fid:
                            fid.write(fit_report(spectrum.result_fit))
                    break

    def save_figures(self, dirname_fig, fnames=None, bounds=None):
        """
        Save spectra figures

        Parameters
        ----------
        dirname_fig: str
            Dirname where to save the figures
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        bounds: tuple of 2 tuples, optional
            Axis limits corresponding to ((xmin, xmax), (ymin, ymax))
        """
        if fnames is None:
            fnames = self.fnames

        for fname in fnames:
            for spectrum in self.all:
                if spectrum.fname == fname:
                    _, ax = plt.subplots()
                    if bounds is not None:
                        ax.set_xlim(bounds[0])
                        ax.set_ylim(bounds[1])
                    spectrum.plot(ax, show_peaks=False)
                    _, name, _ = fileparts(fname)
                    fname_fig = os.path.join(dirname_fig, name + '.png')
                    plt.savefig(fname_fig)
                    break

    @staticmethod
    def load_model(fname_json, ind=0):
        """
        Return a 'model' (dictionary) from a '.json' file

        Parameters
        ----------
        fname_json: str
            Filename associated to the spectra .json file where to extract the
            model
        ind: int, optional
            Spectrum index to consider as model in the spectra issued from the
            .json file reloading

        Returns
        -------
        model: dict
            The corresponding model
        """
        model = load_from_json(fname_json)[ind]
        return model

    def apply_model(self, model, fnames=None, ncpus=1, **fit_kwargs):
        """
        Apply 'model' to all or part of the spectra

        Parameters
        ----------
        model: dict
            Dictionary issued from a .json model reloading
        fnames: list of str, optional
            List of spectrum filename to handle.
            If None, apply the model to all the spectra
        ncpus: int, optional
            Number of CPU to work with in fitting
        fit_kwargs: dict
            Keywords arguments passed to spectrum.fit()
        """
        spectra = []
        for spectrum in self.all:
            if fnames is None or spectrum.fname in fnames:
                fname = spectrum.fname
                spectrum.set_attributes(deepcopy(model), **fit_kwargs)
                spectrum.fname = fname  # reassign the correct fname
                spectrum.preprocess()
                spectra.append(spectrum)

        if len(spectra) == 0:
            return

        if ncpus == 1:
            for spectrum in spectra:
                spectrum.fit()
        else:
            spectrum = spectra[0]
            models = deepcopy(spectrum.models)
            fit_method = spectrum.fit_method
            fit_negative = spectrum.fit_negative
            max_ite = spectrum.max_ite
            fit_mp(spectra, models, fit_method, fit_negative, max_ite, ncpus)

    def save(self, fname_json, fnames=None):
        """
        Save spectra in a .json file

        Parameters
        ----------
        fname_json: str
            Filename associated to the .json file for the spectra saving
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        """
        dirname = os.path.dirname(fname_json)
        if not os.path.isdir(dirname):
            print(f"directory {dirname} doesn't exist")
            return

        if fnames is None:
            fnames = self.fnames

        dict_spectra = {}
        for i, fname in enumerate(fnames):
            spectrum, _ = self.get_objects(fname)
            dict_spectra[i] = spectrum.save()

        save_to_json(fname_json, dict_spectra, indent=3)

    @staticmethod
    def load(fname_json):
        """ Return a Spectra object from a .json file """

        dict_spectra = load_from_json(fname_json)

        spectra = Spectra()
        fname_maps = []
        for i in range(len(dict_spectra.keys())):
            fname = dict_spectra[i]['fname']

            # spectrum attached to a SpectraMap object
            if "X=" in fname:
                fname_map = fname.split("  X=")[0]
                if fname_map not in fname_maps:
                    spectra.spectra_maps.append(SpectraMap.load_map(fname_map))
                    fname_maps.append(fname_map)
                ind = fname_maps.index(fname_map)
                spectra_map = spectra.spectra_maps[ind]
                for spectrum in spectra_map:
                    if fname == spectrum.fname:
                        spectrum.set_attributes(dict_spectra[i])
                        spectrum.preprocess()
                        break
            else:
                spectrum = Spectrum()
                spectrum.set_attributes(dict_spectra[i])
                spectrum.preprocess()
                spectra.append(spectrum)

        return spectra


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
