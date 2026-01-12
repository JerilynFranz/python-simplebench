"""TypedDict related type hints.

This module provides imports for `Required`, `NotRequired`, `Never`,
and `ReadOnly` to be used in defining `TypedDict` types throughout SimpleBench.

These types are conditionally imported from either typing or typing_extensions
based on the Python version to ensure compatibility. The import is centralized
here to reduce boilerplate code for versioned imports, maintain consistency
across the codebase, and to simplify future updates.

See Also:
    - :class:`Required`: Indicates that a key in a `TypedDict` is required.
    - :class:`NotRequired`: Indicates that a key in a `TypedDict` is optional.
    - :class:`ReadOnly`: Indicates that a key in a `TypedDict` is read-only
    - :class:`Never`: Indicates a key in a `TypedDict` that should never be present.
"""

import sys

if sys.version_info >= (3, 11):
    from typing import Never, NotRequired, Required
else:
    from typing_extensions import Never, NotRequired, Required

if sys.version_info >= (3, 13):
    from typing import ReadOnly

else:
    from typing_extensions import ReadOnly

__all__ = ['Never', 'ReadOnly', 'NotRequired', 'Required']
