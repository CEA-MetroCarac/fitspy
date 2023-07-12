---
title: 'Fitspy: A Python package for spectra decomposition'
tags:
  - Python
  - spectrum
  - spectra	
  - decomposition
  - fit
authors:
  - name: Patrick Quéméré
    orcid: 0000-0000-0000-0000
    affiliation: "1" # (Multiple affiliations must be quoted)
affiliations:
 - name: Univ. Grenoble Alpes, CEA, Leti, F-38000 Grenoble, France
   index: 1
date: 11 July 2023
bibliography: paper.bib

---

# Summary

**`Fitspy`** is a dedicated tool to **fit** **sp**ectra in **py**thon.

Spectrum decomposition (also known as fitting) is the choice of a linear combination of peak models to best represent an experimental spectrum. `fitspy` currently has implementations for: Gaussian, Lorientzan, related asymmetric functions and the Pseudovoigt model. Spectrum decomposition corresponds to the resolution of a minimization problem, which can be subject to bounds and constraints on model parameters.

The `fitspy` GUI (see \autoref{fig:GUI}) is designed to be as simple and intuitive to use as possible.

![The `fitpsy` GUI.\label{fig:GUI}](https://cea-metrocarac.github.io/fitspy/fitspy.png){width=85%}

# Statement of need

The analysis of spectra in many areas of physics, from materials characterisation to astrophysics, often requires their decomposition
into more or less complex models to estimate the chemical composition of the subject being analysed.
To carry out these decompositions, research communities can rely on spectral decomposition tools provided in numerous commercial or open source softwares.

Although commercial software is often of very high quality and high performance, they are by definition subject to licensing
which is likely to limit their use within a team of researchers. 
In addition, the large amount of functionalities often proposed in these softwares can sometimes make them difficult to use.
Finally, commercial softwares do not always make it easy to export the results in a open format (like .csv), or to save all the processing steps to be modified at a later time.
These 2 last aspects, among others, severely limit the exchange of results and models within research teams as well as the use and re-use of models to compare analogous sets of spectra.

On the other hand, in the world of Open Source and particularly in the world of Python programming, libraries such as `lmfit` (cf. @lmfit) offer everything that is needed to carry out spectral decomposition. However, their implementations require knowledge in programming, which limits their use by a large groups of people.

`Fitspy` was therefore created to address the weaknesses/drawbacks of each of these 2 approaches by providing a spectral decomposition tool with a GUI designed to be as simple as possible to use.

# `Fitspy` workflow short description

 `Fitspy` accepts at this time two types of input data file formats: 

* a first format where each spectrum is stored individually in a `.txt` file. The input data file consists of a 2 columns base format where the first column is associated to the physical support of the spectrum (typically wavelengths) and the second to the corresponding spectrum intensity.

* the second format is associated to 2D-maps of spectra acquisitions. The related spectra are stored in a single file in which each spectrum is identified thanks to its grid coordinates (X,Y).
  
Once loaded in the GUI via a file-selection widget, the spectra can be processed one by one, in groups depending on spectra selected with the cursor in the file selection widget, or as a whole dataset.

Firstly, the user can choose to reduce the physical support (wavelength axis) to a range of interest for subsequent processing. They can also activate the `Attractors` capability, which are local maxima of a spectrum obtained thanks to the *signal.find_peaks()* function of the `scipy` library (cf. @scipy). 
These attractors can be used subsequently to normalise spectra or to select points associated with the baseline and peaks to be modelled (see below).

Once the range of interest and the spectra are (optionally) normalised, the user can define a **baseline** in order to make the spectra share a common, flat zero-intensity level.
This baseline can be defined in an automatic way or by the user, who positions characteristic points on the figure with the mouse.
These points can be left at their initial positions or attached to the spectrum profile (`Attached` mode).
In the latter case, the points can be attached either to the the raw spectrum or to an averaged spectrum if the user wishes to attenuate the effects of noise.
The baseline is then approximated over the entire spectrum range using either piecewise linear interpolation or an *n*-order polynomial approximation.

Once the baseline has been subtracted, the next step consists od defining the **peaks** of interest for the decomposition.
This can be done either directly in the figure by clicking, or by an `Auto` mode which consists of an iterative process to automatically determine the main peak locations.
Thanks to the functionalities offered by `lmfit`, each peak can be associated to a model, with implementations at this time of a Gaussian model, a Lorentzian model, their asymmetric variants, and a Pseudovoigt model. These models rely essentially on 3 main parameters: a position, an amplitude and a width (full-width half-maximum, FWHM). This width can be differentiated *left-right* in the frame for an asymmetric model.

For the fit, **bounds** can be defined for each of the parameters as well as associated **constraints**. If required, these constraints can be used to link model parameters together, for instance, in the case where a physical ratio between the amplitudes of 2 peaks is expected.

Finally, the parameters can be free to evolve during the fit processing or maintained fixed at their initial values.

Several fit options are also proposed, such as:

* taking into account only the positive values of the spectra.
* a (limited) choice of minimisation algorithms
* the maximum number of fit iterations (used to determine whether the fit process has converged or not)
* the number of CPUs to be used during the fit processing.

At the end of the fit, the fit parameters and the statistics returned by `lmfit` are displayed in related widgets and can be exported in .csv and .txt files respectively.

All the processing steps previously described constitute a model in the sense of the `fitspy` application that can be saved (in a .json file) and easily replayed as-is or applied to other series of spectra.

In term of visualization, the GUI allows the user to display all of the spectra simultaneously (`Show All` mode) or, when a spectrum is selected, to display the corresponding fit decomposition and its residual. Figure titles and axis names can be changed and peak models can be labeled.

All the actions described above can be performed through python scripts without using the GUI. In practice, when performing repeated analyses and for users having some Python skill, it may be useful to use `fitspy` as follows:

1. create a model with the GUI
2. save the model
3. apply the model to several sets of spectra using a python script

This is this approach that has been recently used by teams at CEA to process tens of thousands of Raman spectra acquired on microelectronics chips, taking advantage of the parallelism capabilities offered by `fitpsy`.

# Acknowledgements
This work was made possible thanks to the support of CEA and the resources made available to the "numeric" team at the Nano-Characterisation Platform (PFNC) to develop such a tool and make it available to the research community.


# References