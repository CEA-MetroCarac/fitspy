from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QGroupBox,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
    QLabel,
    QSpacerItem,
    QApplication,
)

from fitspy import FIT_METHODS, FIT_PARAMS
from superqt.cmap import CmapCatalogComboBox
from .custom_spinbox import SpinBox, DoubleSpinBox


class SolverSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Fit Solver Settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()

        self.fit_negative = QCheckBox("Fit negative values:")
        self.fit_negative.setChecked(FIT_PARAMS["fit_negative"])

        self.fit_outliers = QCheckBox("Fit outliers:")
        self.fit_outliers.setChecked(FIT_PARAMS["fit_outliers"])

        self.coef_noise_label = QLabel("Coefficient noise:")
        self.coef_noise = DoubleSpinBox()
        self.coef_noise.setValue(FIT_PARAMS["coef_noise"])

        self.max_ite_label = QLabel("Maximum iterations:")
        self.max_ite = SpinBox()
        self.max_ite.setValue(FIT_PARAMS["max_ite"])

        self.method_label = QLabel("Fit method:")
        self.method = QComboBox()
        self.method.addItems(FIT_METHODS.keys())
        self.method.setCurrentText(FIT_PARAMS["method"])

        self.xtol_label = QLabel("x-tolerance:")
        self.xtol = DoubleSpinBox()
        self.xtol.setDecimals(6)
        self.xtol.setValue(FIT_PARAMS["xtol"])

        vbox.addWidget(self.fit_negative)
        vbox.addWidget(self.fit_outliers)

        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.coef_noise_label)
        hbox0.addWidget(self.coef_noise)
        spacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        hbox0.addItem(spacer)
        vbox.addLayout(hbox0)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.max_ite_label)
        hbox1.addWidget(self.max_ite)
        hbox1.addItem(spacer)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.method_label)
        hbox2.addWidget(self.method)
        hbox2.addItem(spacer)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.xtol_label)
        hbox3.addWidget(self.xtol)
        hbox3.addItem(spacer)
        vbox.addLayout(hbox3)

        vbox.addItem(
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.setLayout(vbox)

    def update_settings(self, fit_params):
        if not fit_params:
            return
        self.blockSignals(True)
        self.fit_negative.setChecked(fit_params["fit_negative"])
        self.fit_outliers.setChecked(fit_params["fit_outliers"])
        self.coef_noise.setValue(fit_params["coef_noise"])
        self.max_ite.setValue(fit_params["max_ite"])
        self.method.setCurrentText(fit_params["method"])
        self.xtol.setValue(fit_params["xtol"])
        self.blockSignals(False)


class OtherSettings(QGroupBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setTitle("Other settings:")
        self.setStyleSheet("QGroupBox { font-weight: bold; }")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        hbox = QHBoxLayout()

        self.coef_label = QLabel("Coef:")
        hbox.addWidget(self.coef_label)

        self.outliers_coef = DoubleSpinBox()
        self.outliers_coef.setRange(0.0, 100.0)
        self.outliers_coef.setSingleStep(0.1)
        hbox.addWidget(self.outliers_coef)

        self.outliers_removal = QPushButton("Outliers removal")
        self.outliers_removal.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        hbox.addWidget(self.outliers_removal)

        vbox.addLayout(hbox)

        # Peaks Colormap Selection
        hbox_peaks_cmap = QHBoxLayout()
        self.peaks_cmap_label = QLabel("Peaks Colormap:")
        hbox_peaks_cmap.addWidget(self.peaks_cmap_label)
        # https://pyapp-kit.github.io/superqt/widgets/colormap_catalog/
        # https://cmap-docs.readthedocs.io/en/stable/catalog/#colormaps-by-category
        self.peaks_cmap = CmapCatalogComboBox(categories="qualitative")
        hbox_peaks_cmap.addWidget(self.peaks_cmap)
        vbox.addLayout(hbox_peaks_cmap)

        # 2D Map Colormap Selection
        hbox_map_cmap = QHBoxLayout()
        self.map_cmap_label = QLabel("2D Map Colormap:")
        hbox_map_cmap.addWidget(self.map_cmap_label)
        self.map_cmap = CmapCatalogComboBox()
        hbox_map_cmap.addWidget(self.map_cmap)
        vbox.addLayout(hbox_map_cmap)

        self.setLayout(vbox)


class MoreSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 10, 10, 10)

        self.solver_settings = SolverSettings()
        self.other_settings = OtherSettings()
        hbox.addWidget(self.solver_settings)
        hbox.addWidget(self.other_settings)

        self.setLayout(hbox)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)

    more_settings = MoreSettings()
    main_layout.addWidget(more_settings)

    main_widget.setLayout(main_layout)
    main_widget.show()

    sys.exit(app.exec())
