"""Execution environment for the MachineInfo class."""
# ruff: noqa: F401

from .execution_environment import ExecutionEnvironment
from .known_environments import KNOWN_ENVIRONMENTS
from .typeddict_types import (
    ExecutionEnvironmentData,
    ExecutionEnvironmentDict,
    ImmutableExecutionEnvironmentData,
    ImmutableExecutionEnvironmentDict,
)

__all__ = []
