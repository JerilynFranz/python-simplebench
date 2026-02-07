"""Validate execution environment data for version 1."""

import re
from collections.abc import Mapping
from types import MappingProxyType

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.report.base import Environment
from simplebench.validators import validate_core_data_mapping

from ..generic_environment import GenericEnvironment
from .known_environments import KNOWN_ENVIRONMENTS

__all__: list[str] = []


_ENV_NAME_REGEX: re.Pattern[str] = re.compile(r'^[a-zA-Z](?:[a-zA-Z0-9_-]*[a-zA-Z0-9])?$')
"""Regular expression for validating environment names."""


def environments(value: Mapping[str, object]) -> MappingProxyType[str, Environment]:
    """Validate the execution environments dictionary.

    Each key in the dictionary represents an execution environment name,
    and each value must be either a :class:`Environment` instance or a :class:`CoreDataMappingType`
    conforming instance.

    Environments that have a name that is recognized as a known environment (e.g. 'python')
    will be validated as their known type. Environments that are not recognized will be
    converted to a :class:`GenericEnvironment` if they are provided as a :class:`CoreDataMappingType`
    compatible data structure.

    The returned dictionary of environments is deeply immutable.

    :param value: The value to validate.
    :return MappingProxyType[str, Environment]: The validated execution environments dictionary.
    :raises SimpleBenchTypeError: If the value is not a valid execution environments dictionary.
    """
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            'Execution environments must be a mapping of environment name to environment data',
            tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENTS_TYPE,
        )

    validated_envs: dict[str, Environment] = {}
    n_environments: int = 0
    for env_name, env_value in value.items():
        if not isinstance(env_name, str):
            raise SimpleBenchTypeError(
                f'Environment name {env_name!r} is not a string',
                tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_NAME_TYPE,
            )
        if not _ENV_NAME_REGEX.match(env_name):
            raise SimpleBenchValueError(
                f"Environment name '{env_name}' is invalid; must match regex {_ENV_NAME_REGEX.pattern!r}",
                tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_NAME_VALUE,
            )
        if env_name in KNOWN_ENVIRONMENTS:
            if not isinstance(env_value, Environment):  # Verify known envs are Environment instances
                raise SimpleBenchTypeError(
                    f"Known environment '{env_name}' must be of type Environment",
                    tag=_ExecutionEnvironmentErrorTag.BAD_KNOWN_ENVIRONMENT_TYPE,
                )
            expected_type = KNOWN_ENVIRONMENTS[env_name]
            if not isinstance(env_value, expected_type):
                raise SimpleBenchTypeError(
                    f"Environment '{env_name}' must be of type {expected_type.__name__}",
                    tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_TYPE,
                )
            validated_envs[env_name] = env_value
        elif isinstance(env_value, Environment):
            validated_envs[env_name] = env_value
        else:
            env_data = validate_core_data_mapping(env_value, f"Environment '{env_name}'")
            validated_envs[env_name] = GenericEnvironment(env_data)

        n_environments += 1
    if n_environments == 0:
        raise SimpleBenchValueError(
            'At least one execution environment must be provided',
            tag=_ExecutionEnvironmentErrorTag.NO_ENVIRONMENTS_PROVIDED,
        )
    return MappingProxyType(validated_envs)
