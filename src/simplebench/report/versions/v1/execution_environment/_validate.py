"""Validate execution environment data for version 1."""

import re
from collections.abc import Mapping

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.report._error_tags import _ExecutionEnvironmentErrorTag
from simplebench.report.versions import v1 as report

from ..environment_info import EnvironmentInfo

__all__: list[str] = []


_ENV_NAME_REGEX: re.Pattern[str] = re.compile(r'^[a-zA-Z](?:[a-zA-Z0-9_-]*[a-zA-Z0-9])?$')
"""Regular expression for validating environment names."""


def environments(value: Mapping[str, object]) -> dict[str, report.EnvironmentInfo]:
    """Validate the execution environments dictionary.

    Each key in the dictionary represents an execution environment name,
    and each value must be either a :class:`Environment` instance or a :class:`CoreDataMappingType`
    conforming instance.

    Environments that have a name that is recognized as a known environment (e.g. 'python')
    will be validated as their known type. Environments that are not recognized will be
    converted to a :class:`Environment` if they are provided as a :class:`CoreDataMappingType`
    compatible data structure.

    The returned dictionary of environments is a shallow copy of the input dictionary with all
    values converted to :class:`Environment` instances as necessary. The input dictionary is not modified.

    :param value: The value to validate.
    :return dict[str, report.Environment]: The validated execution environments dictionary.
    :raises SimpleBenchTypeError: If the value is not a valid execution environments dictionary.
    """
    if not isinstance(value, Mapping):
        raise SimpleBenchTypeError(
            'Execution environments must be a mapping of environment name to environment data',
            tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENTS_TYPE,
        )

    validated_envs: dict[str, report.EnvironmentInfo] = {}
    for env_name, env_data in value.items():
        if not isinstance(env_name, str):
            raise SimpleBenchTypeError(
                f'Environment name {env_name!r} is not a string',
                tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_NAME_TYPE,
            )
        if not _ENV_NAME_REGEX.match(env_name):
            raise SimpleBenchTypeError(
                f'Environment name {env_name!r} is not valid. It must match the regex '
                f'{_ENV_NAME_REGEX.pattern!r}',
                tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_NAME_VALUE,
            )
        if not isinstance(env_data, EnvironmentInfo):
           raise SimpleBenchTypeError(
                f'Data for environment {env_name!r} is not '
                f'an Environment instance: {type(env_data).__name__!r}',
                tag=_ExecutionEnvironmentErrorTag.INVALID_ENVIRONMENT_VALUE_TYPE)
        validated_envs[env_name] = env_data
    return validated_envs
