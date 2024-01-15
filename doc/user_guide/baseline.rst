Baselines and Background models
===============================

Two approaches are available in `Fitspy` to handle **non-flattened profiles**:

* the **baseline** approach

*  the use of a **background model** during the spectra fitting

Baseline approach
-----------------

This approach entails manually predefining points to establish the baseline profile that will be subtracted before fitting.

From the baseline peaks, the profile all along the spectrum support is obtained by interpolation either from **piecewise** or **polynomial** approximations.

.. figure::  ../_static/gen_figures_baseline.png
   :align:   center

When setting a parameter named :code:`attached` to True, the baseline points are attached to the corresponding spectrum intensity profile.
This feature allows to adapt the baseline points to the spectrum notably when processing a dataset of spectra that have variations in intensity.

.. figure::  ../_static/gen_figures_baseline_attached.png
   :align:   center


Note that to minimize the impact of noise in the baseline attached-points definition, a smoothing can be considered on the spectra intensities before linking. This smoothing is based on a gaussian filtering considering :code:`sigma` as the standard deviation.


Background model
----------------

The background model approach consists in selecting a **BKG model** that is taken into account with the peak models during the fit processing.

.. figure::  ../_static/gen_figures_bkg.png
   :align:   center


The available predefined **BKG models** are :code:`Constant`, :code:`Linear`, :code:`Parabolic`, :code:`Exponential` related to the `lmfit` standard models defined `here <https://lmfit.github.io/lmfit-py/builtin_models.html>`_.

User-defined background models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the :code:`%HOMEUSER%/Fitspy` directory, user-defined models can be defined through expressions written in a file named  :code:`bkg_models.txt`::

    Linear_1 = slope * x + constant
    Exponential_1 = ampli * np.exp(-coef * x)

or using Python encoding, in a file named  :code:`bkg_models.py`::

    import numpy as np
    from fitspy import BKG_MODELS


    def linear(x, slope, constant):
        return slope * x + constant

    def exponential(x, ampli, coef):
        return ampli * np.exp(-coef * x)

    BKG_MODELS.update({"Linear_2": linear})
    BKG_MODELS.update({"Exponential_2": exponential})

where in the examples given above, the resulting :code:`Linear_1`, :code:`Linear_2` models yield identical results to those obtained from the predefined :code:`Linear` model, when converged.
The same for :code:`Exponential_1`, :code:`Exponential_2` and :code:`Exponential`.

.. warning::
    Unlike predefined models, user-defined models do not have 'guess' parameter fitting functions.
    All parameters are initialized to 1.
    This can lead to poor convergence of the background.
    To prevent this, it is advisable to review the model parameters using appropriate multiplier coefficients, considering that the initial values for the parameters are 1.

    Example: for a x-range in [0, 1000], the Exponential functions should be rather defined as :code:`ampli * np.exp(-coef * x / 1000)`
