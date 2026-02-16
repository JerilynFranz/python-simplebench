"""KWArgs subclass for StatsBlock.__init__."""

from collections.abc import Sequence
from simplebench.report.versions.v1 import StatsBlock
from simplebench.simplebench_types import Values
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class StatsBlockKWArgs(KWArgs):
    """KWArgs for StatsBlock.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            name: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            unit: str | NoDefaultValue = NO_DEFAULT_VALUE,
            scale: float | NoDefaultValue = NO_DEFAULT_VALUE,
            iterations: int | NoDefaultValue = NO_DEFAULT_VALUE,
            rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
            timer: str | NoDefaultValue = NO_DEFAULT_VALUE,
            mean: float | NoDefaultValue = NO_DEFAULT_VALUE,
            median: float | NoDefaultValue = NO_DEFAULT_VALUE,
            minimum: float | NoDefaultValue = NO_DEFAULT_VALUE,
            maximum: float | NoDefaultValue = NO_DEFAULT_VALUE,
            stdev: float | NoDefaultValue = NO_DEFAULT_VALUE,
            relative_stdev: float | NoDefaultValue = NO_DEFAULT_VALUE,
            percentiles: Sequence[float] | NoDefaultValue = NO_DEFAULT_VALUE,
            measurements: Sequence[float] | Values | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize a StatsBlock object with the given parameters.

        The parameters are validated to ensure they meet the required types and constraints
        and match the contract of the JSON schema for the version 1 report.

        .. note::

            The following parameters can be derived from the measurements and cannot be
            set directly if measurements are provided. If measurements are provided and
            any of these parameters are also provided a value other than `None`,
            a `SimpleBenchTypeError` will be raised.

            - iterations
            - mean
            - median
            - minimum
            - maximum
            - stdev
            - relative_stdev
            - percentiles

        :param str hash_id: The hash identifier for the stats block.
        :param str name: The name of the stats block.
        :param str description: The description.
        :param str semantic_type: The semantic type of the stats block.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param int | None iterations: The number of iterations. (exclusive with `measurements`)
        :param int rounds: The number of rounds in the stats block.
        :param str timer: The timer used for measurements.
        :param float | None mean: The mean value of the data. (exclusive with `measurements`)
        :param float | None median: The median value of the data. (exclusive with `measurements`)
        :param float | None minimum: The minimum value of the data. (exclusive with `measurements`)
        :param float | None maximum: The maximum value of the data. (exclusive with `measurements`)
        :param float | None stdev: The standard deviation of the data. (exclusive with `measurements`)
        :param float | None relative_stdev: The relative standard deviation of the data. (exclusive with `measurements`)
        :param Sequence[float] | None percentiles: The list of percentiles for the data (exclusive with `measurements`).
        :param Sequence[float] | Values | None measurements: The list of raw measurements for the data.
        :raise SimpleBenchTypeError: If any parameter is of an invalid type.
        :raise SimpleBenchValueError: If any parameter has an invalid value."""
        super().__init__(StatsBlock.__init__, kwargs=locals(), globalns=globals())
