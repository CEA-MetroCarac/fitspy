from copy import deepcopy
from typing import Any, Dict, Iterable

from fitspy import FIT_PARAMS, FIT_METHODS, VERSION

CURRENT_MODEL_SCHEMA_VERSION = 1
CURRENT_QSETTINGS_SCHEMA_VERSION = VERSION


# QSettings migration mappings
SETTINGS_KEY_MIGRATIONS: Dict[str, Iterable[str]] = {
    # "new_key": ["old_key1", "old_key2"],
}

SETTINGS_VALUE_MIGRATIONS: Dict[str, Dict[Any, Any]] = {
    "click_mode": {"fitting": "peaks"},
}


def migrate_qsettings(settings, current_version: str = CURRENT_QSETTINGS_SCHEMA_VERSION,
                      version_key: str = "version") -> None:
    stored_version = settings.value(version_key, None)
    if stored_version == current_version:
        return

    print(f"Version migration: {stored_version} -> {current_version}")

    for new_key, old_keys in SETTINGS_KEY_MIGRATIONS.items():
        for old_key in old_keys:
            if settings.contains(old_key):
                value = settings.value(old_key)
                settings.setValue(new_key, value)
                settings.remove(old_key)

    for key, value_map in SETTINGS_VALUE_MIGRATIONS.items():
        if settings.contains(key):
            current_value = settings.value(key)
            if current_value in value_map:
                settings.setValue(key, value_map[current_value])

    settings.setValue(version_key, current_version)
    settings.sync()


def migrate_spectra_dict(dict_spectra: Dict[Any, Any]) -> Dict[Any, Any]:
    if dict_spectra is None:
        return dict_spectra
    migrated = deepcopy(dict_spectra)
    for key, model in list(migrated.items()):
        if key == "data":
            continue
        if isinstance(model, dict):
            migrated[key] = migrate_model_dict(model)
    return migrated


def migrate_model_dict(model_dict: Dict[str, Any], spectrum=None) -> Dict[str, Any]:
    if model_dict is None:
        return model_dict

    migrated = deepcopy(model_dict)
    version = _safe_int(migrated.get("schema_version", 0))

    # print("Migrating model schema: version", version, "->", CURRENT_MODEL_SCHEMA_VERSION)

    while version < CURRENT_MODEL_SCHEMA_VERSION:
        migrator = MODEL_MIGRATIONS.get(version)
        if migrator is None:
            break
        migrated = migrator(migrated, spectrum=spectrum)
        version = _safe_int(migrated.get("schema_version", version + 1))

    return migrated


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _rename_path(data: Dict[str, Any], old_path: str, new_path: str) -> None:
    old_parent, old_key = _ensure_parent(data, old_path.split("."), create=False)
    if old_parent is None or old_key not in old_parent:
        return
    new_parent, new_key = _ensure_parent(data, new_path.split("."), create=True)
    if new_parent is None or new_key in new_parent:
        return
    new_parent[new_key] = old_parent.pop(old_key)


def _ensure_parent(data: Dict[str, Any], path: Iterable[str], create: bool) -> tuple[dict | None, str | None]:
    keys = list(path)
    if not keys:
        return None, None
    parent = data
    for key in keys[:-1]:
        if key not in parent or not isinstance(parent[key], dict):
            if not create:
                return None, None
            parent[key] = {}
        parent = parent[key]
    return parent, keys[-1]


def _map_value(data: Dict[str, Any], path: str, mapping: Dict[str, str]) -> None:
    parent, key = _ensure_parent(data, path.split("."), create=False)
    if parent is None or key not in parent:
        return
    value = parent[key]
    if isinstance(value, str):
        mapped = mapping.get(value, mapping.get(value.strip(), None))
        if mapped is None:
            mapped = mapping.get(value.casefold())
        if mapped is not None:
            parent[key] = mapped


def _normalize_fit_method(data: Dict[str, Any]) -> None:
    parent, key = _ensure_parent(data, "fit_params.method".split("."), create=False)
    if parent is None or key not in parent:
        return
    value = parent[key]
    if isinstance(value, str):
        if value in FIT_METHODS:
            parent[key] = FIT_METHODS[value]
        else:
            parent[key] = value.lower()


def _migrate_baseline_history(data: Dict[str, Any]) -> None:
    if "baseline_history" not in data:
        return
    baseline_history = data.pop("baseline_history")
    if len(baseline_history) > 1:
        msg = "baseline_history with more than 1 item are no more valid"
        raise IOError(msg)
    if len(baseline_history) == 1:
        baseline = data.setdefault("baseline", {})
        mode, order_max, points, *rest = baseline_history[0]
        baseline.setdefault("mode", mode)
        baseline.setdefault("order_max", order_max)
        baseline.setdefault("points", points)
        if rest:
            sigma = rest[0]
            baseline.setdefault("sigma", sigma if sigma is not None else 0)
        baseline.setdefault("is_subtracted", True)


def _migrate_normalization(data: Dict[str, Any], spectrum=None) -> None:
    if "norm_mode" not in data:
        return
    norm_mode = data.pop("norm_mode")
    if norm_mode == "Maximum":
        data.setdefault("normalize", True)
        return

    if "norm_position_ref" in data and spectrum is not None:
        norm_position_ref = data.pop("norm_position_ref")
        if norm_position_ref is not None:
            from fitspy.core.utils import get_1d_profile
            x = get_1d_profile(spectrum.fname)[0]
            # consider 10 pts around 'norm_position_ref' (to simplify)
            delta = abs(10 * (x[1] - x[0]))
            data["normalize"] = True
            data["normalize_range_min"] = norm_position_ref - delta
            data["normalize_range_max"] = norm_position_ref + delta


def _migrate_0_to_1(data: Dict[str, Any], spectrum=None) -> Dict[str, Any]:
    key_renames = [
        ("models", "peak_models"),
        ("models_labels", "peak_labels"),
        ("models_index", "peak_index"),
        ("fit_method", "fit_params.method"),
        ("fit_negative", "fit_params.fit_negative"),
        ("max_ite", "fit_params.max_ite"),
        ("xtol", "fit_params.xtol"),
        ("independent_models", "fit_params.independent_models"),
        ("attached", "baseline.attached"),
    ]
    for old_path, new_path in key_renames:
        _rename_path(data, old_path, new_path)

    if "fit_params" in data and isinstance(data["fit_params"], dict):
        for key, default in FIT_PARAMS.items():
            data["fit_params"].setdefault(key, default)

    _migrate_baseline_history(data)
    _migrate_normalization(data, spectrum=spectrum)

    baseline_aliases = {
        "semi-auto": "arpls",
    }
    _map_value(data, "baseline.mode", baseline_aliases)
    _normalize_fit_method(data)

    data["schema_version"] = 1
    return data


MODEL_MIGRATIONS = {
    0: _migrate_0_to_1,
}