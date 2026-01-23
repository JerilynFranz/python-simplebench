"""V1 Results object class

The V1 Results object represents the results metric of a version 1 JSON report.

"""

from copy import copy
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from simplebench.report.base import BaseResultsInfo
from simplebench.simplebench_types import (
    CoreDataMappingType,
    ImmutableCoreDataMappingType,
    ImmutableVariationMarksType,
    VariationMarksType,
)

from . import _validate
from .results_info_schema import ResultsInfoSchema
from .typeddict_types import ImmutableResultsInfoDict, ResultsInfoData

if TYPE_CHECKING:
    from .. import MetricsObject

__all__ = []


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

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the ResultsInfo class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(ResultsInfoData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = (
        '_group',
        '_title',
        '_description',
        '_n',
        '_variation_marks',
        '_metrics',
        '_extra_info',
        '_to_dict_cache',
        '_hash_id',
    )

    def __init__(
        self,
        *,
        hash_id: str = '',
        group: str,
        title: str,
        description: str,
        n: float,
        variation_marks: VariationMarksType,
        metrics: 'MetricsObject',
        extra_info: CoreDataMappingType,
    ) -> None:
        """Initialize a Results v1 instance.

        The input parameters are validated, converted to immutable types as needed,
        and stored as private attributes that are accessible via read-only properties.

        :param str hash_id: The unique hash identifier for the results.
        :param str group: The group name of the results.
        :param str title: The title of the results.
        :param str description: The description of the results.
        :param n: The complexity analysis n value.
        :param float n: The n value.
        :param VariationMarksType variation_marks: The variation marks mapping.
        :param MetricsObject metrics: The list of metrics.
        :param CoreDataMappingType extra_info: Additional information.
        """
        self._group: str = _validate.group(group)
        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._n: float = _validate.n(n)
        self._variation_marks: ImmutableVariationMarksType = _validate.variation_marks(variation_marks)
        self._metrics: MetricsObject = _validate.metrics(metrics)
        self._extra_info: ImmutableCoreDataMappingType = _validate.extra_info(extra_info)
        self._hash_id: str = _validate.hash_id(hash_id)
        if not self._hash_id:
            self._hash_id: str = self._hash_id_helper(ResultsInfoData)
        self._to_dict_cache: ImmutableResultsInfoDict | None = None

    @classmethod
    def from_dict(cls, data: Any) -> 'ResultsInfo':
        """Create a ResultsInfo object instance from a mapping of data conformant
        to the V1 results-info JSON schema.

        :param ResultsInfoData data: Mapping containing the results-info object data.
        :return ResultsInfo: ResultsInfo instance.
        """
        from .. import MetricsObject

        allowed_keys = cls._data_params()
        kwargs = cls.import_data(
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'version', 'type'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'metrics': MetricsObject.from_dict},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableResultsInfoDict:
        """Convert the ResultsInfo instance to an immutable ResultsInfoDict
        suitable for serialization.

        Results are cached after the first conversion. Because the ResultsInfo
        instance is immutable, the cached mapping is always valid for future calls.

        :return ResultsInfoDict: Immutable mapping containing the ResultsInfo object data.
        """
        if self._to_dict_cache is None:
            self._to_dict_cache = self._to_dict_helper(ImmutableResultsInfoDict)
        return self._to_dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash ID of the ResultsInfo instance.

        The hash ID is a unique identifier based on the content of the instance.

        :return str: The hash ID string.
        """
        return self._hash_id

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
    def metrics(self) -> 'MetricsObject':
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

    def __eq__(self, other: object) -> bool:
        """Check equality between two ResultsInfo instances.

        .. note::
            Triggers the lazy eval properties to be evaluated if they have not been already.
            This ensures that comparisons are made based on the actual values of the properties.

            This can be expensive the first time it is called if many properties
            need to be calculated from many measurements.

            This is unavoidable since equality must reflect the actual state of the object.

        :param other: The other ResultsInfo instance to compare with.
        :return bool: True if the two ResultsInfo instances are equal, False otherwise.
        """
        if not isinstance(other, ResultsInfo):
            return NotImplemented

        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """Compute the hash of the ResultsInfo instance.

        The hash is computed from the hash_id.

        .. note::
            Triggers the lazy eval properties to be evaluated if they have not been already.
            This ensures that the hash is based on the actual values of the properties.

            This can be expensive the first time it is called if many properties
            need to be calculated from many measurements. This is unavoidable
            since the hash must reflect the actual state of the object.

        :return int: The hash value of the ResultsInfo instance.
        """
        return hash(self.hash_id)

    def __repr__(self) -> str:
        """Get the string representation of the ResultsInfo instance.

        The representation is a string that can be used to recreate the object.
        It triggers the lazy evaluation of any properties that have not been calculated yet.

        :return str: The string representation of the ResultsInfo.
        """
        # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the ResultsInfo
        is compact. It achieves this by forcing the calculation of any lazy-evaluated
        statistical properties and then excluding any attributes that are not part of the
        public interface of the ResultsInfo from the pickled state. Those excluded attributes
        can be recalculated upon unpickling on demand and do not need to be stored.

        This prioritizes a small pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # Sweep all slot attributes to force calculation of any lazy properties.
        # and collect any public attribute values for pickling.
        # This effectively forces all public lazy properties to be evaluated and
        # skips any non-public attributes that can be recalculated later.
        # By skipping non-public attributes, we reduce the pickled size by
        # about 50% for typical ResultsInfo instances.

        # Build a list of public attribute values based on the data params.
        # 'type' and 'version' are excluded since they are class-level constants
        # not stored as instance attributes.
        public_attrs = dict(self._data_params())
        public_attrs.pop('type', None)
        public_attrs.pop('version', None)
        slot_values: list[Any] = []
        for slot in self.__slots__:
            attr_name = slot.lstrip('_')
            if attr_name in public_attrs:
                slot_values.append(getattr(self, attr_name))
            else:
                slot_values.append(None)

        # Build the state tuple for a __slots__ class. The first element is for
        # __dict__ (None in our case) and the second is a tuple of the slotted values.
        state = tuple(slot_values)
        return (None, state)

    def __setstate__(self, state: tuple[dict[str, Any] | None, tuple[Any, ...]]) -> None:
        """Restore the object's state from a pickled representation.

        This method is the counterpart to `__getstate__`. It takes the state
        tuple and repopulates the instance's `__slots__`.

        .. note::
            This method bypasses `__init__`, which is standard for unpickling.

        :param state: The state tuple from unpickling.
        :type state: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # The first element of the state tuple is for __dict__, which is None for this class.
        # The second element is a tuple of values for the __slots__.
        slot_values = state[1]
        for slot, value in zip(self.__slots__, slot_values, strict=True):
            # Use object.__setattr__ to bypass our immutable setters.
            object.__setattr__(self, slot, value)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'ResultsInfo':
        """Return a shallow copy of the instance as an optimized deep copy.

        Since the ResultsInfo instance is immutable and composed of immutable components,
        a shallow copy is functionally identical to a deep copy. This method overrides
        the default `copy.deepcopy` behavior to perform a more efficient shallow copy instead.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return ResultsInfo: A new, shallow-copied instance of the ResultsInfo.
        """
        # because the ResultsInfo is immutable, we can return a copy of self
        # instead of performing a full deep copy.
        return copy(self)
