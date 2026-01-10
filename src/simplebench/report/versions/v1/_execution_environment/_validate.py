"""Validate execution environment data for version 1."""
from collections.abc import Mapping
from types import MappingProxyType

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._base import Environment
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.types import CoreDataMappingType, ImmutableCoreDataMappingType
from simplebench.validators import validate_core_data_mapping, validate_type

from ._known_environments import KNOWN_ENVIRONMENTS

__all__ = [
    "environments",
]


def environments(value: Mapping[str, object]) -> MappingProxyType[str, Environment | CoreDataMappingType]:
    """Validate the execution environments dictionary.

    Each key in the dictionary represents an execution environment name,
    and each value must be either a :class:`Environment` instance or a :class:`CoreDataMappingType`
    conforming instance.

    Environments that have a name that is recognized as a known environment (e.g. 'python')
    will be validated as their known type. Environments that are not recognized will be
    validated against :class:`CoreDataMappingType` or :class:`Environment`.

    The returned dictionary of environments is deeply immutable.

    :param value: The value to validate.
    :return MappingProxyType[str, Environment | CoreDataMappingType]: The validated execution environments dictionary.
    :raises SimpleBenchTypeError: If the value is not a valid execution environments dictionary.
    """
    validate_type(value, Mapping, 'Execution environments',
                  _ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENTS_TYPE)

    validated_envs: dict[str, Environment | ImmutableCoreDataMappingType] = {}
    n_environments: int = 0
    for env_name, env_value in value.items():
        if env_name in KNOWN_ENVIRONMENTS:
            if not isinstance(env_value, Environment):  # Verify known envs are Environment instances
                raise SimpleBenchTypeError(
                    f"Known environment '{env_name}' must be of type Environment",
                    tag=_ExecutionEnvironmentErrorTag.BAD_KNOWN_ENVIRONMENT_TYPE)
            expected_type = KNOWN_ENVIRONMENTS[env_name]
            if not isinstance(env_value, expected_type):
                raise SimpleBenchTypeError(
                    f"Environment '{env_name}' must be of type {expected_type.__name__}",
                    tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_TYPE)
            validated_envs[env_name] = env_value
        elif isinstance(env_value, Environment):
            validated_envs[env_name] = env_value
        else:
            env = validate_core_data_mapping(env_value, f"Environment '{env_name}'", max_depth=5)
            validated_envs[env_name] = env

        n_environments += 1
    if n_environments == 0:
        raise SimpleBenchValueError(
            "At least one execution environment must be provided",
            tag=_ExecutionEnvironmentErrorTag.NO_ENVIRONMENTS_PROVIDED)
    return MappingProxyType(validated_envs)
