class SettingsModel:
    def __init__(self):
        self.files = []

    def add_file(self, file_path):
        if file_path not in self.files:
            self.files.append(file_path)

    def remove_file(self, file_path):
        if file_path in self.files:
            self.files.remove(file_path)

    def clear_files(self):
        self.files.clear()

    def get_files(self):
        return self.files