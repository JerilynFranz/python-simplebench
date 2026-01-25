"""Types used by SimpleBench for variations"""
from collections.abc import Mapping
from types import MappingProxyType
from typing import TypeAlias

VariationColsType: TypeAlias = Mapping[str, str]
"""Type alias for variation columns used in SimpleBench."""

ImmutableVariationColsType: TypeAlias = MappingProxyType[str, str]
"""Type alias for immutable variation columns used in SimpleBench."""

VariationMarksType: TypeAlias = Mapping[str, str]
"""Type alias for variation marks used in SimpleBench."""

ImmutableVariationMarksType: TypeAlias = MappingProxyType[str, str]
"""Type alias for immutable variation marks used in SimpleBench."""
