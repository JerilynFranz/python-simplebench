"""Mapping of known execution environments for V1.

This module defines a dictionary that maps known execution environment names
to their corresponding Environment classes for version 1 reports.

This mapping is used to validate and instantiate known execution environments
within the ExecutionEnvironment representation in MachineInfo objects while
preventing the accidental use of incorrect types for these known environments.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simplebench.report.versions.v1 import Environment

__all__: list[str] = []

# This function is defined here to avoid circular import issues, since the known environments
# may need to import types from the execution_environment module, and the execution_environment
# module needs to import this mapping.
