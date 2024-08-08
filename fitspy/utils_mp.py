"""
utilities functions related to multiprocessing

notes:
The strategy (see commented lines below) of passing the models to the workers
once instead of duplicating them for each spectrum turned out to be slightly
  more costly in terms of CPU time finally (?).
"""
from concurrent.futures import ProcessPoolExecutor
import dill


def fit(params):
    """ Fitting function used in multiprocessing """
    spectrum_, fit_only = params

    spectrum = dill.loads(spectrum_)
    if not fit_only:
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
    args = []
    for spectrum in spectra:
        args.append((dill.dumps(spectrum), fit_only))

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
