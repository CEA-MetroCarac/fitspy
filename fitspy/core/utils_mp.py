"""
utilities functions related to multiprocessing

notes:
The strategy (see commented lines below) of passing the models to the workers
once instead of duplicating them for each spectrum turned out to be slightly
  more costly in terms of CPU time finally (?).
"""
from concurrent.futures import ProcessPoolExecutor
import dill


def fit(spectrum_):
    """ Fitting function used in multiprocessing """

    spectrum = dill.loads(spectrum_)
    spectrum.preprocess()
    spectrum.fit()

    shared_queue.put(1)

    return (spectrum.x, spectrum.y, spectrum.weights,
            spectrum.baseline.y_eval, spectrum.baseline.is_subtracted,
            dill.dumps(spectrum.result_fit))


def initializer(queue_incr):
    """ Initialize a global var shared btw the processes and the progressbar """
    global shared_queue  # pylint:disable=global-variable-undefined
    shared_queue = queue_incr


def fit_mp(spectra, ncpus, queue_incr):
    """ Multiprocessing fit function applied to spectra """
    args = []
    for spectrum in spectra:
        args.append(dill.dumps(spectrum))

    with ProcessPoolExecutor(initializer=initializer,
                             initargs=(queue_incr,),
                             max_workers=ncpus) as executor:
        results = executor.map(fit, args)

    for res, spectrum in zip(results, spectra):
        spectrum.x = res[0]
        spectrum.y = res[1]
        spectrum.weights = res[2]
        spectrum.baseline.y_eval = res[3]
        spectrum.baseline.is_subtracted = res[4]
        spectrum.result_fit = dill.loads(res[5])

        spectrum.reassign_params()
