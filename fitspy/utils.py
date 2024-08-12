"""
utilities functions
"""
import os
import re
import json
from pathlib import Path
import importlib
import itertools
import runpy
import numpy as np
import pandas as pd
from lmfit.models import ExpressionModel
from rsciio import IO_PLUGINS


def closest_item(element_list, value):
    """ Return the closest element in the given list """
    return element_list[closest_index(element_list, value)]


def closest_index(element_list, value):
    """Return the closest element index in the given list """
    if value == np.inf:
        return np.argmax(element_list)

    elif value == -np.inf:
        return np.argmin(element_list)

    else:
        return min(range(len(element_list)),
                   key=lambda i: abs(element_list[i] - value))


def hsorted(list_):
    """ Sort the given list in the way that humans expect """
    list_ = [str(x) for x in list_]
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list_, key=alphanum_key)


def fileparts(filename):
    """ Returns different file parts of a file  """
    folder, name_with_ext = os.path.split(filename)
    name, ext = os.path.splitext(name_with_ext)
    return folder, name, ext


def check_or_rename(filename, add=0):
    """ Return filename with increment xx_{add}.yy if file access is denied """
    original_file = filename
    if add > 0:
        split = filename.split(".")
        if len(split) > 1:
            filename = ".".join([split[:-1][0] + "_" + str(add), split[-1]])
        else:
            filename += "_" + str(add)  # filename without extension
    if not os.path.isfile(filename):
        return filename
    else:
        try:
            os.rename(filename, filename)  # check the file access is not denied
            return filename
        except PermissionError:
            add += 1
            return check_or_rename(original_file, add)


def load_from_json(filename):
    """
    Load a dictionary from a '.json' file

    Parameters
    ----------
    filename: str
        Pathname of the .json file

    Returns
    -------
    a dict object
    """
    with open(filename, 'r') as fid:
        return json.load(fid,
                         object_hook=lambda d: {  # to manage 'int' keys
                             int(k) if k.lstrip('-').isdigit() else k: v
                             for k, v in d.items()})


def save_to_json(filename, dictionary, indent=3):
    """
    Function to save dictionary in a '.json' file with a compact format

    Parameters
    ----------
    filename: str
        Pathname of the .json file
    dictionary: dict object
        The dictionary to save
    indent: int, optional
        json keyword for indentation. See dedicated doc for more details
    """
    json_dumps = json.dumps(dictionary, indent=indent)

    # lists on a single line from https://stackoverflow.com/a/73748594/5964076
    indent_ = ' ' * indent
    starts = [x.start() for x in re.finditer(r'\[', json_dumps)]
    ends = [x.start() + 1 for x in re.finditer(r'\]', json_dumps)]
    origs = []
    alters = []
    for start, end in zip(starts, ends):
        orig = json_dumps[start:end]
        alter = orig.replace('\n', '').replace(indent_, '').replace(',', ', ')
        origs.append(orig)
        alters.append(alter)
    for orig, alter in zip(origs, alters):
        json_dumps = json_dumps.replace(orig, alter)

    with open(filename, 'w') as fid:
        fid.write(json_dumps)


def load_models_from_txt(fname, MODELS):
    """
    Load models from '.txt' file

    Parameters
    ----------
    fname: str or WindowsPath
        Filename of the .txt file with the models expressions:
        model_name1 = expression1
        model_name2 = expression2
    MODELS: dict
        Dictionary corresponding to fitspy.PEAK_MODELS or fitspy.BKG_MODELS
    """
    if Path(fname).exists():
        with open(fname, 'r') as fid:
            for line in fid.readlines():
                line = line.replace('\n', '').replace(' ', '')
                words = line.split('=')
                if len(words) == 2:
                    name, expr = words[0], words[1]
                    try:
                        model = ExpressionModel(expr, independent_vars=['x'])
                        model.__name__ = name
                        MODELS.update({name: model})
                        print(f"{name} ADDED")
                    except:
                        print(f"{name} INCORRECT EXPRESSION")


def load_models_from_py(fname):
    """ Load models from '.py' file (See the documentation for more details) """
    if Path(fname).exists():
        runpy.run_path(fname)


def get_dim(fname):
    """ Return the dimension (1, 2 or None) of the spectrum/spectra field """

    dim = None

    if Path(fname).suffix in ['.txt', '.csv']:
        with open(fname, 'r') as fid:
            dim = 2 if fid.readline()[0] == "\t" else 1

    else:
        reader = get_reader_from_rsciio(fname)
        if reader is not None:
            data = reader.file_reader(fname)[0]['data']
            if data.ndim == 1:
                dim = 1
            elif data.ndim == 3:  # 2D-map
                dim = 2

    return dim


def get_reader_from_rsciio(fname):
    """ Return the reader object using the Rosettasciio library """
    sfx = Path(fname).suffix[1:].lower()
    rdrs = [rdr for rdr in IO_PLUGINS if sfx in rdr["file_extensions"]]
    if len(rdrs) == 1:
        reader = rdrs[0]
        return importlib.import_module(reader["api"])
    else:
        return None


def get_x_data_from_rsciio(fname):
    """ Return the spectrum/spectra support ('x') and the related intensities
        ('data') using the Rosettasciio library """

    reader = get_reader_from_rsciio(fname)

    if reader is None:
        raise NotImplementedError(f"unreadable file {fname}")

    fdict = reader.file_reader(fname)[0]
    data = fdict['data']
    axis = fdict['axes'][0]
    x = axis['offset'] + axis['scale'] * np.arange(axis['size'])

    return x, data


def get_1d_profile(fname):
    """ Return the spectrum support ('x0') and its intensity ('y0') """

    if Path(fname).suffix in ['.txt', '.csv']:
        dfr = pd.read_csv(fname,
                          sep=r'\s+|\t|,|;| ', engine='python',
                          skiprows=1, usecols=[0, 1],
                          names=['x0', 'y0'])
        x0 = dfr['x0'].to_numpy()
        y0 = dfr['y0'].to_numpy()
    else:
        x0, y0 = get_x_data_from_rsciio(fname)
        if y0.ndim != 1:
            raise IOError(f"incorrect dimension associated with {fname}")

    return x0, y0


def get_2d_map(fname):
    r""" Return the array related to a 2D-map.
        For more details about the array shape, see:
        https://cea-metrocarac.github.io/fitspy/doc/user_guide/input_data.html#d-map-spectra"
        """
    if Path(fname).suffix in ['.txt', '.csv']:
        dfr = pd.read_csv(fname, sep='\t', header=None)
        arr = dfr.to_numpy()
    else:
        x, data = get_x_data_from_rsciio(fname)
        if data.ndim == 3:
            shape = data.shape
            inds_i, inds_j = range(shape[1]), range(shape[2])
            inds = np.array(list(itertools.product(inds_i, inds_j)))
            data = data.reshape(shape[0], shape[1] * shape[2])
            arr = np.vstack((np.hstack(([0, 0], x)), np.hstack((inds, data.T))))
        else:
            raise IOError(f"incorrect dimension associated with {fname}")

    return arr


def eval_noise_amplitude(y):
    """ Evaluate the noise amplitude wrt oscillations at every other point """
    delta = np.diff(y)
    delta1, delta2 = delta[:-1], delta[1:]
    mask = np.sign(delta1) * np.sign(delta2) == -1
    ampli_noise = np.median(np.abs(delta1[mask] - delta2[mask]) / 2)
    return ampli_noise
