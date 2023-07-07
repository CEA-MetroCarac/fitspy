"""
Example of preprocessed spectra model reloading through the application
"""
import os

from fitspy.app.gui import fitspy_launcher

fname = os.path.join('data', 'spectra_2', 'model.json')
fitspy_launcher(fname_json=fname)
