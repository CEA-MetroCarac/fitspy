from __future__ import annotations

from fitspy.apps.pyside.components.plot.abstractions import PointerEvent


def pointer_event_from_mpl(event) -> PointerEvent:
    return PointerEvent(
        xdata=getattr(event, "xdata", None),
        ydata=getattr(event, "ydata", None),
        button=getattr(event, "button", None),
        in_plot_area=getattr(event, "inaxes", None) is not None,
        raw=event,
    )
