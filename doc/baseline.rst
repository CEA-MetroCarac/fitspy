Baseline
========

.. figure::  _static/baseline.png
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