"""Public API for enums.

Enumarations used throughout SimpleBench.

Provides
--------
- :class:`Calibrate`: Calibration mode for simplebench.
- :class:`Color`: Color options for simplebench output.
- :class:`ExitCode`: Exit codes for simplebench.
- :class:`FlagType`: Type of command line flag for simplebench.
- :class:`Format`: Output format options for simplebench.
- :class:`Target`: Target options for simplebench.
- :class:`Verbosity`: Verbosity levels for simplebench output.

"""
# ruff: noqa: F401

from .calibrate import Calibrate
from .color import Color
from .exit_code import ExitCode
from .flag_type import FlagType
from .format import Format
from .target import Target
from .verbosity import Verbosity

__all__: list[str] = []
