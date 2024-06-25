from PySide6.QtWidgets import QFileDialog
from models.settings_model import SettingsModel

class SettingsController:
    def __init__(self, view):
        self.view = view
        self.model = SettingsModel()
        self.setup_actions()


    def setup_actions(self):
        self.view.select_files.clicked.connect(self.load_files)
        self.view.remove_selected.clicked.connect(self.remove_selected_item)
        self.view.remove_all.clicked.connect(self.remove_all_items)

    def load_files(self):
        # Ensure the dialog has a parent specified and is application modal
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self.view,
            caption="Select Files",
            dir="",
            filter=""
        )

        # Clear the QListWidget and add the selected files
        self.view.selected_files.clear()
        self.view.selected_files.addItems(file_paths)

    def remove_selected_item(self):
        list_items = self.view.selected_files.selectedItems()
        if not list_items: return
        for item in list_items:
            self.model.remove_file(item.text())  # Assuming item.text() returns the file path
        self.update_view()

    def remove_all_items(self):
        self.model.clear_files()
        self.update_view()

    def update_view(self):
        self.view.selected_files.clear()
        for file_path in self.model.get_files():
            self.view.selected_files.addItem(file_path)