"""KWArgs subclass for Stats."""

from simplebench.case.results.metrics.stats._stats import Stats
from simplebench.metrics._metric._metric import Metric
from simplebench.simplebench_types._values._values import Values

from ...kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class StatsKWArgs(KWArgs):
    """KWArgs for Stats"""

    def __init__(self, *,
            metric: Metric | NoDefaultValue = NO_DEFAULT_VALUE,
            data: Values | NoDefaultValue = NO_DEFAULT_VALUE,
            rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
            timer: str | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize the Stats object.

        :param metric: The metric definition for the benchmark.
        :type metric: Metric
        :param data: Values tuple of data points.
        :type data: Values
        :param rounds: The number of rounds each data point represents.
        :type rounds: int
        :param timer: The timer used for the measurement.
        :type timer: str | None
        :raises SimpleBenchTypeError: If any of the arguments are of the wrong type.
        :raises SimpleBenchValueError: If any of the arguments have invalid values."""
        super().__init__(call=Stats.__init__, kwargs=locals(), globalns=globals())

