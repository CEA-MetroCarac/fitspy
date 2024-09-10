from PySide6.QtWidgets import QGroupBox, QGridLayout, QCheckBox

class ViewOptions(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("View options:")

        grid = QGridLayout()
        grid.setContentsMargins(2, 2, 2, 2)
        grid.setSpacing(1)

        checkboxes = [
            ("Legend", "Legend"),
            ("Fit", "Fit"),
            ("Negative values", "Negative values"),
            ("Outliers", "Outliers"),
            ("Outliers limits", "Outliers limits"),
            ("Noise level", "Noise level"),
            ("Baseline", "Baseline"),
            ("Background", "Background"),
            ("Residual", "Residual"),
            ("Peaks", "Peaks"),
            ("Raw", "Raw"),
            # ("Filled", "Filled"),
            # ("Colors", "Colors"),
        ]

        for i, (text, tooltip) in enumerate(checkboxes):
            checkbox = QCheckBox(text)
            checkbox.setToolTip(tooltip)
            grid.addWidget(checkbox, i // 4, i % 4)

        self.setLayout(grid)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    view_options = ViewOptions()
    main_window.setCentralWidget(view_options)
    main_window.show()

    sys.exit(app.exec())