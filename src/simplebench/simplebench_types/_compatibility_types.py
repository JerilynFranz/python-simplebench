"""TypedDict related type hints.

This module provides imports for `Required`, `NotRequired`, `Never`, `ReadOnly` to
be used in defining `TypedDict` types,and `Self` for use in class methods.

These types are conditionally imported from either typing or typing_extensions
based on feature detection.

The import is centralized here to reduce boilerplate code for versioned imports, maintain consistency
across the codebase, and to simplify future updates.

See Also:
    - :class:`Required`: Indicates that a key in a `TypedDict` is required.
    - :class:`NotRequired`: Indicates that a key in a `TypedDict` is optional.
    - :class:`ReadOnly`: Indicates that a key in a `TypedDict` is read-only
    - :class:`Never`: Indicates a key in a `TypedDict` that should never be present.
    - :class:`Self`: Indicates the instance type in class methods.
"""
# ruff: noqa: F401

import sys

if sys.version_info >= (3, 11):
    from typing import Never, NotRequired, Required, Self
else:
    from typing_extensions import Never, NotRequired, Required, Self

if sys.version_info >= (3, 13):
    from typing import ReadOnly

else:
    from typing_extensions import ReadOnly

# No * exports from this module
__all__: list[str] = []
