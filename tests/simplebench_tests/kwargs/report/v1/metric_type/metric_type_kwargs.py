"""KWArgs subclass for MetricType.__init__."""

from simplebench.report.versions.v1.metric_category import MetricCategory
from simplebench.report.versions.v1.metric_type.metric_type import MetricType
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class MetricTypeKWArgs(KWArgs):
    """KWArgs for MetricType.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            semantic_type: str | NoDefaultValue = NO_DEFAULT_VALUE,
            label: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            unit: str | NoDefaultValue = NO_DEFAULT_VALUE,
            scale: float | int | NoDefaultValue = NO_DEFAULT_VALUE,
            category: MetricCategory | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Initialize a MetricType instance.

        :param hash_id: The hash ID of the metric type. This is an optional field that can be used to uniquely
            identify the metric type.
        :type hash_id: str
        :param semantic_type: The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'
        :type semantic_type: str
        :param label: The label of the metric, e.g. 'OPS_PER_SEC'
        :type label: str
        :param description: The description of the metric, e.g. 'Operations per second'
        :type description: str
        :param unit: The unit of the metric, e.g. 'ops/s'
        :type unit: str
        :param scale: The scale of the metric, e.g. 1.0. Accepts an int or float and converts it to a float.
        :type scale: float | int
        :param category: The type of the metric
            - :attr:`MetricCategory.VALUE`
            - :attr:`MetricCategory.STATS`
            - :attr:`MetricCategory.RAW_DATA`
        :type category: MetricCategory"""
        super().__init__(MetricType.__init__, kwargs=locals(), globalns=globals())

