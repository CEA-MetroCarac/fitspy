"""
Class dedicated to spectrum processing
"""
import itertools
from copy import deepcopy
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from lmfit import Model, report_fit
from lmfit.models import ConstantModel, LinearModel, ParabolicModel, \
    ExponentialModel  # pylint:disable=unused-import

from fitspy.utils import closest_index
from fitspy.utils import save_to_json, load_from_json
from fitspy.app.utils import convert_dict_from_tk_variables
from fitspy.app.utils import dict_has_tk_variable
from fitspy.baseline import BaseLine
from fitspy import MODELS, BKG_MODELS


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
    bkg_model: lmfit.Model
        Background model to fit with the composite peaks models, among :
        [None, 'ConstantModel', 'LinearModel', 'ParabolicModel',
        'ExponentialModel']
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
            if key not in ['models', 'bkg_model']:
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

        if dict_attrs['bkg_model']:
            model_name, param_hints = list(dict_attrs['bkg_model'].items())[0]
            self.bkg_model = eval(f"{model_name}()")
            self.bkg_model.param_hints = param_hints

        # to make 'old' models still working
        if "models_labels" not in dict_attrs.keys() or \
                len(dict_attrs["models_labels"]) == 0:
            self.models_labels = list(map(str, range(1, len(self.models) + 1)))

    def preprocess(self):
        """ Preprocess the spectrum: call successively load_profile(),
        subtract_baseline() and normalize() """

        self.load_profile(self.fname)
        for baseline_histo in self.baseline_history:
            self.baseline.mode = baseline_histo[0]
            self.baseline.order_max = baseline_histo[1]
            self.baseline.points = baseline_histo[2]
            if len(baseline_histo) == 4:
                self.baseline.sigma = baseline_histo[3]
            self.subtract_baseline(add_to_history=False)
        self.baseline = BaseLine()
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
    def create_model(index, model_name, x0, ampli,
                     fwhm=2, fwhm_l=2, fwhm_r=2, alpha=0.5):
        """
        Create a 'lmfit' model

        Parameters
        ----------
        index: int
            Index used to create the model 'prefix'
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'PseudoVoigt',
            'GaussianAsym', 'LorentzianAsym'
        x0, ampli: floats
            Parameters associated to the model
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
        if self.bkg_model is not None:
            for key in self.bkg_model.param_names:
                param = self.result_fit.params[key]
                self.bkg_model.set_param_hint(key, value=param.value)

    def add_model(self, model_name, ind=None):
        """
        Add model (=peak) passing model_name and indice position or parameters

        Parameters
        ----------
        ind: int
            index related to x-position for x0 peak localization
        model_name: str
            Model name among 'Gaussian', 'Lorentzian', 'GaussianAsym',
            'LorentzianAsym'
        """
        dx = self.x[1] - self.x[0]
        index = next(self.models_index)
        model = self.create_model(index, model_name,
                                  x0=self.x[ind], ampli=self.y[ind],
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

    def get_bkg_model_name(self):
        """ from 'bkg_model' return the function name associated """
        if self.bkg_model is None:
            return 'None'
        else:
            return self.bkg_model.__class__.__name__

    def remove_models(self):
        """ Remove all the models """
        self.models = []
        self.models_labels = []
        self.models_index = itertools.count(start=1)
        self.result_fit = None

    def set_bkg_model(self, bkg_name):
        """ Set the 'bkg_model' attribute from 'bkg_name' """
        assert bkg_name in BKG_MODELS, f"{bkg_name} not in {BKG_MODELS}"
        if bkg_name == 'None':
            self.bkg_model = None
        else:
            self.bkg_model = eval(bkg_name + 'Model()')
            params = self.bkg_model.guess(self.y, self.x)
            for key, val in params.items():
                self.bkg_model.set_param_hint(key, value=val.value,
                                              min=-np.inf, max=np.inf,
                                              vary=True, expr=None)

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
        if len(self.models) > 0:
            comp_model = self.models[0]
        if len(self.models) > 1:
            for model in self.models[1:]:
                comp_model += model

        # background model addition
        if self.bkg_model is not None:
            if len(self.models) > 0:
                comp_model += self.bkg_model
            else:
                comp_model = self.bkg_model

        params = comp_model.make_params()

        # maximum function evaluation from max_ite
        # consider a minimum of 2 ite to avoid instabilities when fitting 1 by 1
        nvarys = 0  # number of 'free' parameters
        for param in params:
            nvarys += param['vary'] if 'vary' in param else 1
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

    def subtract_baseline(self, attached=True, sigma=None,
                          add_to_history=True):
        """ Subtract the baseline to the spectrum """
        # subtract baseline
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
            model = self.create_model(index, model_name,
                                      x0=self.x[ind], ampli=self.y[ind],
                                      fwhm=dx, fwhm_l=dx, fwhm_r=dx)
            self.models.append(model)
            self.models_labels.append(f"{index}")
            self.fit()
            is_ok = self.result_fit.success
            y = y0 - self.result_fit.best_fit
            if y.max() < 0.05 * y0.max():
                is_ok = False

    def plot(self, ax, show_peaks=True, show_negative_values=False,
             show_background=True):
        """ Plot the spectrum with the fitted models and Return the profiles """
        lines = []
        x, y = self.x, self.y
        ax.plot(x, y, 'ko-', lw=0.5, ms=1)

        peaks = self.peaks
        if show_peaks and peaks is not None:
            ax.plot(x[peaks], y[peaks], 'go', ms=4, label="Attractors")

        if show_negative_values:
            ax.plot(x[y < 0], y[y < 0], 'ro', ms=4, label="Negative values")

        if show_background and self.bkg_model is not None:
            params = self.bkg_model.make_params()
            y_bkg = self.bkg_model.eval(params, x=x)
            line, = ax.plot(x, y_bkg, 'k--', lw=2, label="Background")
            lines.append(line)

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
                         'models', 'models_index', 'bkg_model',
                         'result_fit', 'baseline']
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

        dict_attrs['bkg_model'] = {}
        if self.bkg_model is not None:
            dict_attrs['bkg_model'].update({self.get_bkg_model_name():
                                                self.bkg_model.param_hints})

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
