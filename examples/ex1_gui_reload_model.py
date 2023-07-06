"""
Example of preprocessed spectra model reloading through the application
"""
import os

from fitspy.app.gui import spectra_launch

fname = os.path.join('data', 'spectra_2', 'model.json')
spectra_launch(fname_json=fname)
