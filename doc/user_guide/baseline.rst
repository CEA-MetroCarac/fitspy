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

The background model approach consists in selecting a 'BKG' model that is taken into account with the peak models during the fit processing.

.. figure::  ../_static/gen_figures_bkg.png
   :align:   center


The available predefined `BKG models` are `Constant`, `Linear`, `Parabolic`, `Exponential` related to the `lmfit` standard models defined `here <https://lmfit.github.io/lmfit-py/builtin_models.html>`_.

In python scripting, as for the `Peak models`, **customized users `BKG models`** can be added from a new launcher file (named for instance *my_fistpy_launcher.py*) as follows::

    from fitspy.app.gui import fitspy_launcher
    from fitspy import BKG_MODELS

    def my_bkg_model_0(x, param_1, param_2, param_3):
        return ...

    def my_bkg_model_1(x, param_4, param_5):
        return ...

    BKG_MODELS.update({"My BKG Model 0": my_bkg_model_0})
    BKG_MODELS.update({"My BKG Model 1": my_bkg_model_1})

    fitspy_launcher()

where :code:`param_i` are the model parameters