"""KWArgs subclass for Metric.__init__."""

from simplebench.report.versions.v1.metric.metric import Metric
from simplebench.report.versions.v1.metric_type.metric_type import MetricType
from simplebench_tests.kwargs import KWArgs, NoDefaultValue, NO_DEFAULT_VALUE

class MetricKWArgs(KWArgs):
    """KWArgs for Metric.__init__"""

    def __init__(self, *,
            hash_id: str | NoDefaultValue = NO_DEFAULT_VALUE,
            label: str | NoDefaultValue = NO_DEFAULT_VALUE,
            title: str | NoDefaultValue = NO_DEFAULT_VALUE,
            description: str | NoDefaultValue = NO_DEFAULT_VALUE,
            metric_type: MetricType | NoDefaultValue = NO_DEFAULT_VALUE) -> None:
        """Abstract base __init__ method for all report element classes."""
        super().__init__(Metric.__init__, kwargs=locals(), globalns=globals())

