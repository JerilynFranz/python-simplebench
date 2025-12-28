"""V1 ExecutionEnvironment implementation."""
import hashlib

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.report.base import BaseExecutionEnvironment, Environment
from simplebench.report.versions.v1.python_info import PythonInfo
from simplebench.report.versions.v1.types import ExecutionEnvironmentData, ExecutionEnvironmentDict, PythonInfoData

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
        :raises SimpleBenchTypeError: If the python parameter is not of type PythonInfo.
        """
        self._hash_id: str = ''
        self._python = validate.python(python)

    @classmethod
    def from_dict(cls, data: ExecutionEnvironmentData) -> 'BaseExecutionEnvironment':
        """Create an ExecutionEnvironment instance from a dictionary.

        .. code-block:: python
           :caption: Example

           environment_info = ExecutionEnvironment.from_dict(data)

        :param data: The dictionary containing execution enviornment information.
        :return: A ExecutionEnvironment instance.
        """
        if not isinstance(data, dict):
            raise SimpleBenchTypeError(
                "data must be a dictionary",
                tag=_ExecutionEnvironmentErrorTag.INVALID_DATA_ARG_TYPE)
        if 'python' not in data:
            raise SimpleBenchTypeError(
                "data is missing required 'python' property",
                tag=_ExecutionEnvironmentErrorTag.MISSING_PYTHON_PROPERTY)
        python_data: PythonInfoData = data['python']
        if not isinstance(python_data, dict):
            raise SimpleBenchTypeError(
                "data is missing required 'python' property",
                tag=_ExecutionEnvironmentErrorTag.INVALID_PYTHON_PROPERTY_TYPE)
        python_info = PythonInfo.from_dict(python_data)
        return cls(python=python_info)

    def to_dict(self) -> ExecutionEnvironmentDict:
        """Convert the ExecutionEnvironment to a dictionary.

        :return ExecutionEnvironmentDict: A dictionary representation of the ExecutionEnvironment.
        """
        return ExecutionEnvironmentDict(
            python=self.python.to_dict()
        )

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

    @property
    def python(self) -> PythonInfo:
        """Get the Python property.

        :return: The Python info.
        """
        return self._python
