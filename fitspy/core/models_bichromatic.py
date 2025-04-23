"""
Module related to bichromatic models
"""
import numpy as np

from fitspy.core.models import pseudovoigt
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


def pseudovoigt_ka12(x, ampli, fwhm, x0, alpha=0.5, cathode='Cu'):
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

    ampli2 = ampli / AMPLITUDE_RATIO[cathode]
    ratio = WAVELENGTH_RATIO[cathode]

    if MODE == '2θ':
        x02 = 2 * np.degrees(np.arcsin(ratio * np.sin(np.radians(x0 / 2.))))
    else:  # 'qx'
        x02 = ratio * x0
    fwhm2 = fwhm  # small approx
    return pseudovoigt(x, ampli, fwhm, x0, alpha=alpha) + \
        pseudovoigt(x, ampli2, fwhm2, x02, alpha=alpha)


def pseudovoigt_ka12_Cu(x, ampli, fwhm, x0, alpha=0.5):
    """ PseudoVoigt Bi-chromatic related to 'Cu' cathode """
    return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Cu')


def pseudovoigt_ka12_Mo(x, ampli, fwhm, x0, alpha=0.5):
    """ PseudoVoigt Bi-chromatic related to 'Mo' cathode """
    return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Mo')


def pseudovoigt_ka12_Ag(x, ampli, fwhm, x0, alpha=0.5):
    """ PseudoVoigt Bi-chromatic related to 'Ag' cathode """
    return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Ag')


def pseudovoigt_ka12_Co(x, ampli, fwhm, x0, alpha=0.5):
    """ PseudoVoigt Bi-chromatic related to 'Co' cathode """
    return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Co')


def add_models():
    """ Add bichromatic models in the PEAK_MODELS list """
    for cathode in CATHODES:
        PEAK_MODELS.update({f"PseudoVoigtKa12_{cathode}": eval(f"pseudovoigt_ka12_{cathode}")})


def remove_models():
    """ Remove bichromatic models in the PEAK_MODELS list """
    for cathode in CATHODES:
        PEAK_MODELS.pop(f"PseudoVoigtKa12_{cathode}", None)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    MODE = '2θ'
    # MODE = 'qx'

    x = np.linspace(-10, 10, 201)
    plt.figure()
    plt.plot(x, pseudovoigt_ka12_Cu(x, ampli=100, fwhm=.5, x0=69.14, alpha=0.5))
    plt.show()

    x = np.linspace(1.8, 2.2, 2000)
    plt.figure()
    plt.plot(x, pseudovoigt_ka12_Ag(x, ampli=10, fwhm=0.01, x0=2))
    plt.show()
