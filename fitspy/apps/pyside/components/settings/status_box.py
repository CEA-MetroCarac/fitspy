import os
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QWidget
from fitspy.apps.pyside.components.custom_widgets import ComboBox

class StatusBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def populate_cpu_choices(self):
        self.ncpus.addItem("Auto")
        num_cpus = os.cpu_count()
        if num_cpus is not None:
            for i in range(1, num_cpus + 1):
                self.ncpus.addItem(str(i))
        else:
            self.ncpus.addItem("1")

    def initUI(self):
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # Create a horizontal layout for the label and combobox
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        self.cpuCountLabel = QLabel(self)
        self.cpuCountLabel.setText("CPUs:")
        hbox.addWidget(self.cpuCountLabel)

        self.ncpus = ComboBox(self)
        self.populate_cpu_choices()
        hbox.addWidget(self.ncpus)

        vbox.addLayout(hbox)

        self.progressText = QLabel(self)
        vbox.addWidget(self.progressText)

        hbox2 = QWidget(self)
        rightAlignedLayout = QHBoxLayout(hbox2)
        rightAlignedLayout.setContentsMargins(0, 0, 0, 0)

        self.progressLabel = QLabel(self)
        rightAlignedLayout.addWidget(self.progressLabel)
        rightAlignedLayout.addStretch(1)

        self.progressBar = QProgressBar(hbox2)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setMaximumSize(QSize(16777215, 20))
        rightAlignedLayout.addWidget(self.progressBar, 10)

        vbox.addWidget(hbox2)
