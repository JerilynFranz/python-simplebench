"""Special types used in simplebench.

The primary purpose of this module is to provide deferred imports
for core types like `Case` to avoid circular import issues during
module initialization while still allowing runtime type checks
like `isinstance()` and `issubclass()` to work correctly.

It can be used as follows:
    from simplebench.types import CaseType  # Lazy proxy for Case type

It provides the following exports:
    - `CaseType`: A lazy-loading proxy for the `Case` type that can be
      used in `isinstance()` and `issubclass()` checks.

"""
from .case_type_proxy import CaseTypeProxy, is_case
from .choice_type_proxy import ChoiceTypeProxy, is_choice
from .session_type_proxy import SessionTypeProxy, is_session

__all__ = [
    'CaseTypeProxy',
    'is_case',
    'ChoiceTypeProxy',
    'is_choice',
    'SessionTypeProxy',
    'is_session',
]
"""'*' imports for the simplebench.types module."""
