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
        self.model.filesChanged.connect(self.on_files_changed)

    def on_files_changed(self, files):
        print("Files changed:", files)
        self.refresh_view()

    def updateModelWithFiles(self, file_paths):
        """Append new files to model and refresh view."""
        self.model.set_files(file_paths)

    def load_files(self):
        """Open file dialog and update model with selected files."""
        file_paths = self.open_file_dialog()
        if file_paths:
            self.model.set_files(file_paths)

    def load_folder(self):
        """Loads all *.txt files from a chosen folder."""
        folder_path = self.open_folder_dialog()
        if folder_path:
            self.model.set_folder(folder_path)

    def remove_selected_item(self):
        """Remove selected items from the model and refresh view."""
        files_to_del = self.view.file_list.selectedItems()
        if files_to_del:
            files_to_del = [item.text() for item in files_to_del]
            self.model.remove_file(files_to_del)

    def remove_all_items(self):
        """Clear all items from the model and refresh view."""
        self.model.clear_files()

    def refresh_view(self):
        """Refresh the list widget from the model."""
        self.view.file_list.clear()
        for file_path in self.model.get_files():
            self.view.file_list.addItem(file_path)

    def open_file_dialog(self):
        """Open a file dialog and return the selected file paths."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self.view,
            caption="Select File(s)",
            dir="",
            filter="*.txt"
        )
        return file_paths
    
    def open_folder_dialog(self):
        """Open a folder dialog and return the selected folder path."""
        folder_path = QFileDialog.getExistingDirectory(
            parent=self.view,
            caption="Select Folder",
            dir=""
        )
        return folder_path
