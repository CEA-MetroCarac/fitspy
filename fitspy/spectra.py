"""
Class dedicated to handle 'Spectrum' objects contained in a list managed by
"Spectra"
"""
import os
import sys
import time
from pathlib import Path
from threading import Thread
from multiprocessing import Queue
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from fitspy.spectrum import Spectrum
from fitspy.utils import fileparts, save_to_json, load_from_json
from fitspy.utils_mp import fit_mp


class Spectra(list):
    """
    Class dedicated to handle 'Spectrum' objects contained in a list

    Attributes
    ----------
    spectra_maps: list of SpectraMap objects
    pbar_index: int
        Index related to the Progress bar during the fit processing

    Parameters
    ----------
    spectra_list: list of Spectrum objects, optional
    """

    def __init__(self, spectra_list=None):

        if spectra_list is not None:
            super().__init__(spectra_list)

        self.spectra_maps = []
        self.pbar_index = 0

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

    def intensity(self):
        """Return the raw intensity array related to spectra AND spectra maps"""
        intensity = []
        for spectrum in self.all:
            intensity.append(spectrum.y0)
        return np.asarray(intensity)

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

    def outliers_limit_calculation(self, coef=1.5, nmax=5):
        """ Calculate the outliers limit from 'coef' * intensity_ref """
        intensity = self.intensity()
        inds = np.argsort(intensity, axis=0)[-nmax, :]
        outliers_limit = coef * intensity[inds, np.arange(intensity.shape[1])]
        for spectrum in self.all:
            spectrum.outliers_limit = outliers_limit

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

        from fitspy.spectra_map import SpectraMap

        results = []
        for fname in fnames:
            spectrum, spectra = self.get_objects(fname)
            if hasattr(spectrum.result_fit, "success"):
                spectrum.save_params(dirname_res)
                spectrum.save_stats(dirname_res)
                name = Path(spectrum.fname).name
                success = spectrum.result_fit.success
                x, y = None, None
                if isinstance(spectra, SpectraMap):
                    x, y = spectra.spectrum_coords(spectrum)
                res = spectrum.result_fit.best_values
                res.update({'name': name, 'success': success, 'x': x, 'y': y})
                results.append(res)

        dfr = pd.DataFrame(results).round(3)

        # reindex columns according to the parameters names
        dfr = dfr.reindex(sorted(dfr.columns), axis=1)
        names = []
        for name in dfr.columns:
            if name in ['name', 'success', 'x', 'y']:
                name = '0' + name  # to be in the 4 first columns
            elif '_' in name:
                name = 'z' + name[4:]  # model peak parameters to be at the end
            names.append(name)
        dfr = dfr.iloc[:, list(np.argsort(names, kind='stable'))]

        fname = Path(dirname_res) / "results.csv"
        dfr.to_csv(fname, sep=';', index=False)

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
        Return a fitspy model ('model_dict') from a '.json' file

        Parameters
        ----------
        fname_json: str
            Filename associated to the spectra .json file where to extract the
            fitspy model
        ind: int, optional
            Spectrum index to consider as model in the spectra issued from the
            .json file reloading

        Returns
        -------
        model_dict: dict
            The corresponding fitspy model
        """
        model_dict = load_from_json(fname_json)[ind]
        return model_dict

    def apply_model(self, model_dict, fnames=None, ncpus=1,
                    show_progressbar=True):
        """
        Apply 'model' to all or part of the spectra

        Parameters
        ----------
        model_dict: dict
            Dictionary related to the Spectrum object attributes (obtained from
            Spectrum.save() for instance) to be applied
        fnames: list of str, optional
            List of the spectrum.fname to handle.
            If None, apply the model to all the spectra
        ncpus: int, optional
            Number of CPU to use during the fit processing
        show_progressbar: bool, optional
            Activation key to show the progress bar
        """
        if fnames is None:
            fnames = self.fnames

        spectra = []
        for fname in fnames:
            spectrum, _ = self.get_objects(fname)
            spectrum.reinit()
            spectrum.set_attributes(model_dict)
            spectrum.fname = fname  # reassign the correct fname
            spectra.append(spectrum)

        self.pbar_index = 0

        queue_incr = Queue()
        args = (queue_incr, len(fnames), ncpus, show_progressbar)
        thread = Thread(target=self.progressbar, args=args)
        thread.start()

        if ncpus == 1:
            for spectrum in spectra:
                spectrum.preprocess()
                spectrum.fit()
                queue_incr.put(1)
        else:
            fit_mp(spectra, ncpus, queue_incr)

        thread.join()

    def progressbar(self, queue_incr, ntot, ncpus, show_progressbar):
        """ Progress bar """
        self.pbar_index = 0
        pbar = "\r[{:100}] {:.0f}% {}/{} {:.2f}s " + f"ncpus={ncpus}"
        t0 = time.time()
        while self.pbar_index < ntot:
            self.pbar_index += queue_incr.get()
            percent = 100 * self.pbar_index / ntot
            cursor = "*" * int(percent)
            exec_time = time.time() - t0
            msg = pbar.format(cursor, percent, self.pbar_index, ntot, exec_time)
            if show_progressbar:
                sys.stdout.write(msg)
        if show_progressbar:
            print()

    def save(self, fname_json=None, fnames=None):
        """
        Return a 'dict_spectra' dictionary with all the spectrum attributes and
        Save it in a .json file if a 'fname_json' is given

        Parameters
        ----------
        fname_json: str, optional
            Filename associated to the .json file for the spectra saving
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        """
        if fnames is None:
            fnames = self.fnames

        dict_spectra = {}
        for i, fname in enumerate(fnames):
            spectrum, _ = self.get_objects(fname)
            dict_spectra[i] = spectrum.save()
            dict_spectra[i]['baseline'].pop('y_eval')

        if fname_json is not None:
            dirname = os.path.dirname(fname_json)
            if not os.path.isdir(dirname):
                print(f"directory {dirname} doesn't exist")
                return
            else:
                save_to_json(fname_json, dict_spectra, indent=3)

        return dict_spectra

    @staticmethod
    def load(fname_json, preprocess=False):
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
                        if preprocess:
                            spectrum.preprocess()
                        break
            else:
                spectrum = Spectrum()
                spectrum.set_attributes(dict_spectra[i])
                if preprocess:
                    spectrum.preprocess()
                spectra.append(spectrum)

        return spectra
