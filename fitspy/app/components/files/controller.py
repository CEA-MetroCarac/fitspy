from PySide6.QtCore import QObject, Signal
from .model import Model

class FilesController(QObject):
    loadSpectrum = Signal(list)
    loadSpectraMap = Signal(str)
    delSpectrum = Signal(object, list)
    delSpectraMap = Signal(str)
    mapChanged = Signal(object)  # Can be a string or None
    spectraChanged = Signal(list)
    addMarker = Signal(str)

    def __init__(self, spectrum_list, maps_list):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list
        self.maps_list = maps_list

        self.setup_connections()

    def setup_connections(self):
        self.mapChanged.connect(self.model.set_current_map)

        self.model.loadSpectrum.connect(self.loadSpectrum)
        self.model.loadSpectraMap.connect(self.loadSpectraMap)
        self.model.delSpectrum.connect(self.delSpectrum)
        self.model.delSpectraMap.connect(self.delSpectraMap)
        self.model.spectrumListChanged.connect(self.update_spectrum_list)
        self.model.mapsListChanged.connect(lambda: self.update_list_widget(self.maps_list.list, self.model.spectramaps_fnames))

        self.spectrum_list.list.filesDropped.connect(self.model.load_files)
        self.spectrum_list.list.itemSelectionChanged.connect(lambda: self.update_selection(self.spectrum_list.list, self.spectrum_list.count_label))
        self.spectrum_list.sel_all.clicked.connect(self.spectrum_list.list.selectAll)
        self.spectrum_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.spectrum_list.list))

        self.maps_list.list.filesDropped.connect(self.model.load_files)
        self.maps_list.list.itemSelectionChanged.connect(lambda: self.update_map_selection(self.maps_list.list, self.spectrum_list.list))
        self.maps_list.deselect_btn.clicked.connect(lambda: self.maps_list.list.clearSelection())
        self.maps_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.maps_list.list))

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
            self.update_list_widget(self.spectrum_list.list, self.model.spectramaps_fnames[spectramap])
        else:
            self.maps_list.list.clearSelection()
            self.update_list_widget(self.spectrum_list.list, self.model.spectrum_fnames)

    def update_list_widget(self, list_widget, files):
        """Refresh the list widget with the files and update the label."""
        current_items = [list_widget.item(i).text() for i in range(list_widget.count())]
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

    def remove_selected_files(self, list_widget):
        """Remove the currently selected files from the model."""
        selected_items = [item.text() for item in list_widget.selectedItems()]
        self.model.remove_files(selected_items)

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
                self.update_selection(list_widget, self.spectrum_list.count_label, emit_marker=False)
                break

    def get_selected_fnames(self):
        return [item.text() for item in self.spectrum_list.list.selectedItems()]
    
    def clear(self):
        # Del Maps
        fnames = list(self.model.spectramaps_fnames.keys())
        self.del_map(fnames)

        # Del Independents Spectrum
        fnames = self.model.spectrum_fnames
        self.del_spectrum(fnames)