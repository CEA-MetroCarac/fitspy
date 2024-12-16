DELIMITER = "@"  # Used by Spectra/SpectraMap (in set_attributes) and main_controller.py (in save and load .fspy) to identify correct spectrum object as "map@fname"

from .utils import (
    replace_icon_colors,
    to_snake_case,
    to_title_case,
    get_icon_path,
    update_widget_palette,
    closest_item,
    closest_index,
    hsorted,
    fileparts,
    check_or_rename,
    load_from_json,
    save_to_json,
    load_models_from_txt,
    load_models_from_py,
    get_dim,
    get_reader_from_rsciio,
    get_x_data_from_rsciio,
    get_1d_profile,
    get_2d_map,
    eval_noise_amplitude,
    get_func_args,
    get_model_params,
)
from .baseline import BaseLine
from .spectrum import Spectrum
from .spectra import Spectra
from .spectra_map import SpectraMap
