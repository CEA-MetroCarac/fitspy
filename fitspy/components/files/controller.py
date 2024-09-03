from PySide6.QtCore import QObject
from .model import Model

class FilesController(QObject):
    def __init__(self, spectrum_list):
        super().__init__()
        self.model = Model()
        self.spectrum_list = spectrum_list

        self.setup_connections()
    
    def setup_connections(self):
        self.spectrum_list.list.filesDropped.connect(self.model.set_files)
        self.model.filesChanged.connect(self.update_spectrum_list)

    def update_spectrum_list(self):
        """Refresh the file list widget with the files from the model."""
        # print("Files changed:", files)
        self.spectrum_list.list.clear()
        for file_path in self.model.files:
            self.spectrum_list.list.addItem(file_path)

        self.spectrum_list.list.setCurrentRow(0)
        self.spectrum_list.label.setText(f"Spectra: {self.spectrum_list.list.count()}")