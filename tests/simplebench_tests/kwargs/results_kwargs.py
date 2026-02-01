"""Keyword arguments for :class:`~simplebench.case.Results` testing"""


from simplebench.case import Results
from simplebench.simplebench_types import Extras, Iterations, MetricsTimers, VariationMarks

from .kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ResultsKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Results instance."""

    def __init__(
        self,
        *,
        group: str | NoDefaultValue = NO_DEFAULT_VALUE,
        title: str | NoDefaultValue = NO_DEFAULT_VALUE,
        description: str | NoDefaultValue = NO_DEFAULT_VALUE,
        n: float | NoDefaultValue = NO_DEFAULT_VALUE,
        rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
        iterations: Iterations | NoDefaultValue = NO_DEFAULT_VALUE,
        variation_marks: VariationMarks | NoDefaultValue = NO_DEFAULT_VALUE,
        metrics_timers: MetricsTimers | NoDefaultValue = NO_DEFAULT_VALUE,
        extra_info: Extras | NoDefaultValue = NO_DEFAULT_VALUE,
    ) -> None:
        """Initialize ResultsKWArgs with optional keyword arguments.

        This is a KWArgs subclass for the Results class. It allows for easy
        specification of keyword arguments when initializing a Results instance
        for testing purposes. Arguments not provided will use the default values
        defined in the Results class (if any).

        :param str group: The group name for the results.
        :param str title: The title of the results.
        :param str description: A description of the results.
        :param float n: The O() complexity weight.
        :param int rounds: The number of rounds per iteration.
        :param Iterations iterations: A mapping of Metrics to Values for the benchmark
        :param VariationMarks variation_marks: Variation marks as a dictionary.
        :param MetricsTimers metrics_timers: A mapping of Metrics to their timing information.
        :param Extras extra_info: Additional information as a dictionary.
        """
        super().__init__(call=Results.__init__, kwargs=locals())
