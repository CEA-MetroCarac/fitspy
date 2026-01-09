from __future__ import annotations

import matplotlib
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib import cbook

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPixmap

from fitspy.apps.pyside.components.plot.abstractions import PlotNavigation


class _CustomNavigationToolbar(NavigationToolbar2QT):
    def _icon(self, name: str) -> QIcon:
        path_regular = cbook._get_data_path("images", name)
        path_large = path_regular.with_name(path_regular.name.replace(".png", "_large.png"))
        filename = str(path_large if path_large.exists() else path_regular)

        pm = QPixmap(filename)
        pm.setDevicePixelRatio(self.devicePixelRatioF() or 1)
        if self.palette().color(self.backgroundRole()).value() < 128:
            icon_color = self.palette().color(self.foregroundRole())
            mask = pm.createMaskFromColor(QColor("black"), Qt.MaskMode.MaskOutColor)
            pm.fill(icon_color)
            pm.setMask(mask)
        return QIcon(pm)

    def update_icons(self) -> None:
        icon_map = {
            "Home": "home.png",
            "Back": "back.png",
            "Forward": "forward.png",
            "Pan": "move.png",
            "Zoom": "zoom_to_rect.png",
            "Subplots": "subplots.png",
            "Customize": "qt4_editor_options.png",
            "Save": "filesave.png",
        }

        for action in self.actions():
            icon_name = icon_map.get(action.text(), "").lower()
            if icon_name:
                action.setIcon(self._icon(icon_name))

    def is_pan_active(self) -> bool:
        for action in self.actions():
            if action.text() == "Pan":
                return action.isChecked()
        return False

    def is_zoom_active(self) -> bool:
        for action in self.actions():
            if action.text() == "Zoom":
                return action.isChecked()
        return False


class MatplotlibNavigation(PlotNavigation):
    def __init__(self, canvas):
        self._toolbar = _CustomNavigationToolbar(canvas)
        self._toolbar.update_icons()

    def widget(self):
        return self._toolbar

    def is_pan_active(self) -> bool:
        return self._toolbar.is_pan_active()

    def is_zoom_active(self) -> bool:
        return self._toolbar.is_zoom_active()

    def update(self) -> None:
        self._toolbar.update()

    def push_current(self) -> None:
        if hasattr(self._toolbar, "push_current"):
            self._toolbar.push_current()


def ensure_matplotlib_qt_backend() -> None:
    """Best-effort: ensure matplotlib is configured for Qt.

    This should remain backend-internal.
    """

    try:
        matplotlib.use("QtAgg", force=False)
    except Exception:
        return
