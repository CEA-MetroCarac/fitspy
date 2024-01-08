Normalization
=============

.. figure::  ../_static/normalization.png
   :align:   center

.. raw:: html

   <br>

An **optional** spectra normalization is offered and relies on the two following strategies:

* :code:`Maximum`: each spectrum is normalized to 100 based on its maximum intensity.

* :code:`Attractor`: each spectrum is normalized to 100 according to the intensity of the nearest attractor located at the x-position given by the user.

To be effective, the user should press on :code:`Apply to all`.