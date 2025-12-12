"""report Results base class.

This class represents Results in a JSON report.

It implements validation and serialization/deserialization methods to and from dictionaries
for the results property object in the following JSON Schema version:

https://raw.githubusercontent.com/JerilynFranz/python-simplebench/main/schemas/v1/json-report.json

It is not a standalone JSON schema object, but rather a component of the overall JSON report schema object

It is the base implemention of the JSON results object representation.

This makes the implementations of Results backwards compatible with future versions
of the JSON report schema and the V1 implementation itself is essentially a frozen snapshot
of the results object representation at the time of the V1 schema release."""
from __future__ import annotations

from abc import ABC
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.validators import validate_float, validate_string

from ..exceptions import _ResultsErrorTag
from .metrics import Metrics


class Results(ABC):
    """Base class representing JSON results."""

    VERSION: int = 0
    """The JSON results version number.

    :note: This should be overridden in sub-classes."""

    TYPE: str = "SimpleBenchResults::V0"
    """The JSON results type.

    :note: This should be overridden in sub-classes.
    """

    @classmethod
    def from_dict(cls, data: dict) -> Results:
        """Create a JSON Results object instance from a dictionary.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Results object instance.
        """
        known_keys = {
            'type',
            'group',
            'title',
            'description',
            'n',
            'variation_cols',
            'metrics',
            'extra_info',
        }
        extra_keys = set(data.keys()) - known_keys
        if extra_keys:
            raise SimpleBenchTypeError(
                f"Unexpected keys in data dictionary: {extra_keys}",
                tag=_ResultsErrorTag.INVALID_DATA_ARG_EXTRA_KEYS)

        missing_keys = known_keys - data.keys()
        if missing_keys:
            raise SimpleBenchTypeError(
                f"Missing required keys in data dictionary: {missing_keys}",
                tag=_ResultsErrorTag.INVALID_DATA_ARG_MISSING_KEYS)

        cls.validate_type(data.get('type'), cls.TYPE)

        return cls(
            group=data.get('group'),  # type: ignore[reportArgumentType]
            title=data.get('title'),  # type: ignore[reportArgumentType]
            description=data.get('description'),  # type: ignore[reportArgumentType]
            n=data.get('n'),  # type: ignore[reportArgumentType]
            variation_cols=data.get('variation_cols'),  # type: ignore[reportArgumentType]
            metrics=Metrics.from_dict(data.get('metrics')),  # type: ignore[reportArgumentType]
            extra_info=data.get('extra_info'))  # type: ignore[reportArgumentType]

    def __init__(self,
                 *,
                 group: str,
                 title: str,
                 description: str,
                 n: float,
                 variation_cols: dict[str, Any],
                 metrics: Metrics,
                 extra_info: dict[str, Any]
                 ):  # pylint: disable=super-init-not-called
        """Initialize a Results v1 instance.

        :param group: The group name of the results.
        :param title: The title of the results.
        :param description: The description of the results.
        :param n: The number of iterations.
        :param variation_cols: The variation columns.
        :param metrics: The list of metrics.
        :param extra_info: Additional information.
        """
        self.group = group
        self.title = title
        self.description = description
        self.n = n
        self.variation_cols = variation_cols
        self.metrics = metrics
        self.extra_info = extra_info

    @classmethod
    def validate_type(cls, found: Any, expected: str) -> str:
        """Validate the type.

        :param found: The type string to validate.
        :param expected: The expected type string.
        :return: The validated type string.
        :raise SimpleBenchTypeError: If the type is not a string.
        :raises SimpleBenchValueError: If the type is invalid.
        """
        if not isinstance(found, str):
            raise SimpleBenchValueError(
                f"type must be a string, got {type(found)}",
                tag=_ResultsErrorTag.INVALID_TYPE_TYPE)
        if found != expected:
            raise SimpleBenchValueError(
                f"Incorrect type for JSONResults: {found} (expected '{expected}')",
                tag=_ResultsErrorTag.INVALID_TYPE_VALUE)
        return found

    @property
    def group(self) -> str:
        """Get the group property."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """Set the group property."""
        self._group: str = validate_string(
            value, 'group',
            _ResultsErrorTag.INVALID_GROUP_TYPE,
            _ResultsErrorTag.INVALID_GROUP_VALUE_EMPTY_STRING,
            allow_empty=False)

    @property
    def title(self) -> str:
        """Get the title property."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the title property."""
        self._title: str = validate_string(
            value, 'title',
            _ResultsErrorTag.INVALID_TITLE_TYPE,
            _ResultsErrorTag.INVALID_TITLE_VALUE_EMPTY_STRING,
            allow_empty=False)

    @property
    def description(self) -> str:
        """Get the description property."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description property."""
        self._description: str = validate_string(
            value, 'description',
            _ResultsErrorTag.INVALID_DESCRIPTION_TYPE,
            _ResultsErrorTag.INVALID_DESCRIPTION_EMPTY_STRING,
            allow_empty=False)

    @property
    def n(self) -> float:
        """Get the n property."""
        return self._n

    @n.setter
    def n(self, value: float) -> None:
        """Set the n property."""
        self._n: float = validate_float(
            value, 'n', _ResultsErrorTag.INVALID_N_TYPE)
        if self._n < 1:
            raise SimpleBenchValueError(
                f"n must be >= 1, got {self._n}",
                tag=_ResultsErrorTag.INVALID_N_VALUE)

    @property
    def variation_cols(self) -> dict[str, str]:
        """Get the variation columns.

        :return: A dictionary of variation columns.
        """
        return self._variation_cols

    @variation_cols.setter
    def variation_cols(self, value: dict[str, str]) -> None:
        """Set the variation columns.

        :param value: A dictionary of variation columns.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f"variation_cols must be a dictionary, got {type(value)}",
                tag=_ResultsErrorTag.INVALID_VARIATION_COLS_TYPE)

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
            raise SimpleBenchTypeError(
                "All keys and values in variation_cols must be strings",
                tag=_ResultsErrorTag.INVALID_VARIATION_COLS_CONTENT)

        self._variation_cols: dict[str, str] = value

    @property
    def metrics(self) -> Metrics:
        """Get the metrics.

        :return: The metrics dictionary.
        """
        return self._metrics

    @metrics.setter
    def metrics(self, value: Metrics) -> None:
        """Set the metrics.

        :param value: The metrics.
        """
        if not isinstance(value, Metrics):
            raise SimpleBenchTypeError(
                f"metrics must be a Metrics instance, got {type(value)}",
                tag=_ResultsErrorTag.INVALID_TYPE_TYPE)

        self._metrics: Metrics = value

    @property
    def extra_info(self) -> dict[str, Any]:
        """Get the extra info.

        :return: The extra info dictionary.
        """
        return self._extra_info

    @extra_info.setter
    def extra_info(self, value: dict[str, Any]) -> None:
        """Set the extra info.

        :param value: The extra info dictionary.
        """
        if not isinstance(value, dict):
            raise SimpleBenchTypeError(
                f"extra_info must be a dictionary, got {type(value)}",
                tag=_ResultsErrorTag.INVALID_TYPE_TYPE)
        self._extra_info: dict[str, Any] = value
