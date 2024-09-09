from PySide6.QtCore import QObject, Signal
from .model import Model

class FilesController(QObject):
    loadSpectrum = Signal(list)
    loadSpectraMap = Signal(str)
    delSpectrum = Signal(str)
    delSpectraMap = Signal(str)
    mapChanged = Signal(object)  # Can be a string or None
    spectraPlotChanged = Signal(list)

    def __init__(self, spectrum_list, maps_list):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list
        self.maps_list = maps_list

        self.setup_connections()

    def setup_connections(self):
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

    def del_spectrum(self, fname, spectramap=None):
        self.model.del_spectrum(fname, spectramap)

    def del_map(self, fname):
        self.model.del_map(fname)

    def update_spectrum_list(self, spectramap):
        if spectramap is not None:
            self.update_list_widget(self.spectrum_list.list, self.model.spectramaps_fnames[spectramap])
        else:
            self.maps_list.list.clearSelection()
            self.update_list_widget(self.spectrum_list.list, self.model.spectrum_fnames)

    def update_list_widget(self, list_widget, files):
        """Refresh the list widget with the files and update the label."""
        current_items = {list_widget.item(i).text() for i in range(list_widget.count())}
        new_items = set(files)

        # Determine items to add and remove
        items_to_add = new_items - current_items
        items_to_remove = current_items - new_items
        
        # Remove items
        for i in range(list_widget.count() - 1, -1, -1):
            item = list_widget.item(i)
            if item.text() in items_to_remove:
                list_widget.takeItem(i)

        # Add new items
        for file_path in items_to_add:
            list_widget.addItem(file_path)

        # Auto select the first item if none are selected
        if not list_widget.selectedItems() and list_widget.count():
            list_widget.setCurrentRow(0)

    def update_map_selection(self, maps_list, spectrum_list):
        selected_items = maps_list.selectedItems()
        if selected_items:
            selected_map = selected_items[0].text()
            selected_files = self.model.spectramaps_fnames[selected_map]
        else:
            selected_map = None
            selected_files = self.model.spectrum_fnames

        self.update_list_widget(spectrum_list, selected_files)
        self.mapChanged.emit(selected_map)

    def update_selection(self, list_widget, label_widget):
        """Update Plot and count label when the selection changes."""
        fnames = [item.text() for item in list_widget.selectedItems()]
        total_count = list_widget.count()
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"{selected_count}/{total_count}")
        self.spectraPlotChanged.emit(fnames)

    def remove_selected_files(self, list_widget):
        """Remove the currently selected files from the model."""
        selected_items = [item.text() for item in list_widget.selectedItems()]
        self.model.remove_files(selected_items)

    def update_spectramap(self, file, fnames):
        """Update the lists widgets with the spectra related to the 2D-map."""
        self.model.update_spectramap(file, fnames)