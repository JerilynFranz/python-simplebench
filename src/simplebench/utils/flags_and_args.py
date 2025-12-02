"""Utility functions for command-line flags and argument names."""
import re
from argparse import Namespace
from typing import Sequence

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError

from .exceptions import _UtilsErrorTag


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
            tag=_UtilsErrorTag.FLAG_TO_ARG_INVALID_FLAG_ARG_TYPE)
    if flag == '':
        raise SimpleBenchValueError(
            "flag arg must not be an empty string",
            tag=_UtilsErrorTag.FLAG_TO_ARG_EMPTY_FLAG_ARG)
    if not (flag.startswith('--') and len(flag) > 2):
        raise SimpleBenchValueError(
            "flag arg must start with '--' and have additional characters",
            tag=_UtilsErrorTag.FLAG_TO_ARG_INVALID_FLAG_ARG_VALUE)

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
            tag=_UtilsErrorTag.ARG_TO_FLAG_INVALID_FLAG_ARG_TYPE)
    if arg == '':
        raise SimpleBenchValueError(
            "arg arg must not be an empty string",
            tag=_UtilsErrorTag.ARG_TO_FLAG_EMPTY_FLAG_ARG)

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
            tag=_UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARGS_ARG_TYPE)

    if not isinstance(flag, str):
        raise SimpleBenchTypeError(
            "flag arg must be a str",
            tag=_UtilsErrorTag.COLLECT_ARG_LIST_INVALID_FLAG_ARG_TYPE)

    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise SimpleBenchValueError((
            "flag arg contains invalid characters for a command-line flag. "
            "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
            "and periods are allowed after the prefix."),
            tag=_UtilsErrorTag.COLLECT_ARG_LIST_INVALID_FLAG_ARG_VALUE)

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
                    tag=_UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_ITEM_TYPE)
    else:
        raise SimpleBenchTypeError(
            f"Argument value must be a Sequence (but not str or bytes): found: {arg_value} ",
            tag=_UtilsErrorTag.COLLECT_ARG_LIST_INVALID_ARG_VALUE_TYPE)

    return list(intermediate_values)
