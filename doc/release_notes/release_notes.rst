Release Notes
=============


Version 2025.2 (February 24, 2025)
----------------------------------

**Enhancements:**

- Added python version in About window (PySide).
- Added reinit_spectra method to Appli class for spectra reinitialization (PySide).


**Bug fixes:**

- Fixed #42: Do not reinitialize params when 'vary' is False
- Fixed #43: Fit fails when Xmin/Xmax contains "inf" or "NaN"
- Fixed #44: Peak Table values not in the correct columns


Version 2025.1 (February 17, 2025)
----------------------------------

**New features:**

- A PySide application has been added (MAJOR CHANGE), aiming to be more flexible, easier to maintain (using the MVC approach), and more user-friendly (featuring Drag-and-Drop functionality, etc...).
- Consequently, the project structure has been significantly reorganized: ``Spectrum``, ``Spectra``, and related modules have been moved into the ``fitspy.core`` directory, and ``fitspy.app`` has been renamed to ``fitspy.apps`` (with separate subdirectories for ``tkinter`` and ``pyside``).
- Input data can now be saved directly in the model (as a .json file), allowing it to be replayed as-is, without relying on file path dependencies.


**Enhancements:**

- Spectrum objects can be created directly by passing 'fnames' to Spectra(fnames=fnames)
- a 'model.json' fname can be passed directly as 'model' to apply_model(model=model.json)
- Peak label visibility has been improved (PySide).
- Colormap settings have been added for peaks and 2D maps (PySide).
- User warnings have been introduced for incorrect bounds in model parameters (PySide).
- The 'baseline' subtraction feature has been extended to include the 'background'.
- Spectra subsampling has been introduced in the semi-automatic baseline approach to reduce calculation time when applied to very large spectra.


**Bug fixes:**

- create the related ``dirname_fig`` in ``save_figures()`` if the directory does not exist


Version 2024.5 (September 4, 2024)
----------------------------------

**New features:**

- A semi-automatic approach for the baseline determination has been added
- The spectra can now be displayed before and after the baseline subtraction


**Enhancements:**

- The progressbar (with the number of CPUS used during the calculations) has been integrated in the processing windows.
- The spectra input data formats have been extended to .dm3, .dm4, .emd, .hspy, .nxs files and many other formats thanks to the rosettasciio readers integration


**Bug fixes:**

- Allow fit processing without any peak or background model (just for baselines visualization for instance)


Version 2024.4 (February 27, 2024)
----------------------------------

**New features:**

- noise is now estimated and a noise level criteria enables to automatically deactivate peak models in noisy regions.
- optional outlier detection has been added, enabling the disregarding of outliers during baseline calculation and fitting processes.
- 'xtol' fitting parameter has been added (associated with 'leastsq' and 'least_square' fitting methods).
- all fitted parameters from all loaded spectra can now be saved in a single file named 'results.csv'.


**Enhancements:**

- multi-threaded calculations return now the complete fit report.
- a new boolean argument, 'reinit_guess', has been added in Spectrum.fit(), enabling the adjustment of initial values for 'ampli' and 'fwhm' to the current spectrum. This helps circumvent "ill-conditioned" peak models (with fwhm~0) resulting from previous 'Fitspy' model calculations.
- lists are now written to .json files on a single line.
- parameters and statistics displaying have been separated.


**Bug fixes:**

- the index count used to label the models was not reset to 1 when reloading a model
- 2d-maps with a single X or Y coordinate were not supported
- the Lorentzian model could previously return Nan values when dealing with fwhm=0
- the threads execution used by apply_model() to display the different progress bars did not quit correctly in some cases


Version 2024.2 (January 29, 2024)
---------------------------------

**New features:**

- Add a progressbar in the terminal and in the GUI to follow the calculation progression during the fit processing
- Enable the loading of user-defined models through dedicated 'Load' buttons in the GUI.


**Enhancements:**

- Display the models parameters on the figure whatever the fit status
- Highlight/reduce the peak model curve linewidth according to the fit success status
- Reproduce the same view when reloading a model, considering the fit success status
- Take into account the 'fit_kws' through the 'kwargs' of Spectrum.fit() to be passed to the lmfit Model.fit()


**Code changes:**

- Baseline format/use revisited to disable multiple baselines subtract capability (the 'baseline_history' spectrum attributes has been removed)
- Spectrum attributes has benn changed from:
    * 'peaks' to 'attractors'
    * 'peaks_params' to 'attractors_params'
    * 'models' to 'peak_models'
    * 'models_labels' to 'peak_labels'
    * 'models_index' to 'peak_index'


**Bug fixes:**

- Fixed bug when reloading 'old' model.json in which :code:`bkg_model` was absent
- Fixed bug when using user-defined model in multithreading
- Fixed bug in bkg_model plotting
- Fixed bug in removing 'old' Spectra 2D-map when reloading a 'new' one (the 'old' Spectra 2D-map figures are now closed)


Version 2024.1 (January 16, 2024)
---------------------------------

**New features:**

- Add user-defined model capability from external files (in a '.txt' file located in :code:`%HOMEUSER%/Fitspy` for models creation from literal expressions or in a '.py' file from python scripting)
- Add Fitspy static HTML Sphinx documentation in `https://cea-metrocarac.github.io/fitspy/doc <https://cea-metrocarac.github.io/fitspy/doc/index.html>`_
- in 2D-map, in addition to intensity, the model parameters can now be displayed and the corresponding 2D field can be exported in a .csv file
- Spectra, Spectrum and SpectraMap class have now their own dedicated .py modules


**Enhancements:**

- Add background visualization and display the corresponding parameters in the tabview
- Display only the used parameters models in the tabview
- Add xmin and xmax (optional) arguments to spectrum.load_profile() to ease the x-range setting when loading profiles by python scripts


**Bug fixes:**

- Fixed bug for system identification that enables clipboard copy on Windows only
- Fixed bug on data paths in the examples
- Make the application exit correctly and add a widget to confirm it
- Fixed bug: make the fitting possible for a standalone background model
- Fixed bug: enable the background models to be saved and reloaded



Version 2023.x
--------------

First releases.
