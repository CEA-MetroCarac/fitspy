GUI description
===============

Files selection
---------------

The files selection is realized with the following widget:

.. figure::  ../_static/files_selector.png
   :align:   center

.. raw:: html

   <br>

:code:`Select Files` enables to load spectra (as '.txt' files) selected individually or by block while :code:`Select Dir.` loads all spectra that are contained in a selected directory.

Once loaded in the GUI, if `Fitspy` detects that a '.txt' file corresponds to a 2D-map input data file (via the tabulation :code:`\t` as first character), this one is expanded.
That is to say that each spectra of the 2D-map appears individually in the files selection widget according to the 2D-map file basename and the (X) and (Y) spectrum coordinates in the grid as prefix::

    {basename} X={X} Y={Y}


A  2D-map figure is also opened to facilitate both the spectrum selection and the interaction with the files selector widget.


.. figure::  ../_static/2d-map.png
   :align:   center
   :width:   50%

   interactive 2D-map figure resulting from a `fully defined ordered acquisition grid <https://github.com/CEA-MetroCarac/fitspy/tree/main/examples/data/2D_maps/ordered_map.txt>`_



Global actions
--------------

.. figure::  ../_static/global_actions.png
   :align:   center

.. raw:: html

   <br>

:code:`Show All` enables a global display of all the spectra. When clicking on the canvas with the mouse, the nearest spectra are highlighted (up to a maximum of 10 spectra).

:code:`Auto eval` and :code:`Auto eval All`  perform automatic evaluation of the baseline and peak positions and conduct fitting on the selected spectra or all the spectra (respectively).

:code:`Save settings` enables the saving of user settings in a **.fitspy.json** file located in the :code:`%HOMEUSER%` directory (open this file to have a look on which and how settings are saved).

:code:`Reinitialize` and :code:`Reinitialize All` reinitialize the spectrum and all the spectra (resp.) to their original values.


Overall settings
----------------

.. figure::  ../_static/overall_settings.png
   :align:   center

.. raw:: html

   <br>

:code:`X-range` allows the modification of the (x) support range associated with the current spectrum.

:code:`Apply to All`  applies the (x) support range defined in `X-range` to all the spectra.

:code:`Attractors` are associated with local maxima intensities. When activated, attractors are used for locating baseline and peaks points.
The attractors points are calculated using scipy.signal.find_peaks() based on the parameters defined in :code:`Settings`.
Refer to `scipy.signal.find_peaks <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html>`_ for more details.


Baseline
--------

.. figure::  ../_static/baseline.png
   :align:   center

.. raw:: html

   <br>

**The current frame is activated and deactivated when clicking on it.**

:code:`Import` enables the user to import their own baseline profiles. The imported file should contain 2 columns associated with the (x,y) coordinates of the baseline points.
Similar to spectrum profiles, the separators between the columns can be tabulation :code:`\t`, comma :code:`,`, semicolon :code:`;` or space :code:`\ `.
Note that the first row is skipped, and the (x, y) rows can be unordered.

:code:`Auto` can be used for the automatic determination of baseline points, considering the :code:`Min distance` (minimum distance) between two consecutive points (in pixels).

:code:`Attached` makes the baseline attached to either the raw spectrum profile or a smoothed one derived from Gaussian filtering applied to the raw spectrum profile, using :code:`Sigma` as the standard deviation (in pixels).

Baseline profiles are defined either through :code:`Linear` piecewise or :code:`Polynomial` approximation, considering the specified :code:`Order`.
It's important to note that a '*n*'-order polynomial approximation requires at least '*n+1*' points to be satisfied.


Normalization
-------------

.. figure::  ../_static/normalization.png
   :align:   center

.. raw:: html

   <br>

An **optional** spectra normalization is offered and relies on the two following strategies:

* :code:`Maximum`: each spectrum is normalized to 100 based on its maximum intensity.

* :code:`Attractor`: each spectrum is normalized to 100 according to the intensity of the nearest attractor located at the x-position given by the user.

To be effective, the user should press on :code:`Apply to all`.


Fitting
-------

.. figure::  ../_static/peaks.png
   :align:   center

.. raw:: html

   <br>

**The current frame is activated and deactivated when clicking on it.**

:code:`Auto` can be used for the automatic determination of peaks, considering the selected :code:`Peak model`.


For manual peaks positioning by the user, each :code:`Peak model` (to be chosen between **Gaussian**, **Lorentzian**, **Asymetric Gaussian**, **Asymetric Lorentzian**, **Pseudovoigt** or Custom models, see `here <peak_models.html>`_) is applied when left-clicking in the figure. (A right-click in the figure removes the nearest peak).


:code:`Fit` and :code:`Fit All` perform the fitting based on the conditions defined in the :code:`Fit Settings` widget:

.. figure::  ../_static/fit_settings.png
   :align:   center

.. raw:: html

   <br>

`maximum iterations` can be used to limit the number of iterations, saving CPU time processing consequently.
(An iteration corresponds to a gradient descent attached to all the fit parameters).

Spectrum fit success or failure (related to reaching a fit convergence criterion before reaching the `maxmimum iterations`) is displayed in green or orange (resp.) in the file selector widget.

**It is worth noting that performing several successive fits on a spectrum may slightly change the fitted parameters.**

:code:`Parameters` allows the visualization of parameters values and statistics related to the fitting process.
The :code:`Parameters` widget can be used to interact with each of the spectra (deleting or labeling peak models, redefining models).
By default, all parameters are considered as free but may be fixed during the fitting using the right-handed selection boxes.

.. figure::  ../_static/parameters.png
   :align:   center

.. raw:: html

   <br>

Bounds and fit constraints can be addressed by activating the dedicated selectors located at the top of the parameters widget.

**Bounding** consists in giving left and right parameters bounds.<br>

**Constraints** relies on expressions that can be parameters-dependent, using the prefix defined in the 2nd column.<br>
The example below shows how to constrain the second fitted peak to be half the amplitude of the first one.

.. figure::  ../_static/fit_constraint.png
   :align:   center

.. raw:: html

   <br>

:code:`Save (.csv)` consists of saving the fitted parameters and related statistics in a
folder predefined by the user, respectively in a .csv and a .txt file using the spectrum file basename.


Models
------

.. figure::  ../_static/models.png
   :align:   center

.. raw:: html

   <br>

The **Models** frame is used to save and replay a full spectra processing as-is.

:code:`Save Selec.` or :code:`Save All` allows saving the spectra processing associated with the selected spectra in the files selection widget, or with all the spectra (resp.).

:code:`Reload` replays exactly the spectra processing related to the imported *.json*.
This implies that all the files defined in the *.json*  are reachable when reloading.

:code:`Load Model` consists of reloading the spectrum model (baseline and peaks definition, ...) but **not the spectrum file itself**, related to the first model saved in the *.json*.

:code:`Apply to Sel.` or :code:`Apply to All` allows applying the loaded model to the spectra selected in the files selection widget, or to all the spectra (resp.).


Main Figure
-----------

The main Figure widget displays the loaded spectra and allows manipulation of baseline and peaks models with the mouse.

The standard navigation toolbar from *Matplotlib* allows panning, zooming and saving the current figure.
The function associated with the |home|
icon has been reconfigured to allow spectra rescaling.

.. |home| image:: ../_static/home.png

.. figure:: ../_static/navigation_toolbox.png
   :align:   center

.. raw:: html

   <br>

:code:`Figure settings` (at the top) allows personalizing plots displays, figure title, and axis labels.

.. figure::  ../_static/figure_settings.png
   :align:   center

.. raw:: html

   <br>

:code:`Save All (.png)` (at the bottom) allows saving all the spectra figures in .png format. (Be cautious with 2D-maps as they can generate a large number of figures).

Note that to ease copy/paste, :code:`CTRL+C` allows putting the current figure in the clipboard (only available on Windows).


2D-map Figures
--------------

The 2D-map Figure widgets allow easy selection of spectra and interaction with the cursor selection of the files selector widget.

By default, the full range of integrated spectra intensity is displayed.
A range slider in the figure allows specifying the summation bounds.
Once peaks have been defined, the corresponding model parameters can be also visualized in the 2D-map figures.

.. figure:: ../_static/2d-map_intensity_fwhm.png
   :align:   center

   left: intensity field in a 2D-map figure (default mode). right: FWHM values associated to 'Peak I' (obtained after fitting).