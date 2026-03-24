"""Generic environment module for report version 1."""
# ruff: noqa: F401

from .environment_info import EnvironmentInfo
from .environment_info_schema import EnvironmentInfoSchema
from .environoment_info_dict import (
    EnvironmentInfoData,
    EnvironmentInfoDict,
    ImmutableEnvironmentInfoData,
    ImmutableEnvironmentInfoDict,
)

__all__: list[str] = []
