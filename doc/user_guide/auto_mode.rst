Auto mode
=========

An automatic mode for defining baseline and peak models is proposed in Fitspy. This can help in certain cases but will never override the acuity of a model manually defined by the user.

:code:`Auto eval` mode (in the Tkinter GUI only by using the python scripting) corresponds to the successive execution of the :code:`Semi-Auto` option for **Baseline** (see `here <baseline.html?semi-automatic-approach=#semi-automatic-approach>`_) followed by the :code:`Auto` mode for **Fitting**


The :code:`Auto` mode in **Fitting** involves an iterative process of residual minimization.

At each iteration, a peak model (according to the type defined by the user) is associated with the maximum intensity of the residual, which then joins the peaks defined in the previous iterations. The process of adding peak models and fitting stops when the maximum residual intensity falls below a certain threshold (currently set to 10% of the maximum amplitude of the spectrum).