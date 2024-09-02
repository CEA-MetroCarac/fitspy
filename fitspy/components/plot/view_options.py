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

        legend_checkbox = QCheckBox("Legend")
        best_fit_checkbox = QCheckBox("Best-fit")
        filled_checkbox = QCheckBox("Filled")
        peaks_checkbox = QCheckBox("Peaks")
        raw_checkbox = QCheckBox("Raw")
        residual_checkbox = QCheckBox("Residual")
        colors_checkbox = QCheckBox("Colors")

        grid.addWidget(legend_checkbox, 0, 0)
        grid.addWidget(best_fit_checkbox, 0, 1)
        grid.addWidget(filled_checkbox, 0, 2)
        grid.addWidget(peaks_checkbox, 0, 3)
        grid.addWidget(raw_checkbox, 1, 0)
        grid.addWidget(residual_checkbox, 1, 1)
        grid.addWidget(colors_checkbox, 1, 2)

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