"""Factories for creating argparse-related test objects."""
from __future__ import annotations

import re
from argparse import ArgumentParser, Namespace
from typing import Any, Iterable, Sequence

from simplebench.enums import Target

from ._primitives import flag_name_factory


def namespace_factory(*, argparser: ArgumentParser | None = None, args: Sequence[str] | None = None) -> Namespace:
    """Return an ArgumentParser Namespace instance for testing purposes.

    If passed an ArgumentParser instance, it uses that to parse the arguments (if provided).
    Otherwise, it creates a new ArgumentParser instance with a default program name of 'simplebench'.

    It never performs caching of calls.

    :param argparser: An optional ArgumentParser instance to use for parsing.
    :type argparser: ArgumentParser | None, optional
    :param args: An optional sequence of command-line arguments to parse.
    :type args: Sequence[str] | None, optional
    :return: An ArgumentParser Namespace instance.
    :rtype: Namespace
    """
    if args is None:
        args = []

    if argparser is not None:
        return argparser.parse_args(args=args)
    arg_parser = ArgumentParser(prog='simplebench')
    return arg_parser.parse_args(args=args)


def boolean_flag_factory(flag: str, default: bool = False) -> dict[str, Any]:
    """Returns an argument parser flag configuration for a boolean flag.

    The default value determines whether the flag enables or disables the feature.
    - If default is False, the flag enables the feature when present.
    - If default is True, the flag disables the feature when present.

    :param flag: The name of the flag (including the leading dashes).
    :type flag: str
    :param default: The default value for the flag.
    :type default: bool, optional
    :return: A dictionary suitable for unpacking as argparser.add_argument() flag parameters.
    :rtype: dict[str, Any]

    return {
        'flag': flag,
        'action': 'store_true' if not default else 'store_false',
        'default': default,
        'help': f'Enable {flag.lstrip("-")}' if not default else f'Disable {flag.lstrip("-")}'
    }
    """
    if not isinstance(flag, str):
        raise TypeError("'flag' argument must be a string")
    if not flag.startswith('--'):
        raise ValueError("'flag' argument must start with '--'")
    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise ValueError("'flag' argument contains invalid characters for a command-line flag. "
                         "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
                         "and periods are allowed after the prefix.")
    if not isinstance(default, bool):
        raise TypeError("default arg must be a boolean")

    return {
        'name_or_flags': flag,
        'action': 'store_true' if not default else 'store_false',
        'default': default,
        'help': f'Enable {flag.lstrip("-")}' if not default else f'Disable {flag.lstrip("-")}',
    }


def list_of_strings_flag_factory(flag: str,
                                 choices: Iterable[str] | None = None,
                                 description: str = 'Help string') -> dict[str, Any]:
    """Returns an argument parser flag configuration for a list flag

    It is suitable to multiple values being provided by repeating the flag
    on the command line, e.g.:

    .. code-block:: console

        --flag value1 --flag value2 value3

    It sets the nargs to '*' to allow zero or more values per flag occurrence.

    No caching is performed for this factory function.

    :param flag: The name of the flag (including the leading dashes).
    :type flag: str
    :param choices: An optional iterable of valid string choices for the flag values.
                    If None, no choices are enforced.
    :type choices: Iterable[str] | None, optional
    :param description: A help string description for the flag.
    :type description: str, optional
    :return: A dictionary suitable for unpacking as argparser.add_argument() flag parameters.
    :rtype: dict[str, Any]
    """
    if not isinstance(flag, str):
        raise TypeError("'flag' argument must be a string")
    if not flag.startswith('--'):
        raise ValueError("'flag' argument must start with '--'")
    if not re.match(r'^--[A-Za-z0-9\-_.]+$', flag):
        raise ValueError("'flag' argument contains invalid characters for a command-line flag. "
                         "It must be prefixed with '--' and only letters, numbers, hyphens, underscores, "
                         "and periods are allowed after the prefix.")

    if not (choices is None or isinstance(choices, Iterable)):
        raise TypeError("'choices' argument must be an iterable of strings")
    if choices is not None:
        for choice in choices:
            if not isinstance(choice, str):
                raise TypeError("all items in 'choices' must be strings")

    if not isinstance(description, str):
        raise TypeError("'description' argument must be a string")

    return {
        'name_or_flags': flag,
        'action': 'append',
        'nargs': '*',
        'choices': choices,
        'help': description,
    }


def argument_parser_factory(prog: str = 'simplebench',
                            arguments: Sequence[dict[str, Any]] | None = None) -> ArgumentParser:
    """Return an ArgumentParser instance for testing purposes.

    It creates an ArgumentParser with the specified program name and adds any provided arguments.

    No caching is performed for this factory function.

    :param prog: The program name for the ArgumentParser.
    :type prog: str, optional
    :param arguments: An optional sequence of argument configurations to add to the parser.
                      Each argument configuration should be a dictionary suitable for
                      unpacking into the `add_argument()` method of ArgumentParser.
    :type arguments: Sequence[dict[str, Any]] | None, optional
    :return: An ArgumentParser instance.
    :rtype: ArgumentParser
    """
    if not isinstance(prog, str):
        raise TypeError("'prog' argument must be a string")
    if arguments is not None:
        if not isinstance(arguments, Sequence):
            raise TypeError("'arguments' argument must be a sequence of dictionaries")
        for arg in arguments:
            if not isinstance(arg, dict):
                raise TypeError("each item in 'arguments' must be a dictionary")
    if arguments is not None:
        parser = ArgumentParser(prog=prog)
        for arg in arguments:
            name_or_flags = arg.get('name_or_flags')
            if name_or_flags is None:
                raise ValueError("each argument dictionary must contain a 'name_or_flags' key")
            kwargs = {k: v for k, v in arg.items() if k != 'name_or_flags'}
            parser.add_argument(name_or_flags, **kwargs)
        return parser
    return ArgumentParser(prog=prog)


def reporter_namespace_factory(args: list[str], choices: list[str] | None = None) -> Namespace:
    """Create a parsed `argparse.Namespace` for testing.

    It create a default argument parser with a flag named according to
    the `flag_name_factory()` function and with choices corresponding to
    the `Target` enum values. It then parses the provided args list
    and returns the resulting `Namespace`.

    :param args: A list of strings representing command-line arguments to be parsed.
    :type args: list[str]
    :param choices: An optional list of valid choices for the reporter target flag.
                    If `None`, it defaults to
                    `[Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value]`
    :type choices: list[str] | None, optional
    """
    if not isinstance(args, list):
        raise TypeError("args must be a list of strings")
    if not all(isinstance(arg, str) for arg in args):
        raise TypeError("all items in args must be strings")
    if choices is None:
        choices = [Target.CONSOLE.value, Target.FILESYSTEM.value, Target.CALLBACK.value]
    return argument_parser_factory(arguments=[
        list_of_strings_flag_factory(flag=flag_name_factory(), choices=choices, description="Select reporter targets.")
    ]).parse_args(args=args)
