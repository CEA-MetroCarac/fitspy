"""
Module containing different basic models (gaussian, lorentzian, ...)
"""
import numpy as np

np.seterr(divide='ignore', invalid='ignore')


def gaussian(x, ampli, fwhm, x0):
    r"""
    Return Gaussian function defined as:
    :math:`ampli * e^{-(x-x0)^2/(2*\sigma^2)}`
    with :math:`\sigma = fwhm / (2*\sqrt{2*log(2)})`

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models import gaussian

        x = np.linspace(-10, 10, 201)
        y = gaussian(x, ampli=1, fwhm=2, x0=2)
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
    coef = 1. / (2 * sigma ** 2)
    return ampli * np.exp(-coef * (x - x0) ** 2)


def gaussian_asym(x, ampli, fwhm_l, fwhm_r, x0):
    r"""
    Return Asymmetric Gaussian function defined as:
    :math:`(x < x0) * Gaussian(fwhm\_l) +  (x >= x0) * Gaussian(fwhm\_r)`

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models import gaussian_asym

        x = np.linspace(-10, 10, 201)
        y = gaussian_asym(x, ampli=1, fwhm_l=4, fwhm_r=2, x0=2)
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    return (x < x0) * gaussian(x, ampli, fwhm_l, x0) + \
        (x >= x0) * gaussian(x, ampli, fwhm_r, x0)


def lorentzian(x, ampli, fwhm, x0):
    r"""
    Return Lorentzian function defined as:
    :math:`ampli * \frac{fwhm^2}{4 * ((x - x0)^2 + fwhm^2 / 4)}`

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models import lorentzian

        x = np.linspace(-10, 10, 201)
        y = lorentzian(x, ampli=1, fwhm=2, x0=2)
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    return ampli * fwhm ** 2 / (4 * ((x - x0) ** 2 + fwhm ** 2 / 4) + 1e-6)


def lorentzian_asym(x, ampli, fwhm_l, fwhm_r, x0):
    r"""
    Return Asymmetric Lorentzian function defined as:
    :math:`(x < x0) * Lorentzian(fwhm\_l) +  (x >= x0) * Lorentzian(fwhm\_r)`

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models import lorentzian_asym

        x = np.linspace(-10, 10, 201)
        y = lorentzian_asym(x, ampli=1, fwhm_l=4, fwhm_r=2, x0=2)
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    return (x < x0) * lorentzian(x, ampli, fwhm_l, x0) + \
        (x >= x0) * lorentzian(x, ampli, fwhm_r, x0)


def pseudovoigt(x, ampli, fwhm, x0, alpha=0.5):
    r"""
    Return Pseudovoigt function defined as:
    :math:`alpha * Gaussian + (1 - alpha) * Lorentzian`

    Example
    -------

    .. plot::

        import numpy as np
        import matplotlib.pyplot as plt
        from fitspy.core.models import pseudovoigt

        x = np.linspace(-10, 10, 201)
        y = pseudovoigt(x, ampli=1, fwhm=2, x0=2, alpha=0.5)
        plt.figure()
        plt.grid()
        plt.plot(x, y)
    """
    return alpha * gaussian(x, ampli, fwhm, x0) + \
        (1 - alpha) * lorentzian(x, ampli, fwhm, x0)
