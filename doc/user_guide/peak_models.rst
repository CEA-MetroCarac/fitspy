Peak models
===========

In addition to predefined peak models, the user can define and use their own models.

All of them are / should be defined from the following **peak parameters**:

- :math:`x0` : the peak position
- :math:`ampli` : the peak amplitude
- :math:`fwhm` : the Full Width at Half Maximum
- :math:`fwhm_l` : the `fwhm` at the left side of `x0` (for asymmetric model)
- :math:`fwhm_r` : the `fwhm` at the right side of `x0` (for asymmetric model)
- :math:`alpha` : weighting coefficient (used in pseudovoigt))

Predefined models
-----------------

The available predefined peak models are:

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


Custom models
-------------

Custom user models can be defined using a file named  :code:`fitspy_users_models.txt`, located in the :code:`%HOMEUSER%` directory.

Using basic python encoding, new peaks models can be added as follows::

    import numpy as np
    from lmfit.models import GaussianModel

    gaussian2_model = GaussianModel()

    def gaussian1(x, ampli, fwhm, x0):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        coef = 1. / (2 * sigma ** 2)
        return ampli * np.exp(-coef * (x - x0) ** 2)

    def gaussian2(x, x0, ampli, fwhm):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        return gaussian2_model.eval(x=x, center=x0, amplitude=ampli, sigma=sigma)

where here the `gaussian1` function/model and the :code:`gaussian2` function/model (defined from the built-in lmfit models) return exactly the same results as with the predefined :code:`Gaussian` model.

Note that the users function names are used as model names.

To be correctly interpreted by `Fistpy` the arguments passed to the functions must be chosen from the fit parameters defined at the top, regardless their order.