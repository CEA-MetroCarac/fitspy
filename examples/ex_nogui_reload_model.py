"""
Example of preprocessed spectra model reloading without passing by the GUI
"""
from pathlib import Path
import matplotlib.pyplot as plt

from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum
from fitspy.core.utils import hsorted

DATA = Path(__file__).parent / "data"


def ex_nogui_reload_model(show_plots=False):
    """ Example of 'in line' spectra loading and model application """

    dirname = DATA / "spectra_2"

    spectra = Spectra(fnames=hsorted(dirname.glob("*.txt")))
    spectra.apply_model(dirname / "model.json")

    if show_plots:
        for spectrum in spectra:
            _, ax = plt.subplots()
            spectrum.plot(ax)
        plt.show()
    else:
        return spectra


if __name__ == "__main__":
    ex_nogui_reload_model(show_plots=True)
