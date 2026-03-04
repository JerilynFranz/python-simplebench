""" " Metric class to represent the metric for evaluation."""

import re
from dataclasses import dataclass

from simplebench.exceptions import SimpleBenchValueError
from simplebench.metrics._metric_type import MetricType
from simplebench.metrics._metric_types_registry import metric_types_registry
from simplebench.validators import validate_string, validate_type

from ._error_tags import _MetricErrorTag

__all__: list[str] = []


@dataclass(frozen=True, kw_only=True)
class Metric:
    """Metric class to define a metric for use."""

    label: str
    """Unique identifier for the metric."""
    title: str
    """Title of the metric."""
    description: str
    """Description of the metric."""
    metric_type: MetricType
    """Type of the metric, defined by MetricType"""

    def __post_init__(self) -> None:
        self._validate_label()

    _LABEL_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
    """Regex pattern for validating the label of the metric

    It must start with an uppercase letter, end with an uppercase letter or digit,
    and may contain uppercase letters, digits, and underscores in between.
    """

    def _validate_title(self) -> None:
        """Validate the title of the metric

        The title must be a string, and may not be empty or blank.

        :raises SimpleBenchTypeError: If the title is not a string
        :raises SimpleBenchValueError: If the title is empty or blank
        """
        validate_string(
            self.title,
            'title',
            _MetricErrorTag.INVALID_TITLE_FIELD_TYPE,
            _MetricErrorTag.INVALID_TITLE_FIELD_VALUE,
            allow_blank=False,
            allow_empty=False,
        )

    def _validate_description(self) -> None:
        """Validate the description of the metric

        The description must be a string, and may be empty or blank.

        :raises SimpleBenchTypeError: If the description is not a string
        """
        validate_string(
            self.description,
            'description',
            _MetricErrorTag.INVALID_DESCRIPTION_FIELD,
            _MetricErrorTag.INVALID_DESCRIPTION_FIELD,
            allow_blank=True,
            allow_empty=True,
        )

    def _validate_label(self) -> None:
        """Validate the label of the metric

        The label must be a non-empty string that starts with an uppercase letter and ends with an uppercase letter,
        and may contain uppercase letters, digits, and underscores in between.
        It must not start or end with an underscore.
        The label must not be empty or blank.
        The label must not contain any characters other than uppercase letters, digits, and underscores.

        :raises SimpleBenchValueError: If the label is invalid
        :raises SimpleBenchTypeError: If the label is not a string
        """
        validate_type(self.label, str, 'label', _MetricErrorTag.INVALID_LABEL_FIELD_TYPE)
        if not self._LABEL_REGEX.match(self.label):
            raise SimpleBenchValueError(
                f"Label '{self.label}' does not match the required pattern: '^[A-Z](?:[A-Z0-9_]*[A-Z])?$'",
                tag=_MetricErrorTag.INVALID_LABEL_FIELD_VALUE,
            )

    def _validate_metric_type(self) -> None:
        """Validate the metric_type of the metric

        The metric_type must be an instance of MetricType,
        and must be registered in the metric_types_registry.

        :raises SimpleBenchTypeError: If the metric_type is not an instance of MetricType
        :raises SimpleBenchValueError: If the metric_type is not registered in the metric_types_registry
        """
        validate_type(self.metric_type, MetricType, 'metric_type', _MetricErrorTag.INVALID_METRIC_TYPE_FIELD_TYPE)
        if self.metric_type not in metric_types_registry:
            raise SimpleBenchValueError(
                f"Metric type '{self.metric_type}' is not registered in the metric_types_registry",
                tag=_MetricErrorTag.NOT_REGISTERED_METRIC_TYPE,
            )

    def __eq__(self, value: object) -> bool:
        """Check equality between two Metric instances.

        :param value: The other Metric instance to compare with.
        :type value: object
        :returns: True if both Metric instances are equal, False otherwise.
        :rtype: bool
        :raises TypeError: If the other value is not a Metric instance.
        """

        if not isinstance(value, Metric):
            return NotImplemented
        return (
            self.label == value.label
            and self.title == value.title
            and self.description == value.description
            and self.metric_type == value.metric_type
        )

    def __lt__(self, value: object) -> bool:
        """Less than comparison between two Metric instances based on their labels.

        :param value: The other Metric instance to compare with.
        :type value: object
        :returns: True if this Metric's label is less than the other Metric's label, False otherwise.
        :rtype: bool
        :raises TypeError: If the other value is not a Metric instance.
        """

        if not isinstance(value, Metric):
            return NotImplemented
        return self.label < value.label

