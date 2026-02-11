"""Factories for creating report v1 instances with dummy data for testing."""

from .cpu_info import report_cpu_info, report_cpu_info_data, report_cpu_info_kwargs
from .memory_info import (
    memory_info_factory,
    memory_info_kwargs_factory,
    swap_memory_kwargs,
    swap_memory_object_factory,
    virtual_memory_kwargs_factory,
    virtual_memory_object_factory,
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
    "memory_info_factory",
    "memory_info_kwargs_factory",
    "swap_memory_kwargs",
    "swap_memory_object_factory",
    "virtual_memory_kwargs_factory",
    "virtual_memory_object_factory",
    "report_python_info",
    "report_python_info_data",
    "report_python_info_kwargs",
    "no_hash_id_report_python_info_data",
]
