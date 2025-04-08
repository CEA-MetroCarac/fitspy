"""
Example of weights passed to the fit
"""
import tempfile
from pathlib import Path
import matplotlib.pyplot as plt

from fitspy.core.spectrum import Spectrum


def ex_nogui_weights_in_fit(show_plots=False):
    """ Example of weights taken into account during the fit processing """

    csv_string = """ # x,y,weights
        1,10,1
        2,20,1
        3,0,0
        4,40,1
        5,50,1
    """

    tmpdir = tempfile.gettempdir()
    fname = Path(tmpdir) / 'input.csv'

    with open(fname, 'w') as fid:
        fid.write(csv_string)

    _, ax = plt.subplots(1, 2, figsize=(8, 4))

    def fit(ax, weighted=False, label=None):
        spectrum = Spectrum()
        spectrum.load_profile(fname)
        if not weighted:
            spectrum.weights = None
        spectrum.set_bkg_model('Linear')
        spectrum.fit(coef_noise=0)
        best_fit = spectrum.result_fit.best_fit

        ax.plot(spectrum.x, spectrum.y, 'k--', lw=0.5, marker='o', mfc='r')
        ax.plot(spectrum.x, spectrum.result_fit.best_fit, label=label)
        ax.set_xlim(0, 6)
        ax.legend()

        return best_fit

    best_fit_unweighted = fit(ax[0], weighted=False, label='unweighted fit')
    best_fit_weighted = fit(ax[1], weighted=True, label='weighted fit')

    if show_plots:
        plt.show()
    else:
        plt.close()
        return best_fit_unweighted, best_fit_weighted


if __name__ == "__main__":
    ex_nogui_weights_in_fit(show_plots=True)
