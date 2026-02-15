"""Mapping of known execution environments for V1.

This module defines a dictionary that maps known execution environment names
to their corresponding Environment classes for version 1 reports.

This mapping is used to validate and instantiate known execution environments
within the ExecutionEnvironment representation in MachineInfo objects while
preventing the accidental use of incorrect types for these known environments.
"""

from simplebench.report import base

__all__: list[str] = []

# This function is defined here to avoid circular import issues, since the known environments
# may need to import types from the execution_environment module, and the execution_environment
# module needs to import this mapping.

def known_environments() -> dict[str, type[base.Environment]]:
    """Get the mapping of known execution environment names to their corresponding Environment
    classes for V1 reports."""

    from simplebench.report.versions.v1 import Environment, PythonInfo
    return {
        'simplebench::python': PythonInfo,
        'simplebench::environment': Environment,
    }
