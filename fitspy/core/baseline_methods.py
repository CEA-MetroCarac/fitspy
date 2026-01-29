from typing import Any, Dict


_INTERNAL_METHODS: Dict[object, Dict[str, Any]] = {
    None: {"label": "None", "use_points": False},
     "arpls": {
        "label": "arPLS ⭐",
        "coef_kwarg": "smoothing_factor",
        "use_points": False,
        "category": "Whittaker",
        "help": "Asymmetrically Reweighted PLS. The standard for Raman/IR.",
    },
    "Linear": {
        "label": "Linear Interpolation",
        "use_points": True,
        "sigma_kwarg": "sigma",
        "category": "Manual",
    },
    "Polynomial": {
        "label": "Polynomial Fit",
        "use_points": True,
        "order_kwarg": "order_max",
        "sigma_kwarg": "sigma",
        "category": "Manual",
    },
    "sonneveld_vesser": {
        "label": "Sonneveld-Vesser",
        "coef_kwarg": "niter",
        "category": "Smoothing",
        "help": "Sonneveld-Vesser baseline correction algorithm.",
    },
}


_PYBASELINES_WHITELIST: Dict[str, Dict[str, Any]] = {
    # --- Polynomials ---
    "modpoly": {
        "label": "ModPoly",
        "category": "Polynomial",
        "order_kwarg": "poly_order",
        "help": "Modified Polynomial. Good for simple baselines.",
    },
    "imodpoly": {
        "label": "IModPoly",
        "category": "Polynomial",
        "order_kwarg": "poly_order",
        "help": "Improved ModPoly. More robust against noise.",
    },
    
    # --- Whittaker (Penalized Least Squares) ---
    # "arpls": {
    #     "label": "arPLS",
    #     "coef_kwarg": "lam",
    #     "category": "Whittaker",
    #     "help": "Asymmetrically Reweighted PLS. The standard for Raman/IR.",
    # },
    "airpls": {
        "label": "airPLS",
        "category": "Whittaker",
        "coef_kwarg": "lam",
        # "order_kwarg": "diff_order",
        "help": "Adaptive Iterative PLS. Excellent for varying noise levels.",
    },
    "asls": {
        "label": "AsLS",
        "category": "Whittaker",
        "coef_kwarg": "lam",
        "help": "Asymmetric Least Squares. The classic algorithm.",
    },

    # --- Morphological ---
    "mor": {
        "label": "Mor",
        "category": "Morphological",
        "help": "Traditional Morphological baseline.",
    },
    "rolling_ball": {
        "label": "Rolling Ball",
        "category": "Morphological",
        "help": "Good for backgrounds with varying curvature.",
    },

    # --- Smoothing / Statistics ---
    "snip": {
        "label": "SNIP",
        "category": "Smoothing",
        "order_kwarg": "filter_order",
        "help": "Statistics-sensitive Non-linear Iterative Peak-clipping.",
    },
    "noise_median": {
        "label": "Noise Median",
        "category": "Smoothing",
        "sigma_kwarg": "sigma",
        "help": "Simple median-based estimation.",
    },

    # --- Misc ---
    "rubberband": {
        "label": "Rubberband",
        "category": "Misc",
        "coef_kwarg": "lam",
        "help": "Convex hull of the data.",
    },
}


def get_baseline_method_meta(method_id: object) -> Dict[str, Any]:
    if method_id in _INTERNAL_METHODS:
        return _INTERNAL_METHODS[method_id]

    if isinstance(method_id, str) and method_id in _PYBASELINES_WHITELIST:
        return _PYBASELINES_WHITELIST[method_id]

    raise ValueError(f"Unknown baseline method ID: {method_id}")


PYBASELINES_METHODS = sorted(list(_PYBASELINES_WHITELIST.keys()))
BASELINE_METHODS = list(_INTERNAL_METHODS.keys()) + PYBASELINES_METHODS