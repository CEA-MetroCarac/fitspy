Release Notes
=============

Version 2024.2 (January 29, 2024)
---------------------------------

New features:

- Add a progressbar in the terminal and in the GUI to follow the calculation progression during the fit processing
- Enable the loading of user-defined models through dedicated 'Load' buttons in the GUI.



Bug fixes/enhancements:

- Fixed bug when reloading 'old' model.json in which :code:`bkg_model` was absent
- Baseline format/use revisited to disable multiple baselines subtract capability (the 'baseline_history' spectrum attributes has been removed)
- Display the models parameters on the figure whatever the fit status
- Highlight/reduce the peak model curve linewidth according to the fit success status
- Reproduce the same view when reloading a model, considering the fit success status
- Fixed bug when using user-defined model in multithreading
- Take into account the 'fit_kws' through the 'kwargs' of Spectrum.fit() to be passed to the lmfit Model.fit()
- Fixed bug in bkg_model plotting
- Fixed bug in removing 'old' Spectra 2D-map when reloading a 'new' one


Version 2024.1 (January 16, 2024)
---------------------------------

New features:

- Add user-defined model capability from external files (in a '.txt' file located in :code:`%HOMEUSER%/Fitspy` for models creation from literal expressions or in a '.py' file from python scripting)
- Add Fitspy static HTML Sphinx documentation in `https://cea-metrocarac.github.io/fitspy/doc <https://cea-metrocarac.github.io/fitspy/doc/index.html>`_
- in 2D-map, in addition to intensity, the model parameters can now be displayed and the corresponding 2D field can be exported in a .csv file
- Spectra, Spectrum and SpectraMap class have now their own dedicated .py modules


Bug fixes/enhancements:

- Fixed bug for system identification that enables clipboard copy on Windows only
- Fixed bug on data paths in the examples
- Make the application exit correctly and add a widget to confirm it
- Fixed bug: make the fitting possible for a standalone background model
- Add background visualization and display the corresponding parameters in the tabview
- Fixed bug: enable the background models to be saved and reloaded
- Display only the used parameters models in the tabview
- Add xmin and xmax (optional) arguments to spectrum.load_profile() to ease the x-range setting when loading profiles by python scripts


Version 2023.x
--------------

First releases.
