"""MetricsUnspecified metrics class."""
from simplebench.metric.metrics_selection.metrics_selection_type import MetricsSelectionType

from .metrics_selection import MetricsSelection


class MetricsUnspecified(MetricsSelection):
    """Represents an unresolved set of metrics.

    A reporter that uses this class will be responsible for resolving the set
    of metrics itself before reporting.
    """
    def __init__(self):
        super().__init__(selector_type=MetricsSelectionType.UNSPECIFIED)
