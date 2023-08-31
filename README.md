![](https://cea-metrocarac.github.io/fitspy/fitspy.png)

# Fitspy

**Fitspy** is a generic tool dedicated to **fit** **sp**ectra in **py**thon
with a GUI that aims to be as simple and intuitive to use as possible.

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

A `constant`, `linear`, `parabolic`, `gaussian` or `exponential` background can
also be added in the fitting.

All actions allowed with the GUI can be easily executed in script mode (see
examples [here](https://github.com/CEA-MetroCarac/fitspy/tree/main/examples)).
These actions (like baseline definition and removal, peaks definition,
parameters constraints, ...) can be saved in a 'fitspy' `model` and replayed as
is or applied to other new spectra.

See the [documentation](https://github.com/CEA-MetroCarac/fitspy/tree/main/doc) for more details.

### Installation

```
pip install fitspy
```


### Authors informations

In case you use the results of this code in an article, please cite:

- (To come)

