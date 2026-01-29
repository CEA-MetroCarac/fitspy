import copy

import pytest

from fitspy.core.migrations import (
    CURRENT_MODEL_SCHEMA_VERSION,
    migrate_model_dict,
    migrate_qsettings,
    migrate_spectra_dict,
)


class DummySettings:
    def __init__(self, initial=None):
        self._data = dict(initial or {})
        self.synced = False

    def value(self, key, default=None):
        return self._data.get(key, default)

    def contains(self, key):
        return key in self._data

    def setValue(self, key, value):
        self._data[key] = value

    def remove(self, key):
        if key in self._data:
            del self._data[key]

    def sync(self):
        self.synced = True


def test_migrate_model_dict_key_renames_and_schema_version():
    legacy = {
        "models": {0: {"Gaussian": {"x0": {"value": 1}}}},
        "models_labels": ["p1"],
        "models_index": 2,
        "fit_method": "Leastsq",
        "fit_negative": True,
        "max_ite": 10,
        "xtol": 1e-3,
        "independent_models": True,
        "attached": False,
        "baseline": {"mode": "Semi-Auto"},
    }

    migrated = migrate_model_dict(legacy)

    assert "schema_version" in migrated
    assert migrated["schema_version"] == CURRENT_MODEL_SCHEMA_VERSION
    assert "models" not in migrated
    assert "models_labels" not in migrated
    assert "models_index" not in migrated
    assert migrated["peak_models"][0]["Gaussian"]["x0"]["value"] == 1
    assert migrated["peak_labels"] == ["p1"]
    assert migrated["peak_index"] == 2
    assert migrated["baseline"]["attached"] is False
    assert migrated["baseline"]["mode"] == "arpls"
    assert migrated["fit_params"]["method"] == "leastsq"
    assert migrated["fit_params"]["fit_negative"] is True
    assert migrated["fit_params"]["max_ite"] == 10
    assert migrated["fit_params"]["xtol"] == 1e-3
    assert migrated["fit_params"]["independent_models"] is True


def test_migrate_model_dict_baseline_history():
    legacy = {
        "baseline_history": [["Polynomial", 2, [[1, 2], [3, 4]], 0.5]],
        "baseline": {},
    }

    migrated = migrate_model_dict(legacy)
    assert "baseline_history" not in migrated
    assert migrated["baseline"]["mode"] == "Polynomial"
    assert migrated["baseline"]["order_max"] == 2
    assert migrated["baseline"]["points"] == [[1, 2], [3, 4]]
    assert migrated["baseline"]["sigma"] == 0.5
    assert migrated["baseline"]["is_subtracted"] is True


def test_migrate_model_dict_norm_mode_maximum():
    legacy = {
        "norm_mode": "Maximum",
    }

    migrated = migrate_model_dict(legacy)
    assert "norm_mode" not in migrated
    assert migrated["normalize"] is True


def test_migrate_spectra_dict_applies_to_each_item():
    legacy = {
        0: {"models": {0: {"Gaussian": {"x0": {"value": 1}}}}},
        1: {"models": {0: {"Lorentzian": {"x0": {"value": 2}}}}},
        "data": {"dummy": "payload"},
    }

    migrated = migrate_spectra_dict(copy.deepcopy(legacy))
    assert migrated["data"]["dummy"] == "payload"
    assert "peak_models" in migrated[0]
    assert "peak_models" in migrated[1]


def test_migrate_qsettings_updates_version_and_values():
    settings = DummySettings({"version": "old", "click_mode": "fitting"})
    migrate_qsettings(settings, current_version="new")

    assert settings.value("version") == "new"
    assert settings.value("click_mode") == "peaks"
    assert settings.synced is True


def test_migrate_qsettings_noop_when_version_matches():
    settings = DummySettings({"version": "same", "click_mode": "fitting"})
    migrate_qsettings(settings, current_version="same")

    assert settings.value("click_mode") == "fitting"
    assert settings.synced is False
