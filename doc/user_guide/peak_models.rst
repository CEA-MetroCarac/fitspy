Peak models
===========

As for the background models, the peak models in `Fitspy` are issued either from **predefined models**, or by **user-defined models**.


Predefined models
-----------------

The predefined peak models available in `Fitspy` relies on the following parameters:

- :math:`x0` : the peak position
- :math:`ampli` : the peak amplitude
- :math:`fwhm` : the Full Width at Half Maximum
- :math:`fwhm_l` : the `fwhm` at the left side of `x0` (for the asymmetric models)
- :math:`fwhm_r` : the `fwhm` at the right side of `x0` (for the asymmetric models)
- :math:`alpha` : weighting coefficient (used in the Pseudovoigt model)

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

As for the background, users models can be defined through literal expressions in a *'.txt'* file or from python scripts in a *'.py'* file.

Example of a model defined by a literal expression::


    Gaussian_1 = ampli * exp(-(x - x0) ** 2 / (fwhm**2 / (4 * log(2))))


Example of a model defined in python::

    import numpy as np
    from lmfit.models import GaussianModel
    from fitspy import PEAK_MODELS

    LMFIT_GAUSSIAN_MODEL = GaussianModel()

    def gaussian_2(x, ampli, fwhm, x0):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        coef = 1. / (2 * sigma ** 2)
        return ampli * np.exp(-coef * (x - x0) ** 2)

    def gaussian_3(x, x0, ampli, fwhm):
        sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
        return sigma * np.sqrt(2. * np.pi) * LMFIT_GAUSSIAN_MODEL.eval(x=x, center=x0, amplitude=ampli, sigma=sigma)

    PEAK_MODELS.update({"Gaussian_2": gaussian_2})
    PEAK_MODELS.update({"Gaussian_3": gaussian_3})

where in the examples given above, the resulting :code:`Gaussian_1`, :code:`Gaussian_2` and :code:`Gaussian_3` yield identical results to those obtained from the predefined :code:`Gaussian` model.

The users models must be defined with the same parameters that those used in the predefined models concerning the peak position and amplitude (:code:`x` and :code:`ampli`). Concerning the width of the peak models, it is recommended (but not required) to use the :code:`fwhm` (or derived parameter). Extra parameters can also be used but in such cases, it is important to know that these parameters will be initialized to 1 before the fitting process and will be not subject to any range limitations.

Similarly to the background models:

Through the GUI, the corresponding *'.txt'* or *'.py'* files can be loaded via the button :code:`Load` located to the right of the **Peak model** combobox.

In python, the users models can be loaded by the functions :func:`~fitspy.utils.load_models_from_txt` and :func:`~fitspy.utils.load_models_from_py`.
*(See example in* `ex_gui_users_defined_models.py <https://github.com/CEA-MetroCarac/fitspy/tree/main/examples/ex_gui_users_defined_models.py>`_ *)*

.. note::

    **For recurrent use**, the user-defined models can be defined in files named :code:`peak_models.txt` or :code:`peak_models.py` to put in :code:`%HOMEUSER%/Fitspy`.

Bichromatic models
------------------

In the case of bichromatic sources, as used for example in **XRD** or **XRF**, double-peak models can be defined and applied using the **recurrent use** approach notified in the **User-defined** section above.
Here is an example of a peak_models.py file to be placed in :code:`%HOMEUSER%/Fitspy`, considering:

:math:`x0` : the peak position as 2Theta angle in degree

and

.. math::
    2d_{hkl} \sin \theta_{1} = \lambda_{Ka1}
    2d_{hkl} \sin \theta_{2} = \lambda_{Ka2}
    \sin \theta_{2}  =  \frac{\lambda_{Ka2}}{\lambda_{Ka1}} \sin \theta_{1}

::

    import numpy as np
    from fitspy.core.models import pseudovoigt
    from fitspy import PEAK_MODELS

    def pseudovoigt_ka12(x, ampli, fwhm, x0, alpha=0.5, cathode='Cu'):

        # KL3/KL2 fluorescence energy ratio
        wavelength_ratio = {'Cu': 1.0024847494284688,
                            'Mo': 17.4793 / 17.3744,
                            'Ag': 22.1629 / 21.9903,
                            'Co': 6.9303 / 6.9153}

        # KL3/KL2 fluorescence rate ratio
        amplitude_ratio = {'Cu': .558282 / .29913,
                           'Mo': .549 / .288,
                           'Ag': .5411 / .2865,
                           'Co': .58292 / .29807}

        ampli2 = ampli / amplitude_ratio[cathode]
        ratio = wavelength_ratio[cathode]

        x02 = 2 * np.degrees(np.arcsin(ratio * np.sin(np.radians(x0 / 2.))))
        fwhm2 = fwhm # small approx

        return pseudovoigt(x, ampli, fwhm, x0, alpha=alpha) + \
            pseudovoigt(x, ampli2, fwhm2, x02, alpha=alpha)


    def pseudovoigt_ka12_Cu(x, ampli, fwhm, x0, alpha=0.5):
        return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Cu')

    def pseudovoigt_ka12_Mo(x, ampli, fwhm, x0, alpha=0.5):
        return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Mo')

    def pseudovoigt_ka12_Ag(x, ampli, fwhm, x0, alpha=0.5):
        return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Ag')

    def pseudovoigt_ka12_Co(x, ampli, fwhm, x0, alpha=0.5):
        return pseudovoigt_ka12(x, ampli, fwhm, x0, alpha, cathode='Co')

    PEAK_MODELS.update({"PseudoVoigtKa12_Cu": pseudovoigt_ka12_Cu})
    PEAK_MODELS.update({"PseudoVoigtKa12_Mo": pseudovoigt_ka12_Mo})
    PEAK_MODELS.update({"PseudoVoigtKa12_Ag": pseudovoigt_ka12_Ag})
    PEAK_MODELS.update({"PseudoVoigtKa12_Co": pseudovoigt_ka12_Co})