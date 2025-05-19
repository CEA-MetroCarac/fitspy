import re
from pathlib import Path
import numpy as np

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QPixmap, QImage


def replace_icon_colors(icon, old_color, new_color):
    pixmap = icon.pixmap(icon.availableSizes()[0])
    image = pixmap.toImage()
    image = image.convertToFormat(QImage.Format_ARGB32)

    width = image.width()
    height = image.height()

    ptr = image.bits()
    arr = np.array(ptr).reshape((height, width, 4))

    old_color_arr = np.array([old_color.red(), old_color.green(), old_color.blue()])
    new_color_arr = np.array([new_color.red(), new_color.green(), new_color.blue(),
                              new_color.alpha()])

    mask = np.all(arr[:, :, :3] == old_color_arr, axis=-1)
    arr[mask, :3] = new_color_arr[:3]  # Replace only the RGB channels

    new_image = QImage(arr.data, width, height, image.bytesPerLine(), QImage.Format_ARGB32)
    return QIcon(QPixmap.fromImage(new_image))


def to_snake_case(s):
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    s = re.sub(r'\s+', '_', s)
    return s


def to_title_case(any_case_str):
    """Convert a string from any case to Title Case with only the first word capitalized."""
    words = re.findall(r'[A-Za-z][^A-Z_\s]*', any_case_str)
    return ' '.join([words[0].capitalize()] + [word.lower() for word in words[1:]])


def get_icon_path(icon_name):
    """ Return the QIcon object from the icon name """
    icon_path = Path(__file__).parents[2] / "resources" / "iconpack" / icon_name
    return str(icon_path)


def update_widget_palette(widget, palette):
    widget.setPalette(palette)
    for child in widget.findChildren(QWidget):
        child.setPalette(palette)
