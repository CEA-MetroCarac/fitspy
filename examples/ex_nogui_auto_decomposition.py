"""
Example of spectra automatic decomposition without passing by the GUI
"""
import os
import glob
import tempfile
from pathlib import Path
import matplotlib.pyplot as plt
from lmfit import report_fit

from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum
from fitspy.core.utils import hsorted

DATA = Path(__file__).parent / "data"


def auto_decomposition(verbosity=True, show_plots=False):
    """ Example of 'in line' spectra automatic decomposition """

    fnames = hsorted(glob.glob(os.path.join(DATA, 'spectra_1', '*.txt')))

    # spectra fitting processing
    spectra_list = []
    for fname in fnames:
        spectrum = Spectrum()
        spectrum.load_profile(fname)
        spectrum.apply_range(range_min=60)
        spectrum.baseline.mode = 'Semi-Auto'
        spectrum.eval_baseline()
        spectrum.subtract_baseline()
        spectrum.auto_peaks(model_name="Lorentzian")
        # spectrum.fit() # fit is already performed during auto_peaks processing
        spectra_list.append(spectrum)

    if verbosity:
        print(f"\n\nfilename: {fname}")
        report_fit(spectrum.result_fit)

    # spectra object creation, saving and reloading
    with tempfile.TemporaryDirectory() as dirtemp:
        fname_json = os.path.join(dirtemp, 'spectra.json')
        spectra = Spectra(spectra_list)
        spectra.save(fname_json=fname_json)
        spectra_reloaded = Spectra.load(fname_json=fname_json)

    if show_plots:
        # spectra plotting
        for i, spectrum in enumerate(spectra_reloaded):
            _, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4))

            # Raw spectra
            spectrum0 = Spectrum()
            spectrum0.load_profile(fnames[i])
            ax0.set_title('Raw')
            spectrum0.plot(ax=ax0)

            # Fitted spectra
            ax1.set_title('Flattened + Fitted')
            spectrum.preprocess()
            spectrum.plot(ax=ax1)
            ax1.legend()

        plt.show()

    else:
        return spectra_reloaded


if __name__ == "__main__":
    auto_decomposition(show_plots=True)
