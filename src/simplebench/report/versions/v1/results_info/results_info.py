"""V1 Results object class

The V1 Results object represents the results metric of a version 1 JSON report.

"""
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from simplebench.report.base import BaseResultsInfo
from simplebench.types import CoreDataMappingType, ImmutableCoreDataMappingType
from simplebench.validators import validate_core_data_mapping

from .. import MetricsObject
from . import validate
from .results_info_schema import ResultsInfoSchema


class ResultsInfo(BaseResultsInfo):
    """An immutable class representing the results-info object for V1 reports.

    This class encapsulates the structure and validation logic
    of the results-info section.
    """
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
                 variation_cols: Mapping[str, str],
                 variation_marks: Mapping[str, str],
                 metrics: MetricsObject,
                 extra_info: CoreDataMappingType,
                 ):
        """Initialize a Results v1 instance.

        The input parameters are validated, converted to immutable types as needed,
        and stored as private attributes that are accessible via read-only properties.

        :param str group: The group name of the results.
        :param str title: The title of the results.
        :param str description: The description of the results.
        :param n: The complexity analysis n value.
        :param float n: The n value.
        :param Mapping[str, str] variation_cols: The variation columns.
        :param MetricsObject metrics: The list of metrics.
        :param CoreDataMappingType extra_info: Additional information.
        """
        self._group: str = validate.group(group)
        self._title: str = validate.title(title)
        self._description: str = validate.description(description)
        self._n: float = validate.n(n)
        self._variation_cols: MappingProxyType[str, str] = validate.variation_cols(variation_cols)
        self._variation_marks: MappingProxyType[str, str] = validate.variation_marks(variation_marks)
        self._metrics: MetricsObject = validate.metrics(metrics)
        self._extra_info: ImmutableCoreDataMappingType = validate.extra_info(extra_info)

    @classmethod
    def from_dict(cls, data: CoreDataMappingType) -> 'ResultsInfo':
        """Create a ResultsInfo object instance from a mapping of data conformant
        to the V1 results-info JSON schema.

        :param CoreDataMappingType data: Mapping containing the results-info object data.
        :return ResultsInfo: ResultsInfo instance.
        """
        allowed_keys = cls.init_params()
        allowed_keys['version'] = int
        allowed_keys['type'] = str

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'metrics': MetricsObject.from_dict})
        return cls(**kwargs)

    def to_dict(self) -> CoreDataMappingType:
        """Convert the ResultsInfo instance to a mapping suitable for serialization.

        :return CoreDataMappingType: Mapping containing the ResultsInfo object data.
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
        return validate_core_data_mapping(data, 'ResultsInfo.to_dict output',
                                          max_depth=10)

    @property
    def group(self) -> str:
        """Get the group property."""
        return self._group

    @property
    def title(self) -> str:
        """Get the title property."""
        return self._title

    @property
    def description(self) -> str:
        """Get the description property."""
        return self._description

    @property
    def n(self) -> float:
        """Get the n property."""
        return self._n

    @property
    def variation_cols(self) -> MappingProxyType[str, str]:
        """Get the variation columns.

        :return: A mapping of variation columns.
        """
        return self._variation_cols

    @property
    def metrics(self) -> MetricsObject:
        """Get the metrics.

        :return: The metrics dictionary.
        """
        return self._metrics

    @property
    def extra_info(self) -> ImmutableCoreDataMappingType:
        """Get the extra info.

        The extra info immutable mapping is returned.

        :return ImmutableCoreDataMappingType: The extra info immutable mapping.
        """
        return self._extra_info
