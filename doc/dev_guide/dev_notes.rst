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
   - Run the following commands to install Dev environment dependencies::

     pip install -e .[dev]

Pull Requests
-------------

If you want to contribute to improve the Fitspy source code, you can send us a `pull request <https://github.com/CEA-MetroCarac/fitspy/pulls>`_ against the main branch. Small bug fixes and corrections to the user guide are typically a good starting point. But don’t hesitate also for significant code contributions, such as support for a new file format - if needed, we’ll help you to get the code ready to common standards.


TODO List
---------

TODO Base:
    - [ ] when changing a component of a fitted spectrum (peak, baseline, ...) 'reset' the spectrum color status
    - [ ] Revisit the slider to make it visible (particularly in the light mode)
    - [x] Add None in Baseline Options
    - [x] Write a submodule that provides all functions necessary to manipulate GUI via code only. + Rewrite examples to use this submodule
    - [/] Update documentation (partially done) - adapt the doc for Models and Main Figure in the GUI section
    - [x] Add a "Highlight spectra" click mode
    - [x] restore spectrum colorize_from_fit_status
    - [x] Implement peaks model + bkg model load button
    - [x] Implement back save_results
    - [x] Implement back model reloading
    Menubar:
      - [x] Implement CLEAR + SAVE GLOBAL STATE + OPEN GLOBAL STATE (drag n drop & open button should call same function)
      - [x] About + Manual + Doc (could redirect to sphinx doc)
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
    - [x] Results of previous calculations have to be preserved and displayed (colorize_from_status) when reloading a map
    - [ ] Investigate exit not exiting properly on some systems (could be due to Threads, use QThread instead ?) `ultralytics issue 1167 <https://github.com/ultralytics/ultralytics/issues/11679>`_
    - [ ] reinit in Spectrum() doesn't reinit fit_params
    - [ ] Expressions in saved models are "" instead of None
    - [ ] Manage callbacks when no files have been loaded (allow saving model, placing points, and baseline without loading spectra)
    - [ ] Baseline_points, empty Y if attached ?
    - [x] Peaks labels can sometimes overflow the plot
    - [x] Icons color dont follow theme
    - [x] Spectrum list is disordered compared to the map. When browsing through the spectra in the list, it should traverse the map from top to bottom and left to right.
    - [x] Port updates commit 6d303df (main)

TODO Opti:
    - [ ] Check (and avoid) multiple calls - code profiling
    - [ ] Refactor peaks_table.py + bkg_table.py by creating a new class
    - [ ] MULTIPROC BASELINE via apply_model ?
    - [ ] Optimize plotting (setxdata and setydata instead of replotting the whole figure ?)

TODO Others:
    - [x] restore & update examples/ + tests/
    - [ ] Defaults values for peaks (and maybe more) may be irrelevant depending on data's nature
    - [ ] Inconsistencies in args names fnames vs files
    - [ ] Explicit types in functions might be useful for maintainers(e.g. `def func(arg: type) -> type: <https://github.com/CEA-MetroCarac/fitspy/blob/cfee0e6c881045447feed2105ec79c208b8d6a5a/fitspy/app/components/settings/controller.py#L183C9-L183C20>`_)
    - [x] Change peak table colum _vary to _fixed
    - [ ] Why using np.float64 for baseline points ??
    - [ ] update README.md
    - [ ] update CITATION.cff
    - [x] add github workflows back
    - [x] update paper/

TODO Nice to Have:
    - [ ] Fitspy Icon for taskbar
    - [ ] Multirow-edit for peaks settings (see https://stackoverflow.com/questions/14586715/how-can-i-achieve-to-update-multiple-rows-in-a-qtableview)
    - [ ] Update save/load mechanisms to include data or not based on 'save spectrum file path only' checkbox state
    - [ ] update dynamically the 2D map figure during fitting
    - [ ] Plot Dark/Light `dynamic theme change <https://stackoverflow.com/questions/77748488/how-to-dynamically-change-the-sheet-type-theme-during-runtime>`_
    - [ ] Idea : scroll on plot to edit nearest peak bounds
    - [ ] Add a button to copy 2D Map in clipboard ? (add mpl toolbar ?)
    - [x] See multiple spectrum with their baseline subtracted or not (need to redefine what to plot for secondary spectrum instead of just x0+y0)   
    - [x] add a confirmation prompt before load_state to avoid erasing current work
    - [x] New View option 'subtract bkg' (see existing 'subtract baseline')
    - [x] Colormap settings
    - [x] Add shortcuts for menu actions
    - [x] Warn user to disable pan/zoom if 3 clicks are detected in a short time (indicating user might want to place a peak/baseline point)

TODO Production:
    - [ ] Update Github Actions tests + Auto Pypi Pre-release/Pre-release, see `pyvsnr workflows <https://github.com/CEA-MetroCarac/pyvsnr/tree/main/.github/workflows>`_
    - [ ] Update Zenodo