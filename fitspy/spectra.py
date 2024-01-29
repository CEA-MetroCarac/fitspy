"""
Class dedicated to handle 'Spectrum' objects contained in a list managed by
"Spectra"
"""
import os
import sys
import time
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
from threading import Thread
from multiprocessing import Queue
import matplotlib.pyplot as plt
from lmfit.models import ExpressionModel
import dill

from fitspy.utils import fileparts, save_to_json, load_from_json
from fitspy.spectrum import Spectrum
from fitspy import MODELS, MODELS_NAMES


def fit(params):
    """ Fitting function used in multiprocessing """
    x, y, models_, method, fit_negative, max_ite = params

    models = []
    for model_ in models_:
        if isinstance(model_, bytes):
            models.append(dill.loads(model_))
        else:
            models.append(model_)

    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y
    spectrum.models = models
    spectrum.fit(fit_method=method, fit_negative=fit_negative, max_ite=max_ite)
    shared_queue.put(1)

    result_fit = spectrum.result_fit
    return result_fit.values, result_fit.success, result_fit.fit_report


def initializer(queue_incr):
    """ Initialize a global var shared btw the processes and the progressbar """
    global shared_queue  # pylint:disable=global-variable-undefined
    shared_queue = queue_incr


def fit_mp(spectra, ncpus, queue_incr):
    """ Multiprocessing fit function applied to spectra """

    ncpus = ncpus or os.cpu_count()
    ncpus = min(ncpus, os.cpu_count())

    spectrum = spectra[0]
    models_ = []
    for model in spectrum.models:
        if model.name2 not in MODELS_NAMES:
            models_.append(dill.dumps(model))
        else:
            models_.append(model)
    if spectrum.bkg_model is not None:
        if spectrum.bkg_model.name2 not in MODELS_NAMES:
            models_.append(dill.dumps(spectrum.bkg_model))
        else:
            models_.append(spectrum.bkg_model)
    fit_method = spectrum.fit_method
    fit_negative = spectrum.fit_negative
    max_ite = spectrum.max_ite

    args = []
    for spectrum in spectra:
        x, y = spectrum.x, spectrum.y
        args.append((x, y, models_, fit_method, fit_negative, max_ite))

    with ProcessPoolExecutor(initializer=initializer,
                             initargs=(queue_incr,),
                             max_workers=ncpus) as executor:
        results = tuple(executor.map(fit, args))

    # dictionary of custom function names and definitions
    funcdefs = {}
    for val in MODELS.values():
        funcdefs[val.__name__] = val

    for (values, success, fit_report), spectrum in zip(results, spectra):
        spectrum.result_fit.success = success
        spectrum.result_fit.fit_report = fit_report
        for model in spectrum.models:
            for key in model.param_names:
                model.set_param_hint(key[4:], value=values[key])
        if spectrum.bkg_model is not None:
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
                    fit_only=False, tk_progressbar=None, **fit_kwargs):
        """
        Apply 'model' to all or part of the spectra

        Parameters
        ----------
        model: dict
            Dictionary related to the Spectrum object attributes (obtained from
            Spectrum.save() for instance)
        fnames: list of str, optional
            List of the spectrum.fname to handle.
            If None, apply the model to all the spectra
        ncpus: int, optional
            Number of CPU to work with in fitting
        fit_only: bool, optional
            Activation key to process only fitting
        tk_progressbar: ProgressBar obj, optional
            Progression bar using tkinter.ttk.Progressbar to follow the
            'apply_model' progression
        fit_kwargs: dict
            Keywords arguments passed to spectrum.fit()
        """
        if fnames is None:
            fnames = self.all

        ntot = len(fnames)
        if ntot == 0:
            return

        spectra = []
        for fname in fnames:
            spectrum, _ = self.get_objects(fname)
            spectrum.set_attributes(model, **fit_kwargs)
            spectrum.fname = fname  # reassign the correct fname
            if not fit_only:
                spectrum.preprocess()
            spectra.append(spectrum)

        queue_incr = Queue()

        def proc():
            if ncpus == 1:
                for spectrum in spectra:
                    spectrum.fit()
                    queue_incr.put(1)
            else:
                fit_mp(spectra, ncpus, queue_incr)

            queue_incr.put("finished")

        Thread(target=proc).start()
        progressbar(queue_incr, ntot, tk_progressbar)

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


def progressbar(queue_incr, ntot, tk_progressbar=None):
    """ Progress bar """
    n = 0
    is_finished = False
    pbar = "\r[{:100}] {:.0f}% {}/{} {:.2f}s"
    t0 = time.time()
    while not is_finished:
        val = queue_incr.get()
        if val == 'finished':
            is_finished = True
        else:
            n += val
            percent = 100 * n / ntot
            cursor = "*" * int(percent)
            exec_time = time.time() - t0
            sys.stdout.write(pbar.format(cursor, percent, n, ntot, exec_time))
            if tk_progressbar is not None:
                tk_progressbar.var.set(percent)
                tk_progressbar.label['text'] = f"{n}/{ntot}"
                tk_progressbar.frame.update()
    print()
