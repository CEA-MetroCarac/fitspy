from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Signal, QObject
from models.settings_model import SettingsModel

class SettingsController(QObject):
    selectionChanged = Signal(list)

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.model = SettingsModel()
        self.setup_actions()

    def setup_actions(self):
        """Connect UI actions to controller methods."""
        self.view.file_list.itemSelectionChanged.connect(self.on_selection_change)
        self.view.load_file.clicked.connect(self.load_files)
        self.view.open_dir.clicked.connect(self.load_folder)
        self.view.file_list.filesDropped.connect(self.model.set_files)
        self.view.remove_selected.clicked.connect(self.remove_selected_item)
        self.view.remove_all.clicked.connect(self.model.clear_files)
        self.model.filesChanged.connect(self.refresh_view)

    def select_all_files(self):
        """Select all items in the list widget."""
        self.view.file_list.selectAll()
        
    def on_selection_change(self):
        """Triggered when the selection in the list widget changes.
        Emits a signal with the selected files."""
        selected_files = [item.text() for item in self.view.file_list.selectedItems()]
        self.selectionChanged.emit(selected_files)  # Used to connect selection change to plot update via main controller

    def load_files(self):
        """Open file dialog and update model with selected files."""
        file_paths = self.load_file_dialog()
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

    def refresh_view(self, files):
        """Refresh the file list widget with the files from the model."""
        # print("Files changed:", files)
        self.view.file_list.clear()
        for file_path in self.model.get_files():
            self.view.file_list.addItem(file_path)

        self.view.file_list.setCurrentRow(0)

    def load_file_dialog(self):
        """Open a file dialog and return the selected file paths."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self.view,
            caption="Open File(s)",
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
