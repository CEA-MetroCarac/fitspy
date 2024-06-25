from PySide6.QtWidgets import QFileDialog

class SettingsController:
    def __init__(self, view):
        self.view = view

        # Connect the "Select Files" button to the file loading method
        self.view.select_files.clicked.connect(self.load_files)


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