Workflow
========


all the spectra fitting operations can be realized both by the GUI or by python scripts.

However, although python scripts can be very practical when working with repetitive actions (like batches in the case of parametric studies for instance), from a practical point of view, it is easier:

- 1/ to use the GUI to define **visually** a `Fitspy` model then

- 2/ to apply it to new data sets.


GUI Mode
--------

.. figure::  ../_static/workflow.png
   :align:   center
   :width:   300

.. raw:: html

   <br>

To create a `Fitspy` model:

- (`1 <gui.html?files_selection.html>`_) **Select file(s) from** :code:`Select Files`  **or**  :code:`Select Dir`
- (`2 <gui.html?overall_settings.html>`_) *Define the* :code:`X-range`
- (`3 <gui.html?baseline.html>`_) *Click on the* :code:`Baseline` *panel to activate it (if not)*
- (`4 <gui.html?baseline.html>`_) *Select baseline points on the main figure* **(*)**
- (`5 <gui.html?baseline.html>`_) :code:`subtract` the baseline to the selected spectra *or* :code:`subtract All` the baseline(s)
- (`6 <gui.html?fitting.html>`_) **Click on the** :code:`Peaks` **panel to activate it (if not)**
- (`7 <gui.html?fitting.html>`_) **Select a** :code:`Peak model`
- (`8 <gui.html?fitting>`_) *Select a peak point on the main figure* **(*)**
- (`9 <gui.html?fitting>`_) *Add a background* (:code:`BKG model`) *to be fitted*
- (`11 <gui.html?fitting>`_) *Use* :code:`Parameters` *to see the results and to set bounds and constraints for a new fitting*
- (`13 <gui.html?models>`_) :code:`Save Select` *or* :code:`Save All` *the `Models` in a `.json` file (to be replayed later)*

(*) **use left/right click on the figure to add/delete a baseline or a peak point**

Once saved, a `Fitspy` model enables to recover a previous state (as-it) if all the spectra defined in the model can be loaded again as follows:

- (`14 <gui.html?fitting>`_) :code:`Reload` *the `Fitspy` model (`.json` file)*
- (`10 <gui.html?fitting>`_) :code:`Fit` **or** :code:`Fit All` **the selected spectrum/spectra**
- (`12 <fitting.html>`_) :code:`Save (.csv)` **the fitting parameters**

Or, after removing all spectra in the file selector widget (:code:`Remove All`), the `Fitspy` model can be apply to another data set as follows:

- (`1 <gui.html?files_selection.html>`_) **Select file(s) from** :code:`Select Files`  **or**  :code:`Select Dir`
- (`13 <gui.html?models>`_) :code:`Load Model` *(associated to the first `spectra` if several)
- (`13 <gui.html?models>`_) :code:`Apply to Sel.` *or* :code:`Apply to All`
- (`10 <gui.html?fitting>`_) :code:`Fit` **or** :code:`Fit All` **the selected spectrum/spectra**
- (`12 <fitting.html>`_) :code:`Save (.csv)` **the fitting parameters**


Scripting Mode
--------------

Although it is more recommended to use the GUI to define **visually** a `Fitspy` model, here is a partial example of how to do it by script::


    from fitspy.spectrum import Spectrum

    spectrum = Spectrum()

    # load a spectrum to create the model
    spectrum.load_profile(fname=..., xmin=..., xmax=...)

    # baseline definition and subtract
    spectrum.baseline.points = [[..., ...,], [..., ...]] # (x, y) baseline points coordinates
    spectrum.subtract_baseline()

    # model creation (based on 2 peaks) and saving
    model0 = spectrum.create_model(0, 'Lorentzian', x0=..., ampli=...)
    model1 = spectrum.create_model(1, 'Lorentzian', x0=..., ampli=...)
    spectrum.models = [model0, model1]
    spectrum.save(fname_json=...)

For more details about functions and arguments to pass, see the `API doc <../api/fitspy.html>`_.

A `Fitspy` model ('.json' file) is applied to a data set as follows::

    from fitspy.spectra import Spectra
    from fitspy.spectrum import Spectrum

    # Fitspy model to be applied
    model = Spectra.load_model(fname_json=...)

    # list of the spectra pathnames to handle
    fnames = [..., ..., ...]

    spectra = Spectra()
    for fname in fnames:
        spectrum = Spectrum()
        spectrum.load_profile(fname)
        spectra.append(spectrum)

    # apply the model with fitting
    spectra.apply_model(model, ncpus=...)

    # save the calculated fitting parameters
    spectra.save_results(dirname_results=...)

Note that a '.csv' parameters file can be used to define first a basic `spectrum` model only based on `peaks` models definition, this one used to define more globally a `spectra` model as follows::

    import pandas as pd
    from fitspy.spectra import Spectra
    from fitspy.spectrum import Spectrum

    dfr = pd.read_csv(fname_csv=..., sep=';')
    peaks_model = []
    for i in dfr.index:
        params = list(dfr.iloc[i, 1:])
        model = Spectrum.create_model(i, *params)
        peaks_model.append(model)

    spectrum = Spectrum()
    spectrum.models = peaks_models

    # Basic Fitspy model to be applied (without baseline, x-range, ... considerations)
    model = spectrum.save()

    # model application (same as above)
    ...






