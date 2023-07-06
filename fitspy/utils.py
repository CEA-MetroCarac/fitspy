"""
utilities functions
"""
import os
import re
import numpy as np
import json


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
    with open(filename, 'w') as fid:
        json.dump(dictionary, fid, indent=indent)
