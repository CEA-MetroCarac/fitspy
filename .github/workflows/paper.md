---
title: 'Fitspy : A Python package for spectra decomposition'
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
bibliography: https://github.dev/CEA-MetroCarac/fitspy/.github/workflows/paper.bib
---

# Summary

**Fitspy** is a tool dedicated to **fit** **sp**ectra in **py**thon.

Spectrum decomposition (also known as fitting) is based on peak models that can be in fitspy : `Gaussian`, `Lorientzan`, related `Asymetric` functions or `Pseudovoigt` ones. Spectrum decomposition corresponds to the resolution of a minimization problem, 
which can take into account bounds and constraints on model parameters.

The fitspy's graphical user interface (**GUI** - see \autoref{fig:GUI}) is designed to be as simple and intuitive as possible.

![Fitpsy GUI illustration.\label{fig:GUI}](https://cea-metrocarac.github.io/fitspy/fitspy.png)

# Statement of need

The analysis of spectra in many areas of physics, from materials characterisation to astrophysics, often requires decompositions
into more or less complex models to account for the chemical elements composition.
To carry out these decompositions, the research communities can rely on the services offered by numerous commercial or open source softwares. .

Although commercial softwares are often of very high quality and high performance, they are by definition subject to licensing
which is likely to limit their use within a team of researchers. 
In addition, the large amount of functionalities often offered in these softwares can sometimes make them difficult to use.
Finally, commercial softwares do not always make it easy to export the results in a open format (like .csv), 
or to save all the processing steps to be replayed. 
These 2 last aspects, among others, severely limit the results and models exchanges as well as 
 the use and re-use of models to analogeous set of spectra within reasearch teams.

On the other hand, in the world of Open Source and particularly in the world of Python programming, 
libraries such as @lmfit offer everything that is needed to carry out spectra decompositions. 
However, their implementation requires knowledge in programming, which limits their use by the greatest number of people.

Fitspy was therefore created to address the various weaknesses/drawbacks of each of these 2 options 
by providing an access to a spectral decomposition tool in open source with a GUI designed to be as simple as possible.

# Features

 Fitspy adresses presently 2 types of input file data format: 

* a first format where each spectrum is stored individually in a .txt file. The input data file consists of a 2 columns base format where
  the first one is associated to the physical support of the spectrum (typically wavelengths)
  and the seconde one to the corresponding spectrum intensity.

* the second format is associated to the 2D-map spectra acquisition mode.
  The related spectra are stored in a single file and each spectrum is identified thanks to its grid coordinates (X,Y).
  
Once loaded in the GUI via a files selection widget, the spectra can be processed one by one or by groups (depending on spectra selected with the cursor in the file selection widget) or as a whole if corresponding `Apply to All` exists.

Firstly, the user can choose to reduce the physical support to a range of interest for the next.<br>
he can also activate the "attractors" capabilities. The attractors correspond to local maxima, cobtained with @scipy. 
They can be used to define points of interest used to normalise spectra or to select points associated with
the baseline and peaks to be modelled (see below).

Once the range of interest and the (optional) spectra normalisation set, the user may define a baseline in order to flat the spectra.
This baseline can be defined in an automatic way or by the user himself by positionning characteristic points on the figure with the mouse.
These points can be left at their initial positions or attached to the spectrum profile ("Attached" mode). 
In the latter case, the points can be attached either to the the raw spectrum or to an averaged spectrum if the user wishes to attenuate the effects of noise.
The baseline is then approximated over the entire x-support using either piecewise linear interpolation or an *n*-order polynomial approximation.

Once the baseline has been subtracted, the next step consists in defining the peaks of interest for the decomposition.
This could be done either directly in the figure by clicking or by an 'Auto' mode which consists in an iterative process to automatically determine the main peaks locations.<br>
Thanks to the functionalities offered by lmfit, each peak can be associated to a model to choose among a Gaussian model,
a Lorentzian model, their Assymetric variations or a Pseudovoigt model. These models relies basically on 3 main parameters : a x position, an amplitude and a width (FWHM) that is differentiated (*left-right*) in the frame of assymetric variations.<br>
Bounds (min-max values) can also be defined for each of these parameters during the fit, as well as associated constraints.
If required, these constrains can be used to link models parameters together, for example in the case where a physical ratio between the amplitudes of 2 peaks is expected.

Finally, as part of the fit, the parameters can be free to evolve (within the bounds and according to the constraints defined above) or fixed at their initial values.

Several fit options are also proposed, such as :

* taking into account only the positive values of the spectra.
* a (limited) choice of minimisation algorithms
* the maximum number of fit iterations (used to determine whether the fit process has converged or not)
* and the number of CPUs to be used during the fit processing.

At the end of the fit, the fit parameters and the statistics returned by lmfit are displayed in related widgets and can be exported in .csv and .txt files respectively.<br><br>


All the processing steps previously described constitute a model in the sense of the fitspy application
that can be saved (in a .json file) and easily replayed as is or applied to other series of spectra.

In term of visualization, the GUI allows to display all the spectra simultaneously ('Show All' mode) or,
when a spectrum is selected, to display the corresponding fit decomposition and its residual. 
Figure titles and axes names can be changed, peaks model can be labelized, etc...

All the actions described above can of course be performed throught python scripts without using the GUI.<br>
On a practical point of view, inthe frame of repetitive processes and for users having some Python skillness, it may be useful to use fitspy as followed:

    * creating a model using the GUI,

    * saving the model,

    * apply the model to several sets of spectra using a script (just a few lines are needed).

This is the approach that has been recently followed by teams at CEA to process tens of thousands of Raman spectra acquired on microelectronics chips, taking advantage of the parallelism capabilities offered by fitpsy.


# Acknowledgements
This work was made possible thanks to the support of CEA and the resources made available to the "numeric" team at the nanocaracterisation platform
to develop such a tool and make it available to the research community.

