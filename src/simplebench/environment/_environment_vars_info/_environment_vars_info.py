"""Contains the EnvironmentVarsInfo class, which provides information about environment variables."""
import os
from collections.abc import Iterable, Sequence, Set

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataMapping

from ._error_tags import _EnvironmentVarsInfoErrorTag


class EnvironmentVarsInfo(CoreDataMapping[str]):
    """Provides information about environment variables."""

    def __init__(self, __vars: Set[str] | Sequence[str] | Iterable[str]) -> None:
        """Initializes the EnvironmentVarsInfo instance.

        Takes a set, sequence, or iterable of environment variable names and retrieves
        their values from the environment, creating a mapping of variable names to their
        corresponding values. If a variable is not set in the environment,
        the environment, the variable will be excluded from the mapping.

        EnvironmentVarsInfo is a subclass of CoreDataMapping, which means it behaves
        like a mapping (dictionary) where the keys are the environment variable names
        and the values are their corresponding values.

        It is immutable, so once an instance is created, the environment variable information it contains
        cannot be modified.

        Example:

        .. code-block:: python
            env_info = EnvironmentVarsInfo(['HOME', 'PATH', 'SHELL'])

        :param __vars: A set, sequence, or iterable of environment variable names to retrieve information for.
        :type __vars: Set[str] | Sequence[str] | Iterable[str]
        :raises SimpleBenchTypeError: If the provided __vars is not a set, sequence, or iterable of strings, or
            if any of the keys are not strings.
        :raises SimpleBenchTypeError: If __vars is a string or bytes object, which is not a valid type
            for environment variables information.
        """
        if isinstance(__vars, (str, bytes)):
            raise SimpleBenchTypeError(
                "Expected a set, sequence, or iterable for environment variables information, "
                f"got {type(__vars).__name__}",
                tag=_EnvironmentVarsInfoErrorTag.INVALID_ENV_VARS_INFO_TYPE_STR_OR_BYTES,
            )
        if not isinstance(__vars, (Set, Sequence, Iterable)):
            raise SimpleBenchTypeError(
                "Expected a set, sequence, or iterable for environment variables information, "
                f"got {type(__vars).__name__}",
                tag=_EnvironmentVarsInfoErrorTag.INVALID_ENV_VARS_INFO_TYPE,
            )
        var_names = set(__vars)  # Capture to prevent loss of single pass iterables and ensure uniqueness
        if not all(isinstance(key, str) for key in var_names):
            raise SimpleBenchTypeError(
                "All environment variables keys must be strings",
                tag=_EnvironmentVarsInfoErrorTag.INVALID_ENV_VARS_INFO_KEY_TYPE,
            )
        env_vars: dict[str, str] = {}
        for var in var_names:
            var_value = os.environ.get(var)
            if var_value is not None:
                env_vars[var] = var_value
        super().__init__(env_vars)
