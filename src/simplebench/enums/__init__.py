"""Public API for enums.

Enumarations used throughout SimpleBench.

Provides
--------
- :class:`Color`
- :class:`ExitCode`
- :class:`FlagType`
- :class:`Format`
- :class:`Target`
- :class:`Verbosity`

"""
from .color import Color
from .exit_code import ExitCode
from .flag_type import FlagType
from .format import Format
from .target import Target
from .verbosity import Verbosity

__all__ = [
    'Color',
    'ExitCode',
    'FlagType',
    'Format',
    'Target',
    'Verbosity',
]
