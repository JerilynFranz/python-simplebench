"""Mapping of known execution environments for V1.

This module defines a dictionary that maps known execution environment names
to their corresponding Environment classes for version 1 reports.

:cvar KNOWN_ENVIRONMENTS: dict[str, type[Environment]]
    A mapping of known execution environment names to their corresponding
    Environment classes.

This mapping is used to validate and instantiate known execution environments
within the ExecutionEnvironment representation in MachineInfo objects while
preventing the accidental use of incorrect types for these known environments.
"""
from simplebench.report._base import Environment
from simplebench.report.versions.v1._python_info._python_info import PythonInfo

__all__ = [
    "KNOWN_ENVIRONMENTS",
]


KNOWN_ENVIRONMENTS: dict[str, type[Environment]] = { 'python': PythonInfo }
"""Mapping of known execution environments for V1 reports"""
