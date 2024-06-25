from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        # Create and set layout for this widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Select Files button
        self.select_files = QPushButton("Select Files")
        layout.addWidget(self.select_files)
        # self.select_files.clicked.connect(self.load_files)

        # QListWidget to display selected files
        self.selected_files = QListWidget()
        layout.addWidget(self.selected_files)

        # Remove Selected button
        self.remove_selected = QPushButton("Remove Selected")
        layout.addWidget(self.remove_selected)

        # Remove All button
        self.remove_all = QPushButton("Remove All")
        layout.addWidget(self.remove_all)