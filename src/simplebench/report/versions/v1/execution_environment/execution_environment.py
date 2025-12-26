"""V1 ExecutionEnvironment implementation."""
import hashlib
from typing import Any

from simplebench.report.base import ExecutionEnvironment as BaseExecutionEnvironment
from simplebench.report.protocols import Environment

from ..python_info import PythonInfo
from . import validate


class ExecutionEnvironment(BaseExecutionEnvironment):
    """Implementation of the ExecutionEnvironment interface for V1."""

    ALLOWED_ENVIRONMENTS: dict[str, type[Environment]] = {
        'python': PythonInfo,
    }

    def __init__(self, python: PythonInfo) -> None:
        """Initialize the ExecutionEnvironment with Python info.

        In the V1 implementation, the python parameter is required and must be of
        type PythonInfo.

        :param python: The Python info.
        :raises TypeError: If the python parameter is not of type PythonInfo.
        """
        self._hash_id: str = ''
        self._python = validate.python(python)

    @property
    def python(self) -> PythonInfo:
        """Get the Python property.

        :return: The Python info.
        """
        return self._python

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

        :return: A 64-character hexadecimal hash_id string.
        """
        if self._hash_id == '':
            hash_input = (
                f"python:{self.python.hash_id}"
            ).encode('utf-8')
            self._hash_id = hashlib.sha256(hash_input).hexdigest()
        return self._hash_id
