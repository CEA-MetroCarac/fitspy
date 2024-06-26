from PySide6.QtCore import QObject, Signal

class SettingsModel(QObject):
    filesChanged = Signal(list)  # Signal to emit when the files list changes

    def __init__(self):
        super().__init__()
        self._files = []

    def set_files(self, files):
        file_added = False
        # Iterate through the new files and add them if they're not already present
        for file in files:
            if file not in self._files:
                self._files.append(file)
                file_added = True 

        if file_added:
            self.filesChanged.emit(self._files)

    def remove_file(self, files):
        for file in files:
            self._files.remove(file)
        self.filesChanged.emit(self._files)

    def clear_files(self):
        self._files = []
        self.filesChanged.emit(self._files)  # Emit signal when files list is cleared

    def get_files(self):
        return self._files
