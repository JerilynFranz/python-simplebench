"""Typed dictionaries for the V1 ExecutionEnvironment data structure."""
from typing import TypedDict

from .python_info_dict import PythonInfoData, PythonInfoDict


# --- For data used as INPUT (e.g., to `from_dict`) ---

class ExecutionEnvironmentData(TypedDict, total=True):
    """Typed dictionary for V1 ExecutionEnvironment data used as INPUT.

    :param PythonInfoData python: The Python info.
    """
    python: PythonInfoData


# --- For data used as OUTPUT (e.g., from `to_dict`) ---

class ExecutionEnvironmentDict(TypedDict, total=True):
    """Typed dictionary for the JSON representation of a V1 ExecutionEnvironment (OUTPUT).

    :param PythonInfoDict python: The Python info.
    """
    python: PythonInfoDict
