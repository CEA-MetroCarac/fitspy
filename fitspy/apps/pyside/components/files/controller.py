import os
from PySide6.QtCore import QObject, Signal

from fitspy.apps.pyside.components.files.model import Model


class FilesController(QObject):
    showToast = Signal(str, str, str)
    askConfirmation = Signal(str, object, tuple, dict)
    loadSpectra = Signal(object)
    loadSpectrum = Signal(list)
    loadSpectraMap = Signal(str)
    delSpectrum = Signal(dict)
    delSpectraMap = Signal(str)
    reinitSpectra = Signal(list)
    mapChanged = Signal(object)  # Can be a string or None
    mapChanged2 = Signal()
    spectraChanged = Signal(list)
    saveResults = Signal(list)
    addMarker = Signal(str)
    loadState = Signal(object)

    def __init__(self, spectrum_list, maps_list):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list
        self.maps_list = maps_list

        self.setup_connections()

    def setup_connections(self):
        self.mapChanged.connect(self.model.set_current_map)

        self.model.showToast.connect(self.showToast)
        self.model.askConfirmation.connect(self.askConfirmation)
        self.model.loadSpectra.connect(self.loadSpectra)
        self.model.loadSpectrum.connect(self.loadSpectrum)
        self.model.loadSpectraMap.connect(self.loadSpectraMap)
        self.model.delSpectrum.connect(self.delSpectrum)
        self.model.delSpectraMap.connect(self.delSpectraMap)
        self.model.spectrumListChanged.connect(self.update_spectrum_list)
        self.model.mapsListChanged.connect(
            lambda: self.update_list_widget(self.maps_list.list, self.model.spectramaps_fnames))
        self.model.loadState.connect(self.loadState)
        self.model.clear.connect(self.clear)

        self.spectrum_list.list.filesDropped.connect(self.load_files)
        self.spectrum_list.list.itemSelectionChanged.connect(
            lambda: self.update_selection(self.spectrum_list.list, self.spectrum_list.count_label))
        self.spectrum_list.sel_all.clicked.connect(self.spectrum_list.list.selectAll)
        self.spectrum_list.reinit.clicked.connect(
            lambda: self.reinitSpectra.emit(self.get_selected_fnames()))
        self.spectrum_list.rm_btn.clicked.connect(
            lambda: self.remove_selected_files(self.spectrum_list.list))
        self.spectrum_list.list.remove_selected_files = self.remove_selected_files
        self.spectrum_list.save_btn.clicked.connect(
            lambda: self.saveResults.emit(self.get_selected_fnames()))

        self.maps_list.list.filesDropped.connect(self.load_files)
        self.maps_list.list.itemSelectionChanged.connect(
            lambda: self.update_map_selection(self.maps_list.list, self.spectrum_list.list))
        self.maps_list.deselect_btn.clicked.connect(self.maps_list.clearSelection)
        self.maps_list.rm_btn.clicked.connect(
            lambda: self.remove_selected_files(self.maps_list.list))
        self.maps_list.list.remove_selected_files = self.remove_selected_files

    def load_files(self, files):
        self.model.load_files(files)

    def add_spectrum(self, fname):
        self.model.add_spectrum(fname)

    def del_spectrum(self, items):
        self.model.del_spectrum(items)

    def del_map(self, fname):
        if isinstance(fname, list):
            for item in fname:
                self.model.del_map(item)
        else:
            self.model.del_map(fname)

    def update_spectrum_list(self, spectramap):
        if spectramap is not None:
            self.update_list_widget(self.spectrum_list.list,
                                    self.model.spectramaps_fnames[spectramap])
        else:
            self.maps_list.clearSelection()
            self.update_list_widget(self.spectrum_list.list,
                                    self.model.spectrum_fnames)

    def update_list_widget(self, list_widget, files):
        """Refresh the list widget with the files and update the label."""
        # Save current selection texts
        old_selection = set(list_widget.get_selected_fnames())
        
        current_items = list_widget.get_all_fnames()
        new_items = files  # New items list, order preserved
        
        # Determine items to add and remove using set operations
        current_items_set = set(current_items)
        new_items_set = set(new_items)
        items_to_add = list(new_items_set - current_items_set)
        items_to_remove = list(current_items_set - new_items_set)

        # Block signals to prevent multiple onSelectionUpdate calls
        list_widget.blockSignals(True)

        # Remove items
        for i in range(list_widget.count() - 1, -1, -1):
            item = list_widget.item(i)
            if item.text() in items_to_remove:
                list_widget.takeItem(i)

        # Add new items
        for file_path in new_items:
            if file_path in items_to_add:
                list_widget.addItem(file_path)

        # Unblock signals after updating
        list_widget.blockSignals(False)

        # Auto select the first item if none are selected
        if not list_widget.get_selected_fnames() and list_widget.count():
            list_widget.setCurrentRow(0)
        
        # Compare new selection against the old selection and emit signal only if changed
        new_selection = set(item for item in list_widget.get_selected_fnames())
        if old_selection != new_selection:
            list_widget.itemSelectionChanged.emit()

    def update_map_selection(self, maps_list, spectrum_list):
        selected_fnames = maps_list.get_selected_fnames()
        if selected_fnames:
            selected_map = selected_fnames[0]
            selected_files = self.model.spectramaps_fnames[selected_map]
        else:
            selected_map = None
            selected_files = self.model.spectrum_fnames

        self.mapChanged.emit(selected_map)
        self.update_list_widget(spectrum_list, selected_files)
        # FIXME: not so good but mapChanged and update_list_widget cannot be reversed in state :(
        self.mapChanged2.emit()
        spectrum_list.itemSelectionChanged.emit()

    def update_count(self, list_widget, label_widget):
        """Update the count label based on the current selection."""
        total_count = list_widget.count()
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"{selected_count}/{total_count}")

    def update_selection(self, list_widget, label_widget, emit_marker=True):
        """Update Plot and count label when the selection changes."""
        fnames = list_widget.get_selected_fnames()
        self.update_count(list_widget, label_widget)
        self.spectraChanged.emit(fnames)

        if emit_marker and fnames and self.model.current_map:
            self.addMarker.emit(fnames[0])

    def remove_files(self, fnames):
        self.model.remove_files(fnames)

    def remove_selected_files(self, list_widget):
        """Remove the currently selected files from the model."""
        selected_items = list_widget.get_selected_fnames()
        # if user is about to delete all files and a map is selected
        # just delete the map instead of deleting all files
        if len(selected_items) == list_widget.count() and list_widget == self.spectrum_list.list:
            selected_map = self.maps_list.selectedItems()
            if selected_map:
                self.del_map(selected_map[0].text())
                return

        self.remove_files(selected_items)

    def update_spectramap(self, map_fname, fnames):
        """Update the lists widgets with the spectra related to the 2D-map."""
        self.model.update_spectramap(map_fname, fnames)

    def highlight_spectrum(self, fnames, plot_highlighted):
        """Select the given spectrum(s) in the list widget."""
        list_widget = self.spectrum_list.list

        if isinstance(fnames, str):
            fnames = [fnames]
        list_widget.blockSignals(True)
        list_widget.clearSelection()
        first_selected_item = None
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() in fnames:
                item.setSelected(True)
                if first_selected_item is None:
                    first_selected_item = item
        list_widget.blockSignals(False)

        if plot_highlighted:
            self.update_selection(list_widget, self.spectrum_list.count_label, emit_marker=False)
        else:
            self.update_count(list_widget, self.spectrum_list.count_label)
            if fnames and self.model.current_map:
                self.addMarker.emit(fnames[0])

        self.spectrum_list.list.setFocus()
        if first_selected_item:
            list_widget.scrollToItem(first_selected_item)

    def get_selected_fnames(self):
        """Return the selected filenames in the spectrum list."""
        return self.spectrum_list.list.get_selected_fnames()

    def get_selected_map_fname(self):
        """Return the selected map filename."""
        return self.model.current_map

    def get_full_selection(self):
        """Return the selected map filename and the selected spectrum filenames."""
        return self.get_selected_map_fname(), self.get_selected_fnames()

    def get_spectra_fnames(self, map_fname=None):
        """Return the list of spectrum filenames for the given map filename."""
        if map_fname:
            return self.model.spectramaps_fnames[map_fname]
        return self.model.spectrum_fnames

    def get_map_fnames(self):
        """Return the list of map filenames."""
        return list(self.model.spectramaps_fnames.keys())

    def colorize_from_fit_status(self, fit_status: dict):
        """
        Colorize the items in the spectrum list based on the fit status.

        Parameters
        ----------
        fit_status: dict
            A dictionary where keys are filenames (str) and values are either booleans (bool) or
            objects with a 'success' attribute indicating the fit status (like
            lmfit.model.ModelResult).
        """
        if not fit_status:
            # Colorize all items with transparent bkg if fit_status is empty
            self.spectrum_list.list.colorize_items()
            return

        for fname, result_fit in fit_status.items():
            if isinstance(result_fit, bool):
                color = 'Lime' if result_fit else 'Orange'
            elif hasattr(result_fit, 'success'):
                color = 'Lime' if result_fit.success else 'Orange'
            else:
                color = None
            self.spectrum_list.list.colorize_items([os.path.normpath(fname)], color)

    def set_selection(self, list_widget, selection_list, emit_signal=True):
        if not isinstance(selection_list, list):
            selection_list = [selection_list]

        list_widget.blockSignals(True)
        list_widget.clearSelection()

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() in selection_list:
                item.setSelected(True)
        list_widget.blockSignals(False)

        if emit_signal:
            list_widget.itemSelectionChanged.emit()

    def clear(self):
        fnames_map = list(self.model.spectramaps_fnames.keys())  # Maps
        fnames = self.model.spectrum_fnames  # Independents Spectrum

        # Using remove_files acts as if the user would manually delete everything
        # thus, the signals to delete the spectrum objects associated to files are emitted
        for fname_map in fnames_map:
            self.remove_files([fname_map])
        if fnames:
            self.remove_files(fnames)
