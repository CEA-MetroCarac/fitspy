<p align="center" width="100%">
    <img align="center" width=200 src=https://cea-metrocarac.github.io/fitspy/logo.png>
</p>

**Fitspy** is a generic tool dedicated to **fit** **sp**ectra in **py**thon
with a GUI that aims to be as simple and intuitive to use as possible.

<p align="center" width="100%">
    <img align="center" width="75%" src=https://cea-metrocarac.github.io/fitspy/fitspy.png>
</p>

Processed spectra may be independent of each other or may result from 2D-maps
acquisitions.
<p align="center" width="100%">
    <img align="center" width="30%" src=https://cea-metrocarac.github.io/fitspy/2d-map.png> <br>
    <em>Example of fitspy 2D-map frame interacting with the main GUI.</em> 

</p>

The fitting algorithm has multiprocessing capabilities and relies on
the [lmfit](https://github.com/lmfit/lmfit-py) library.<br>
Bounds and constraints can be set on each peaks models parameter.

The peak models considered in fitspy are :

* `Gaussian`
* `Lorentzian`
* `Asymetric Gaussian`
* `Asymetric Lorentzian`
* `Pseudovoigt`

A `constant`, `linear`, `parabolic` or `exponential` background can
also be added in the fitting.

All actions allowed with the GUI can be easily executed in script mode (see
examples [here](https://github.com/CEA-MetroCarac/fitspy/tree/main/examples)).
These actions (like baseline definition and removal, peaks definition,
parameters constraints, ...) can be saved in a 'fitspy' `model` and replayed as
is or applied to other new spectra.


### Installation

```
pip install fitspy
```

### Tests and examples execution

```
pip install pytest
git clone https://github.com/CEA-MetroCarac/fitspy.git
cd fitspy
pytest
python example/ex0_gui_auto_decomposition.py
...
```

### Quick start

Launch the application:
```
fitspy
```
Then, from the top to the bottom of the right panel:

- `Select` file(s)
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* Define the **X-range**</span>
- Define the baseline to `subtract` *(left or right click on the figure to add or delete (resp.) a baseline point)*
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* Normalize the spectrum/spectra</span>
- Click on the `Peaks` panel to activate it
- Select `Peak model` and add peaks *(left or right click on the figure to add or delete (resp.) a peak)*
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* Add a background (**BKG model**) to be fitted</span>
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* Use **Parameters** to set bounds and constraints</span>
- `Fit` the selected spectrum/spectra 
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* **Save** the parameters in **.csv** format</span>
- <span style="color: rgba(0, 0, 0, 0.3);">*(Optional)* **Save** the **Model** in a .json file (to be replayed later)</span>

See the [documentation](https://github.com/CEA-MetroCarac/fitspy/tree/main/doc) for more details.


### Authors informations

In case you use the results of this code in an article, please cite:

- Patrick Quéméré, Univ. Grenoble Alpes, CEA, Leti, F-38000 Grenoble, France, https://github.dev/CEA-MetroCarac/fitspy