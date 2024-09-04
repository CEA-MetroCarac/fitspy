from PySide6.QtCore import QObject, Signal
from .model import Model

class FilesController(QObject):
    spectraMapInit = Signal(str)

    def __init__(self, spectrum_list, maps_list):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list
        self.maps_list = maps_list

        self.setup_connections()

    def setup_connections(self):
        self.spectrum_list.list.filesDropped.connect(self.model.load_files)
        self.spectrum_list.list.itemSelectionChanged.connect(lambda: self.update_selection(self.spectrum_list.list, self.spectrum_list.count_label))
        self.spectrum_list.sel_all.clicked.connect(self.spectrum_list.list.selectAll)
        self.spectrum_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.spectrum_list.list))
        self.model.spectrumListChanged.connect(lambda: (self.maps_list.list.clearSelection(), self.update_list_widget(self.spectrum_list.list, self.model.spectrum_fnames)))

        self.model.spectraMapInit.connect(self.spectraMapInit)
        self.maps_list.list.filesDropped.connect(self.model.load_files)
        self.maps_list.list.itemSelectionChanged.connect(lambda: self.update_map_selection(self.maps_list.list, self.spectrum_list.list))
        self.maps_list.deselect_btn.clicked.connect(lambda: self.maps_list.list.clearSelection())
        self.maps_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.maps_list.list))
        self.model.mapsListChanged.connect(lambda: self.update_list_widget(self.maps_list.list, self.model.spectramaps_fnames))

    def update_list_widget(self, list_widget, files):
        """Refresh the list widget with the files and update the label."""
        list_widget.clear()
        for file_path in files:
            list_widget.addItem(file_path)
        # auto select the first item
        if not list_widget.selectedItems() and list_widget.count():
            list_widget.setCurrentRow(0)

    def update_map_selection(self, maps_list, spectrum_list):
        selected_items = maps_list.selectedItems()
        if selected_items:
            selected_map = selected_items[0].text()
            selected_files = self.model.spectramaps_fnames[selected_map]
        else:
            selected_files = self.model.spectrum_fnames

        self.update_list_widget(spectrum_list, selected_files)

    def update_selection(self, list_widget, label_widget):
        """Update the label with the count of selected and total files."""
        total_count = list_widget.count()
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"{selected_count}/{total_count}")

    def remove_selected_files(self, list_widget):
        """Remove the currently selected files from the model."""
        selected_items = [item.text() for item in list_widget.selectedItems()]
        self.model.remove_files(selected_items)

    def update_spectramap(self, file, fnames):
        """Update the lists widgets with the spectra related to the 2D-map."""
        self.model.update_spectramap(file, fnames)