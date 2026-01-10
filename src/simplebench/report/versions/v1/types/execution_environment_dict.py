"""Typed dictionaries for the V1 ExecutionEnvironment data structure.

This module defines two distinct dictionary types for handling ExecutionEnvironment data/

    - `ExecutionEnvironmentData`: For use as INPUT (e.g., to `from_dict`).
    - `ExecutionEnvironmentDict`: For use as OUTPUT (e.g., from `to_dict`).

    These types ensure proper validation and serialization of ExecutionEnvironment data
"""
from simplebench.report._base.report_element_typed_dict import ReportElementTypedDict
from simplebench.types import Never, NotRequired, Required

from ._python_info_dict import PythonInfoData, PythonInfoDict

__all__ = [
    "ExecutionEnvironmentData",
    "ImmutableExecutionEnvironmentData",
    "ExecutionEnvironmentDict",
    "ImmutableExecutionEnvironmentDict",
]

# --- For data used as INPUT (e.g., to `from_dict`) ---

class ExecutionEnvironmentData(ReportElementTypedDict, total=True):
    """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

    :param Required[PythonInfoData] python_info: Information about the Python interpreter.
    """
    python_info: Required[PythonInfoData]


class ImmutableExecutionEnvironmentData(ExecutionEnvironmentData, total=False):
    """Immutable typed dictionary for V1 ExecutionEnvironment data used as INPUT.


    :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
    """
    __immutable__: NotRequired[Never]

# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ExecutionEnvironmentDict(ReportElementTypedDict, total=True):
    """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

    All fields are required (`total=True`), and their types are immutable.

    The type asserts to type checkers that all required fields are present and
    that all fields are of the correct immutable types, but cannot enforce
    immutability of the instance itself (Python limitation).

    :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
    """
    python_info: Required[PythonInfoDict]


class ImmutableExecutionEnvironmentDict(ExecutionEnvironmentDict, total=False):
    """Immutable typed dictionary for V1 ExecutionEnvironment data used as OUTPUT.

    :param Required[PythonInfoDict] python_info: Information about the Python interpreter.
    """
    __immutable__: NotRequired[Never]
