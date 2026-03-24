"""KWArgs subclass for ValueBlock.__init__."""

from simplebench.report.versions.v1 import Metric, ValueBlock
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ValueBlockKWArgs(KWArgs):
    """KWArgs for ValueBlock.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            metric: Metric | NoDefaultValue = NO_DEFAULT_VALUE,
            value: float | int | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize ValueBlock instance.

        :param str hash_id: The unique hash identifier for the value block.
            If not provided, it defaults to an empty string and will be computed automatically.
        :param str semantic_type: The semantic type string for the value block. ('type' field in JSON data)
        :param Metric metric: The Metric instance associated with this value block.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value."""
        super().__init__(ValueBlock.__init__, kwargs=locals(), globalns=globals())
