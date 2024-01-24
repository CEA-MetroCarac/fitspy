"""
Class dedicated to handle 'Spectrum' objects contained in a list managed by
"Spectra"
"""
import os
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from lmfit.models import ExpressionModel

from fitspy.utils import fileparts, save_to_json, load_from_json
from fitspy.spectrum import Spectrum
from fitspy import MODELS


def fit(params):
    """ Fitting function used in multiprocessing """
    x, y, models, method, fit_negative, max_ite = params
    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y

    models_ = []
    for model in models:
        if isinstance(model, dict):
            model_ = ExpressionModel(model['expr'], independent_vars=['x'])
            model_.__name__ = model['name']
            model_.param_hints = deepcopy(model['param_hints'])
            model_.make_params()
            param_names = model_.param_names.copy()
            model_.prefix = model['prefix']  # -> make model.param_names = []
            for name in param_names:  # reassign model.param_names with prefix
                model_.param_names.append(model['prefix'] + name)
            models_.append(model_)
        else:
            models_.append(model)

    spectrum.models = models_
    spectrum.fit(fit_method=method, fit_negative=fit_negative, max_ite=max_ite)
    return spectrum.result_fit.values, spectrum.result_fit.success


def fit_mp(spectra, models, bkg_model,
           fit_method=None, fit_negative=None, max_ite=None, ncpus=None):
    """ Multiprocessing fit function applied to spectra """

    ncpus = ncpus or os.cpu_count()
    ncpus = min(ncpus, os.cpu_count())

    def picklable_model(model):
        if isinstance(model, ExpressionModel):
            return {'expr': model.expr,
                    'name': model.__name__,
                    'prefix': model.prefix,
                    'param_hints': model.param_hints}
        else:
            return model

    args = []
    for spectrum in spectra:
        x, y = spectrum.x, spectrum.y
        models_ = []
        for model in models:
            models_.append(picklable_model(model))
        models_.append(picklable_model(bkg_model))
        args.append((x, y, models_, fit_method, fit_negative, max_ite))

    with ProcessPoolExecutor(max_workers=ncpus) as executor:
        results = tuple(executor.map(fit, args))

    # dictionary of custom function names and definitions
    funcdefs = {}
    for val in MODELS.values():
        funcdefs[val.__name__] = val

    for (values, success), spectrum in zip(results, spectra):
        spectrum.result_fit.success = success
        for model in spectrum.models:
            for key in model.param_names:
                model.set_param_hint(key[4:], value=values[key])
        for key in spectrum.bkg_model.param_names:
            spectrum.bkg_model.set_param_hint(key, value=values[key])


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

        for fname in fnames:
            spectrum, _ = self.get_objects(fname)
            if hasattr(spectrum.result_fit, "success"):
                spectrum.save_params(dirname_res)
                spectrum.save_stats(dirname_res)

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
            spectrum, _ = self.get_objects(fname)
            _, ax = plt.subplots()
            spectrum.plot(ax, show_peaks=False)
            if bounds is not None:
                ax.set_xlim(bounds[0])
                ax.set_ylim(bounds[1])
            _, name, _ = fileparts(fname)
            fname_fig = os.path.join(dirname_fig, name + '.png')
            plt.savefig(fname_fig)

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

    def apply_model(self, model, fnames=None, ncpus=1,
                    fit_only=False, **fit_kwargs):
        """
        Apply 'model' to all or part of the spectra

        Parameters
        ----------
        model: dict
            Dictionary related to the Spectrum object attributes (obtained from
            Spectrum.save())
        fnames: list of str, optional
            List of spectrum filename to handle.
            If None, apply the model to all the spectra
        ncpus: int, optional
            Number of CPU to work with in fitting
        fit_only: bool, optional
            Activation key to process only fittin
        fit_kwargs: dict
            Keywords arguments passed to spectrum.fit()
        """
        if fnames is None:
            fnames = self.all

        if len(fnames) == 0:
            return

        spectra = []
        for fname in fnames:
            spectrum, _ = self.get_objects(fname)
            spectrum.set_attributes(model, **fit_kwargs)
            spectrum.fname = fname  # reassign the correct fname
            if not fit_only:
                spectrum.preprocess()
            spectra.append(spectrum)

        if ncpus == 1:
            for spectrum in spectra:
                spectrum.fit()
        else:
            spectrum = spectra[0]
            models = spectrum.models
            bkg_model = spectrum.bkg_model
            fit_method = spectrum.fit_method
            fit_negative = spectrum.fit_negative
            max_ite = spectrum.max_ite
            fit_mp(spectra, models, bkg_model,
                   fit_method, fit_negative, max_ite, ncpus)

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
                    from fitspy.spectra_map import SpectraMap
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
