"""Utility functions for simplebench."""

from .filenames import sanitize_filename
from .flags_and_args import arg_to_flag, collect_arg_list, flag_to_arg
from .kwargs_variations import kwargs_variations
from .math import smallest_abs
from .serialization import serialize_to_dict_list_or_primitive, serialize_to_json
from .significant_figures import sigfigs
from .timestamp import iso8601_to_timestamp, timestamp_to_iso8601

__all__ = [
    # filenames.py
    'sanitize_filename',
    # flags_and_args.py
    'arg_to_flag',
    'flag_to_arg',
    'collect_arg_list',
    # kwargs_variations.py
    'kwargs_variations',
    # math.py
    'smallest_abs',
    # serialization.py
    'serialize_to_dict_list_or_primitive',
    'serialize_to_json',
    # significant_figures.py
    'sigfigs',
    # timestamp.py
    'timestamp_to_iso8601',
    'iso8601_to_timestamp',
]
