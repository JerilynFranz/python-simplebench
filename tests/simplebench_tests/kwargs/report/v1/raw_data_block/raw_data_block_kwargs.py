"""KWArgs subclass for RawDataBlock.__init__."""

from collections.abc import Sequence
from simplebench.report.versions.v1.raw_data_block.raw_data_block import RawDataBlock
from simplebench.simplebench_types._values._values import Values
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class RawDataBlockKWArgs(KWArgs):
    """KWArgs for RawDataBlock.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            name: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            unit: str | NoDefaultValue = NO_DEFAULT_VALUE,
            scale: float | NoDefaultValue = NO_DEFAULT_VALUE,
            rounds: int | NoDefaultValue = NO_DEFAULT_VALUE,
            timer: str | NoDefaultValue = NO_DEFAULT_VALUE,
            data: Sequence[int | float] | Values | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize RawDataBlock class.

        :param str hash_id: The hash ID string for the raw data block.
        :param str name: The name string for the raw data block.
        :param str description: The description string for the raw data block.
        :param str semantic_type: The semantic type string for the raw data block.
        :param str timer: The timer string.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param int rounds: The number of rounds per data point.
        :param Values data: The raw data values of the block.
        :param str timer: The timer string.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value."""
        super().__init__(RawDataBlock.__init__, kwargs=locals(), globalns=globals())
