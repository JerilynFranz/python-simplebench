"""V1 Results object class

The V1 Results object represents the results section of a version 1 JSON report.

"""
from typing import Any

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.reporters.json.report.base import Metrics
from simplebench.reporters.json.report.base import ResultsInfo as BaseResultsInfo
from simplebench.reporters.json.report.exceptions import _ResultsInfoErrorTag
from simplebench.validators import validate_float, validate_string

from .results_info_schema import ResultsInfoSchema


class ResultsInfo(BaseResultsInfo):
    """Class representing JSON results object for V1 reports."""
    SCHEMA = ResultsInfoSchema
    """The JSON report schema for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""

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
    def from_dict(cls, data: dict) -> 'ResultsInfo':
        """Create a JSON Results object instance from a dictionary.

        :param data: Dictionary containing the JSON results object data.
        :return: JSON Results object instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed=allowed_keys,
            skip={'version', 'type'},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'metrics': Metrics.from_dict})
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert the JSON Results object instance to a dictionary.

        :return: Dictionary containing the JSON results object data.
        """
        data: dict[str, Any] = {}
        for key in self.init_params():
            value = getattr(self, key)
            if hasattr(value, 'to_dict'):
                data[key] = value.to_dict()
            else:
                data[key] = value

        data['type'] = self.TYPE
        data['version'] = self.VERSION
        return data

    @property
    def group(self) -> str:
        """Get the group property."""
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """Set the group property."""
        self._group: str = validate_string(
            value, 'group',
            _ResultsInfoErrorTag.INVALID_GROUP_TYPE,
            _ResultsInfoErrorTag.INVALID_GROUP_VALUE_EMPTY_STRING,
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
            _ResultsInfoErrorTag.INVALID_TITLE_TYPE,
            _ResultsInfoErrorTag.INVALID_TITLE_VALUE_EMPTY_STRING,
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
            _ResultsInfoErrorTag.INVALID_DESCRIPTION_TYPE,
            _ResultsInfoErrorTag.INVALID_DESCRIPTION_EMPTY_STRING,
            allow_empty=False)

    @property
    def n(self) -> float:
        """Get the n property."""
        return self._n

    @n.setter
    def n(self, value: float) -> None:
        """Set the n property."""
        self._n: float = validate_float(
            value, 'n', _ResultsInfoErrorTag.INVALID_N_TYPE)
        if self._n < 1:
            raise SimpleBenchValueError(
                f"n must be >= 1, got {self._n}",
                tag=_ResultsInfoErrorTag.INVALID_N_VALUE)

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
                tag=_ResultsInfoErrorTag.INVALID_VARIATION_COLS_TYPE)

        if not all(isinstance(k, str) and isinstance(v, str) for k, v in value.items()):
            raise SimpleBenchTypeError(
                "All keys and values in variation_cols must be strings",
                tag=_ResultsInfoErrorTag.INVALID_VARIATION_COLS_CONTENT)

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
                tag=_ResultsInfoErrorTag.INVALID_TYPE_TYPE)

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
                tag=_ResultsInfoErrorTag.INVALID_TYPE_TYPE)
        self._extra_info: dict[str, Any] = value
