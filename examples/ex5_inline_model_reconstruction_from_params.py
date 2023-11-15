"""
Example of 'in line' spectrum model reconstruction from .json and .csv
parameters
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fitspy.spectra import Spectra, Spectrum

DATA = Path(__file__).parent / "data"


def plot_spectrum_models(spectrum, title=None):
    """ Plot 'spectrum' model """

    # x-support for spectrum models evaluation
    x = np.linspace(100, 800., 200)

    plt.figure()
    y_sum = np.zeros_like(x)
    for model in spectrum.models:
        y = model.eval(model.make_params(), x=x)
        y_sum += y
        plt.plot(x, y)
    plt.plot(x, y_sum, 'b')
    plt.title(title)


def inline_model_reconstruction_from_json():
    """ Example of 'inline' spectrum model reconstruction from '.json' params"""

    fname_json = DATA / 'spectra_2' / 'model.json'

    # considering the first spectrum model
    spectrum = Spectra.load(fname_json)[0]

    plot_spectrum_models(spectrum, title='from .json')


def inline_model_reconstruction_from_csv():
    """ Example of 'inline' spectrum model reconstruction from '.csv' params"""

    fname_csv = DATA / 'spectra_2' / 'InP-1_42-P21.csv'

    dfr = pd.read_csv(fname_csv, sep=';')
    models = []
    for i in dfr.index:
        params = list(dfr.iloc[i, 1:])
        model = Spectrum.create_model(i, *params)
        models.append(model)

    spectrum = Spectrum()
    spectrum.models = models

    plot_spectrum_models(spectrum, title='from .csv')


if __name__ == "__main__":
    inline_model_reconstruction_from_json()
    inline_model_reconstruction_from_csv()
    plt.show()
