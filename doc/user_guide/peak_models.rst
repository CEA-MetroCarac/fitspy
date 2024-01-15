Peak models
===========

As for the background models, the peak models in `Fitspy` are issued either from predefined models, or by he user-defined models.

.. warning::
    To be correctly interpreted by `Fitspy`, all the models are / should be defined from the following parameters:

    - :math:`x0` : the peak position
    - :math:`ampli` : the peak amplitude
    - :math:`fwhm` : the Full Width at Half Maximum
    - :math:`fwhm_l` : the `fwhm` at the left side of `x0` (for the asymmetric models)
    - :math:`fwhm_r` : the `fwhm` at the right side of `x0` (for the asymmetric models)
    - :math:`alpha` : weighting coefficient (used in the Pseudovoigt model))

Predefined models
-----------------

The predefined peak models available in `Fitspy` are:

Gaussian
~~~~~~~~

.. math::
   ampli * exp({-(x-x0)^2/(2*\sigma^2)}) \quad with \quad \sigma = fwhm / (2*\sqrt{2*log(2)})

Lorentzian
~~~~~~~~~~

.. math::
   ampli * fwhm^2 / [4 * ((x - x0)^2 + fwhm^2 / 4)]

Asymetric Gaussian
~~~~~~~~~~~~~~~~~~

.. math::
   (x < x0) * Gaussian(fwhm_l) +  (x ≥ x0) * Gaussian(fwhm_r)

Asymetric Lorentzian
~~~~~~~~~~~~~~~~~~~~

.. math::
   (x < x0) * Lorentzian(fwhm_l) +  (x ≥ x0) * Lorentzian(fwhm_r)

Pseudovoigt
~~~~~~~~~~~

.. math::
   alpha * Gaussian + (1 - alpha) * Lorentzian


User-defined models
-------------------

In the :code:`%HOMEUSER%/Fitspy` directory, users models can be defined through expressions written in a file named  :code:`models.txt`::

    Gaussian_1 = ampli * exp(-(x - x0) ** 2 / (fwhm**2 / (4 * log(2))))


or using Python encoding, in a file named  :code:`models.py`::

    import numpy as np
    from lmfit.models import GaussianModel
    from fitspy import MODELS

    LMFIT_GAUSSIAN_MODEL = GaussianModel()

    def gaussian_2(x, ampli, fwhm, x0):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        coef = 1. / (2 * sigma ** 2)
        return ampli * np.exp(-coef * (x - x0) ** 2)

    def gaussian_3(x, x0, ampli, fwhm):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        return sigma * np.sqrt(2. * np.pi) * LMFIT_GAUSSIAN_MODEL.eval(x=x, center=x0, amplitude=ampli, sigma=sigma)

    MODELS.update({"Gaussian_2": gaussian_2})
    MODELS.update({"Gaussian_3": gaussian_3})

where in the examples given above, the resulting :code:`Gaussian_1`, :code:`Gaussian_2` and :code:`Gaussian_3` yield identical results to those obtained from the predefined :code:`Gaussian` model.

.. warning::
    users models issued from expressions in the `models.txt` are not serializable. Consequently, for **multiprocessing calculations**, the user should instead opt for models defined through the Python script.