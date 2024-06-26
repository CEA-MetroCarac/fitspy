class SettingsModel:
    def __init__(self):
        self.files = []

    def set_files(self, file_paths):
        self.files = file_paths

    def get_files(self):
        return self.files

    def remove_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)

    def clear_files(self):
        self.files = []