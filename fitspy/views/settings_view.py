from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super(SettingsView, self).__init__(parent)

        # Create and set layout for this widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Select Files button
        self.select_files = QPushButton("Select Files")
        layout.addWidget(self.select_files)

        # QListWidget to display selected files
        self.selected_files = QListWidget()
        layout.addWidget(self.selected_files)
