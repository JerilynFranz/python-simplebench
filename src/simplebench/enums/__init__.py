"""Public API for enums.

Enumarations used throughout SimpleBench.

Provides
--------
- :class:`Color`
- :class:`ExitCode`
- :class:`FlagType`
- :class:`Format`
- :class:`Section`
- :class:`Target`
- :class:`Verbosity`
- :func:`enum_docstrings`

"""
from .color import Color
from .decorators import enum_docstrings
from .exit_code import ExitCode
from .flag_type import FlagType
from .format import Format
from .section import Section
from .target import Target
from .verbosity import Verbosity

__all__ = [
    'Color',
    'ExitCode',
    'FlagType',
    'Format',
    'Section',
    'Target',
    'Verbosity',
    'enum_docstrings',
]
