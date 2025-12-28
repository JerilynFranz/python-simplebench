"""Validate execution environment data for version 1."""
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.validators import validate_type

from ..python_info import PythonInfo


def python(value: PythonInfo) -> PythonInfo:
    """Validate that the provided value is a PythonInfo instance.

    :param value: The value to validate.
    :return PythonInfo: The validated PythonInfo instance.
    :raises SimpleBenchTypeError: If the value is not a PythonInfo instance.
    """
    return validate_type(
        value, PythonInfo, "python",
        _ExecutionEnvironmentErrorTag.INVALID_PYTHON_PROPERTY_TYPE)
