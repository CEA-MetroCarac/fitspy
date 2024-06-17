from PySide6.QtWidgets import QFileDialog

class SettingsController:
    def __init__(self, view):
        self.view = view

        # Connect the "Select Files" button to the file loading method
        self.view.select_files.clicked.connect(self.load_files)

    def load_files(self):
        # Open a file dialog and get the selected file paths
        file_paths, _ = QFileDialog.getOpenFileNames(self.view, "Select Files")

        # Clear the QListWidget and add the selected files
        self.view.selected_files.clear()
        self.view.selected_files.addItems(file_paths)