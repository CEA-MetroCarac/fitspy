from fitspy import VERSION

DEFAULTS = {
    'version': VERSION,
    'theme': 'dark',
    'ncpus': 'Auto',
    'outliers_coef': 1.5,
    'click_mode': 'highlight',
    'dx0': 20,
    'dfwhm': 200,
    'alpha': {'min': 0, 'value': 0.5, 'max': 1},
    'peaks_cmap': 'tab10',
    'map_cmap': 'viridis',
    'figure_options': {'title': 'DEFAULT_TITLE (edit in toolbar)'},
    'view_options': {
        "legend": True,
        "fit": True,
        "negative_values": True,
        "outliers": True,
        "outliers_limits": True,
        "noise_level": True,
        "baseline": True,
        "subtract_bkg+baseline": False,
        "background": True,
        "residual": False,
        "peaks": True,
        "peak_labels": True,
        "annotations": True,
        'preserve_axes': False,
    }
}
DEFAULTS_INITIAL = DEFAULTS.copy()

# Settings migration mappings
SETTINGS_KEY_MIGRATIONS = {
    # "new_key_1": ["old_key_1a", "old_key_1b"],
}
SETTINGS_VALUE_MIGRATIONS = {
    "click_mode": {"fitting": "peaks"},
}
