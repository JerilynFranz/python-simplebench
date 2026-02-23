"""KWArgs subclass for ResultsInfo.__init__."""
from collections.abc import Mapping

from simplebench.report.versions.v1 import ExtrasObject, MetricsObject, ResultsInfo
from simplebench_tests.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue


class ResultsInfoKWArgs(KWArgs):
    """KWArgs for ResultsInfo.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            group: str | NoDefaultValue = NO_DEFAULT_VALUE,
            title: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            n: float | NoDefaultValue = NO_DEFAULT_VALUE,
            variation_marks: Mapping[str, str] | NoDefaultValue = NO_DEFAULT_VALUE,
            metrics: MetricsObject | NoDefaultValue = NO_DEFAULT_VALUE,
            extra_info: ExtrasObject | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize a Results v1 instance.

        The input parameters are validated, converted to immutable types as needed,
        and stored as private attributes that are accessible via read-only properties.

        :param str hash_id: The unique hash identifier for the results.
        :param str group: The group name of the results.
        :param str title: The title of the results.
        :param str description: The description of the results.
        :param n: The complexity analysis n value.
        :param float n: The n value.
        :param VariationMarks variation_marks: The variation marks mapping.
        :param MetricsObject metrics: The list of metrics.
        :param ExtrasObject extra_info: Additional information."""
        super().__init__(ResultsInfo.__init__, kwargs=locals(), globalns=globals())
