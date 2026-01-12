"""V1 Results object class

The V1 Results object represents the results metric of a version 1 JSON report.

"""
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, cast

from simplebench.report._base import BaseResultsInfo
from simplebench.types import (
    CoreDataMappingType,
    ImmutableCoreDataMappingType,
    ImmutableVariationMarksType,
    VariationMarksType,
)
from simplebench.validators import validate_core_data_mapping

from . import validate
from ._typeddict_types import ResultsInfoDict
from .results_info_schema import ResultsInfoSchema

_deferred_imports_done: bool = False

if TYPE_CHECKING:
    from .. import MetricsObject
    _deferred_imports_done = True
else:
    MetricsObject = None  # pylint: disable=invalid-name

def _deferred_imports() -> None:
    """Perform deferred imports to avoid circular dependencies."""
    global MetricsObject, _deferred_imports_done  # pylint: disable=global-statement
    if _deferred_imports_done:
        return
    from .. import MetricsObject  # pylint: disable=import-outside-toplevel
    _deferred_imports_done = True

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
                 variation_marks: VariationMarksType,
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
        :param VariationMarksType variation_marks: The variation marks mapping.
        :param MetricsObject metrics: The list of metrics.
        :param CoreDataMappingType extra_info: Additional information.
        """
        self._group: str = validate.group(group)
        self._title: str = validate.title(title)
        self._description: str = validate.description(description)
        self._n: float = validate.n(n)
        self._variation_marks: ImmutableVariationMarksType = validate.variation_marks(variation_marks)
        self._metrics: MetricsObject = validate.metrics(metrics)
        self._extra_info: ImmutableCoreDataMappingType = validate.extra_info(extra_info)
        self._to_dict_cache: ResultsInfoDict | None = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'ResultsInfo':
        """Create a ResultsInfo object instance from a mapping of data conformant
        to the V1 results-info JSON schema.

        :param ResultsInfoData data: Mapping containing the results-info object data.
        :return ResultsInfo: ResultsInfo instance.
        """
        _deferred_imports()

        allowed_keys = cls.init_params()  # Hydrate allowed keys from init params
        allowed_keys['version'] = int  # Allowed and checked if present, but not passed to init
        allowed_keys['type'] = str  # Allowed and checked if present, but not passed to init

        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'metrics': MetricsObject.from_dict})
        return cls(**kwargs)

    def to_dict(self) -> ResultsInfoDict:
        """Convert the ResultsInfo instance to an immutable ResultsInfoDict
        suitable for serialization.

        Results are cached after the first conversion. Because the ResultsInfo
        instance is immutable, the cached mapping is always valid for future calls.

        :return ResultsInfoDict: Immutable mapping containing the ResultsInfo object data.
        """
        if self._to_dict_cache is not None:
            return self._to_dict_cache

        property_keys = self.init_params(ResultsInfoDict).keys()
        data: dict[str, Any] = {}
        # This loop handles calling to_dict on any properties that
        # themselves have a to_dict method. This ensures nested objects,
        # known or unknown, are properly serialized in the future as needed.
        for key in property_keys:
            if key in {'type', 'version'}:
                continue
            value = getattr(self, key)
            to_dict_fn = getattr(value, "to_dict", None)
            data[key] = to_dict_fn() if callable(to_dict_fn) else value
        cls = self.__class__
        data['type'] = cls.TYPE
        data['version'] = cls.VERSION

        # We control the data structure here, so this cast is safe
        self._to_dict_cache = cast(ResultsInfoDict,
            validate_core_data_mapping(data, 'ResultsInfo.to_dict output'))
        return self._to_dict_cache

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
    def variation_marks(self) -> ImmutableVariationMarksType:
        """Get the variation marks.

        :return: The variation marks immutable mapping.
        """
        return self._variation_marks

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
