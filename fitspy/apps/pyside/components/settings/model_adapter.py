from dataclasses import dataclass
from typing import Any, Optional

from fitspy.core.migrations import migrate_model_dict
from fitspy.core.spectrum import Spectrum


@dataclass
class PeakRow:
    prefix: str
    label: str
    model_name: str
    param_hints: dict
    fwhm: Optional[float] = None


@dataclass
class BkgRow:
    id: str
    model_name: str
    param_hints: dict
    order: int = 0


@dataclass
class FitModelView:
    model_dict: dict
    peak_rows: list[PeakRow]
    bkg_rows: list[BkgRow]
    baseline_points: list


def fit_model_view_from(source: Any) -> FitModelView:
    model_dict = _model_dict_from(source)
    return FitModelView(
        model_dict=model_dict,
        peak_rows=_extract_peak_rows(model_dict, source),
        bkg_rows=_extract_bkg_rows(model_dict),
        baseline_points=model_dict.get("baseline", {}).get("points", [[], []]),
    )


def _model_dict_from(source: Any) -> dict:
    if isinstance(source, Spectrum):
        model_dict = source.save()
        model_dict.get("baseline", {}).pop("y_eval", None)
        model_dict.pop("fname", None)
        return migrate_model_dict(model_dict, spectrum=source)

    if isinstance(source, dict):
        return migrate_model_dict(source)

    raise TypeError(f"Unsupported fit model source: {type(source).__name__}")


def _extract_peak_rows(model_dict: dict, source: Any) -> list[PeakRow]:
    peak_models = model_dict.get("peak_models", {})
    peak_labels = model_dict.get("peak_labels") or []
    rows = []

    for index, key in enumerate(peak_models):
        model_payload = peak_models[key]
        label = peak_labels[index] if index < len(peak_labels) else str(index + 1)
        prefix = f"m{index + 1:02d}_"
        fwhm = None

        if isinstance(source, Spectrum) and index < len(source.peak_models):
            model = source.peak_models[index]
            prefix = getattr(model, "_prefix", prefix)
            x0 = model.param_hints.get("x0", {}).get("value")
            if x0 is not None:
                fwhm = source.dx(x0=x0)

        for model_name, param_hints in model_payload.items():
            rows.append(PeakRow(prefix, label, model_name, param_hints, fwhm=fwhm))

    return rows


def _extract_bkg_rows(model_dict: dict) -> list[BkgRow]:
    components = model_dict.get("bkg_models") or []
    if isinstance(components, dict):
        components = components.values()

    rows = []
    for index, component in enumerate(components, start=1):
        if not isinstance(component, dict):
            continue

        model_name = component.get("model_name")
        if not model_name:
            continue

        rows.append(BkgRow(
            id=component.get("id", f"b{index:02d}"),
            model_name=model_name,
            order=component.get("order", index),
            param_hints=component.get("param_hints", {}),
        ))

    return sorted(rows, key=lambda row: row.order)
