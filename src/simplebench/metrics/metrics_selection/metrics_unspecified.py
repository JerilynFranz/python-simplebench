"""MetricsUnspecified metrics class."""

from simplebench.metrics.metrics_selection.metrics_selection_type import MetricsSelectionType

from .metrics_selection import MetricsSelection

__all__: list[str] = []


class MetricsUnspecified(MetricsSelection):
    """Represents an unresolved set of metrics.

    A reporter that uses this class will be responsible for resolving the set
    of metrics itself before reporting.
    """

    def __init__(self) -> None:
        super().__init__(selector_type=MetricsSelectionType.UNSPECIFIED)
