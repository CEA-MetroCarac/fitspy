from PySide6.QtCore import QObject
from .model import Model

class FilesController(QObject):
    def __init__(self, spectrum_list, ):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list
        # self.maps_list = maps_list

        self.setup_connections()
    
    def setup_connections(self):
        self.spectrum_list.list.filesDropped.connect(self.model.set_files)
        self.spectrum_list.list.itemSelectionChanged.connect(lambda: self.update_selection(self.spectrum_list.list, self.spectrum_list.label))
        self.spectrum_list.sel_all.clicked.connect(self.spectrum_list.list.selectAll)
        self.spectrum_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.spectrum_list.list, self.spectrum_list.label, self.model.files))
        self.model.filesChanged.connect(lambda: self.update_list_widget(self.spectrum_list.list, self.spectrum_list.label, self.model.files))

        # self.maps_list.list.filesDropped.connect(self.model.set_map_files)
        # self.maps_list.list.itemSelectionChanged.connect(lambda: self.update_selection(self.maps_list.list, self.maps_list.label))
        # self.maps_list.sel_all.clicked.connect(self.maps_list.list.selectAll)
        # self.maps_list.rm_btn.clicked.connect(lambda: self.remove_selected_files(self.maps_list.list, self.model.map_files))
        # self.model.mapFilesChanged.connect(lambda: self.update_list_widget(self.maps_list.list, self.maps_list.label, self.model.map_files))

    def update_list_widget(self, list_widget, label_widget, files):
        """Refresh the list widget with the files and update the label."""
        list_widget.clear()
        for file_path in files:
            list_widget.addItem(file_path)

        list_widget.setCurrentRow(0)
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"Items: {selected_count}/{list_widget.count()}")

    def update_selection(self, list_widget, label_widget):
        """Update the label with the count of selected and total files."""
        total_count = list_widget.count()
        selected_count = len(list_widget.selectedItems())
        label_widget.setText(f"Items: {selected_count}/{total_count}")

    def remove_selected_files(self, list_widget, label_widget, files):
        """Remove the currently selected files from the model."""
        selected_items = list_widget.selectedItems()
        if selected_items:
            selected_files = [item.text() for item in selected_items]
            for file in selected_files:
                files.remove(file)
            self.update_list_widget(list_widget, label_widget, files)