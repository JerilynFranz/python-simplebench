"""Factories for creating report v1 instances with dummy data for testing."""

from .cpu_info import report_cpu_info, report_cpu_info_data, report_cpu_info_kwargs
from .memory_info import (
    memory_info,
    memory_info_kwargs,
    swap_memory_kwargs,
    swap_memory_object,
    virtual_memory_kwargs,
    virtual_memory_object,
)
from .python_info import (
    no_hash_id_report_python_info_data,
    report_python_info,
    report_python_info_data,
    report_python_info_kwargs,
)

__all__: list[str] = [
    "report_cpu_info",
    "report_cpu_info_data",
    "report_cpu_info_kwargs",
    "memory_info",
    "memory_info_kwargs",
    "swap_memory_kwargs",
    "swap_memory_object",
    "virtual_memory_kwargs",
    "virtual_memory_object",
    "report_python_info",
    "report_python_info_data",
    "report_python_info_kwargs",
    "no_hash_id_report_python_info_data",
]
