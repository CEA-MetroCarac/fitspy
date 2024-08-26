"""
Class dedicated to spectrum processing
"""
import os
import re
import csv
import itertools
from copy import deepcopy
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.ndimage import uniform_filter1d
from lmfit.model import ModelResult
from lmfit.models import ConstantModel, LinearModel, ParabolicModel, \
    ExponentialModel, ExpressionModel  # pylint:disable=unused-import

from fitspy.utils import closest_index, fileparts, check_or_rename
from fitspy.utils import save_to_json, load_from_json
from fitspy.baseline import BaseLine
from fitspy import PEAK_MODELS, PEAK_PARAMS, BKG_MODELS, ATTRACTORS_PARAMS, \
    FIT_PARAMS


def create_model(model, model_name, prefix=None):
    """ Return a 'model' (peak_model or 'bkg_model') object """
    if isinstance(model, ExpressionModel):
        model = ExpressionModel(model.expr, independent_vars=['x'])
        model.__name__ = model_name
        model.name = model_name
        model.make_params()
        if prefix is not None:
            param_names = model.param_names.copy()
            model.prefix = prefix  # -> make model.param_names = []
            for name in param_names:  # reassign model.param_names with prefix
                model.param_names.append(prefix + name)
    elif isinstance(model, type):
        model = model()
    else:
        from lmfit import Model
        model = Model(model, independent_vars=['x'], prefix=prefix)
    model.name2 = model_name
    return model


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
    x0, y0: numpy.array((n0))
        Arrays related to the spectrum raw support and intensity (resp.)
    x, y: numpy.array((n))
        Arrays related to spectrum modified support and intensity (resp.)
    attractors: list of ints
        Indices of attractors
    attractors_params: dict
        Dictionary passed to scipy.signal.find_peaks for attractors
        determination. Could be a dictionary with Tkinter.Variable as values.
    outliers_limit: numpy.array((n0))
        Array related to the outliers limit associated to the raw data (x0, y0)
    baseline: Baseline object
        Baseline associated to the spectrum (to subract)
    baseline_history: list of list - DEPRECATED from v2024.2
        Concatenation list of all baselines applied to the spectrum. Each item
        of the list consist in the max order of the baseline polynom and the
        (x, y) baseline points coordinates.
    bkg_model: lmfit.Model
        Background model to fit with the composite peaks models, among :
        [None, 'ConstantModel', 'LinearModel', 'ParabolicModel',
        'ExponentialModel']
    peak_models: list of lmfit.Model
        List of peak models
    peak_labels: list of str
        List of labels associated to the peak models. Default is ['1', '2', ...]
    peak_index: itertools.count
        Counter used for peak models indexing when creating a lmfit.Model
    fit_params: dict
        Dictionary used to manage the fit parameters:
        * method: str
            Method used for fitting. See lmfit.Model.fit().
            Default method is 'Leastsq'.
        * fit_negative: bool
            Activation keyword to take into account negative values when
            fitting.
            Default is False.
        * fit_outliers: bool
            Activation keyword to take into account outliers points when
            fitting.
            Default is False.
        * max_ite: int
            Maximum number of iteration associated to the fitting process.
            An iteration consists in evaluating all the 'free' parameters once.
            Default is 200.
        * coef_noise: float
            Coefficient applied to the estimated noise amplitude to define a
            threshold below which the fit weights are set to 0, and local
            peak models are disabled .
            Default is 2.
        * xtol: float
            Relative error desired in the solution approximated by the 'Leastsq'
            or the 'Least_square' algorithm.
            Default is 1e-4.
    result_fit: lmfit.ModelResult
        Object resulting from lmfit fitting. Default value is a 'None' object
        (function) that enables to address a 'result_fit.success' status.
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
        self.attractors = None
        self.attractors_params = ATTRACTORS_PARAMS
        self.outliers_limit = None
        self.baseline = BaseLine()
        self.bkg_model = None
        self.peak_models = []
        self.peak_labels = []
        self.peak_index = itertools.count(start=1)
        self.fit_params = FIT_PARAMS
        self.result_fit = lambda: None
        self.plot_elements = {}

    def set_attributes(self, model_dict):
        """Set attributes from a dictionary (obtained from a .json reloading)"""

        keys = model_dict.keys()

        # compatibility with 'old' key names
        if 'peaks' in keys:
            model_dict['attractors'] = model_dict.pop('peaks')
        if 'peaks_params' in keys:
            model_dict['attractors_params'] = model_dict.pop('peaks_params')
        if 'models' in keys:
            model_dict['peak_models'] = model_dict.pop('models')
        if 'models_labels' in keys:
            model_dict['peak_labels'] = model_dict.pop('models_labels')
        if 'models_index' in keys:
            model_dict['peak_index'] = model_dict.pop('models_index')
        if 'fit_method' in keys:
            self.fit_params['method'] = model_dict.pop('fit_method')
        if 'fit_negative' in keys:
            self.fit_params['fit_negative'] = model_dict.pop('fit_negative')
        if 'max_ite' in keys:
            self.fit_params['max_ite'] = model_dict.pop('max_ite')
        if 'xtol' in keys:
            self.fit_params['xtol'] = model_dict.pop('xtol')

        for key, val in vars(self).items():
            if key in keys:
                if isinstance(val, dict) and key:
                    for key2 in val.keys():
                        if key2 in model_dict[key].keys():
                            val[key2] = model_dict[key][key2]
                else:
                    setattr(self, key, model_dict[key])

        if 'peak_models' in keys:
            self.peak_index = itertools.count(start=1)
            self.peak_models = []
            for _, dict_model in model_dict['peak_models'].items():
                for model_name, param_hints in dict_model.items():
                    model = PEAK_MODELS[model_name]
                    index = next(self.peak_index)
                    prefix = f'm{index:02d}_'
                    model = create_model(model, model_name, prefix)
                    model.param_hints = deepcopy(param_hints)
                    self.peak_models.append(model)

        if 'bkg_model' in keys and model_dict['bkg_model']:
            model_name, param_hints = list(model_dict['bkg_model'].items())[0]
            bkg_model = BKG_MODELS[model_name]
            self.bkg_model = create_model(bkg_model, model_name)
            self.bkg_model.name2 = model_name
            self.bkg_model.param_hints = deepcopy(param_hints)

        if 'baseline' in keys:
            self.baseline = BaseLine()
            for key in vars(self.baseline).keys():
                if key in model_dict['baseline'].keys():
                    setattr(self.baseline, key, model_dict['baseline'][key])

        if 'result_fit_success' in keys:
            self.result_fit.success = model_dict['result_fit_success']

        # COMPATIBILITY with 'old' models
        #################################

        if "peak_labels" not in keys or \
                len(model_dict["peak_labels"]) == 0:
            npeaks = len(self.peak_models)
            self.peak_labels = list(map(str, range(1, npeaks + 1)))

        if "baseline_history" in keys:
            baseline_history = model_dict["baseline_history"]
            if len(baseline_history) > 1:
                msg = "baseline_history with more than 1 item are no more valid"
                raise IOError(msg)
            if len(baseline_history) == 1:
                self.baseline.mode = baseline_history[0][0]
                self.baseline.order_max = baseline_history[0][1]
                self.baseline.points = baseline_history[0][2]
                if len(baseline_history[0]) == 4:
                    sigma = baseline_history[0][3]
                    self.baseline.sigma = sigma if sigma is not None else 0
                self.baseline.is_subtracted = True

        if "attached" in keys:
            self.baseline.attached = model_dict["attached"]

    def preprocess(self):
        """ Preprocess the spectrum: call successively load_profile(),
        subtract_baseline() and normalize() """

        self.load_profile(self.fname)
        if self.baseline.is_subtracted:
            self.baseline.is_subtracted = False
            self.subtract_baseline()
        self.normalize()

    def load_profile(self, fname, xmin=None, xmax=None):
        """ Load profile from 'fname' with 1 header line and 2 (x,y) columns"""

        if xmin is not None:
            self.range_min = xmin
        if xmax is not None:
            self.range_max = xmax

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

    def calculate_outliers(self):
        """ Return outliers points (x,y) coordinates """
        x_outliers, y_outliers = None, None
        if self.outliers_limit is not None:
            x0, y0 = self.x0, self.y0
            inds = np.where(y0 > self.outliers_limit)[0]
            mask = (self.x.min() <= x0[inds]) * (x0[inds] <= self.x.max())
            if np.any(mask):
                inds = inds[mask]
                x_outliers, y_outliers = x0[inds], y0[inds]
        return x_outliers, y_outliers

    @property
    def y_no_outliers(self):
        """ Return spectrum profile where outliers have been removed
            and replaced by interpolated values """
        x_outliers, _ = self.calculate_outliers()
        if x_outliers is None:
            return self.y
        else:
            mask = ~np.isin(self.x, x_outliers)
            x, y = self.x[mask], self.y[mask]  # coords without outliers
            func_interp = interp1d(x, y, fill_value="extrapolate")
            return func_interp(self.x)

    def normalize(self):
        """
        Normalize spectrum according to the 'Maximum' value or the nearest
        'Attractor' value from reference position, assuming that the baseline
        has been correctly defined (y_min value ~ 0)
        """
        if self.norm_mode == 'Maximum':
            self.y *= 100. / self.y_no_outliers.max()
        elif self.norm_mode == 'Attractor':
            ind = closest_index(self.x[self.attractors], self.norm_position_ref)
            self.y *= 100. / self.y_no_outliers[self.attractors][ind]

    def attractors_calculation(self):
        """ Calculate attractors positions ordered wrt decreasing intensities"""
        from scipy.signal import find_peaks
        attractors, _ = find_peaks(self.y_no_outliers, **self.attractors_params)
        inds = np.argsort(self.y[attractors])
        self.attractors = attractors[inds[::-1]].astype(int).tolist()

    @staticmethod
    def create_peak_model(index, model_name, x0, ampli,
                          fwhm=1., fwhm_l=1., fwhm_r=1., alpha=0.5):
        """
        Create a 'lmfit' model associated to one peak

        Parameters
        ----------
        index: int
            Index used to create the 'prefix' associated to the peak model
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'PseudoVoigt',
            'GaussianAsym', 'LorentzianAsym'
        x0: float
            Position of the peak model
        ampli: float
            Amplitude of the peak model.
        fwhm, fwhm_l, fwhm_r: floats, optional
            Optional parameters passed to the model related to the Full Width
            at Half Maximum. Default values are 1.
        alpha: float, optional
            Optional parameter passed to the 'PseudoVoigt' model.
            Default value is 0.5.

        Returns
        -------
        peak_model: lmfit.Model
        """
        # pylint:disable=unused-argument, unused-variable
        peak_model = PEAK_MODELS[model_name]
        prefix = f'm{index:02d}_'
        peak_model = create_model(peak_model, model_name, prefix)

        kwargs_ = {'min': -np.inf, 'max': np.inf, 'vary': True, 'expr': None}
        kwargs_ampli = {'min': 0, 'max': np.inf, 'vary': True, 'expr': None}
        kwargs_fwhm = {'min': 0, 'max': 200, 'vary': True, 'expr': None}
        kwargs_fwhm_l = {'min': 0, 'max': 200, 'vary': True, 'expr': None}
        kwargs_fwhm_r = {'min': 0, 'max': 200, 'vary': True, 'expr': None}
        kwargs_x0 = {'min': x0 - 20, 'max': x0 + 20, 'vary': True, 'expr': None}
        kwargs_alpha = {'min': 0, 'max': 1, 'vary': True, 'expr': None}

        for name in peak_model.param_names:
            name = name[4:]  # remove prefix 'mXX_'
            if name in PEAK_PARAMS:
                value, kwargs = eval(name), eval('kwargs_' + name)
            else:
                value, kwargs = 1, kwargs_
            peak_model.set_param_hint(name, value=value, **kwargs)

        return peak_model

    def reassign_params(self):
        """ Reassign fitted 'params' values to the 'models' """
        for peak_model in self.peak_models:
            for key in peak_model.param_names:
                param = self.result_fit.params[key]
                name = key[4:]  # remove prefix 'mXX_'
                peak_model.set_param_hint(name, value=param.value)
        if self.bkg_model is not None:
            for key in self.bkg_model.param_names:
                param = self.result_fit.params[key]
                self.bkg_model.set_param_hint(key, value=param.value)

    def add_peak_model(self, model_name, x0, ampli=None,
                       fwhm=None, fwhm_l=None, fwhm_r=None, alpha=0.5):
        """
        Add a peak model passing model_name and indice position or parameters

        Parameters
        ----------
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'GaussianAsym',
            'LorentzianAsym'
        x0: float
            Position of the peak model
        ampli: float, Optional
            Amplitude of the peak model. If None, consider the amplitude of the
            spectrum profile at position x0
        fwhm, fwhm_l, fwhm_r: floats, optional
            Optional parameters passed to the model related to the Full Width
            at Half Maximum. Default values are x-step size (x[1]-x[0]).
        alpha: float, optional
            Optional parameter passed to the 'PseudoVoigt' model.
            Default values is 0.5.
        """
        dx = max(np.diff(self.x))

        ampli = ampli or self.y_no_outliers[closest_index(self.x, x0)]
        fwhm = fwhm or dx
        fwhm_l = fwhm_l or dx
        fwhm_r = fwhm_r or dx

        index = next(self.peak_index)
        peak_model = self.create_peak_model(index, model_name, x0, ampli,
                                            fwhm, fwhm_l, fwhm_r, alpha)
        self.peak_models.append(peak_model)
        self.peak_labels.append(f"{index}")

    def del_peak_model(self, i):
        """ Delete the ith-peak model """
        del self.peak_models[i]
        del self.peak_labels[i]

    def reorder(self, key="x0", reverse=False):
        """ Return increasing or decreasing ordered models list from 'key' """
        vals = [model.param_hints[key]["value"] for model in self.peak_models]
        inds = np.argsort(vals)
        if reverse:
            inds = inds[::-1]
        return [self.peak_models[i] for i in inds]

    @staticmethod
    def get_model_name(model):
        """ from model class attribute return the function name associated
            Ex: Model('LorentzianAsym'...) -> 'lorentzian_asym' """
        if 'prefix' in model.name:
            name_fun = model.name.split(',')[0][6:]
        else:
            name_fun = re.search(r'\((.*?)\)', model.name).group(1)
        names = list(PEAK_MODELS.keys())
        names_fun = [x.__name__ for x in PEAK_MODELS.values()]
        ind = names_fun.index(name_fun)
        return names[ind]

    def remove_models(self):
        """ Remove all the models """
        self.peak_models = []
        self.peak_labels = []
        self.peak_index = itertools.count(start=1)
        self.bkg_model = None
        self.result_fit = lambda: None

    def set_bkg_model(self, bkg_name):
        """ Set the 'bkg_model' attribute from 'bkg_name' """
        assert bkg_name in BKG_MODELS.keys(), f"{bkg_name} not in {BKG_MODELS}"
        if bkg_name == 'None':
            self.bkg_model = None
        else:
            from lmfit import Model

            bkg_model = BKG_MODELS[bkg_name]
            if isinstance(bkg_model, type):
                self.bkg_model = bkg_model()
                params = self.bkg_model.guess(self.y, self.x)
            elif isinstance(bkg_model, Model):
                self.bkg_model = bkg_model
                params = self.bkg_model.make_params()
                for val in params.values():
                    val.value = 1
            else:
                self.bkg_model = Model(bkg_model, independent_vars=['x'])
                params = self.bkg_model.make_params()
                for val in params.values():
                    val.value = 1
            for key, val in params.items():
                self.bkg_model.set_param_hint(key, value=val.value,
                                              min=-np.inf, max=np.inf,
                                              vary=True, expr=None)
        self.bkg_model.name2 = bkg_name

    def fit(self, fit_method=None, fit_negative=None, fit_outliers=None,
            max_ite=None, coef_noise=None, xtol=None, reinit_guess=True,
            **kwargs):
        """
        Fit the peaks and background models

        Parameters
        ----------
        fit_method: str, optional
            Method passed to lmfit.fit() like ‘leastsq’, ‘least_squares’,
            ‘nelder’, ‘slsqp’, ... (see the lmfit documentation).
            Default value is 'leastsq'.
        fit_negative: bool, optional
            Activation key to take into account negative values during the fit.
            Default value is False.
        fit_outliers: bool, optional
            Activation key to take into account outliers during the fit.
            Default value is False.
        max_ite: int, optional
            Number of maximum iterations (1 iteration corresponds to 1 gradient
            descent of all the variables).
            Default value is 200.
        coef_noise: float, optional
            Multiplication factor associated with the estimated noise level.
            Default value is 1.
        xtol: float, optional
            Relative tolerance associated with the ‘leastsq’ and the
            ‘least_squares’ fit algorithm.
            Default value is 0.0001.
        reinit_guess: bool, optional
            Key to adapt initial values for 'ampli' and 'fwhm', 'fwhm_l' or
            'fwhm_r' to the spectrum intensity at the corresponding point 'x0'.
            Default value is True.
        kwargs: dict, optional
            Dictionary of optional arguments passed to lmfit.fit()
        """
        # """  """
        # update class attributes
        if fit_method is not None:
            self.fit_params['method'] = fit_method
        if fit_negative is not None:
            self.fit_params['fit_negative'] = fit_negative
        if fit_outliers is not None:
            self.fit_params['fit_outliers'] = fit_outliers
        if max_ite is not None:
            self.fit_params['max_ite'] = max_ite
        if coef_noise is not None:
            self.fit_params['coef_noise'] = coef_noise
        if xtol is not None:
            self.fit_params['xtol'] = xtol

        x, y = self.x, self.y
        weights = np.ones_like(x)
        vary_init = None
        noise_level = 0

        if not self.fit_params['fit_negative']:
            weights[y < 0] = 0

        if not self.fit_params['fit_outliers']:
            x_outliers, _ = self.calculate_outliers()
            if x_outliers is not None:
                weights[np.where(np.isin(x, x_outliers))] = 0

        if self.fit_params['coef_noise'] > 0:
            delta = np.diff(y)
            delta1, delta2 = delta[:-1], delta[1:]
            mask = np.sign(delta1) * np.sign(delta2) == -1
            ampli_noise = np.median(np.abs(delta1[mask] - delta2[mask]) / 2)
            noise_level = self.fit_params['coef_noise'] * ampli_noise
            weights[y < noise_level] = 0

        # composite model creation
        comp_model = None
        if len(self.peak_models) > 0:
            comp_model = self.peak_models[0]
        if len(self.peak_models) > 1:
            for peak_model in self.peak_models[1:]:
                comp_model += peak_model

        # reinitialize 'ampli' and 'fwhm'
        if reinit_guess and comp_model is not None:
            fwhm_min = max(np.diff(x))
            for component in comp_model.components:
                params = component.param_hints
                ind = closest_index(x, params['x0']['value'])
                params['ampli']['value'] = self.y_no_outliers[ind]
                for key in params.keys():
                    if key in ['fwhm', 'fwhm_l', 'fwhm_r']:
                        param = params[key]
                        param['value'] = max(fwhm_min, param['value'])

        # disable a peak_models in a noisy areas
        if noise_level > 0 and comp_model is not None:

            # save initial 'vary' state
            vary_init = [param['vary'] for component in comp_model.components
                         for param in component.param_hints.values()]

            # set 'ampli'/'fwhm' to 0 and 'vary' to False in noisy areas
            ymean = uniform_filter1d(y, size=5)
            for component in comp_model.components:
                params = component.param_hints
                ind = closest_index(x, params['x0']['value'])
                if ymean[ind] < noise_level:
                    params['ampli']['value'] = 0
                    for key in params.keys():
                        if key in ['fwhm', 'fwhm_l', 'fwhm_r']:
                            params[key]['value'] = 0
                        params[key]['vary'] = False

        # bkg_model addition
        if self.bkg_model is not None:
            if len(self.peak_models) > 0:
                comp_model += self.bkg_model
            else:
                comp_model = self.bkg_model

        params = comp_model.make_params()

        # maximum function evaluation from max_ite
        # consider a minimum of 2 ite to avoid instabilities when fitting 1 by 1
        nvarys = 0  # number of 'free' parameters
        for param in params:
            nvarys += param['vary'] if 'vary' in param else 1
        max_nfev = max(2, self.fit_params['max_ite']) * nvarys

        fit_kws = {}
        if 'fit_kws' in kwargs:
            fit_kws = kwargs['fit_kws']  # example: fit_kws={'xtol': 1.e-2}
            kwargs.pop('fit_kws')
        if self.fit_params['method'] in ['leastsq', 'least_squares']:
            fit_kws.update({'xtol': self.fit_params['xtol']})

        self.result_fit = comp_model.fit(y, params, x=x, weights=weights,
                                         method=self.fit_params['method'],
                                         max_nfev=max_nfev,
                                         fit_kws=fit_kws,
                                         **kwargs)
        self.reassign_params()

        # reassign initial 'vary' values
        if vary_init is not None:
            i = itertools.count()
            components = comp_model.components
            if self.bkg_model is not None:
                components = components[:-1]
            for component in components:
                for param in component.param_hints.values():
                    param['vary'] = vary_init[next(i)]

    def auto_baseline(self):
        """ Calculate 'baseline.points' considering 'baseline.distance'"""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(-self.y_no_outliers,
                              distance=self.baseline.distance)
        self.baseline.points[0] = list(self.x[peaks])
        self.baseline.points[1] = list(self.y[peaks])

    def subtract_baseline(self):
        """ Subtract the baseline to the spectrum
            if this has not been done previously """
        if not self.baseline.is_subtracted:
            y = self.y_no_outliers if self.baseline.attached else None
            self.y -= self.baseline.eval(x=self.x, y=y)
            self.baseline.is_subtracted = True

    def auto_peaks(self, model_name):
        """ Create automatically 'model_name' peak-models in the limit of
            5% of the maximum intensity peaks and nmax_nfev=400 """
        self.remove_models()
        self.attractors_calculation()
        y = y0 = self.y_no_outliers.copy()
        dx = max(np.diff(self.x))

        is_ok = True
        while is_ok:
            index = next(self.peak_index)
            ind = np.argmax(y)
            peak_model = self.create_peak_model(index, model_name,
                                                x0=self.x[ind],
                                                ampli=self.y[ind],
                                                fwhm=dx, fwhm_l=dx, fwhm_r=dx)
            self.peak_models.append(peak_model)
            self.peak_labels.append(f"{index}")
            self.fit(reinit_guess=False)
            is_ok = self.result_fit.success
            y = y0 - self.result_fit.best_fit
            if y.max() < 0.05 * y0.max():
                is_ok = False

    def set_main_line(self, ax, linewidth=0.5):
        x,y = self.x, self.y
        main_line, = ax.plot(x, y, 'ko-', lw=linewidth, ms=1)
        self.plot_elements['main_line'] = main_line

    def set_attractors(self, ax, ms=4):
        self.attractors_calculation()
        if self.attractors is not None:
            x,y,inds = self.x, self.y, self.attractors
            attractors, = ax.plot(x[inds], y[inds], 'go', ms=ms, label="Attractors")
            self.plot_elements['attractors'] = attractors

    def set_outliers(self, ax):
        """ Set outliers points in the spectrum """
        x_outliers, y_outliers = self.calculate_outliers()
        if x_outliers is not None:
            outliers, = ax.plot(x_outliers, y_outliers, 'o', c='lime', label='Outliers')
            self.plot_elements['outliers'] = outliers

    def set_outliers_limit(self, ax):
        """ Set outliers limit in the spectrum """
        if self.outliers_limit is not None:
            imin, imax = list(self.x0).index(self.x[0]), list(self.x0).index(self.x[-1])
            y_lim = self.outliers_limit[imin:imax + 1]
            outliers_limit, = ax.plot(self.x, y_lim, 'r-', lw=2, label='Outliers limit')
            self.plot_elements['outliers_limit'] = outliers_limit

    def set_negative_values(self, ax):
        """ Set negative values in the spectrum """
        negative_values, = ax.plot(self.x[self.y < 0], self.y[self.y < 0], 'ro', ms=4, label='Negative values')
        self.plot_elements['negative_values'] = negative_values

    def set_noise_level(self, ax):
        """ Set noise level in the spectrum """
        ampli_noise = np.median(np.abs(self.y[:-1] - self.y[1:]) / 2)
        y_noise_level = self.fit_params['coef_noise'] * ampli_noise
        noise_level = ax.hlines(y=y_noise_level, xmin=self.x[0], xmax=self.x[-1], colors='r',
                                linestyles='dashed', lw=0.5, label="Noise level")
        self.plot_elements['noise_level'] = noise_level

    def set_baseline(self, ax):
        """ Set the baseline in the spectrum """
        if self.baseline.is_subtracted:
            baseline = self.baseline.plot(ax, x=self.x, show_all=False)
            self.plot_elements['baseline'] = baseline

    def set_background(self, ax, flag=True):
        """ Set the background in the spectrum """
        if self.bkg_model is not None:
            self.y_bkg = self.bkg_model.eval(self.bkg_model.make_params(), x=self.x)
        else:
            self.y_bkg = np.zeros_like(self.x)
        if flag:
            background, = ax.plot(self.x, self.y_bkg, 'k--', lw=0.5, label="Background")
            self.plot_elements['background'] = background

    def set_peak_models(self, ax, flag=True):
        """ Set the peak models in the spectrum """
        self.y_peaks = np.zeros_like(self.x)
        peak_lines = []
        for peak_model in self.peak_models:
            param_hints_orig = deepcopy(peak_model.param_hints)
            for key, _ in peak_model.param_hints.items():
                peak_model.param_hints[key]['expr'] = ''
            params = peak_model.make_params()
            peak_model.param_hints = param_hints_orig

            y_peak = peak_model.eval(params, x=self.x)
            self.y_peaks += y_peak
            if flag:
                peak_line, = ax.plot(self.x, y_peak, lw=0.5)
                peak_lines.append(peak_line)
        self.plot_elements['peak_models'] = peak_lines

    def plot(self, ax,
         show_attractors=True, show_outliers=True, show_outliers_limit=True,
         show_negative_values=True, show_noise_level=True,
         show_baseline=True, show_background=True,
         show_peak_models=True, show_result=True):
        """Plot the spectrum with the peak models"""
        plot_elements = {}
        linewidth = 1 if hasattr(self.result_fit, 'success') and self.result_fit.success else 0.5

        self.set_main_line(ax, linewidth)

        if show_attractors:
            self.set_attractors(ax)

        if show_outliers:
            self.set_outliers(ax)

        if show_outliers_limit:
            self.set_outliers_limit(ax)

        if show_negative_values:
            self.set_negative_values(ax)

        if show_noise_level:
            self.set_noise_level(ax)

        if show_baseline:
            self.set_baseline(ax)

        self.set_background(ax, show_background)

        self.set_peak_models(ax, show_peak_models)

        if show_result and hasattr(self.result_fit, 'success'):
            y_fit = self.y_bkg + self.y_peaks
            result, = ax.plot(self.x, y_fit, 'b', lw=linewidth, label="Fitted profile")
            plot_elements['result'] = result
        # return plot_elements

    def plot_residual(self, ax, factor=1):
        """ Plot the residual x factor obtained after fitting """
        x, y = self.x, self.y
        if hasattr(self.result_fit, 'residual'):
            residual = self.result_fit.residual
        else:
            y_fit = np.zeros_like(x)
            for peak_model in self.peak_models:
                y_fit += peak_model.eval(peak_model.make_params(), x=x)
            if self.bkg_model is not None:
                bkg_model = self.bkg_model
                y_fit += bkg_model.eval(bkg_model.make_params(), x=x)
            residual = y - y_fit
        ax.plot(x, factor * residual, 'r', label=f"residual (x{factor})")
        ax.legend()

    def save_params(self, dirname_params):
        """ Save fit parameters in a '.csv' file located in 'dirname_params' """
        _, name, _ = fileparts(self.fname)
        fname_params = os.path.join(dirname_params, name + '.csv')
        fname_params = check_or_rename(fname_params)
        if len(self.peak_models) == 0:
            return

        peak_models = self.peak_models
        peak_labels = self.peak_labels
        with open(fname_params, 'w', newline='') as fid:
            writer = csv.writer(fid, delimiter=';')
            writer.writerow(['label', 'model'] + PEAK_PARAMS)
            for peak_label, peak_model in zip(peak_labels, peak_models):
                vals = [peak_label, self.get_model_name(peak_model)]
                for key in PEAK_PARAMS:
                    params = peak_model.param_hints
                    if key in params.keys():
                        vals.append(params[key]['value'])
                    else:
                        vals.append('')
                writer.writerow(vals)

    def save_stats(self, dirname_stats):
        """ Save statistics in a '.txt' file located in 'dirname_stats' """
        from lmfit import fit_report
        if isinstance(self.result_fit, ModelResult):
            _, name, _ = fileparts(self.fname)
            fname_stats = os.path.join(dirname_stats, name + '_stats.txt')
            fname_stats = check_or_rename(fname_stats)
            with open(fname_stats, 'w') as fid:
                fid.write(fit_report(self.result_fit))

    def save(self, fname_json=None):
        """ Return a 'model_dict' dictionary from the spectrum attributes and
            Save it if a 'fname_json' is given """

        excluded_keys = ['x0', 'y0', 'x', 'y', 'outliers_limit',
                         'peak_models', 'peak_index', 'bkg_model',
                         'result_fit', 'baseline']
        model_dict = {}
        for key, val in vars(self).items():
            if key not in excluded_keys:
                model_dict[key] = val

        model_dict['baseline'] = dict(vars(self.baseline).items())

        bkg_model = self.bkg_model
        if bkg_model is not None:
            model_dict['bkg_model'] = {bkg_model.name2: bkg_model.param_hints}

        peak_models = {}
        for i, peak_model in enumerate(self.peak_models):
            model_name = self.get_model_name(peak_model)
            peak_models[i] = {}
            peak_models[i][model_name] = peak_model.param_hints
        model_dict['peak_models'] = peak_models

        if hasattr(self.result_fit, 'success'):
            model_dict['result_fit_success'] = self.result_fit.success

        if fname_json is not None:
            save_to_json(fname_json, model_dict)

        return model_dict

    @staticmethod
    def load(fname_json):
        """ Return a Spectrum object created from a .json file reloading """

        model_dict = load_from_json(fname_json)

        spectrum = Spectrum()
        spectrum.set_attributes(model_dict)
        spectrum.preprocess()

        return spectrum
