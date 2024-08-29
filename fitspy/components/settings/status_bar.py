from PySide6.QtCore import QSize
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QSizePolicy, QSpinBox, QWidget, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.label_38 = QLabel(self)
        self.label_38.setObjectName("label_38")
        self.addWidget(self.label_38)

        self.label_19 = QLabel(self)
        self.label_19.setObjectName("label_19")
        self.label_19.setText("Number of CPUs")
        self.addWidget(self.label_19)

        self.label_21 = QLabel(self)
        self.label_21.setObjectName("label_21")
        self.addWidget(self.label_21)

        self.ncpus = QSpinBox(self)
        self.ncpus.setObjectName("ncpus")
        self.ncpus.setMinimum(1)
        self.ncpus.setMaximum(64)
        self.addWidget(self.ncpus)

        self.progressText = QLabel(self)
        self.progressText.setObjectName("progressText")
        self.addWidget(self.progressText)

        self.label_95 = QLabel(self)
        self.label_95.setObjectName("label_95")
        self.addWidget(self.label_95)

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

        self.label_24 = QLabel(rightAlignedWidget)
        self.label_24.setObjectName("label_24")
        rightAlignedLayout.addWidget(self.label_24)

        self.addPermanentWidget(rightAlignedWidget)