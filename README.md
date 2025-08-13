[![PyPI](https://img.shields.io/pypi/v/fitspy.svg)](https://pypi.org/project/fitspy/)
[![Github](https://img.shields.io/badge/GitHub-GPL--3.0-informational)](https://github.com/CEA-MetroCarac/fitspy)
[![Doc](https://img.shields.io/badge/%F0%9F%95%AE-docs-green.svg)](https://cea-metrocarac.github.io/fitspy/index.html)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10812333.svg)](https://doi.org/10.5281/zenodo.10812333)
[![status](https://joss.theoj.org/papers/971a02868d903c0b7c0cbc3d1cd3d139/status.svg)](https://joss.theoj.org/papers/971a02868d903c0b7c0cbc3d1cd3d139)


<p align="center" width="100%">
    <img align="center" width=250 src=https://cea-metrocarac.github.io/fitspy/logo.png>
</p>


**Fitspy** is a generic tool dedicated to **fit sp**ectra in **py**thon with GUIs that aims to be as simple and intuitive to use as possible.

<p align="center" width="100%">
    <img align="center" width="45%" src="https://cea-metrocarac.github.io/fitspy/_static/pyside/fitspy.png">
    <img align="center" width="45%" src="https://cea-metrocarac.github.io/fitspy/_static/tkinter/fitspy.png">
</p>
<p align="center">
    <em>Illustration of the PySide GUI (left) and Tkinter GUI (right).</em>
</p>

Processed spectra may be independent of each other or may result from 2D-maps
acquisitions.

<p align="center" width="100%">
    <img align="center" width="30%" src=https://cea-metrocarac.github.io/fitspy/2d-map.png> <br>
    <em>Example of fitspy 2D-map frame interacting with the main GUI.</em> 
</p>

![Demo](https://cea-metrocarac.github.io/fitspy/demo.gif)

The predefined peak models considered in Fitspy are  `Gaussian`, `Lorentzian`, `Asymetric Gaussian`, `Asymetric Lorentzian` and `Pseudovoigt`. Some `Bichromatic` models related to bichromatic sources are also available as explained [here](https://cea-metrocarac.github.io/fitspy/user_guide/peak_models.html#bichromatic-models)

A `Constant`, `Linear`, `Parabolic`, `Exponential` or `Power Law` background model can also be added in the fitting.

In both cases, `user-defined models` can be added.

Fitspy main features:

- Fitspy uses the [lmfit](https://github.com/lmfit/lmfit-py) library to fit the spectra
- The fit processing can be multi-threaded
- Bounds and constraints can be set on each peaks models parameter
- From an automatic noise level estimation, according to the local noise, peak models can be automatically deactivated
- Fitspy also includes automatic outlier detection to be excluded during the fitting process

All actions allowed with the GUI can be executed in script mode (see examples [here](https://github.com/CEA-MetroCarac/fitspy/tree/main/examples)).
These actions (like baseline and peaks definition, parameters constraints, ...) can be saved in a `Fitspy model` and replayed as-is or applied to other new spectra datasets.

## Installation

### From PyPI (recommended)

```bash
pip install fitspy
```

### From GitHub (latest version)

```bash
pip install git+https://github.com/CEA-MetroCarac/fitspy
```

*(See the [documentation](https://cea-metrocarac.github.io/fitspy/user_guide/intro.html#install-and-launching) for more details)*

## Upgrade

In the case of 'just' a **Fitspy** upgrade:

```bash
pip uninstall fitspy
pip install fistspy # considering here the install from Pypi 
```

For a full upgrade (**Fitspy** and its dependencies):

```bash
pip install fitspy --upgrade # considering here the install from Pypi
```

## Tests and examples execution

```
pip install pytest
git clone https://github.com/CEA-MetroCarac/fitspy.git
cd fitspy
pytest
python examples/ex_gui_auto_decomposition.py
python examples/ex_.......
```

*(See the [documentation](https://cea-metrocarac.github.io/fitspy/user_guide/intro.html#install-and-launching) for more details)*

## Quick start

Since its 2025.1 version, Fitspy can be launched using two interfaces: either the one corresponding to the original GUI built with **Tkinter**, or a more recent and advanced one, using **PySide**. As of 2025, both GUIs offer nearly identical features, but future efforts regarding fixes and updates will primarily focus on the PySide GUI.

<u>**PySide GUI**</u>:

Launch the application:

```
fitspy
```

From the right to the left, select the files to work with (considering the drag and drop capabilities).
Then, use the **Model**  panel to set the model parameters to be used during the fitting process.
Peaks and an optional baseline associated with the model can be defined interactively by clicking on the desired position in the figure after activating **Peak points** (or **Baseline points** resp.) from the **Click Mode** radiobuttons located under the figure.
Once the model build, The **Fit** can be launched. The corresponding model can be saved (in the **Model** panel) to be reload later (from the bottom-central panel) as-it with the same spectra (if the pathnames are still available) or just as a model for other spectra to be processed.

<u>**Tkinter GUI**</u>:

Launch the application:

```
fitspy-tk
```

From the top to the bottom of the right panel:

- `Select` file(s)
- *(Optional)* Define the **X-range**
- Define the baseline to `subtract` *(left or right click on the figure to add or delete (resp.) a baseline point)*
- *(Optional)* Normalize the spectrum/spectra
- Click on the `Fitting` panel to activate it
- Select `Peak model` and add peaks *(left or right click on the figure to add or delete (resp.) a peak)*
- *(Optional)* Add a background (**BKG model**) to be fitted
- *(Optional)* Use **Parameters** to set bounds and constraints
- `Fit` the selected spectrum/spectra
- *(Optional)* **Save** the parameters in **.csv** format
- *(Optional)* **Save** the **Model** in a .json file (to be replayed later)

*(See the [documentation](https://cea-metrocarac.github.io/fitspy/user_guide/workflow.html) for more details)*

## Acknowledgements

This work, carried out on the CEA - Platform for Nanocharacterisation (PFNC), was supported by the “Recherche Technologique de Base” program of the French National Research Agency (ANR).

Warm thanks to the [JOSS](https://joss.theoj.org/) reviewers ([@maurov](https://github.com/maurov) and [@FCMeng](https://github.com/FCMeng)) and editor ([@phibeck](https://github.com/phibeck)) for their contributions to enhancing Fitspy.

## Citations

In case you use the results of this code in an article, please cite:

- Quéméré P., (2024). Fitspy: A python package for spectral decomposition. Journal of Open Source Software. doi: [10.21105/joss.05868](https://doi.org/10.21105/joss.05868)

- Newville M., (2014). LMFIT: Non-Linear Least-Square Minimization and Curve-Fitting for Python. Zenodo. doi: [10.5281/zenodo.11813](https://doi.org/10.5281/zenodo.11813).
