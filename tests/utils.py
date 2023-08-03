"""
utilities functions for test
"""
import os
import glob
import tkinter

import pandas as pd

from fitspy.utils import hsorted


def extract_results(dirname_res):
    """ Return results extracted from fit parameters .csv files """
    fnames = glob.glob(os.path.join(dirname_res, "*.csv"))
    fnames = hsorted([x for x in fnames if "stat" not in x])
    results = []
    for fname in fnames:
        dfr = pd.read_csv(fname, sep=';', header=1)
        results.append(list(map(float, list(dfr)[2:-3])))
    return results


def display_is_ok():
    """ Check that Tkinter can be launched """
    try:
        tkinter.Tk()
        return True
    except tkinter.TclError:
        try:
            os.environ['DISPLAY'] = ':99'  # opened port in pytest.yml
            tkinter.Tk()
            return True
        except tkinter.TclError:
            return False
