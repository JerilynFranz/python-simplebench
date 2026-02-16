"""Factories for creating report v1 instances with dummy data for testing."""

from .cpu_info import cpu_info, cpu_info_data, cpu_info_kwargs
from .memory_info import (
    memory_info,
    memory_info_data,
    memory_info_kwargs,
    swap_memory_kwargs,
    swap_memory_object,
    swap_memory_object_dict,
    virtual_memory_kwargs,
    virtual_memory_object,
    virtual_memory_object_dict,
)
from .python_info import (
    no_hash_id_python_info_data,
    python_info,
    python_info_data,
    python_info_kwargs,
)
from .stats_block import (
    no_hash_id_stats_block_data,
    stats_block,
    stats_block_data,
    stats_block_kwargs,
    stats_block_measurements,
    stats_block_measurements_kwargs,
)
from .system_info import no_hash_id_system_info_data, system_info, system_info_data, system_info_kwargs
from .value_block import no_hash_id_value_block_data, value_block, value_block_data, value_block_kwargs
from .vcs_info import no_hash_id_vcs_info_data, vcs_info, vcs_info_data, vcs_info_kwargs

__all__: list[str] = [
    "cpu_info",
    "cpu_info_data",
    "cpu_info_kwargs",
    "memory_info",
    "memory_info_kwargs",
    "swap_memory_kwargs",
    "swap_memory_object",
    "swap_memory_object_dict",
    "virtual_memory_kwargs",
    "virtual_memory_object",
    "virtual_memory_object_dict",
    "memory_info_data",
    "python_info",
    "python_info_data",
    "python_info_kwargs",
    "no_hash_id_python_info_data",
    "stats_block",
    "stats_block_data",
    "stats_block_kwargs",
    "stats_block_measurements",
    "no_hash_id_stats_block_data",
    "stats_block_measurements_kwargs",
    "system_info",
    "system_info_data",
    "system_info_kwargs",
    "no_hash_id_system_info_data",
    "value_block",
    "value_block_data",
    "value_block_kwargs",
    "no_hash_id_value_block_data",
    "vcs_info",
    "vcs_info_data",
    "vcs_info_kwargs",
    "no_hash_id_vcs_info_data",
]
