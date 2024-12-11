import os
from PySide6.QtCore import QObject, Signal
from .model import Model


class FilesController(QObject):
    showToast = Signal(str, str, str)
    askConfirmation = Signal(str, object, tuple, dict)
    loadSpectrum = Signal(list)
    loadSpectraMap = Signal(str)
    delSpectrum = Signal(dict)
    delSpectraMap = Signal(str)
    mapChanged = Signal(object)  # Can be a string or None
    spectraChanged = Signal(list)
    saveResults = Signal(object)
    addMarker = Signal(str)
    loadState = Signal(dict, dict)

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
        self.model.loadSpectrum.connect(self.loadSpectrum)
        self.model.loadSpectraMap.connect(self.loadSpectraMap)
        self.model.delSpectrum.connect(self.delSpectrum)
        self.model.delSpectraMap.connect(self.delSpectraMap)
        self.model.spectrumListChanged.connect(self.update_spectrum_list)
        self.model.mapsListChanged.connect(
            lambda: self.update_list_widget(
                self.maps_list.list, self.model.spectramaps_fnames
            )
        )
        self.model.loadState.connect(self.loadState)
        self.model.clear.connect(self.clear)

        self.spectrum_list.list.filesDropped.connect(self.load_files)
        self.spectrum_list.list.itemSelectionChanged.connect(
            lambda: self.update_selection(
                self.spectrum_list.list, self.spectrum_list.count_label
            )
        )
        self.spectrum_list.sel_all.clicked.connect(
            self.spectrum_list.list.selectAll
        )
        self.spectrum_list.rm_btn.clicked.connect(
            lambda: self.remove_selected_files(self.spectrum_list.list)
        )
        self.spectrum_list.save_btn.clicked.connect(
            lambda: self.saveResults.emit(self.spectrum_list.list)
        )

        self.maps_list.list.filesDropped.connect(self.load_files)
        self.maps_list.list.itemSelectionChanged.connect(
            lambda: self.update_map_selection(
                self.maps_list.list, self.spectrum_list.list
            )
        )
        self.maps_list.deselect_btn.clicked.connect(
            lambda: self.maps_list.list.clearSelection()
        )
        self.maps_list.rm_btn.clicked.connect(
            lambda: self.remove_selected_files(self.maps_list.list)
        )

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
            self.update_list_widget(
                self.spectrum_list.list,
                self.model.spectramaps_fnames[spectramap],
            )
        else:
            self.maps_list.list.clearSelection()
            self.update_list_widget(
                self.spectrum_list.list, self.model.spectrum_fnames
            )

    def update_list_widget(self, list_widget, files):
        """Refresh the list widget with the files and update the label."""
        current_items = [
            list_widget.item(i).text() for i in range(list_widget.count())
        ]
        new_items = files  # Keep new_items as a list to preserve order

        # Convert lists to sets for set operations
        current_items_set = set(current_items)
        new_items_set = set(new_items)

        # Determine items to add and remove using set operations
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
        if not list_widget.selectedItems() and list_widget.count():
            list_widget.setCurrentRow(0)
        elif list_widget.count() == 0:
            list_widget.itemSelectionChanged.emit()

    def update_map_selection(self, maps_list, spectrum_list):
        selected_items = maps_list.selectedItems()
        if selected_items:
            selected_map = selected_items[0].text()
            selected_files = self.model.spectramaps_fnames[selected_map]
        else:
            selected_map = None
            selected_files = self.model.spectrum_fnames

        self.mapChanged.emit(selected_map)
        self.update_list_widget(spectrum_list, selected_files)
        spectrum_list.itemSelectionChanged.emit()

    def update_selection(self, list_widget, label_widget, emit_marker=True):
        """Update Plot and count label when the selection changes."""
        fnames = [item.text() for item in list_widget.selectedItems()]
        total_count = list_widget.count()
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"{selected_count}/{total_count}")
        self.spectraChanged.emit(fnames)

        if emit_marker and fnames and self.model.current_map:
            self.addMarker.emit(fnames[0])

    def remove_files(self, fnames):
        self.model.remove_files(fnames)

    def remove_selected_files(self, list_widget):
        """Remove the currently selected files from the model."""
        selected_items = [item.text() for item in list_widget.selectedItems()]
        self.remove_files(selected_items)

    def update_spectramap(self, map_fname, fnames):
        """Update the lists widgets with the spectra related to the 2D-map."""
        self.model.update_spectramap(map_fname, fnames)

    def highlight_spectrum(self, fname):
        """Select the given spectrum in the list widget."""
        list_widget = self.spectrum_list.list

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() == fname:
                list_widget.blockSignals(True)
                # list_widget.clearSelection()
                list_widget.setCurrentItem(item)
                list_widget.blockSignals(False)
                self.update_selection(
                    list_widget,
                    self.spectrum_list.count_label,
                    emit_marker=False,
                )
                break

    def get_selected_fnames(self):
        """Return the selected filenames in the spectrum list."""
        return [item.text() for item in self.spectrum_list.list.selectedItems()]

    def get_selected_map_fname(self):
        """Return the selected map filename."""
        return self.model.current_map

    def get_full_selection(self):
        """Return the selected map filename and the selected spectrum filenames."""
        return self.get_selected_map_fname(), self.get_selected_fnames()

    def get_spectrum_fnames(self, map_fname=None):
        """Return the list of spectrum filenames for the given map filename."""
        if map_fname:
            return self.model.spectramaps_fnames[map_fname]
        return self.model.spectrum_fnames

    def get_map_fnames(self):
        """Return the list of map filenames."""
        return list(self.model.spectramaps_fnames.keys())

    def get_all_spectrum_ids(self, delimiter):
        """Return the list of all spectrum IDs across all maps.

        The format is: map_fname + delimiter + spectrum_fname.
        """
        all_spectrum_ids = []
        map_fnames = self.get_map_fnames() + [
            None
        ]  # Include None for spectrum without map
        for map_fname in map_fnames:
            spectrum_fnames = self.get_spectrum_fnames(map_fname)
            for spectrum_fname in spectrum_fnames:
                normalized_map_fname = (
                    os.path.normpath(map_fname) if map_fname else "None"
                )
                normalized_spectrum_fname = os.path.normpath(spectrum_fname)
                all_spectrum_ids.append(
                    f"{normalized_map_fname}{delimiter}{normalized_spectrum_fname}"
                )
        return all_spectrum_ids

    def convert_spectrum_ids_to_dict(self, spectrum_ids, delimiter):
        """Convert a list of spectrum IDs into a dictionary.

        The dictionary format is: {map_fname: [spectrum_fname, ...], ...}
        """
        spectrum_dict = {}
        for spectrum_id in spectrum_ids:
            map_fname, spectrum_fname = spectrum_id.split(delimiter)

            if map_fname == "None":
                map_fname = "None"

            if map_fname not in spectrum_dict:
                spectrum_dict[map_fname] = []
            spectrum_dict[map_fname].append(spectrum_fname)
        return spectrum_dict

    def colorize_from_fit_status(self, fit_status: dict):
        """
        Colorize the items in the spectrum list based on the fit status.

        Parameters:
        fit_status (dict): A dictionary where keys are filenames (str) and values are lmfit.model.ModelResult objects.
                        The ModelResult objects should have a 'success' attribute indicating the fit status.
        """
        if not fit_status:
            # Colorize all items in white if fit_status is empty
            self.spectrum_list.list.colorize_items()
            return
        # OTHER IDEA of implementation that works:
        # for fname, result_fit in fit_status.items():
        #     if hasattr(result_fit, 'success'):
        #         color = 'green' if result_fit.success else 'orange'
        #     else:
        #         color = 'white'

        #     self.spectrum_list.list.colorize_items([fname], color)
        color_groups = {
            "green": [],
            "orange": [],
            None: [],  # default bkg color
        }

        for fname, result_fit in fit_status.items():
            if hasattr(result_fit, "success"):
                if result_fit.success:
                    color_groups["green"].append(fname)
                else:
                    color_groups["orange"].append(fname)
            else:
                color_groups[None].append(fname)

        for color, fnames in color_groups.items():
            if fnames:
                self.spectrum_list.list.colorize_items(fnames, color)

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
        map_fnames = list(self.model.spectramaps_fnames.keys())  # Maps
        fnames = self.model.spectrum_fnames  # Independents Spectrum

        # Using remove_files acts as if the user would manually delete everything
        # thus, the signals to delete the spectrum objects associated to files are emitted
        for map in map_fnames:
            self.remove_files([map])
        if fnames:
            self.remove_files(fnames)
