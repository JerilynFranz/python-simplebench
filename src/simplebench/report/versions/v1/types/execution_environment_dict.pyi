"""Typed dictionaries for the V1 ExecutionEnvironment data structure.

(type stub version)

This is the type stub version of the type definitions for V1 ExecutionEnvironment data.

There are two versions (.pyi and .py) to accommodate different versions
of Python supporting different features in TypedDicts.

If you edit one of these files, please remember to update the other to
match.

The files are otherwise identical in structure and content.

This module defines two distinct dictionary types for handling ExecutionEnvironment data/

    - `ExecutionEnvironmentData`: For use as INPUT (e.g., to `from_dict`).
    - `ExecutionEnvironmentDict`: For use as OUTPUT (e.g., from `to_dict`).

    These types ensure proper validation and serialization of ExecutionEnvironment data
"""
import sys
from typing import Required, TypedDict

from .python_info_dict import PythonInfoData, PythonInfoDict

# --- For data used as INPUT (e.g., to `from_dict`) ---

if sys.version_info >= (3, 12):
    class ExecutionEnvironmentData(TypedDict, total=False, closed=True):
        """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

        .. note::
            This TypedDict uses `closed=True`, which is only supported in Python 3.12 and
            later. To maintain compatibility with earlier versions, an alternative
            definition without `closed=True` is provided automatically to older Python
            versions.

        :param Required[PythonInfoData] python_info: Information about the Python interpreter.
        """
        python: Required[PythonInfoData]

else:  # For Python versions < 3.12 where closed=True is not supported
    class ExecutionEnvironmentData(TypedDict, total=False):
        """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

        .. note::
            No additional fields are allowed beyond those defined here but
            `closed=True` is not being enforced due to Python version limitations
            before Python 3.12.

        :param Required[PythonInfoData] python_info: Information about the Python interpreter.
        """
        python: Required[PythonInfoData]


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

if sys.version_info >= (3, 12):
    class ExecutionEnvironmentDict(TypedDict, total=True, closed=True):
        """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

        All fields are required (`total=True`), and their types are immutable.
        No additional fields are allowed beyond those defined here (`closed=True`).

        .. note::
            This TypedDict uses `closed=True`, which is only supported in Python 3.12 and later.
            An alternative definition without `closed=True`is also provided automatically
            to older Python versions for compatibility.

        The type asserts to type checkers that all required fields are present and
        that all fields are of the correct immutable types, but cannot enforce
        immutability of the instance itself (Python limitation).

        :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
        """
        python: Required[PythonInfoDict]

else:  # For Python versions < 3.12 where closed=True is not supported
    class ExecutionEnvironmentDict(TypedDict, total=True):
        """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

        All fields are required (`total=True`), and their types are immutable.
        No additional fields are allowed beyond those defined here (`closed=True`).

        .. note::
            No additional fields are allowed beyond those defined here but
            `closed=True` is not being enforced due to Python version limitations
            before Python 3.12.

        The type asserts to type checkers that all required fields are present and
        that all fields are of the correct immutable types, but cannot enforce
        immutability of the instance itself (Python limitation).

        :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
        """
        python: Required[PythonInfoDict]
