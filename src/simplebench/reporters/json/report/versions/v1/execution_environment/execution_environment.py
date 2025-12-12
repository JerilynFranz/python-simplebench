"""V1 ExecutionEnvironment implementation."""
import hashlib
from typing import Any

from simplebench.reporters.json.report.base import ExecutionEnvironment as BaseExecutionEnvironment
from simplebench.reporters.json.report.base import PythonInfo
from simplebench.reporters.json.report.exceptions import _ExecutionEnvironmentErrorTag
from simplebench.reporters.json.report.protocols import Environment
from simplebench.validators import validate_type

from ..python_info import PythonInfo as PythonInfoV1


class ExecutionEnvironment(BaseExecutionEnvironment):
    """Implementation of the ExecutionEnvironment interface for V1."""

    ALLOWED_ENVIRONMENTS: dict[str, type[Environment]] = {
        'python': PythonInfoV1,
    }

    def __init__(self, python: PythonInfo) -> None:
        """Initialize the ExecutionEnvironment with Python info.

        In the V1 implementation, the python parameter is required and must be of
        type PythonInfo.

        :param python: The Python info.
        :raises TypeError: If the python parameter is not of type PythonInfo.
        """
        self._hash_id: str = ''
        self.python = python

    @property
    def python(self) -> PythonInfo:
        """Get the Python property.

        :return: The Python info.
        """
        return self._python

    @python.setter
    def python(self, value: PythonInfo) -> None:
        """Set the Python property.

        :param value: The Python info to set.
        """
        self._python = validate_type(
            value, PythonInfo, "python",
            _ExecutionEnvironmentErrorTag.INVALID_PYTHON_PROPERTY_TYPE)

    def to_dict(self) -> dict[str, dict[str, Any]]:
        """Convert the ExecutionEnvironment to a dictionary.

        :return: A dictionary representation of the ExecutionEnvironment.
        """
        return {
            'python': self.python.to_dict(),
        }

    @property
    def hash_id(self) -> str:
        """Get the hash_id property.

        :return: The hash_id string.
        """
        if self._hash_id == '':
            hash_input = (
                f"python:{self.python.hash_id}"
            ).encode('utf-8')
            self._hash_id = hashlib.sha256(hash_input).hexdigest()
        return self._hash_id
