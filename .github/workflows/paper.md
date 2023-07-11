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
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
affiliations:
 - name: Univ. Grenoble Alpes, CEA, Leti, F-38000 Grenoble, France
   index: 1
date: 11 July 2023
bibliography: paper.bib
---

# Summary

**Fitspy** is a tool dedicated to **fit** **sp**ectra in **py**thon.
Spectrum decomposition (also known as fitting) are based on peak models that can be Gaussian, Lorientzan, related Asymetric functions or Pseudovoigt ones.
Spectrum decomposition corresponds to the resolution of a minimization problem, 
which can take into account bounds and constraints on model parameters. 
The fitspy's graphical user interface (GUI) is designed to be as simple and intuitive as possible.

# Statement of need

The analysis of spectra in many areas of physics, from materials characterisation to astrophysics, often requires decompositions
into more or less complex models to account for the chemical elements.
To carry out these decompositions, the research communities can rely on the services offered by numerous commercial or open source software packages.

Although commercial softwares are often of very high quality and high performance, they are by definition subject to licensing (for a fee)
and are therefore likely to limit their use within a team of researchers. 
In addition, the large number of functions often offered in these software can sometimes make them difficult to learn and use.
Finally, commercial softwares do not always make it easy to export the results of decompositions
in open formats (such as csv), or to record all the processing steps that led to such decompositions. 
These 2 last aspects, among others, severely limit the transmission of results and models within the same team and 
restrict the use and re-use of models to other series of analogeous spectra.

On the other hand, in the world of Open Source and in particular in the world of Python programming, 
libraries such as lmfit offer everything that is needed to carry out the decompositions expected in terms of spectral processing. 
However, their implementation requires knowledge in programming, which limits their use by the greatest number of people.

Fitspy was therefore created to address the various weaknesses/drawbacks of each of these 2 options 
by providing access to a spectral decomposition tool in open source with a GUI designed to be as simple as possible, 
both in terms of use and re-use thanks to fitspy model saving and reloading.

# Features

 Fitspy can process spectra in 2 types of input format: 
- a first format where each spectrum is entered individually in a .txt file. The input data file consists of a 2 columns base format where
  the first one is associated to physical support of the spectrum (typically wavelengths)
  and the seconde one to the corresponding spectrum  intensity.
- the second format is linked to the acquisition of spectra in the form of 2D maps.
  The related spectra are stored in a single file and each has an associated grid coordinate (X,Y).
  
Once loaded via a files selection widget, the spectra can then be processed individually (spectra related to selected ones in the widget) 
or as a whole (i.e. all the loaded spectra).

Firstly, users can choose to reduce the physical support to the range of interest for the next.
They can also activate the notion of attractors. These attractors correspond to local maxima, calculated using scipy. 
They can be used to define points of interest, which can be used to normalise spectra or to select points associated with
the baseline and peaks to be modelled (see below).

Once the range of interest and the (optional) spectra normlisation have been defined, the users may need to define a baseline in order to flat the spectra.
This baseline can be defined in automatic mode or by the users, who then position the characteristic points of the baseline on the figure using the mouse.
These points can be left at their initial position or attached to the spectrum profile ("Attached" mode). 
In the latter case, the points can be attached either according to the value at the same characteristic point abscissa of 1/ the raw spectrum or 2/
an averaged spectrum if the user wishes to attenuate the effects of noise. In this case, the spectrum is averaged usinga  Gaussian filtering with a standard sigma deviation.
The baseline is then approximated over the entire x-support using either piecewise linear interpolation or an nth-order polynomial approximation.

Once the baseline has been subtracted, the next step consists in defining the peaks of interest for the decomposition.
In the 'Auto' mode, an iterative process based on successive subtractions of the fit of the peak with the greatest intensity is implemented until
the residual reach 10%of the maximum intensity of the original signal.
Thanks to the functionalities offered by lmfit, a proper model can be associated with each peak; the models can be selected from a Gaussian model,
a Lorentzian model, their Assymetric variations or a Pseudovoigt model. 
Bounds (min, max values) can also be defined for each of the parameters during the fit, as well as constraints using mathematical expressions.
If required, these constrains can be used to link models parameters together, for example in the case where a physical ratio between 2 peaks are expected after fitting.

Finally, as part of the fit, the parameters can be free to evolve (within the bounds and according to the constraints defined above) or fixed at their initial values.

Several fit options are also proposed, such as :
- taking into account only the positive values of the spectra.
- a (limited) choice of minimisation algorithms
- the maximum number of fit iterations that allow to determine whether the fit process has converged or not)
- and the number of CPUs to be called upon during processing.

At the end of the fit, the fit parameters and statistics returned by lmfit are displayed in the related widgets and can be exported in a .csv and .txt files respectively.

All the processing steps leading from the spectra loading to the fit, via the the baseline removal, constitute a model in the sense of the fitspy application
that can be saved (in a .json) and replayed as is or applied to other series of spectra.

In term of visualization, the GUI allows to display all the spectra simultaneously ('show All' mode) or,
when a spectrum is selected, to display the fit and its residual. Figure title and axes names can be changed, peaks model can be labelized, etc...

All the actions described above can of course be performed in script lines without using the GUI.
On a practical point of view, for repetitive processing actions and for users with some knowledge of Python, it may be useful to use fitspy under the following conditions:
1/ creating a model using the GUI
2/ saving the model  
3/ apply the model to several sets of spectra using a script (just a few lines are needed). 
This is the approach recently taken by teams at CEA-Grenoble to process tens of thousands of Raman spectra acquired on microelectronics chips,
taking advantage of the parallelism capabilities offered by the tool.


# Acknowledgements
This work was made possible thanks to the support of CEA-Grenoble and the resources made available to the "numeric" team at the nanocaracterisation platform
to develop such a tool and make it available to the research community.

