Developers Notes
================

Fitspy is a new project (started in 2023).

Developers are warmly encouraged to collaborate and contribute to the ongoing improvement of Fitspy. Contributions are welcome in the form of bug reports, documentation, code , feature requests, and more...

... keeping in mind that Fitspy must maintain its primary goal: to remain as simple, generic and user-friendly as possible :)


Issues
------

The `issue tracker <https://github.com/CEA-MetroCarac/fitspy/issues>`_ can be used to report bugs or propose new features. When reporting a bug, the following is useful:

* give a minimal example demonstrating the bug,

* copy and paste the error traceback.


Visual Studio Code Setup to Preview .rst Files
----------------------------------------------------------

1. **Install the RestructuredText Extension**:
   - Open Visual Studio Code.
   - Go to the Extensions view (`Ctrl+Shift+X`).
   - Search for "reStructuredText" and install the extension by LeXtudio.

2. **Install Dependencies**:
   - Open the terminal in Visual Studio Code (`Ctrl+` ` `).
   - Run the following commands to install Sphinx and other useful tools::

     pip install sphinx doc8 rstcheck sphinx-rtd-theme sphinx-copybutton

Pull Requests
-------------

If you want to contribute to improve the Fitspy source code, you can send us a `pull request <https://github.com/CEA-MetroCarac/fitspy/pulls>`_ against the main branch. Small bug fixes and corrections to the user guide are typically a good starting point. But don’t hesitate also for significant code contributions, such as support for a new file format - if needed, we’ll help you to get the code ready to common standards.


TODO List
---------

TODO Base:
    - [x] restore spectrum colorize_from_fit_status
    - [ ] Implement peaks model + bkg model load button
    Menubar:
      - [x] Implement CLEAR + SAVE GLOBAL STATE + OPEN GLOBAL STATE (drag n drop & open button should call same function)
      - [ ] About + Manual (could redirect to sphinx doc)
    Peaks Table:
      - [x] Add background parameters (in table or elsewhere in GUI)
      - [x] Add missing columns for some Peak Models
      - [x] Implement expressions
      - [x] User Warning for incorrect bounds
    Toolbar:
      - [x] Add checkbox “preserve axis” (= preserve zoom)
    2DMap:
      - [x] Implement back export .csv
      - [x] Implement Min/Max (replace with a DoubleRangedSlider ?)
      - [x] Add Label choice and plot update

TODO Fixes:
    - [ ] Peaks labels can sometimes overflow the plot
    - [ ] Manage callbacks when no files have been loaded (allow saving model, placing points, and baseline without loading spectra)
    - [ ] Normalization is messing with baseline/peaks_points and maybe more (for e.g. when applying normalization to a spectrum with a baseline, the baseline points are not normalized)
    - [ ] Baseline_points, empty Y if attached ?
    - [x] Icons color dont follow theme
    - [x] Spectrum list is disordered compared to the map. When browsing through the spectra in the list, it should traverse the map from top to bottom and left to right.
    - [x] Port updates commit 6d303df (main)

TODO Opti:
    - [ ] Refactor peaks_table.py + bkg_table.py by creating a new class
    - [ ] MULTIPROC BASELINE via apply_model ?
    - [ ] Useless calls to apply_model at start ? `settings_controller.py > apply_model(self, fit_model)`_
    - [ ] Optimize plotting (setxdata and setydata instead of replotting the whole figure ?)

TODO Others:
    - [ ] Defaults values for peaks (and maybe more) may be irrelevant depending on data's nature
    - [ ] Inconsitencies in args names fnames vs files
    - [ ] Explicit types in functions might be useful for maintainers(e.g. `def func(arg: type) -> type:`)
    - [ ] Change peak table colum _vary to _fixed
    - [ ] Save selected spectrum per spectramap to reselect it after spectramap change ?
    - [ ] Store model folder for next sessions in QSettings ?
    - [ ] Why using np.float64 for baseline points ??
    - [ ] Make sure every ERROR/WARNING/INFO/SUCCESS is handled with showToast
    - [ ] restore & update examples/
    - [ ] update README.md
    - [ ] update CITATION.cff
    - [ ] update doc/
    - [ ] add tests/ back
    - [ ] add github workflows back
    - [ ] update paper/
    - [ ] Is commented code better ? (in files controller > colorize_from_fit_status)

TODO Nice to Have:
    - [ ] Multirow-edit for peaks settings (see https://stackoverflow.com/questions/14586715/how-can-i-achieve-to-update-multiple-rows-in-a-qtableview)
    - [ ] See multiple spectrum with their baseline subtracted or not (need to redefine what to plot for secondary spectrum instead of just x0+y0)
    - [ ] New View option 'subtract bkg' (see existing 'subtract baseline')
    - [ ] Update save/load mechanisms to include data or not based on 'save spectrum file path only' checkbox state
    - [ ] add a confirmation prompt before load_state to avoid erasing current work
    - [ ] update dynamically the 2D map figure during fitting
    - [ ] Fitspy Icon for taskbar
    - [ ] Plot Dark/Light theme `https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime`_
    - [ ] Idea : scroll on plot to edit nearest peak bounds
    - [ ] Add a button to copy 2D Map in clipboard ? (add mpl toolbar ?)
    - [x] Add shortcuts for menu actions
    - [x] Warn user to disable pan/zoom if 3 clicks are detected in a short time (indicating user might want to place a peak/baseline point)

TODO Production:
    - [ ] Get rid of MANIFEST.in, use pyproject.toml instead
    - [ ] Update documentation
    - [ ] Update Github Actions tests + Auto Pypi Pre-release/Pre-release, see `https://github.com/CEA-MetroCarac/pyvsnr/tree/main/.github/workflows`_
    - [ ] Update Zenodo

.. _settings_controller.py > apply_model(self, fit_model): https://github.com/CEA-MetroCarac/fitspy/blob/cfee0e6c881045447feed2105ec79c208b8d6a5a/fitspy/app/components/settings/controller.py#L183C9-L183C20
.. _https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime: https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime
.. _https://github.com/CEA-MetroCarac/pyvsnr/tree/main/.github/workflows: https://github.com/CEA-MetroCarac/pyvsnr/tree/main/.github/workflows 