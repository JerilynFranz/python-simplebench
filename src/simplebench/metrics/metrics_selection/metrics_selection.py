"""MetricSelection class for selecting and managing metrics."""

from .metrics_selection_type import MetricsSelectionType

__all__ = []


class MetricsSelection:
    """Represents a set of metrics that can be selected from a given universe.

    This class is a base class for different types of metric selections.
    """

    def __init__(self, selector_type: MetricsSelectionType) -> None:
        self._selector_type = selector_type

    @property
    def selector_type(self) -> MetricsSelectionType:
        """Returns the type of the metric selection.

        Possible values are:
        - MetricsSelectionType.COLLECTION: Represents a collection of metrics.
        - MetricsSelectionType.UNSPECIFIED: Represents an unspecified metric selection type.

        :return: The type of the metric selection.
        """
        return self._selector_type
