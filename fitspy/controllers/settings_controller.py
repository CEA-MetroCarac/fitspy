from PySide6.QtWidgets import QFileDialog
from models.settings_model import SettingsModel

class SettingsController:
    def __init__(self, view):
        self.view = view
        self.model = SettingsModel()
        self.setup_actions()

    def setup_actions(self):
        """Connect UI actions to controller methods."""
        self.view.select_files.clicked.connect(self.load_files)
        self.view.file_list.filesDropped.connect(self.updateModelWithFiles)
        self.view.remove_selected.clicked.connect(self.remove_selected_item)
        self.view.remove_all.clicked.connect(self.remove_all_items)

    def updateModelWithFiles(self, file_paths):
        """Update model with files and refresh view."""
        self.model.set_files(file_paths)
        self.refresh_view()

    def load_files(self):
        """Open file dialog and update model with selected files."""
        file_paths = self.open_file_dialog()
        if file_paths:
            self.model.set_files(file_paths)
            self.refresh_view()

    def remove_selected_item(self):
        """Remove selected items from the model and refresh view."""
        list_items = self.view.file_list.selectedItems()
        if list_items:
            for item in list_items:
                self.model.remove_file(item.text())
            self.refresh_view()

    def remove_all_items(self):
        """Clear all items from the model and refresh view."""
        self.model.clear_files()
        self.refresh_view()

    def refresh_view(self):
        """Refresh the list widget from the model."""
        self.view.file_list.clear()
        for file_path in self.model.get_files():
            self.view.file_list.addItem(file_path)

    def open_file_dialog(self):
        """Open a file dialog and return the selected file paths."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self.view,
            caption="Select Files",
            dir="",
            filter=""
        )
        return file_paths