from typing import Literal
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QSpinBox,
    QComboBox,
    QAbstractSpinBox,
    QMenu,
)
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDropEvent,
    QPainter,
    QPalette,
    QValidator,
)


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(
        self,
        parent=None,
        empty_value=None,
        significant_digits: int = 4,
        notation: Literal["auto", "fixed", "scientific"] = "auto"
    ):
        super().__init__(parent)
        self.empty_value = empty_value
        self.significant_digits = significant_digits
        self.notation = notation
        self.setMaximum(float("inf"))
        self.setMinimum(-float("inf"))
        self.setDecimals(16)
        self.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.setAccelerated(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def wheelEvent(self, event):
        event.ignore()

    def handle_empty_text(self):
        if not self.text():
            if self.empty_value is None:
                self.clear()
            else:
                self.setValue(self.empty_value)

    def value(self):
        if self.text() == "":
            return None
        return super().value()

    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)

    def contextMenuEvent(self, event):
        menu = self.lineEdit().createStandardContextMenu()

        set_to_inf_action = QAction("Set to Max", self)
        set_to_inf_action.triggered.connect(self.set_to_max)
        menu.addAction(set_to_inf_action)

        set_to_default_action = QAction("Set to Default", self)
        set_to_default_action.triggered.connect(self.set_to_default)
        menu.addAction(set_to_default_action)

        menu.exec(event.globalPos())

    def set_to_max(self):
        self.setValue(float("inf"))

    def set_to_default(self):
        self.setValue(self.empty_value)

    def validate(self, text, pos):
        import re

        sci_pattern = r"^[-+]?((\d+\.?\d*)|(\.\d+))([eE][-+]?\d+)?$"
        if re.match(sci_pattern, text.strip()) or text.strip() == "":
            return (QValidator.Acceptable, text, pos)
        return (QValidator.Invalid, text, pos)

    def valueFromText(self, text):
        try:
            return float(text)
        except Exception:
            return 0.0

    def textFromValue(self, value):
        digits = self.significant_digits
        if self.notation == "fixed":
            return f"{value:.{digits}f}"
        elif self.notation == "scientific":
            return f"{value:.{digits}e}"
        else:
            return f"{value:.{digits}g}"


class SpinBox(QSpinBox):
    def __init__(self, parent=None, empty_value=None):
        super().__init__(parent)
        self.empty_value = empty_value
        self.setMaximum(999999999)
        self.setFocusPolicy(Qt.StrongFocus)
        self.lineEdit().textChanged.connect(self.handle_empty_text)

    def wheelEvent(self, event):
        event.ignore()

    def handle_empty_text(self):
        if not self.text():
            if self.empty_value is None:
                self.clear()
            else:
                self.setValue(self.empty_value)

    def value(self):
        if self.text() == "":
            return None
        return super().value()

    def setValue(self, value):
        if value is None:
            self.clear()
        else:
            super().setValue(value)

    def contextMenuEvent(self, event):
        menu = self.lineEdit().createStandardContextMenu()

        set_to_default_action = QAction("Set to Default", self)
        set_to_default_action.triggered.connect(self.set_to_default)
        menu.addAction(set_to_default_action)

        menu.exec(event.globalPos())

    def set_to_default(self):
        self.setValue(self.empty_value)

    def validate(self, text, pos):
        import re

        sci_pattern = r"^[-+]?((\d+\.?\d*)|(\.\d+))([eE][-+]?\d+)?$"
        if re.match(sci_pattern, text.strip()) or text.strip() == "":
            return (QValidator.Acceptable, text, pos)
        return (QValidator.Invalid, text, pos)

    def valueFromText(self, text):
        try:
            return int(float(text))
        except Exception:
            return 0


class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.NoFocus)

    def wheelEvent(self, event):
        event.ignore()


class DragNDropCombo(ComboBox):
    itemAdded = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.drag_active = False

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drag_active = True
            self.update()
        else:
            super().dragMoveEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.drag_active = False
        self.update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            fname = url.toLocalFile()
            if fname not in [self.itemText(i) for i in range(self.count())]:
                self.itemAdded.emit(fname)
        event.acceptProposedAction()
        self.drag_active = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self)
            painter.save()

            if self.drag_active:
                painter.setPen(self.palette().color(QPalette.Highlight))
                text = "Release to load file(s)"
            else:
                painter.setPen(
                    self.palette().color(QPalette.Disabled, QPalette.Text)
                )
                text = "Fitting Models: Drag and Drop File(s) Here"

            rect = self.rect()
            painter.drawText(rect, Qt.AlignCenter, text)

            painter.restore()


class CategorizedComboBox(ComboBox):
    CATEGORY_ROLE = Qt.UserRole + 1

    def showPopup(self):
        if self.count() == 0:
            return

        menu = QMenu(self)
        menu.setToolTipsVisible(True)
        action_group = QActionGroup(menu)
        action_group.setExclusive(True)

        top_level_indices = []
        categories = {}
        category_order = []

        for i in range(self.count()):
            category = self.itemData(i, self.CATEGORY_ROLE)  # may be None
            if category in (None, ""):
                top_level_indices.append(i)
                continue

            if category not in categories:
                categories[category] = []
                category_order.append(category)
            categories[category].append(i)

        current_index = self.currentIndex()

        for i in top_level_indices:
            label = self.itemText(i)
            action = menu.addAction(label)
            action.setCheckable(True)
            action.setData(i)
            action.setToolTip(self.itemData(i, Qt.ToolTipRole))
            action_group.addAction(action)
            if i == current_index:
                action.setChecked(True)
                menu.setActiveAction(action)

        if top_level_indices and category_order:
            menu.addSeparator()

        for category in category_order:
            submenu = menu.addMenu(str(category))
            submenu.setToolTipsVisible(True)
            for i in categories[category]:
                label = self.itemText(i)
                action = submenu.addAction(label)
                action.setCheckable(True)
                action.setData(i)
                action.setToolTip(self.itemData(i, Qt.ToolTipRole))
                action_group.addAction(action)

        def _on_action_triggered(action):
            index = action.data()
            if isinstance(index, int):
                self.setCurrentIndex(index)

        action_group.triggered.connect(_on_action_triggered)
        menu.exec(self.mapToGlobal(self.rect().bottomLeft()))


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    obj = SpinBox()
    # obj = DoubleSpinBox()
    obj.show()
    sys.exit(app.exec())
