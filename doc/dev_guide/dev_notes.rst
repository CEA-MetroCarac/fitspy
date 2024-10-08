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
   - Run the following commands to install Sphinx and other useful tools:
     ```sh
     pip install sphinx doc8 rstcheck sphinx-rtd-theme
     ```

Pull Requests
-------------

If you want to contribute to improve the Fitspy source code, you can send us a `pull request <https://github.com/CEA-MetroCarac/fitspy/pulls>`_ against the main branch. Small bug fixes and corrections to the user guide are typically a good starting point. But don’t hesitate also for significant code contributions, such as support for a new file format - if needed, we’ll help you to get the code ready to common standards.


TODO List
---------

TODO Base:
    Menubar:
      - [ ] Implement CLEAR + SAVE GLOBAL STATE+ OPEN GLOBAL STATE (drag n drop & open button should call same function)
      - [ ] About + Manual

    Toolbar:
      - [ ] Add checkbox “preserve axis” (= preserve zoom)

    Peaks Table:
      - [ ] Add missing columns for some Peak Models
      - [ ] Add background parameters (in table or elsewhere in GUI)
      - [ ] Add expressions
      - [ ] Connect min + max to setLimits/setRange + showToast alert

TODO Fixes:
    - [ ] Manage callbacks when no files have been loaded (allow saving model, placing points, and baseline without loading spectra)
    - [ ] Spectrum list is disordered compared to the map. When browsing through the spectra in the list, it should traverse the map from top to bottom and left to right.
    - [ ] Normalization is messing with baseline/peaks_points and maybe more (for e.g. when applying normalization to a spectrum with a baseline, the baseline points are not normalized)
    - [ ] Baseline_points, empty Y if attached ?
    - [ ] Icons color dont follow theme

TODO Opti:
    - [ ] MULTIPROC BASELINE via apply_model ?
    - [ ] Useless calls to apply_model at start ? `settings_controller.py > apply_model(self, fit_model)`_
.. _settings_controller.py > apply_model(self, fit_model): https://github.com/CEA-MetroCarac/fitspy/blob/cfee0e6c881045447feed2105ec79c208b8d6a5a/fitspy/app/components/settings/controller.py#L183C9-L183C20
    - [ ] Optimize plotting by using setxdata and setydata instead of replotting the whole figure

TODO Others:
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

TODO Nice to Have:
    - [ ] update dynamically the 2D map figure during fitting
    - [ ] Fitspy Icon for taskbar
    - [ ] Plot Dark/Light theme `https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime`_
.. _https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime: https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime
    - [ ] Idea : scroll on plot to edit nearest peak bounds (VOIR STASH)
    - [ ] Automatically re-open last saved .fitspy workspace