# Fitspy

**Fitspy** is a generic tool dedicated to **fit** **sp**ectra in **py**thon.

Its GUI aims to be as simple and intuitive as possible.

Processed spectra may be independent of each other or may result from 2D-maps acquisitions.

The fitting algorithm relies on the [lmfit](https://github.com/lmfit/lmfit-py) library.
It has multiprocessing capabilities and allows bounds and constraints settings on each peaks models parameter.

The peak models considered in fitspy are :

* `Gaussian`
* `Lorentzian`
* `Asymetric Gaussian`
* `Asymetric Lorentzian`
* `Pseudovoigt` 

A `constant`, `linear`, `parabolic`, `gaussian` or `exponential` background can also be added in the fitting.

All actions allowed by the GUI can be easily executed in script mode (see examples [here](examples)).

All users instructions (baseline definition and removal, peaks definition, parameters constraints, ...) can be saved 
in a 'fitspy' `model` and replayed as is or applied to other new spectra.

<p align="center" width="100%">
    <img align="center" width="70%" src=doc/_static/fitspy.png>
    <img align="center" width="25%" src=doc/_static/2d-map.png>
</p>

### Authors informations

In case you use the results of this code in an article, please cite:

- (To come)

