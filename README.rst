|docs|_  |github|_  |pypi|_ 

.. |docs| image:: https://img.shields.io/badge/%F0%9F%95%AE-docs-green.svg
.. _docs: https://cea-metrocarac.github.io/fitspy/doc/index.html

.. |github| image:: https://img.shields.io/badge/GitHub-GPL--3.0-informational
.. _github: https://github.dev/CEA-MetroCarac/fitspy

.. |pypi| image:: https://img.shields.io/pypi/v/fitspy?label=pypi%20package
.. _pypi: https://pypi.org/project/fitspy/


.. image::
    
    :target: https://cea-metrocarac.github.io/fitspy/logo.png
    :align: center
    :width: 250

**Fitspy** is a generic tool dedicated to **fit sp**\ ectra in **py**\ thon with a GUI that aims to be as simple and intuitive to use as possible.

.. raw:: html

    <p align="center" width="100%">
    <img align="center" width="90%" src=https://cea-metrocarac.github.io/fitspy/fitspy.png>
    </p>
    </br>

Processed spectra may be independent of each other or may result from 2D-maps
acquisitions.

.. raw:: html

    <p align="center" width="100%">
    <img align="center" width="40%" src=https://cea-metrocarac.github.io/fitspy/2d-map.png> <br>
    <em>Example of fitspy 2D-map frame interacting with the main GUI.</em> 
    </p>

The predefined peak models considered in Fitspy are  :code:`Gaussian`, :code:`Lorentzian`, :code:`Asymetric Gaussian`, :code:`Asymetric Lorentzian` and :code:`Pseudovoigt`.

A :code:`constant`, :code:`linear`, :code:`parabolic` or :code:`exponential` background model can also be added in the fitting.

In both cases, :code:`user-defined models` can be added.

Fitspy main features:

- Fitspy uses the `lmfit <https://github.com/lmfit/lmfit-py>`_ library to fit the spectra
- The fit processing can be multi-threaded
- Bounds and constraints can be set on each peaks models parameter.
- From an automatic noise level estimation, according to the local noise, peak models can be automatically deactivated.
- Fitspy also includes automatic outlier detection to be excluded during the fitting process.

All actions allowed with the GUI can be executed in script mode (see examples `here <https://github.com/CEA-MetroCarac/fitspy/tree/main/examples>`_).
These actions (like baseline and peaks definition, parameters constraints, ...) can be saved in a `Fitspy model` and replayed as-is or applied to other new spectra datasets.


Installation
------------

.. code-block::

    pip install fitspy


Tests and examples execution
----------------------------

.. code-block::

    pip install pytest
    git clone https://github.com/CEA-MetroCarac/fitspy.git
    cd fitspy
    pytest
    python example/ex_gui_auto_decomposition.py
    ...


Quick start
-----------

Launch the application:

.. code-block::

    fitspy

Then, from the top to the bottom of the right panel:

- :code:`Select` file(s)
- *(Optional)* Define the **X-range**
- Define the baseline to :code:`subtract` *(left or right click on the figure to add or delete (resp.) a baseline point)*
- *(Optional)* Normalize the spectrum/spectra
- Click on the :code:`Fitting` panel to activate it
- Select :code:`Peak model` and add peaks *(left or right click on the figure to add or delete (resp.) a peak)*
- *(Optional)* Add a background (**BKG model**) to be fitted
- *(Optional)* Use **Parameters** to set bounds and constraints
- :code:`Fit` the selected spectrum/spectra
- *(Optional)* **Save** the parameters in **.csv** format
- *(Optional)* **Save** the **Model** in a .json file (to be replayed later)


See the `documentation <https://cea-metrocarac.github.io/fitspy/doc/index.html>`_ for more details.


Authors information
-------------------

In case you use the results of this code in an article, please cite:

- Quéméré P., (2024). Fitspy: A python package for spectral decomposition. *Journal of Open Source Software. (submitted)*

- Newville M., (2014). LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python. Zenodo. doi: 10.5281/zenodo.11813.