import os
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QSizePolicy, QWidget, QStatusBar, QComboBox

class StatusBar(QStatusBar):
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
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.label_19 = QLabel(self)
        self.label_19.setObjectName("label_19")
        self.label_19.setText("Number of CPUs")
        self.addWidget(self.label_19)

        self.ncpus = QComboBox(self)
        self.ncpus.setObjectName("ncpus")
        self.populate_cpu_choices()
        self.addWidget(self.ncpus)

        self.progressText = QLabel(self)
        self.progressText.setObjectName("progressText")
        self.addWidget(self.progressText)

        rightAlignedWidget = QWidget(self)
        rightAlignedLayout = QHBoxLayout(rightAlignedWidget)
        rightAlignedLayout.setContentsMargins(0, 0, 0, 0)
        rightAlignedLayout.addStretch()

        self.progressBar = QProgressBar(rightAlignedWidget)
        self.progressBar.setObjectName("progressBar")
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QSize(200, 10))
        self.progressBar.setMaximumSize(QSize(200, 10))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        rightAlignedLayout.addWidget(self.progressBar)

        self.addPermanentWidget(rightAlignedWidget)