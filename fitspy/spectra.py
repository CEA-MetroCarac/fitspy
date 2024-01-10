"""
Class dedicated to handle 'Spectrum' objects contained in a list managed by
"Spectra"
"""
import os
import csv
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from lmfit import Model, fit_report, Parameters
from lmfit.model import ModelResult

from fitspy.utils import fileparts, check_or_rename
from fitspy.utils import save_to_json, load_from_json
from fitspy.models import gaussian
from fitspy.spectrum import Spectrum
from fitspy import MODELS, PARAMS


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
           fit_method=None, fit_negative=None, max_ite=None, ncpus=None,
           models_labels=None):
    """ Multiprocessing fit function applied to spectra """

    ncpus = ncpus or os.cpu_count()
    ncpus = min(ncpus, os.cpu_count())

    if models_labels is None:
        models_labels = [str(i) for i in range(len(models))]

    args = []
    for spectrum in spectra:
        x, y = spectrum.x, spectrum.y
        args.append((x, y, models, fit_method, fit_negative, max_ite))

    with ProcessPoolExecutor(max_workers=ncpus) as executor:
        results = tuple(executor.map(fit, args))

    # dictionary of custom function names and definitions
    funcdefs = {}
    for val in MODELS.values():
        funcdefs[val.__name__] = val

    for result_fit_json, spectrum in zip(results, spectra):
        spectrum.models = deepcopy(models)
        spectrum.models_labels = models_labels.copy()
        spectrum.fit_method = fit_method
        spectrum.fit_negative = fit_negative
        spectrum.max_ite = max_ite
        # dummy ModelResult that will be overwritten hereafter
        modres = ModelResult(Model(gaussian), Parameters())
        spectrum.result_fit = modres.loads(result_fit_json, funcdefs=funcdefs)
        spectrum.reassign_params()


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
                writer.writerow(['label', 'model'] + PARAMS)
                for label, model in zip(labels, models):
                    vals = [label, Spectrum.get_model_name(model)]
                    for key in PARAMS:
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
