---
title: 'Fitspy: A Python package for spectral decomposition'
tags:
  - Python
  - spectrum
  - spectra
  - decomposition
  - fit
authors:
  - name: Patrick Quéméré
    orcid: 0009-0008-6936-1249
    affiliation: "1" # (Multiple affiliations must be quoted)
affiliations:
  - name: Univ. Grenoble Alpes, CEA, Leti, F-38000 Grenoble, France
    index: 1
date: 11 July 2023
bibliography: paper.bib

---

# Summary

**`Fitspy`** is a dedicated tool to **fit** **sp**ectra in **py**thon.

Spectrum decomposition (also known as fitting) is the choice of a linear combination of peak models to best represent an experimental spectrum. `Fitspy` currently has implementations for Gaussian, Lorentzian, related asymmetric functions and the Pseudovoigt model. User-defined models can also be added. For the fitting, the model parameters can be subject to bounds and constraints.
From a practical point of view, the `Fitspy` GUI (see \autoref{fig:GUI}) is designed to be as simple and intuitive to use as possible.

![The `Fitpsy` GUI.\label{fig:GUI}](https://cea-metrocarac.github.io/fitspy/fitspy.png){width=85%}

# Statement of need

The analysis of spectra in many areas of physics, from materials characterisation to astrophysics, often requires their decomposition into more or less complex models to estimate the chemical composition of the subject being analysed.
To carry out these decompositions, research communities can rely on spectral decomposition tools.
While many open-source tools for spectral fitting exist, most of them have, however, been designed for specific application domains, offering a broad range of services beyond mere spectral fitting. Consequently, these tools can prove challenging to use, especially for less experienced individuals.

In the vein of generic tools like `Fityk` [@Fityk] or `PRISMA`  [@PRISMA], `Fitspy` is a dedicated tool for spectral fitting — and only spectral fitting — with the following characteristics or functionalities:

* **Agnostic Nature**: `Fitspy` is not tied to any specific physical quantity or database. It is designed to process spectra regardless of their x-support and y-intensity without any prior knowledge.

* **Python Implementation**: `Fitspy` is coded in Python. As a result, for individuals with basic knowledge of the language, spectra can be easily processed by scripts.

* **2D Maps**: `Fitspy` has been designed to handle spectra derived from 2D acquisitions. Note that "2D" can encompass time or any other dimension. When dealing with 2D data, an interactive map in the `Fitspy` GUI allows users to locate and select spectra of interest easily.

* **Multiprocessing Capabilities**: `Fitspy` enables spectral fit processing on multiple processors, enhancing efficiency.

* **Constrained Parameters**: Leveraging the `lmfit` library [@lmfit], `Fitspy` empowers users to impose constraints on parameter ranges or establish constraints between parameters using literal expressions.

* **Simple GUI**: `Fitspy` has been designed to be as intuitive and simple to use as possible (subjective criterion).

To the author's knowledge, although many open-source softwares are much more advanced in certain aspects mentioned, none of them seems to encompass all the functionalities described above. Therefore, the features of `Fitspy` make it an ideal tool for quickly fitting a few spectra through its GUI or for fitting several thousand of spectra (or more) by python batches, as can occur in the context of large-scale parametric studies [@wafer].

# `Fitspy` workflow short description

`Fitspy` accepts at this time two types of input data file formats:

* a first format where each spectrum is stored individually in a `.txt` file. The input data file consists of a 2 columns base format where the first column is associated to the physical support of the spectrum (typically wavelengths) and the second to the corresponding spectrum intensity.

* the second format is associated to 2D-maps of spectra acquisitions. The related spectra are stored in a single file in which each spectrum is identified thanks to its grid coordinates (X,Y).

Once loaded in the GUI via a files selector widget, the spectra can be processed one by one or in groups (depending on spectra selected with the cursor in the file selector widget), or as a whole dataset.

Firstly, the users can choose to reduce the physical support (wavelength axis) to a range of interest for subsequent processing. They can also activate the `Attractors` capability, which are the local maxima of spectra obtained with the *signal.find_peaks()* function of the `scipy` library [@scipy].
These attractors can be used subsequently to normalise spectra or to select points associated with the baseline and peaks to be modelled (see below).

Once the range of interest and the spectra are (optionally) normalised, the users can define a **baseline** in order to make the spectra share a common, flat zero-intensity level.
This baseline can be defined in an automatic way or by the users, who positions characteristic points on the figure with the mouse.
These points can be left at their initial positions or attached to the spectrum profile (`Attached` mode).
In the latter case, the points can be attached either to the raw spectrum or to an averaged spectrum if the users wish to attenuate the effects of noise.
The baseline is then approximated over the entire spectrum range using either piecewise linear interpolation or an *n*-order polynomial approximation.

Once the baseline has been subtracted, the next step consists of defining the **peaks** of interest for the decomposition.
This can be done either directly in the figure by clicking, or by an `Auto` mode which consists of an iterative process to automatically determine the main peak locations.
Thanks to the functionalities offered by `lmfit`, each peak can be associated to a predefined model (a Gaussian model, a Lorentzian model, their asymmetric variants, or a Pseudovoigt model) or a user-defined model. These models rely essentially on 3 main parameters: a position, an amplitude and a width (full-width half-maximum, FWHM). This width can be differentiated *left and right* in the frame for an asymmetric model.

For the fit, a additional background model can be added.
**Bounds** can be imposed for each of the parameters as well as associated **constraints**. If required, these constraints can be used to link model parameters together, for instance in the case where a physical ratio between the amplitudes of 2 peaks is expected.

Finally, the parameters can be free to evolve during the fit processing or maintained fixed at their initial values.

Several fit options are also proposed, such as:

* taking into account only the positive values of the spectra.
* a (limited) choice of minimisation algorithms
* the maximum number of fit iterations
* the number of CPUs to be used during the fit processing.

At the end of the fit, the fit parameters and the statistics returned by `lmfit` are displayed in related widgets and can be exported in .csv and .txt files respectively.

All the processing steps previously described constitute a model in the sense of the `Fitspy` application that can be saved (in a .json file) and easily replayed as-is or applied to other spectra datasets.

In terms of visualization, the GUI allows the users to display all of the spectra simultaneously (`Show All` mode) or, when a spectrum is selected, to display the corresponding fit decomposition and its residual. Figure titles and axis names can be customized and peak models labeled.

All the actions described above can be performed through python scripts without using the GUI. In practice, when performing repeated analyses, for users having some Python skill, it may be useful to use `Fitspy` as follows:

1. create a `Fitspy model` with the GUI
2. save the model
3. apply the model to several sets of spectra using a python script

This is this approach that has been recently used by teams at CEA to process tens of thousands of PhotoLuminescence and Raman spectra acquired on wafers, taking advantage of the parallelism capabilities offered by `Fitpsy` (see \autoref{fig:wafer}).

![Example of a `Fitpsy` application used in photoluminescence to characterize exciton intensities on a wafer [@wafer].\label{fig:wafer}](https://cea-metrocarac.github.io/fitspy/2d-map-PL.png){width=85%}

# Acknowledgements

This work, carried out on the Platform for Nanocharacterisation (PFNC), was supported by the “Recherche Technologique de Base” program of the French National Research Agency (ANR).

# References