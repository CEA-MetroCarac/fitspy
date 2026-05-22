from fitspy.apps.pyside.components.settings.model_adapter import fit_model_view_from


def test_fit_model_view_from_legacy_bkg_model():
    model = {
        "baseline": {"points": [[], []]},
        "peak_models": {},
        "peak_labels": [],
        "bkg_model": {
            "Linear": {
                "slope": {"min": 0, "value": 1, "max": 2, "vary": True, "expr": ""},
            },
        },
    }

    view = fit_model_view_from(model)

    assert view.model_dict["schema_version"] == 2
    assert len(view.bkg_rows) == 1
    assert view.bkg_rows[0].id == "b01"
    assert view.bkg_rows[0].model_name == "Linear"
    assert view.bkg_rows[0].param_hints["slope"]["value"] == 1


def test_fit_model_view_from_schema_v2_bkg_models():
    model = {
        "schema_version": 2,
        "baseline": {"points": [[1], [2]]},
        "peak_models": {
            0: {
                "Gaussian": {
                    "x0": {"min": 0, "value": 1, "max": 2, "vary": True, "expr": ""},
                },
            },
        },
        "peak_labels": ["peak-a"],
        "bkg_models": [
            {
                "id": "b02",
                "model_name": "Constant",
                "order": 2,
                "param_hints": {
                    "c": {"min": 0, "value": 3, "max": 4, "vary": False, "expr": ""},
                },
            },
            {
                "id": "b01",
                "model_name": "Linear",
                "order": 1,
                "param_hints": {},
            },
        ],
    }

    view = fit_model_view_from(model)

    assert view.baseline_points == [[1], [2]]
    assert len(view.peak_rows) == 1
    assert view.peak_rows[0].prefix == "m01_"
    assert view.peak_rows[0].label == "peak-a"
    assert view.peak_rows[0].model_name == "Gaussian"
    assert [row.id for row in view.bkg_rows] == ["b01", "b02"]
