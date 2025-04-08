"""
Example of weights passed to the fit
"""
from pathlib import Path
import matplotlib.pyplot as plt

from fitspy.core.spectrum import Spectrum


def fit(fname, weighted=False):
    spectrum = Spectrum()
    spectrum.load_profile(fname)
    if not weighted:
        spectrum.weights = None
    spectrum.set_bkg_model('Linear')
    spectrum.fit(coef_noise=0)
    return spectrum


def plot(ax, spectrum, label):
    ax.plot(spectrum.x, spectrum.y, 'k--', lw=0.5, marker='o', mfc='r')
    ax.plot(spectrum.x, spectrum.result_fit.best_fit, label=label)
    ax.set_xlim(0, 6)
    ax.legend()


def ex_nogui_weights_in_fit(dirname, show_plots=False):
    """ Example of weights taken into account during the fit processing """

    csv_string = """x,y,weights
        1,10,1
        2,20,1
        3,0,0
        4,40,1
        5,50,1
    """
    fname = Path(dirname) / 'input.csv'

    with open(fname, 'w') as fid:
        fid.write(csv_string)

    spectrum_unweighted = fit(fname, weighted=False)
    spectrum_weighted = fit(fname, weighted=True)

    if show_plots:
        _, ax = plt.subplots(1, 2, figsize=(8, 4))
        plot(ax[0], spectrum_unweighted, label='unweighted fit')
        plot(ax[1], spectrum_weighted, label='weighted fit')
        plt.show()
    else:
        best_fit_unweighted = spectrum_unweighted.result_fit.best_fit
        best_fit_weighted = spectrum_weighted.result_fit.best_fit
        return best_fit_unweighted, best_fit_weighted


if __name__ == "__main__":
    import tempfile

    tmpdir = tempfile.gettempdir()
    ex_nogui_weights_in_fit(tmpdir, show_plots=True)
