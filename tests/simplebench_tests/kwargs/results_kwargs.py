"""Keyword arguments for :class:`~simplebench.case.Results` testing"""

from collections.abc import Mapping
from typing import Any

from simplebench_tests.kwargs.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.case import Results
from simplebench.metrics import Metric
from simplebench.simplebench_types import Values


class ResultsKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Results instance."""

    def __init__(  # pylint: disable=unused-argument
        self,
        *,
        group: str | NoDefaultValue = NO_DEFAULT_VALUE,
        title: str | NoDefaultValue = NO_DEFAULT_VALUE,
        description: str | NoDefaultValue = NO_DEFAULT_VALUE,
        n: int | NoDefaultValue = NO_DEFAULT_VALUE,
        rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
        iterations: Mapping[Metric, Values] | NoDefaultValue = NO_DEFAULT_VALUE,
        variation_cols: dict[str, str] | NoDefaultValue = NO_DEFAULT_VALUE,
        marks: dict[str, tuple[str, ...]] | NoDefaultValue = NO_DEFAULT_VALUE,
        extra_info: dict[str, Any] | NoDefaultValue = NO_DEFAULT_VALUE,
    ) -> None:
        """Initialize ResultsKWArgs with optional keyword arguments.

        This is a KWArgs subclass for the Results class. It allows for easy
        specification of keyword arguments when initializing a Results instance
        for testing purposes. Arguments not provided will use the default values
        defined in the Results class (if any).

        :param str group: The group name for the results.
        :param str title: The title of the results.
        :param str description: A description of the results.
        :param int n: The number of iterations.
        :param int rounds: The number of rounds in the benchmark case.
        :param Mapping[Metric, Values] iterations: A mapping of Metric to their corresponding Values.
        :param dict[str, str] variation_cols: Variation columns as a dictionary.
        :param dict[str, tuple[str, ...]] marks: Variation marks as a dictionary.
        :param dict[str, Any] extra_info: Additional information as a dictionary.
        """
        super().__init__(call=Results.__init__, kwargs=locals())
