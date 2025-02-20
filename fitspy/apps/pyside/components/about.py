import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QFrame
from PySide6.QtGui import QPixmap

from fitspy import VERSION
from fitspy.apps.pyside.utils import get_icon_path


class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Fitspy")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(get_icon_path("logo.png"))
        scaled_pixmap = logo_pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title_label = QLabel("Fitspy")
        font = title_label.font()
        font.setPointSize(20)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Fitspy Version
        version_label = QLabel(f"Version: {VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        # Python Version
        python_version_label = QLabel(f"Python version: {sys.version.split()[0]}")
        python_version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(python_version_label)

        # Authors
        authors_label = QLabel(
            "Authors:\nPatrick Quéméré (patrick.quemere@cea.fr)\nKillian Pavy (killian.pavy@cea.fr)"
        )
        authors_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(authors_label)

        # Description
        description_label = QLabel(
            "Fitspy is a Python application for processing and analyzing spectral data.")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_label)

        # License
        license_label = QLabel("License: GPL v3")
        license_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(license_label)

        # Website
        website_label = QLabel('<a href="https://github.com/CEA-MetroCarac/fitspy">Homepage</a>')
        website_label.setOpenExternalLinks(True)
        website_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(website_label)

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # CEA MetroCarac Logos
        additional_logo_label = QLabel()
        additional_logo_pixmap = QPixmap(get_icon_path("logos.png"))
        additional_scaled_pixmap = additional_logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio,
                                                                 Qt.SmoothTransformation)
        additional_logo_label.setPixmap(additional_scaled_pixmap)
        additional_logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(additional_logo_label)

        self.setLayout(layout)

        # Acknowledgments
        acknowledgments_text = (
            "This work, carried out on the CEA - Platform for Nanocharacterisation (PFNC), "
            "was supported by the “Recherche Technologique de Base” program of the French "
            "National Research Agency (ANR).\n\n"
            "Warm thanks to the <a href='https://joss.theoj.org/'>JOSS</a> reviewers "
            "(<a href='https://github.com/maurov'>@maurov</a> and <a "
            "href='https://github.com/FCMeng'>@FCMeng</a>) "
            "and editor (<a href='https://github.com/phibeck'>@phibeck</a>) for their "
            "contributions to enhancing Fitspy."
        )
        acknowledgments_label = QLabel()
        acknowledgments_label.setTextFormat(Qt.RichText)
        acknowledgments_label.setText(acknowledgments_text)
        acknowledgments_label.setWordWrap(True)
        acknowledgments_label.setAlignment(Qt.AlignCenter)
        acknowledgments_label.setOpenExternalLinks(True)
        layout.addWidget(acknowledgments_label)

        self.setLayout(layout)
