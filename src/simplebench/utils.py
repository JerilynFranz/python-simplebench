# -*- coding: utf-8 -*-
"""Utility functions"""
from argparse import Namespace
from functools import cache
import itertools
import math
import platform
import re
import sys
from typing import Any, Sequence, TypedDict

from cpuinfo import get_cpu_info  # type: ignore[import-untyped]

from .defaults import DEFAULT_SIGNIFICANT_FIGURES
from .exceptions import SimpleBenchValueError, SimpleBenchTypeError, UtilsErrorTag


class MachineInfo(TypedDict):
    """TypedDict for machine info returned by get_machine_info()."""
    node: str
    """Computer's network name."""
    processor: str
    """Processor name."""
    machine: str
    """Machine type."""
    python_compiler: str
    """Python compiler used."""
    python_implementation: str
    """Python implementation name."""
    python_implementation_version: str
    """Python implementation version."""
    python_version: str
    """Python version."""
    python_build: tuple[str, str]
    """Python build information."""
    release: str
    """Operating system release."""
    system: str
    """Operating system name."""
    cpu: dict[str, str]
    """CPU information."""


def python_implementation_version() -> str:
    """Return the Python implementation version.

    For CPython, this is the same as platform.python_version().
    For PyPy, this is the PyPy version (e.g., '7.3.5').

    Returns:
        str: The Python implementation version.
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

    Returns:
        str: The platform ID.
    """
    return '{system}-{python_impl}-{python_version}-{arch}'.format(  # pylint: disable=consider-using-f-string
          system=platform.system(),
          python_impl=platform.python_implementation(),
          python_version='.'.join(platform.python_version_tuple()[:2]),
          arch=platform.architecture()[0]).lower().replace(' ', '')


def sanitize_filename(name: str) -> str:
    """Sanitizes a filename by replacing invalid characters with _.

    Only 'a-z', 'A-Z', '0-9', '_', and '-' are allowed. All other characters
    are replaced with '_' and multiple sequential '_' characters are then collapsed to
    single '_' characters.

    Args:
        name (str): The filename to sanitize.

    Returns:
        str: The sanitized filename.
    """
    if not isinstance(name, str):
        raise SimpleBenchTypeError(
            "name arg must be a str",
            tag=UtilsErrorTag.SANITIZE_FILENAME_INVALID_NAME_ARG_TYPE)
    if name == '':
        raise SimpleBenchValueError(
            "name arg must not be an empty string",
            tag=UtilsErrorTag.SANITIZE_FILENAME_EMPTY_NAME_ARG)
    first_pass: str = re.sub(r'[^a-zA-Z0-9_-]+', '_', name)
    return re.sub(r'_+', '_', first_pass)


def sigfigs(number: float, figures: int = DEFAULT_SIGNIFICANT_FIGURES) -> float:
    """Rounds a floating point number to the specified number of significant figures.

    If the number of significant figures is not specified, it defaults to
    DEFAULT_SIGNIFICANT_FIGURES.

    * 14.2 to 2 digits of significant figures becomes 14
    * 0.234 to 2 digits of significant figures becomes 0.23
    * 0.0234 to 2 digits of significant figures becomes 0.023
    * 14.5 to 2 digits of significant figures becomes 15
    * 0.235 to 2 digits of significant figures becomes 0.24

    Args:
        number (float): The number to round.
        figures (int): The number of significant figures to round to.

    Returns:
        The rounded number as a float.

    Raises:
        TypeError: If the number arg is not a float or the figures arg is not an int.
        ValueError: If the figures arg is not at least 1.
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

    Example
    -------
    If the input is:
    {
        'arg1': [1, 2],
        'arg2': ['a', 'b']
    }
    The output will be:
    [
        {'arg1': 1, 'arg2': 'a'},
        {'arg1': 1, 'arg2': 'b'},
        {'arg1': 2, 'arg2': 'a'},
        {'arg1': 2, 'arg2': 'b'}
    ]

    Args:
        kwargs (dict[str, Sequence[Any]]): A dictionary of keyword arguments and their possible values.
        The value must be a Sequence (e.g., list, tuple, set), but not a str or bytes instance.

    Returns:
        A list of dictionaries, each representing a unique combination of keyword arguments and values.
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
    to a valid Python argument name (e.g., 'my_flag') as expected in a Namespace
    result by removing leading dashes and replacing hyphens with underscores.

    Args:
        flag (str): The command-line flag to convert.

    Returns:
        str: The corresponding Python argument name.

    Raises:
        SimpleBenchTypeError: If the flag arg is not a str.
        SimpleBenchValueError: If the flag arg is an empty string or does not start with '--'.
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

    Args:
        arg (str): The Python argument name to convert.

    Returns:
        str: The corresponding command-line flag.

    Raises:
        SimpleBenchTypeError: If the arg argument is not a str.
        SimpleBenchValueError: If the arg argument is an empty string.
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


def collect_arg_list(args: Namespace, flag: str, include_comma_separated: bool = True) -> list[str]:
    """Collects a list of argument values from a Namespace for a given flag.

    This function retrieves the value associated with the specified flag from
    the provided Namespace object. If the value is a sequence (excluding str and bytes),
    it returns the value as a list. If the value is a single item, it returns a list
    containing that single item. If the flag does not exist in the Namespace,
    it returns an empty list.

    argparse lists consist of lists of lists of strings and so they have to be flattened
    to be processed.

    If include_comma_separated is True , comma-separated strings are split into multiple values.

    Args:
        args (Namespace): The Namespace object containing argument values.
        flag (str): The command-line flag whose value is to be collected.
        include_comma_separated (bool): If True, splits comma-separated strings
                into multiple values.

    Returns:
        list[str]: A list of unique argument values associated with the specified flag.

    Raises:
        SimpleBenchTypeError: If the args argument is not a Namespace or
                              if the retrieved argument value is of an unexpected type.
    """
    if not isinstance(args, Namespace):
        raise SimpleBenchTypeError(
            "args arg must be an argparse.Namespace instance",
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE)

    arg_name = flag_to_arg(flag)
    arg_value = getattr(args, arg_name, NO_ATTRIBUTE)

    if arg_value is NO_ATTRIBUTE:
        return []

    # flatten the argparse list structure
    intermediate_values: list[str] = []
    if isinstance(arg_value, Sequence) and not isinstance(arg_value, (str, bytes)):
        for item in arg_value:
            if isinstance(item, Sequence) and not isinstance(item, (str, bytes)):
                intermediate_values.extend(item)
            else:
                raise SimpleBenchTypeError(
                    "Argument value items must be str or bytes",
                    tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE)
    else:
        raise SimpleBenchTypeError(
            "Argument value must be a Sequence ",
            tag=UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE)

    # process intermediate values and handle comma-separated strings if needed
    unique_values: set[str] = set()
    for item in intermediate_values:
        if include_comma_separated and isinstance(item, str):
            for sub_item in item.split(','):
                stripped_item = sub_item.strip()
                if stripped_item:
                    unique_values.add(stripped_item)
        else:
            unique_values.add(str(item))

    return list(unique_values)
