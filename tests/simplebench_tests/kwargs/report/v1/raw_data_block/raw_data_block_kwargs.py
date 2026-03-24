"""KWArgs subclass for RawDataBlock.__init__."""

from collections.abc import Sequence

from simplebench.report.versions.v1 import Metric, RawDataBlock
from simplebench.simplebench_types import Values
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class RawDataBlockKWArgs(KWArgs):
    """KWArgs for RawDataBlock.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            name: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            metric: Metric | NoDefaultValue = NO_DEFAULT_VALUE,
            rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
            timer: str | NoDefaultValue = NO_DEFAULT_VALUE,
            data: Sequence[int | float] | Values | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize RawDataBlock class.

        :param str hash_id: The hash ID string for the raw data block.
        :param str name: The name string for the raw data block.
        :param str description: The description string for the raw data block.
        :param str semantic_type: The semantic type string for the raw data block.
        :param Metric metric: The Metric object associated with the raw data block.
        :param int rounds: The number of rounds per data point.
        :param Values data: The raw data values of the block.
        :param str timer: The timer string.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value."""
        super().__init__(RawDataBlock.__init__, kwargs=locals(), globalns=globals())
