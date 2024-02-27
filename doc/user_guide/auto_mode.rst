Auto mode
=========

An automatic mode for defining baseline and peak models is proposed in Fitspy. This can help in certain cases but will never override the acuity of a model manually defined by the user.

:code:`Auto eval` mode in the GUI corresponds to the successive execution of the :code:`Auto` mode for **Baseline** followed by the :code:`Auto` mode for **Fitting**


Baseline Auto
-------------

The :code:`Auto` mode, in the case of baselines, consists of defining the minimum intensity points using the `find_peaks() <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html>`_ function from scipy and a certain minimum distance between points, given by :code:`Min. distance` (in pixel) in the GUI.



Fitting Auto
------------

In the case of fitting, the :code:`Auto` mode involves an iterative process of residual minimization.

At each iteration, a peak model (according to the type defined by the user) is associated with the maximum intensity of the residual, which then joins the peaks defined in the previous iterations. The process of adding peak models and fitting stops when the maximum residual intensity falls below a certain threshold (currently set to 10% of the maximum amplitude of the spectrum).