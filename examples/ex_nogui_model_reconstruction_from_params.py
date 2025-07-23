"""
Example of spectrum peak models reconstruction from .json and .csv parameters
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fitspy.core.spectra import Spectra
from fitspy.core.spectrum import Spectrum

DATA = Path(__file__).parent / "data"


def plot_spectrum_peak_models(spectrum, title=None):
    """ Plot 'spectrum' peak models """

    # x-support for spectrum peak models evaluation
    x = np.linspace(100, 800., 200)

    plt.figure()
    y_sum = np.zeros_like(x)
    for peak_model in spectrum.peak_models:
        y = peak_model.eval(peak_model.make_params(), x=x)
        y_sum += y
        plt.plot(x, y)
    plt.plot(x, y_sum, 'b')
    plt.title(title)


def model_reconstruction_from_json():
    """ Example of 'inline' spectrum model reconstruction from '.json' params"""

    fname_json = DATA / 'spectra_2' / 'model.json'

    # considering the first spectrum model
    spectrum = Spectra.load(fname_json)[0]

    plot_spectrum_peak_models(spectrum, title='from .json')


def model_reconstruction_from_csv():
    """ Example of 'inline' spectrum model reconstruction from '.csv' params"""

    fname_csv = DATA / 'spectra_2' / 'spectrum_2_1.csv'

    dfr = pd.read_csv(fname_csv, sep=';')
    peak_models = []
    for i in dfr.index:
        params = list(dfr.iloc[i, 1:])
        peak_model = Spectrum.create_peak_model(i, *params)
        peak_models.append(peak_model)

    spectrum = Spectrum()
    spectrum.peak_models = peak_models

    plot_spectrum_peak_models(spectrum, title='from .csv')


def profiles_visualisation_from_csv():
    """ Example of 'inline' spectrum profiles plotting from 'xxx_profiles.csv' """

    fname_csv = DATA / 'spectra_2' / 'spectrum_2_1_profiles.csv'

    dfr = pd.read_csv(fname_csv, sep=';')

    first_keys = ['x', 'y_raw', 'y_subtract', 'y_fit', 'baseline', 'bkg']
    model_keys = [k for k in dfr.columns if k not in first_keys]
    y_keys = ['y_subtract', 'y_fit']

    for key in y_keys + model_keys:
        plt.plot(dfr['x'], dfr[key], lw=2 if key in y_keys else 0.7, label=key)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    model_reconstruction_from_json()
    model_reconstruction_from_csv()
    profiles_visualisation_from_csv()
    plt.show()
