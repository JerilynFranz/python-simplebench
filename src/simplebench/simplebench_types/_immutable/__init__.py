"""Immutable type hint validation functions and protocols."""
from ._immutable import is_immutable, is_immutable_data_typehint, is_immutable_typeddict_typehint, validate_immutable
from ._protocol import Immutable, ImmutableTypedDict

__all__ = (
    "Immutable",
    "is_immutable",
    "is_immutable_data_typehint",
    "is_immutable_typeddict_typehint",
    "validate_immutable",
    "ImmutableTypedDict",
)
