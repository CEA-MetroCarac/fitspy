"""
utilities functions for test
"""
import os
import glob
import tkinter
import pandas as pd

from fitspy.core.utils import hsorted


def extract_results(dirname_res):
    """ Return results extracted from fit parameters .csv files """
    fnames = glob.glob(os.path.join(dirname_res, "*.csv"))
    fnames = hsorted([x for x in fnames if "results.csv" not in x and "_profiles.csv" not in x])
    results = []
    print(fnames)
    for fname in fnames:
        dfr = pd.read_csv(fname, sep=';', skiprows=1, header=None)
        results.append([val for val in dfr.iloc[0, 2:].values if not pd.isna(val)])
    return results


def display_is_ok():
    """ Check that Tkinter can be launched """
    try:
        tkinter.Tk()
        return True
    except tkinter.TclError:
        return False
