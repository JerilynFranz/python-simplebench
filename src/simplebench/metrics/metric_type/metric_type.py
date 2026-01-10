"""Definition for a metric for the simplebench library."""
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_float, validate_namespaced_identifier, validate_string, validate_type

from ._error_tags import _MetricTypeErrorTag

_deferred_imports_done: bool = False

if TYPE_CHECKING:
    from simplebench.metrics.metric_category import MetricCategory
    _deferred_imports_done = True

else:
    MetricCategory = None  # pylint: disable=invalid-name


def _deferred_imports() -> None:
    """Perform deferred imports for runtime use to avoid circular dependencies."""
    global MetricCategory, _deferred_imports_done  # pylint: disable=global-statement
    if not _deferred_imports_done:
        from simplebench.metrics.metric_category import MetricCategory  # pylint: disable=import-outside-toplevel
        _deferred_imports_done = True


@dataclass(frozen=True, kw_only=True)
class MetricType:
    """Definition for a metric

    This class defines a metric with a name, semantic type, label, description, unit, and scale.

    Metrics are used to measure and report the performance of a system or application. They are used to track and report
    various performance metrics, such as the number of operations per second, the number of bytes transferred, or
    the time taken to complete a task.

    :param semantic_type: The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'
    :param label: The label of the metric, e.g. 'OPS_PER_SEC'
    :param description: The description of the metric, e.g. 'Operations per second'
    :param unit: The unit of the metric, e.g. 'ops/s'
    :param scale: The scale of the metric, e.g. 1.0. Accepts an int and converts it to a float.
    :param category: The type of the metric
        - `MetricCategory.CUMULATIVE`
        - `MetricCategory.STATISTICAL`
        - `MetricCategory.RAW`
    """
    semantic_type: str
    """The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'"""
    label: str
    """The label of the metric, e.g. 'OPS_PER_SEC'"""
    description: str
    """The description of the metric, e.g. 'Operations per second'"""
    unit: str
    """The unit of the metric, e.g. 'ops/s'"""
    scale: float
    """The scale of the metric, e.g. 1.0"""
    category: MetricCategory
    """The type of the metric, e.g. `MetricCategory.CUMULATIVE`, `MetricCategory.STATISTICAL` or `MetricCategory.RAW`"""

    _LABEL_REGEX = re.compile(r'^[A-Z](?:[A-Z0-9_]*[A-Z0-9])?$')
    _UNIT_REGEX = re.compile(r'^[A-Za-z](?:[A-Za-z0-9/\-_\.]*[A-Za-z0-9])?$')

    def __post_init__(self) -> None:
        scale = validate_float(
                    self.scale, 'scale',
                    _MetricTypeErrorTag.INVALID_SCALE_FIELD_TYPE)
        object.__setattr__(self, 'scale', scale)
        self._validate_label()
        self._validate_description()
        self._validate_unit()
        self._validate_scale()
        self._validate_semantic_type()
        self._validate_category()

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
        validate_type(self.label, str, 'label',
                      _MetricTypeErrorTag.INVALID_LABEL_FIELD_TYPE)
        if not self._LABEL_REGEX.match(self.label):
            raise SimpleBenchValueError(
                f"Label '{self.label}' does not match the required pattern: '^[A-Z](?:[A-Z0-9_]*[A-Z])?$'",
                tag=_MetricTypeErrorTag.INVALID_LABEL_FIELD_VALUE)

    def _validate_description(self) -> None:
        """Validate the description of the metric

        The description must be a string, and may be empty or blank.

        :raises SimpleBenchTypeError: If the description is not a string
        """
        validate_string(
            self.description, 'description',
            _MetricTypeErrorTag.INVALID_DESCRIPTION_FIELD,
            _MetricTypeErrorTag.INVALID_DESCRIPTION_FIELD,
            allow_blank=True, allow_empty=True)

    def _validate_unit(self):
        """Validate the unit of the metric

        The unit must be a non-empty string that starts with a letter
        and may contain letters, digits, slashes, hyphens, underscores, and dots.
        It must not start or end with a slash, hyphen, underscore, or dot.
        The unit must not be empty or blank.

        :raises SimpleBenchValueError: If the unit is invalid
        :raises SimpleBenchTypeError: If the unit is not a string
        """
        validate_type(self.unit, str, 'unit',
                      _MetricTypeErrorTag.INVALID_UNIT_FIELD_TYPE)
        if not self._UNIT_REGEX.match(self.unit):
            raise SimpleBenchValueError(
                f"Unit '{self.unit}' does not match the required pattern: '^[A-Za-z](?:[A-Za-z0-9/\\-_\\.]*)$'",
                tag=_MetricTypeErrorTag.INVALID_UNIT_FIELD_VALUE)

    def _validate_scale(self) -> None:
        """Validate the scale of the metric

        The scale must be a positive float (greater than 0.0). A type error will be raised if the value
        cannot be converted to a float.

        :raises SimpleBenchValueError: If the scale is not positive.
        :raises SimpleBenchTypeError: If the scale is not a float or int.
        """
        if self.scale <= 0.0:
            raise SimpleBenchValueError(
                f"Scale '{self.scale}' must be greater than 0.0",
                tag=_MetricTypeErrorTag.INVALID_SCALE_FIELD_VALUE)

    def _validate_semantic_type(self) -> None:
        """Validate the semantic type of the metric

        The semantic type must be a valid namespaced identifier, e.g. 'simplebench_std::operations_per_second'.
        The semantic type must not be empty or blank.

        :raises SimpleBenchValueError: If the semantic type is invalid
        :raises SimpleBenchTypeError: If the semantic type is not a string
        """
        validate_namespaced_identifier(
            self.semantic_type, 'semantic_type',
            _MetricTypeErrorTag.INVALID_SEMANTIC_TYPE_FIELD_TYPE,
            _MetricTypeErrorTag.INVALID_SEMANTIC_TYPE_FIELD_VALUE)

    def _validate_category(self) -> None:
        """Validate the category of the metric

        The category must be a valid MetricCategory enum value.

        :raises SimpleBenchTypeError: If the category is not a valid MetricCategory enum value
        """
        _deferred_imports()
        if not isinstance(self.category, MetricCategory):
            raise SimpleBenchTypeError(
                f"Metric category '{self.category}' is not a valid MetricCategory enum value",
                tag=_MetricTypeErrorTag.INVALID_CATEGORY_FIELD_VALUE)
