DEFAULTS = {
    'theme': 'dark',
    'ncpus': 'Auto',
    'outliers_coef': 1.5,
    'click_mode': 'highlight',
    'peaks_cmap': 'tab10',
    'map_cmap': 'viridis',
    'figure_options': {'title': 'DEFAULT_TITLE (edit in toolbar)'},
    'view_options': {
        "raw": False,
        "legend": True,
        "fit": True,
        "negative_values": True,
        "outliers": True,
        "outliers_limits": True,
        "noise_level": True,
        "baseline": True,
        "subtract_bkg+baseline": True,
        "background": True,
        "residual": True,
        "peaks": True,
        "peak_labels": True,
        'preserve_axes': False,
    }
}

DEFAULTS_INITIAL = DEFAULTS.copy()
