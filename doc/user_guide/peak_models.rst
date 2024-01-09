Peak models
===========

In addition to predefined peak models, the user can define and use their own models.
All of them should be defined from the following peak parameters:

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

When working with python script, customized users models can be easily defined from a new launcher file (named for instance *my_fistpy_launcher.py*, to be executed) as follows::

    from fitspy.app.gui import fitspy_launcher
    from fitspy.spectra import MODELS

    def my_model_0(x, param_1, param_2, param_3, ...):
        return ...

    def my_model_1(x, param_1, param_2, param_3, ...):
        return ...

    MODELS.update({"My Model 0": my_model_0})
    MODELS.update({"My Model 1": my_model_1})
    fitspy_launcher()

where the expression returned by the function :code:`my_model` is defined from arguments :math:`param_i` associated -fully or partially- with the fit parameters defined at the top section  **whatever their order**.