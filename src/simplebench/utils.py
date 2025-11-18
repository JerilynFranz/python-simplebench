# -*- coding: utf-8 -*-
"""Utility functions"""
import itertools
import math
import platform
import re
import sys
from argparse import Namespace
from functools import cache
from typing import Any, Sequence, TypedDict, TypeVar

from cpuinfo import get_cpu_info  # type: ignore[import-untyped]

from .defaults import DEFAULT_SIGNIFICANT_FIGURES
from .exceptions import SimpleBenchTypeError, SimpleBenchValueError, UtilsErrorTag

T = TypeVar('T')


class MachineInfo(TypedDict):
    """TypedDict for machine info returned by :func:`get_machine_info`.

    :ivar node: Computer's network name.
    :vartype node: str
    :ivar processor: Processor name.
    :vartype processor: str
    :ivar machine: Machine type.
    :vartype machine: str
    :ivar python_compiler: Python compiler used.
    :vartype python_compiler: str
    :ivar python_implementation: Python implementation name.
    :vartype python_implementation: str
    :ivar python_implementation_version: Python implementation version.
    :vartype python_implementation_version: str
    :ivar python_version: Python version.
    :vartype python_version: str
    :ivar python_build: Python build information.
    :vartype python_build: tuple[str, str]
    :ivar release: Operating system release.
    :vartype release: str
    :ivar system: Operating system name.
    :vartype system: str
    :ivar cpu: CPU information.
    :vartype cpu: dict[str, str]
    """
    node: str
    processor: str
    machine: str
    python_compiler: str
    python_implementation: str
    python_implementation_version: str
    python_version: str
    python_build: tuple[str, str]
    release: str
    system: str
    cpu: dict[str, str]


def python_implementation_version() -> str:
    """Return the Python implementation version.

    For CPython, this is the same as :func:`platform.python_version`.
    For PyPy, this is the PyPy version (e.g., '7.3.5').

    :return: The Python implementation version.
    :rtype: str
    """
    python_implementation: str = platform.python_implementation()
    py_implementation_version: str = platform.python_version()
    if python_implementation == 'PyPy':
        version_info = getattr(sys, 'pypy_version_info', None)
        if version_info is not None:
            py_implementation_version = (
                f'{version_info.major:d}.{version_info.minor:d}.{version_info.micro:d}'
                f'-{version_info.releaselevel:d}{version_info.serial:d}')
        else:
            py_implementation_version = 'unknown'
    return py_implementation_version


@cache
def get_machine_info() -> MachineInfo:
    """Return a dictionary of information about the current machine and Python version."""
    python_implementation = platform.python_implementation()
    machine_info: MachineInfo = {
        'node': platform.node(),
        'processor': platform.processor(),
        'machine': platform.machine(),
        'python_compiler': platform.python_compiler(),
        'python_implementation': python_implementation,
        'python_implementation_version': python_implementation_version(),
        'python_version': platform.python_version(),
        'python_build': platform.python_build(),
        'release': platform.release(),
        'system': platform.system(),
        'cpu': get_cpu_info(),
    }
    return machine_info


def platform_id() -> str:
    """Return a string that uniquely identifies the current machine and Python version.

    The platform ID is a lowercase string that combines the operating system, Python implementation,
    Python version, and architecture.

    :return: The platform ID.
    :rtype: str
    """
    return '{system}-{python_impl}-{python_version}-{arch}'.format(  # pylint: disable=consider-using-f-string
          system=platform.system(),
          python_impl=platform.python_implementation(),
          python_version='.'.join(platform.python_version_tuple()[:2]),
          arch=platform.architecture()[0]).lower().replace(' ', '')


# Finds all characters that are not a-z, A-Z, 0-9, _ (underline), or - (dash)
_SANITIZE_FILENAME_RE = re.compile(r'[^-a-zA-Z0-9_]+')


def sanitize_filename(name: str) -> str:
    """Sanitizes a filename by replacing invalid characters with _ (underline).

    Only a-z, A-Z, 0-9, _  (underline), and - (dash) characters are allowed. All other
    characters are replaced with _ and multiple sequential _ characters are then
    collapsed to single _ characters. Leading and trailing _ and - characters are removed.

    :param name: The filename to sanitize.
    :type name: str
    :return: The sanitized filename.
    :rtype: str
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            "name arg must be a str",
            tag=UtilsErrorTag.SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE)
    if name == '':
        raise SimpleBenchValueError(
            "name arg must not be an empty string",
            tag=UtilsErrorTag.SANITIZE_FILENAME_EMPTY_NAME_ARG)
    first_pass: str = re.sub(_SANITIZE_FILENAME_RE, '_', name)
    second_pass: str = first_pass.strip('_-')
    return re.sub(r'_+', '_', second_pass)


def sigfigs(number: float, figures: int = DEFAULT_SIGNIFICANT_FIGURES) -> float:
    """Rounds a floating point number to the specified number of significant figures.

    If the number of significant figures is not specified, it defaults to
    :data:`~.defaults.DEFAULT_SIGNIFICANT_FIGURES`.

    * 14.2 to 2 digits of significant figures becomes 14
    * 0.234 to 2 digits of significant figures becomes 0.23
    * 0.0234 to 2 digits of significant figures becomes 0.023
    * 14.5 to 2 digits of significant figures becomes 15
    * 0.235 to 2 digits of significant figures becomes 0.24

    :param number: The number to round.
    :type number: float
    :param figures: The number of significant figures to round to.
    :type figures: int
    :raises TypeError: If the ``number`` arg is not a float or the ``figures`` arg is not an int.
    :raises ValueError: If the ``figures`` arg is not at least 1.
    :return: The rounded number as a float.
    :rtype: float
    """
    if not isinstance(number, float):
        raise SimpleBenchTypeError(
            "number arg must be a float",
            tag=UtilsErrorTag.SIGFIGS_INVALID_NUMBER_ARG_TYPE)
    if not isinstance(figures, int):
        raise SimpleBenchTypeError(
            "figures arg must be an int",
            tag=UtilsErrorTag.SIGFIGS_INVALID_FIGURES_ARG_TYPE)
    if figures < 1:
        raise SimpleBenchValueError(
            "figures arg must be at least 1",
            tag=UtilsErrorTag.SIGFIGS_INVALID_FIGURES_ARG_VALUE)

    if number == 0.0:
        return 0.0
    return round(number, figures - int(math.floor(math.log10(abs(number)))) - 1)


def kwargs_variations(kwargs: dict[str, Sequence[Any]]) -> list[dict[str, Any]]:
    '''Variations of keyword arguments for the benchmark.

    This function takes a dictionary where each key is a keyword argument name
    and the value is a Sequence of possible values for that argument. It returns a list
    of dictionaries, each dictionary representing a unique combination of keyword arguments and
    their values.

    Example:

    .. code-block:: python

        kwargs_variations({
            'arg1': [1, 2],
            'arg2': ['a', 'b']
        })
        # output:
        # [
        #     {'arg1': 1, 'arg2': 'a'},
        #     {'arg1': 1, 'arg2': 'b'},
        #     {'arg1': 2, 'arg2': 'a'},
        #     {'arg1': 2, 'arg2': 'b'}
        # ]

    :param kwargs: A dictionary of keyword arguments and their possible values.
        The value must be a Sequence (e.g., list, tuple, set), but not a str or bytes instance.
    :type kwargs: dict[str, Sequence[Any]]
    :return: A list of dictionaries, each representing a unique combination of keyword arguments and values.
    :rtype: list[dict[str, Any]]
    '''
    if not isinstance(kwargs, dict):
        raise SimpleBenchTypeError(
            "kwargs arg must be a dict or dict sub-class",
            tag=UtilsErrorTag.KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE
        )
    for key, value in kwargs.items():
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            raise SimpleBenchTypeError(
                ("kwargs arg values must be a Sequence (not str or bytes); "
                 f"key '{key}' has invalid value type {type(value)}"),
                tag=UtilsErrorTag.KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE
            )

    keys = kwargs.keys()
    if not keys:
        return [{}]
    values = [kwargs[key] for key in keys]
    return [dict(zip(keys, v)) for v in itertools.product(*values)]


def flag_to_arg(flag: str) -> str:
    """Convert a command-line flag to a valid Python argument name.

    This function takes a command-line flag (e.g., '--my-flag') and converts it
    to a valid Python argument name (e.g., 'my_flag') as expected in a :class:`~argparse.Namespace`
    result by removing leading dashes and replacing hyphens with underscores.

    :param flag: The command-line flag to convert.
    :type flag: str
    :raises SimpleBenchTypeError: If the ``flag`` arg is not a str.
    :raises SimpleBenchValueError: If the ``flag`` arg is an empty string or does not start with '--'.
    :return: The corresponding Python argument name.
    :rtype: str
    """
    if not isinstance(flag, str):
        raise SimpleBenchTypeError(
            "flag arg must be a str",
            tag=UtilsErrorTag.FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE)
    if flag == '':
        raise SimpleBenchValueError(
            "flag arg must not be an empty string",
            tag=UtilsErrorTag.FLAG_TO_ARG_EMPTY_FLAG_ARG)
    if not (flag.startswith('--') and len(flag) > 2):
        raise SimpleBenchValueError(
            "flag arg must start with '--' and have additional characters",
            tag=UtilsErrorTag.FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE)

    arg_name: str = flag.replace('--', '', 1).replace('-', '_')
    return arg_name


def arg_to_flag(arg: str) -> str:
    """Convert a Python argument name to a command-line flag.

    This function takes a Python argument name (e.g., 'my_flag') and converts it
    to a command-line flag (e.g., '--my-flag') by adding leading dashes and
    replacing underscores with hyphens.

    :param arg: The Python argument name to convert.
    :type arg: str
    :raises SimpleBenchTypeError: If the ``arg`` argument is not a str.
    :raises SimpleBenchValueError: If the ``arg`` argument is an empty string.
    :return: The corresponding command-line flag.
    :rtype: str
    """
    if not isinstance(arg, str):
        raise SimpleBenchTypeError(
            "arg arg must be a str",
            tag=UtilsErrorTag.ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE)
    if arg == '':
        raise SimpleBenchValueError(
            "arg arg must not be an empty string",
            tag=UtilsErrorTag.ARG_TO_FLAG_EMPTY_FLAG_ARG)

    flag_name: str = '--' + arg.replace('_', '-')

    return flag_name


NO_ATTRIBUTE = object()


def collect_arg_list(*, args: Namespace, flag: str) -> list[str]:
    """Collects a list of argument values from a Namespace for a given flag.

    This function retrieves the values associated with the specified flag from
    the provided :class:`~argparse.Namespace` object. If the value is a sequence (excluding str and bytes),
    it returns the values as a list. If the value is a single item, it returns a list
    containing that single item. If the flag does not exist in the Namespace,
    it returns an empty list.

    argparse lists consist of lists of lists of strings and so they have to be flattened
    to be processed.

    :param args: The :class:`~argparse.Namespace` object containing argument values.
    :type args: Namespace
    :param flag: The command-line flag whose value is to be collected.
    :type flag: str
    :raises SimpleBenchTypeError: If the ``args`` argument is not a :class:`~argparse.Namespace` or
        if the retrieved argument value is of an unexpected type.
    :return: A list of unique argument values associated with the specified flag.
    :rtype: list[str]
    """
    if not isinstance(args, Namespace):
        raise SimpleBenchTypeError(
            "args arg must be an argparse.Namespace instance",
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE)

    if not isinstance(flag, str):
        raise SimpleBenchTypeError(
            "flag arg must be a str",
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE)

    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise SimpleBenchValueError((
            "flag arg contains invalid characters for a command-line flag. "
            "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
            "and periods are allowed after the prefix."),
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE)

    arg_name = flag_to_arg(flag)
    arg_value = getattr(args, arg_name, NO_ATTRIBUTE)

    if arg_value is NO_ATTRIBUTE:
        return []

    # flatten the argparse list of lists structure
    intermediate_values: set[str] = set()
    if isinstance(arg_value, Sequence) and not isinstance(arg_value, (str, bytes)):
        for item in arg_value:
            if isinstance(item, str):
                intermediate_values.add(item)
            elif isinstance(item, Sequence) and all(isinstance(subitem, str) for subitem in item):
                intermediate_values.update(item)
            else:
                raise SimpleBenchTypeError(
                    "Argument value items must be str or sequence of str",
                    tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE)
    else:
        raise SimpleBenchTypeError(
            f"Argument value must be a Sequence (but not str or bytes): found: {arg_value} ",
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE)

    return list(intermediate_values)


def first_not_none(items: Sequence[T]) -> T | None:
    """Return the first not None element from a sequence of items. If all are None, return None.

    This utility method is used to prioritize non-None values when determining
    configuration settings, such as default options or targets.

    :param items: The sequence of items to check.
    :type items: Sequence[T]
    :return: The first not None element from items, or None if all are None.
    :rtype: T or None
    """
    for element in items:
        if element is not None:
            return element
    return None
