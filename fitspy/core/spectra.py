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

from fitspy.core.spectrum import Spectrum
from fitspy.core.utils import fileparts, save_to_json, load_from_json, compress, decompress
from fitspy.core.utils_mp import fit_mp


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
    fnames: list of str, optional
        List of spectra pathname
    """

    def __init__(self, spectra_list=None, fnames=None):

        if spectra_list is not None:
            super().__init__(spectra_list)

        if fnames is not None:
            for fname in fnames:
                spectrum = Spectrum()
                spectrum.load_profile(fname)
                self.append(spectrum)

        self.spectra_maps = []
        self.pbar_index = 0

    @property
    def fnames(self):
        """ Return all the fnames related to spectra AND spectra maps """
        return [os.path.normpath(spectrum.fname) for spectrum in self.all]

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
        # Get all y0 values
        intensities = [spectrum.y0 for spectrum in self.all]
        max_len = max(len(y0) for y0 in intensities)

        # Pad shorter arrays with NaN to match max length
        padded = [
            np.pad(y0, (0, max_len - len(y0)),
                   mode='constant',
                   constant_values=np.nan) if len(y0) < max_len else y0
            for y0 in intensities
        ]

        return np.asarray(padded)

    def get_spectrum(self, fname):
        """ Return spectrum from 'fname' contained in the 'spectra' list only """
        fname = os.path.normpath(fname)
        fnames = [os.path.normpath(spectrum.fname) for spectrum in self]
        try:
            return self[fnames.index(fname)]
        except:
            print(f"{fname} not found in the spectra list")
            return None

    def get_objects(self, fname):
        """ Return spectrum and parent (spectra or spectra map) related to 'fname' """
        fname = os.path.normpath(fname)
        if "  X=" in fname:
            fname_map = fname.split("  X=")[0]
            fname_maps = [spectra_map.fname for spectra_map in self.spectra_maps]
            spectra_map = self.spectra_maps[fname_maps.index(fname_map)]
            return spectra_map.get_spectrum(fname), spectra_map
        else:
            return self.get_spectrum(fname), self

    def outliers_limit_calculation(self, coef=1.5, nmax=5):
        """ Calculate the outliers limit from 'coef' * intensity_ref """
        intensity = self.intensity()

        # Get mean of top nmax values for each wavelength point
        sorted_values = -np.sort(-intensity, axis=0)
        intensity_ref = np.nanmean(sorted_values[:nmax], axis=0)

        outliers_limit = coef * intensity_ref
        for spectrum in self.all:
            spectrum.outliers_limit = outliers_limit[:len(spectrum.y0)]

    def save_results(self, dirname_res, fnames=None):
        """
        Save spectra results (peaks parameters and statistics) in .csv files

        Parameters
        ----------
        dirname_res: str or pathlib.Path object
            Dirname where to save the .csv files
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        """
        dirname_res = Path(dirname_res)
        dirname_res.mkdir(parents=True, exist_ok=True)

        if fnames is None:
            fnames = self.fnames

        from fitspy.core.spectra_map import SpectraMap

        results = []
        for fname in fnames:
            spectrum, spectra = self.get_objects(fname)
            if hasattr(spectrum.result_fit, "success"):
                spectrum.save_profiles(dirname_res)
                spectrum.save_params(dirname_res)
                spectrum.save_stats(dirname_res)
                name = Path(spectrum.fname).name
                success = spectrum.result_fit.success
                x, y = SpectraMap.spectrum_coords(spectrum) if "  X=" in fname else (None, None)
                result_fit = spectrum.result_fit
                res = result_fit.best_values if hasattr(result_fit, 'best_values') else {}
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

        fname = dirname_res / "results.csv"
        dfr.to_csv(fname, sep=';', index=False)

    def save_figures(self, dirname_fig, fnames=None, bounds=None):
        """
        Save spectra figures

        Parameters
        ----------
        dirname_fig: str or pathlib.Path object
            Dirname where to save the figures
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        bounds: tuple of 2 tuples, optional
            Axis limits corresponding to ((xmin, xmax), (ymin, ymax))
        """
        dirname_fig = Path(dirname_fig)
        dirname_fig.mkdir(parents=True, exist_ok=True)

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
            fname_fig = dirname_fig / (name + '.png')
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

    def apply_model(self, model, fnames=None, ncpus=1, show_progressbar=True):
        """
        Apply 'model' to all or part of the spectra

        Parameters
        ----------
        model: str or dict
            filename to a Fitspy model ('.json' file) or
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
        if isinstance(model, (str, Path)) and Path(model).is_file():
            model_dict = Spectra.load_model(model)
        elif isinstance(model, dict):
            model_dict = model
        else:
            raise IOError("'model' passes to apply_model() is not correct")

        if fnames is None:
            fnames = self.fnames

        spectra = []
        for fname in fnames:
            spectrum, _ = self.get_objects(fname)
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

    def save(self, fname_json=None, fnames=None, save_data=False):
        """
        Return a 'dict_spectra' dictionary with all the spectrum attributes (but objects) and
        Save it in a .json file if a 'fname_json' is given

        Parameters
        ----------
        fname_json: str, optional
            Filename associated to the .json file for the spectra saving
        fnames: list of str, optional
            List of the spectrum 'fnames' to save. If None, consider all the
            spectrum contained in the 'spectra' list
        save_data: bool, optional
            Activation keyword to write spectra/spectramap values at the end of the dictionary

        Returns
        -------
        dict_spectra: dict
            Dictionary with all the spectrum attributes but objects, and input data if 'save_data'
            is set to True

        """
        if fnames is None:
            fnames = self.fnames

        dict_spectra = {}
        for i, fname in enumerate(fnames):
            spectrum, parent = self.get_objects(fname)
            dict_spectra[i] = spectrum.save(save_data=save_data and parent is self)
            dict_spectra[i]['baseline'].pop('y_eval')

        if save_data and len(self.spectra_maps) > 0:
            dict_spectra['data'] = {}
            for spectra_map in self.spectra_maps:
                dict_spectra['data'][spectra_map.fname] = compress(spectra_map.arr0)

        if fname_json is not None:
            dirname = os.path.dirname(fname_json)
            if not os.path.isdir(dirname):
                print(f"directory {dirname} doesn't exist")
                return
            else:
                save_to_json(fname_json, dict_spectra, indent=3)

        return dict_spectra

    @staticmethod
    def load(fname_json=None, dict_spectra=None, preprocess=False):
        """ Return a Spectra object from a .json file or directly from 'dict_spectra' """
        dict_spectra = dict_spectra or load_from_json(fname_json)

        spectra = Spectra()
        fname_maps = []
        for key, model in dict_spectra.items():
            if key != 'data':
                fname = os.path.normpath(model['fname'])

                if "  X=" in fname:  # spectrum attached to a SpectraMap object
                    from fitspy.core.spectra_map import SpectraMap
                    fname_map = fname.split("  X=")[0]
                    if fname_map not in fname_maps:
                        if os.path.isfile(fname_map):
                            spectra.spectra_maps.append(SpectraMap.load_map(fname_map))
                        elif fname_map in dict_spectra.get('data', {}):
                            arr0 = decompress(dict_spectra['data'][fname_map])
                            spectra.spectra_maps.append(SpectraMap.load_map(fname_map, arr0=arr0))
                        else:
                            print(f'ERROR: unable to reload data related to {Path(fname_map).name}')
                        fname_maps.append(fname_map)
                else:
                    spectrum = Spectrum()
                    spectrum.fname = fname
                    spectra.append(spectrum)

        spectra.set_attributes(dict_spectra, preprocess=preprocess)

        return spectra

    def set_attributes(self, dict_spectra, preprocess=False):
        """ Set attributes to spectrum object related to 'dict_spectra' """
        for key, model in dict_spectra.items():
            if key != 'data':
                spectrum, _ = self.get_objects(model['fname'])
                spectrum.set_attributes(model)
                if preprocess:
                    spectrum.preprocess()
