"""Typed dictionaries for the V1 ExecutionEnvironment data structure.

This module defines two distinct dictionary types for handling ExecutionEnvironment data/

    - `ExecutionEnvironmentData`: For use as INPUT (e.g., to `from_dict`).
    - `ExecutionEnvironmentDict`: For use as OUTPUT (e.g., from `to_dict`).

    These types ensure proper validation and serialization of ExecutionEnvironment data
"""
from typing import Required, TypedDict

from .python_info_dict import PythonInfoData, PythonInfoDict

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ExecutionEnvironmentData(TypedDict, total=False):
    """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

    :param Required[PythonInfoData] python_info: Information about the Python interpreter.
    """
    python_info: Required[PythonInfoData]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ExecutionEnvironmentDict(TypedDict, total=True):
    """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

    All fields are required (`total=True`), and their types are immutable.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
    """
    python_info: Required[PythonInfoDict]
