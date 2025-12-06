"""Utility functions for simplebench."""
from .filenames import sanitize_filename
from .flags_and_args import arg_to_flag, collect_arg_list, flag_to_arg
from .kwargs_variations import kwargs_variations
from .machine_info import (
    MachineInfo,
    get_machine_info,
    platform_architecture,
    platform_id,
    platform_implementation,
    platform_machine,
    platform_processor,
    platform_system,
    platform_version,
    python_implementation_version,
)
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

    # machine_info.py
    'MachineInfo',
    'get_machine_info',
    'python_implementation_version',
    'platform_processor',
    'platform_machine',
    'platform_id',
    'platform_implementation',
    'platform_system',
    'platform_version',
    'platform_architecture',

    # significant_figures.py
    'sigfigs',

    # timestamp.py
    'timestamp_to_iso8601',
    'iso8601_to_timestamp',
]
