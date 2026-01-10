"""V1 ExecutionEnvironment implementation."""
import hashlib
from collections.abc import Mapping
from types import MappingProxyType

from typechecked import isinstance_of_typehint

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._base import BaseExecutionEnvironment, Environment
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.report.versions.v1._python_info import PythonInfo
from simplebench.types import CoreDataMappingType, ImmutableCoreDataMappingType
from simplebench.validators import validate_core_data_mapping

from . import _validate
from ._known_environments import KNOWN_ENVIRONMENTS
from ._typeddict_types import (
    ExecutionEnvironmentData,
    ExecutionEnvironmentDict,
    ImmutableExecutionEnvironmentData,
    ImmutableExecutionEnvironmentDict,
    PythonInfoData,
)


class ExecutionEnvironment(BaseExecutionEnvironment):
    """Implementation of the ExecutionEnvironment interface for V1."""

    def __init__(self, **kwargs: CoreDataMappingType | Environment) -> None:
        """Initialize the ExecutionEnvironment with environment information.

        In the V1 implementation, the python parameter is the only pre-defined
        environment and must be of type PythonInfo. Additional environments can be
        provided as keyword arguments and must conform to the CoreDataMappingType.

        At least one environment must be provided.

        :param PythonInfo python: (optional) The Python info.
        :param CoreDataMappingType | Environment kwargs: (optional) Other execution
            environments as keyword arguments.
        :raises SimpleBenchTypeError: If a passed environment is of an incorrect type.
        """
        self._hash_id: str = ''
        self._environments: MappingProxyType[
            str, Environment | CoreDataMappingType] = _validate.environments(dict(kwargs))

    @classmethod
    def from_dict(cls, data: Mapping[str, CoreDataMappingType]) -> 'ExecutionEnvironment':
        """Create an ExecutionEnvironment instance from a dictionary.

        .. code-block:: python
           :caption: Example

           environment_info = ExecutionEnvironment.from_dict(data)

        :param data: The dictionary containing execution environment information.
        :return: A ExecutionEnvironment instance.
        """
        imported_environments: dict[str, ImmutableCoreDataMappingType | Environment] = {}
        for env_name, env_value in data.items():
            if env_name in KNOWN_ENVIRONMENTS:
                environment: type[Environment] = KNOWN_ENVIRONMENTS[env_name]
                imported_instance = environment.from_dict(env_value)
                imported_environments[env_name] = imported_instance
            else:
                imported_environments[env_name] = validate_core_data_mapping(
                    env_value, f"Environment '{env_name}'", max_depth=5)
        return cls(**imported_environments)


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
    def python(self) -> PythonInfo:
        """Get the Python property.

        :return: The Python info.
        """
        return self._python
