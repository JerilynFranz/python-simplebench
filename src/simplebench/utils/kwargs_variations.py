"""Utility function for generating keyword argument permutations."""
import itertools
from typing import Any, Sequence

from simplebench.exceptions import SimpleBenchTypeError

from .exceptions import _UtilsErrorTag


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
            tag=_UtilsErrorTag.KWARGS_VARIATIONS_INVALID_KWARGS_ARG_TYPE
        )
    for key, value in kwargs.items():
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            raise SimpleBenchTypeError(
                ("kwargs arg values must be a Sequence (not str or bytes); "
                 f"key '{key}' has invalid value type {type(value)}"),
                tag=_UtilsErrorTag.KWARGS_VARIATIONS_INVALID_KWARGS_VALUE_TYPE
            )

    keys = kwargs.keys()
    if not keys:
        return [{}]
    values = [kwargs[key] for key in keys]
    return [dict(zip(keys, v)) for v in itertools.product(*values)]
