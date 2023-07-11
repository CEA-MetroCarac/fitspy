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

**Fitspy** is a tool dedicated to **fit** **sp**ectra in **py**thon. <br>
Spectrum decomposition (also known as fitting) is based on peak models that can be in fitspy : `Gaussian`, `Lorientzan`, related `Asymetric` functions or `Pseudovoigt` ones.<br>
Spectrum decomposition corresponds to the resolution of a minimization problem, 
which can take into account bounds and constraints on model parameters. <br>
The fitspy's graphical user interface (**GUI**) \autoref{fig:GUI} is designed to be as simple and intuitive as possible.

![Fitpsy GUI illustration.\label{fig:GUI}](https://cea-metrocarac.github.io/fitspy/fitspy.png)

# Statement of need

The analysis of spectra in many areas of physics, from materials characterisation to astrophysics, often requires decompositions
into more or less complex models to account for the chemical elements.
To carry out these decompositions, the research communities can rely on the services offered by numerous commercial or open source software packages.

Although commercial softwares are often of very high quality and high performance, they are by definition subject to licensing (for a fee)
which is likely to limit their use within a team of researchers. 
In addition, the large number of functions often offered in these softwares can sometimes make them difficult to use.
Finally, commercial softwares do not always make it easy to export the results in a open format (like .csv), 
or to save all the processing steps that led to such decompositions to be replayed. 
These 2 last aspects, among others, severely limit the results and models exchanges within a team and 
 the use and re-use of models to analogeous set of spectra.

On the other hand, in the world of Open Source and in particular in the world of Python programming, 
libraries such as @lmfit offer everything that is needed to carry out spectra decompositions. 
However, their implementation requires knowledge in programming, which limits their use by the greatest number of people.

Fitspy was therefore created to address the various weaknesses/drawbacks of each of these 2 options 
by providing an access to a spectral decomposition tool in open source with a GUI designed to be as simple as possible.

# Features

 Fitspy adresses presently 2 types of input file data format: 
* a first format where each spectrum is stored individually in a .txt file. The input data file consists of a 2 columns base format where
  the first one is associated to the physical support of the spectrum (typically wavelengths)
  and the seconde one to the corresponding spectrum intensity.
* the second format is linked to the mode acquisition of spectra generating a 2D map.
  The related spectra are stored in a single file and each spectrum is identified thanks to its grid coordinate (X,Y).
  
Once loaded in the GUI via a files selection widget, the spectra can be processed one by one or by groups (depending on spectra selected by the cursor in the fiel selection widget) or as a whole if corresponding `Apply All` exists.

Firstly, the user can choose to reduce the physical support to a range of interest for the next.<br>
he can also activate the notion of attractors. These attractors correspond to local maxima, calculated using @scipy. 
They can be used to define points of interest, which can be used to normalise spectra or to select points associated with
the baseline and peaks to be modelled (see below).

Once the range of interest and the (optional) spectra normalisation have been set, the user may need to define a baseline in order to flat the spectra.
This baseline can be defined in an automatic way or by the user himself by positionning characteristic points on the figure with the mouse.
These points can be left at their initial position or attached to the spectrum profile ("Attached" mode). 
In the latter case, the points can be attached at the same characteristic point abscissa either to the value of the raw spectrum or to
an averaged spectrum if the user wishes to attenuate the effects of noise. In this case, the spectrum is averaged using a Gaussian filtering of $\sigma$-standard deviation.
The baseline is then approximated over the entire x-support using either piecewise linear interpolation or an *n*-order polynomial approximation.

Once the baseline has been subtracted, the next step consists in defining the peaks of interest for the decomposition.
This could be done either directly in the figure by clicking or thanks to an 'Auto' mode which consists in an iterative process to automatically determine the main peaks locations.<br>
Thanks to the functionalities offered by lmfit, a proper model can be associated to each peak; the model could be selected among a Gaussian model,
a Lorentzian model, their Assymetric variations or a Pseudovoigt model. These models relies basically on 3 main paremeters : a x position, an amplitude and a width (FWHM) that is differentiated (*left-right*) in the frame of assymetric variations.<br>
Bounds (min-max values) can also be defined for each of the parameters during the fit, as well as associated constraints.
If required, these constrains can be used to link models parameters together, for example in the case where a physical ratio between 2 peaks amplitudes are expected.

Finally, as part of the fit, the parameters can be free to evolve (within the bounds and according to the constraints defined above) or fixed at their initial values.

Several fit options are also proposed, such as :
* taking into account only the positive values of the spectra.
* a (limited) choice of minimisation algorithms
* the maximum number of fit iterations (used to determine whether the fit process has converged or not)
* and the number of CPUs to be used during the fit processing.

At the end of the fit, the fit parameters and the statistics returned by lmfit are displayed in related widgets and can be exported in .csv and .txt files respectively.<br><br>


All the processing steps previously described and leading from the spectra loading to the fit, via the the baseline removal, constitute a model in the sense of the fitspy application
that can be saved (in a .json) and replayed as is or applied to other series of spectra.

In term of visualization, the GUI allows to display all the spectra simultaneously ('show All' mode) or,
when a spectrum is selected, to display the fit decomposition and its residual. Figure title and axes names can be changed, peaks model can be labelized, etc...

All the actions described above can of course be performed in script lines without using the GUI.<br>
On a practical point of view, for repetitive processing actions and for users with some Python skillness, it may be useful to use fitspy under the following conditions:
<ol>
  <li>creating a model using the GUI,</li>
  <li>saving the model,</li>
  <li>apply the model to several sets of spectra using a script (just a few lines are needed).</li>
</ol>
This is the approach that has been recently followed by teams at CEA to process tens of thousands of Raman spectra acquired on microelectronics chips, taking advantage of the parallelism capabilities offered by fitpsy.


# Acknowledgements
This work was made possible thanks to the support of CEA and the resources made available to the "numeric" team at the nanocaracterisation platform
to develop such a tool and make it available to the research community.

