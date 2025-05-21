"""
Module related to bichromatic models
"""
import numpy as np

from fitspy.core.models import pseudovoigt
from fitspy.core.utils import with_independent_vars
from fitspy import PEAK_MODELS

MODE = '2θ'  # or 'qx'

# KL3/KL2 fluorescence energy ratio
WAVELENGTH_RATIO = {'Cu': 1.0024847494284688,
                    'Mo': 17.4793 / 17.3744,
                    'Ag': 22.1629 / 21.9903,
                    'Co': 6.9303 / 6.9153}
# KL3/KL2 fluorescence rate ratio
AMPLITUDE_RATIO = {'Cu': .558282 / .29913,
                   'Mo': .549 / .288,
                   'Ag': .5411 / .2865,
                   'Co': .58292 / .29807}
CATHODES = WAVELENGTH_RATIO.keys()


def is_bichromatic(name):
    return 'PseudoVoigtKa12' in name


def pseudovoigt_ka12(x, ampli, fwhm, x0, alpha=0.5, cathode='Cu', coefs=None):
    r"""
    Return a double Pseudovoigt function often used in X-Ray Diffraction when
    using a lab source delivering a bichromatic beam.
    When deriving Bragg law for both wavelength. The position of the Ka2 peak
    is fully determined by the Ka1 one. For sake a simplicity, fwhm2 is set to
    fwhm (minor approximation).

    .. math::

       2d_{hkl} \sin \theta_{1} = \lambda_{Ka1} \quad
       2d_{hkl} \sin \theta_{2} = \lambda_{Ka2} \quad
       \sin \theta_{2}  =  \frac{\lambda_{Ka2}}{\lambda_{Ka1}} \sin \theta_{1}

    The ratio between wavelengths depends on the cathode element (Cu, Mo, Ag, Co...).

    Parameters
    ----------
    x: ndarray
       '2θ' angles in degree or 'qx' (depending on 'MODE')
    ampli: float
      amplitude of the pseudo-Voigt
    fwhm: float
       width of the pseudo-Voigt
    x0: float
       center of the pseudo-Voigt
    alpha: float
       gaussian weight of the pseudo-Voigt
    cathode: str
       element of the X-ray source cathode
    coefs: iterable of 2 floats, optional
        coefficients applied to each peak contribution. Default values are (1, 1)

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models_bichromatic import pseudovoigt_ka12
        from fitspy.core.models_bichromatic import MODE, WAVELENGTH_RATIO, AMPLITUDE_RATIO

        x = np.linspace(68, 71, 2000)
        y = pseudovoigt_ka12(x, ampli=100, fwhm=.2, x0=69.14, alpha=0.5, cathode='Cu')
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    assert MODE in ['2θ', 'qx']
    coefs = coefs or (1., 1.)

    ampli2 = ampli / AMPLITUDE_RATIO[cathode]
    ratio = WAVELENGTH_RATIO[cathode]

    if MODE == '2θ':
        x02 = 2 * np.degrees(np.arcsin(ratio * np.sin(np.radians(x0 / 2.))))
    else:  # 'qx'
        x02 = ratio * x0
    fwhm2 = fwhm  # small approx

    return coefs[0] * pseudovoigt(x, ampli, fwhm, x0, alpha=alpha) + \
        coefs[1] * pseudovoigt(x, ampli2, fwhm2, x02, alpha=alpha)


def make_pseudovoigt_ka12_for(cathode):
    """ Return function associated with the 'given' cathode """
    assert cathode in CATHODES

    @with_independent_vars('x', 'coefs')
    def func(x, ampli, fwhm, x0, alpha=0.5, coefs=None):
        return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode=cathode, coefs=coefs)

    func.__name__ = f"pseudovoigt_ka12_{cathode}"
    func.__doc__ = f"PseudoVoigt Bi-chromatic related to '{cathode}' cathode"
    return func


def add_models():
    """ Add bichromatic models in the PEAK_MODELS list """
    for cathode in CATHODES:
        PEAK_MODELS.update({f"PseudoVoigtKa12_{cathode}": make_pseudovoigt_ka12_for(cathode)})


# WARNING : to maintain consistency, it is normally recommended not to remove models once added
# def remove_models():
#     """ Remove bichromatic models in the PEAK_MODELS list """
#     for cathode in CATHODES:
#         PEAK_MODELS.pop(f"PseudoVoigtKa12_{cathode}", None)

def plot_decomposition(ax, model, x, params, lw=None, color=None):
    """ Plot each peak contribution """
    if is_bichromatic(model.name2):
        ax.plot(x, model.eval(params, x=x, coefs=(1, 0)), lw=lw, color=color)
        ax.plot(x, model.eval(params, x=x, coefs=(0, 1)), lw=lw, color=color)


if __name__ == "__main__":
    from fitspy.core.spectrum import Spectrum
    import matplotlib.pyplot as plt

    MODE = '2θ'
    # MODE = 'qx'

    add_models()
    model_name = "PseudoVoigtKa12_Ag"

    spectrum = Spectrum()
    spectrum.x = np.linspace(1.8, 2.2, 2000)
    spectrum.y = PEAK_MODELS[model_name](spectrum.x, ampli=10, fwhm=0.01, x0=2)
    spectrum.add_peak_model(model_name, x0=2)
    spectrum.fit()

    _, ax = plt.subplots()
    spectrum.plot(ax)
    plt.show()
