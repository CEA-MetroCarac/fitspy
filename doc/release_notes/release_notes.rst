Release Notes
=============

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
