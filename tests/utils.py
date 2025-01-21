"""
utilities functions for test
"""
import os
import glob
import tkinter
import pandas as pd

from fitspy.core.utils import hsorted


def safe_float(x):
    """ Convert string to float """
    try:
        return float(x)
    except ValueError:
        return None


def safe_float(x):
    """ Convert string to float """
    try:
        return float(x)
    except ValueError:
        return None


def extract_results(dirname_res):
    """ Return results extracted from fit parameters .csv files """
    fnames = glob.glob(os.path.join(dirname_res, "*.csv"))
    fnames = hsorted([x for x in fnames if "results.csv" not in x])
    results = []
    print(fnames)
    for fname in fnames:
        dfr = pd.read_csv(fname, sep=';', header=1)
        results.append([safe_float(x) for x in dfr.iloc[:, 2:]
                        if safe_float(x) is not None])
    return results


def display_is_ok():
    """ Check that Tkinter can be launched """
    try:
        tkinter.Tk()
        return True
    except tkinter.TclError:
        return False
