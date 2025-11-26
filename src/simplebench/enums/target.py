# -*- coding: utf-8 -*-
"""Target enums for SimpleBench."""

from enum import Enum

from .decorators import enum_docstrings


@enum_docstrings
class Target(str, Enum):
    """Categories for different output targets.

    The enums are used in generating calling parameters
    for the report() methods in the Reporter subclasses.

    Defined Targets are:
      - CONSOLE: Output to console.
      - FILESYSTEM: Output to filesystem.
      - CALLBACK: Pass generated output to a callback function.
      - CUSTOM: Output to a custom target.
      - NULL: No output.
    """
    CONSOLE = 'console'
    """Output to console."""
    FILESYSTEM = 'filesystem'
    """Output to filesystem."""
    CALLBACK = 'callback'
    """Pass generated output to a callback function."""
    CUSTOM = 'custom'
    """Output to a custom target."""
    NULL = 'null'
    """No output."""
    INVALID = 'invalid'
    """Invalid target. This is a testing placeholder and should not be used."""
