Overall settings
================

.. figure::  ../_static/overall_settings.png
   :align:   center

.. raw:: html

   <br>

:code:`X-range` allows the modification of the (x) support range associated with the current spectrum.

:code:`Apply to All`  applies the (x) support range defined in `X-range` to all the spectra.

:code:`Attractors` are associated with local maxima intensities. When activated, attractors are used for locating baseline and peaks points.
The attractors points are calculated using scipy.signal.find_peaks() based on the parameters defined in :code:`Settings`.
Refer to `scipy.signal.find_peaks <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html>`_ for more details.
