"""KWArgs subclass for ValueBlock.__init__."""

from simplebench.report.versions.v1 import ValueBlock
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class ValueBlockKWArgs(KWArgs):
    """KWArgs for ValueBlock.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            timer: str | NoDefaultValue = NO_DEFAULT_VALUE,
            unit: str | NoDefaultValue = NO_DEFAULT_VALUE,
            scale: float | NoDefaultValue = NO_DEFAULT_VALUE,
            value: float | int | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize ValueBlock instance.

        :param str hash_id: The unique hash identifier for the value block.
            If not provided, it defaults to an empty string and will be computed automatically.
        :param str semantic_type: The semantic type string for the value block. ('type' field in JSON data)
        :param (str | None) timer: The timer string or None.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param float | int value: The value of the block.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value."""
        super().__init__(ValueBlock.__init__, kwargs=locals(), globalns=globals())

