"""
utilities functions related to multiprocessing
"""
import os
from concurrent.futures import ProcessPoolExecutor
import dill

from fitspy.spectrum import Spectrum
from fitspy import MODELS_NAMES, PEAK_MODELS


def fit(params):
    """ Fitting function used in multiprocessing """
    x, y, models_, method, fit_negative, max_ite = params

    models = []
    for model_ in models_:
        if isinstance(model_, bytes):
            models.append(dill.loads(model_))
        else:
            models.append(model_)

    spectrum = Spectrum()
    spectrum.x = x
    spectrum.y = y
    spectrum.models = models
    spectrum.fit(fit_method=method, fit_negative=fit_negative, max_ite=max_ite)
    shared_queue.put(1)

    result_fit = spectrum.result_fit
    return result_fit.values, result_fit.success, result_fit.fit_report


def initializer(queue_incr):
    """ Initialize a global var shared btw the processes and the progressbar """
    global shared_queue  # pylint:disable=global-variable-undefined
    shared_queue = queue_incr


def fit_mp(spectra, ncpus, queue_incr):
    """ Multiprocessing fit function applied to spectra """

    ncpus = ncpus or os.cpu_count()
    ncpus = min(ncpus, os.cpu_count())

    spectrum = spectra[0]
    models_ = []
    for model in spectrum.models:
        if model.name2 not in MODELS_NAMES:
            models_.append(dill.dumps(model))
        else:
            models_.append(model)
    if spectrum.bkg_model is not None:
        if spectrum.bkg_model.name2 not in MODELS_NAMES:
            models_.append(dill.dumps(spectrum.bkg_model))
        else:
            models_.append(spectrum.bkg_model)
    fit_method = spectrum.fit_method
    fit_negative = spectrum.fit_negative
    max_ite = spectrum.max_ite

    args = []
    for spectrum in spectra:
        x, y = spectrum.x, spectrum.y
        args.append((x, y, models_, fit_method, fit_negative, max_ite))

    with ProcessPoolExecutor(initializer=initializer,
                             initargs=(queue_incr,),
                             max_workers=ncpus) as executor:
        results = tuple(executor.map(fit, args))

    # dictionary of custom function names and definitions
    funcdefs = {}
    for val in PEAK_MODELS.values():
        funcdefs[val.__name__] = val

    for (values, success, fit_report), spectrum in zip(results, spectra):
        spectrum.result_fit.success = success
        spectrum.result_fit.fit_report = fit_report
        for model in spectrum.models:
            for key in model.param_names:
                model.set_param_hint(key[4:], value=values[key])
        if spectrum.bkg_model is not None:
            for key in spectrum.bkg_model.param_names:
                spectrum.bkg_model.set_param_hint(key, value=values[key])
