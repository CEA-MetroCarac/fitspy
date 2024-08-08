"""
utilities functions related to multiprocessing

notes:
The strategy (see commented lines below) of passing the models to the workers
once instead of duplicating them for each spectrum turned out to be slightly
  more costly in terms of CPU time finally (?).
"""
from concurrent.futures import ProcessPoolExecutor
import dill

from fitspy.spectrum import Spectrum


def fit(params):
    """ Fitting function used in multiprocessing """
    (x0, y0, x, y, range_min, range_max,
     normalize_status, normalize_range_min, normalize_range_max,
     peak_models_, bkg_models_,
     fit_params, baseline_params, outliers_limit, fit_only) = params

    spectrum = Spectrum()
    spectrum.x0 = x0
    spectrum.y0 = y0
    spectrum.x = x
    spectrum.y = y
    spectrum.range_min = range_min
    spectrum.range_max = range_max
    spectrum.normalize_status = normalize_status
    spectrum.normalize_range_min = normalize_range_min
    spectrum.normalize_range_max = normalize_range_max
    spectrum.peak_models = dill.loads(peak_models_)
    spectrum.bkg_model = dill.loads(bkg_models_)
    spectrum.fit_params = fit_params
    spectrum.outliers_limit = outliers_limit

    if not fit_only:
        for attr, value in baseline_params.items():
            setattr(spectrum.baseline, attr, value)
        spectrum.preprocess()
    spectrum.fit()

    res = (dill.dumps(spectrum.result_fit),)
    if not fit_only:
        res += (spectrum.x, spectrum.y, spectrum.baseline.y_eval)

    shared_queue.put(1)

    return res


def initializer(queue_incr):
    """ Initialize a global var shared btw the processes and the progressbar """
    global shared_queue  # pylint:disable=global-variable-undefined
    shared_queue = queue_incr


def fit_mp(spectra, ncpus, queue_incr, fit_only):
    """ Multiprocessing fit function applied to spectra """

    # models and fit_params are assumed to be consistent across all spectra,
    # the 2 dill.dumps are performed once to limit the CPU cost
    peak_models_ = dill.dumps(spectra[0].peak_models)
    bkg_models_ = dill.dumps(spectra[0].bkg_model)
    fit_params = spectra[0].fit_params
    baseline_params = vars(spectra[0].baseline)
    outliers_limit = spectra[0].outliers_limit

    args = []
    for spectrum in spectra:
        args.append((spectrum.x0, spectrum.y0, spectrum.x, spectrum.y,
                     spectrum.range_min, spectrum.range_max,
                     spectrum.normalize_status,
                     spectrum.normalize_range_min, spectrum.normalize_range_max,
                     peak_models_, bkg_models_, fit_params,
                     baseline_params, outliers_limit, fit_only))

    with ProcessPoolExecutor(initializer=initializer,
                             initargs=(queue_incr,),
                             max_workers=ncpus) as executor:
        results = executor.map(fit, args)

    for res, spectrum in zip(results, spectra):
        spectrum.result_fit = dill.loads(res[0])
        if not fit_only:
            spectrum.x = res[1]
            spectrum.y = res[2]
            spectrum.baseline.y_eval = res[3]
        spectrum.reassign_params()

# import os
# from concurrent.futures import ProcessPoolExecutor
# from copy import deepcopy
# import dill
#
# from fitspy.spectrum import Spectrum
# from fitspy import PEAK_MODELS
#
#
# def fit(params):
#     """ Fitting function used in multiprocessing """
#     models_, fit_method, fit_negative, max_ite, xy = params
#
#     models = []  # all peak_models and bkg_model have been put in 'models_'
#     params = []
#     for model_ in models_:
#         model = dill.loads(model_)
#         models.append(model)
#         params.append(model.param_hints)
#
#     spectrum = Spectrum()
#     spectrum.peak_models = models
#
#     result_fits = []
#     for x, y in xy:
#         spectrum.x = x
#         spectrum.y = y
#         for model, param_hints in zip(models, params):
#             model.param_hints = deepcopy(param_hints)
#         spectrum.fit(fit_method, fit_negative, max_ite)
#         res = spectrum.result_fit
#         result_fits.append((res.values, res.success, res.report))
#         shared_queue.put(1)
#
#     return result_fits
#
#
# def initializer(queue_incr):
#     """ Initialize a global var shared btw the processes and the
#     progressbar """
#     global shared_queue  # pylint:disable=global-variable-undefined
#     shared_queue = queue_incr
#
#
# def fit_mp(spectra, ncpus, queue_incr):
#     """ Multiprocessing fit function applied to spectra """
#
#     ncpus = ncpus or os.cpu_count()
#     ncpus = min(ncpus, os.cpu_count())
#
#     spectrum = spectra[0]
#     fit_method = spectrum.fit_method
#     fit_negative = spectrum.fit_negative
#     max_ite = spectrum.max_ite
#     models_ = []  # all peak_models and bkg_model are put in a single
#     'models_'
#     for peak_model in spectrum.peak_models:
#         models_.append(dill.dumps(peak_model))
#     if spectrum.bkg_model is not None:
#         models_.append(dill.dumps(spectrum.bkg_model))
#
#     xy = []
#     for spectrum in spectra:
#         x, y = spectrum.x, spectrum.y
#         xy.append((x, y))
#     ntot = len(spectra)
#     size = ntot // ncpus + 1
#     xy_partitions = [xy[i:i + size] for i in range(0, ntot, size)]
#     spectra_partitions = [spectra[i:i + size] for i in range(0, ntot, size)]
#
#     args = []
#     for xy_partition in xy_partitions:
#         args.append((models_, fit_method, fit_negative, max_ite,
#         xy_partition))
#
#     with ProcessPoolExecutor(initializer=initializer,
#                              initargs=(queue_incr,),
#                              max_workers=ncpus) as executor:
#         results = tuple(executor.map(fit, args))
#
#     for result, spectra in zip(results, spectra_partitions):
#         for (values, success, report), spectrum in zip(result, spectra):
#             spectrum.result_fit.success = success
#             spectrum.result_fit.report = report
#             for peak_model in spectrum.peak_models:
#                 for key in peak_model.param_names:
#                     peak_model.set_param_hint(key[4:], value=values[key])
#             if spectrum.bkg_model is not None:
#                 for key in spectrum.bkg_model.param_names:
#                     spectrum.bkg_model.set_param_hint(key, value=values[key])
