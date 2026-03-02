"""Report version 1 class.

The Report class represents a version 1 report.

It provides methods to convert to and from dictionary representations
and includes schema validation specific to version 1 reports.

It's primarily used for handling benchmark reports in SimpleBench.

The to_dict and from_dict methods facilitate safe serialization and
deserialization of report data.

The version 1 report is the first stable version of the report format
and serves as a foundation for future versions.
"""

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from simplebench.report._error_tags import _ReportErrorTag
from simplebench.report.base import BaseReport, JSONSchema
from simplebench.report.versions.v1 import MachineInfo
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, VariationCols
from simplebench.validators import validate_sequence_of_type

from . import _validate
from .report_schema import ReportSchema
from .typeddict_types import ImmutableReportDict, ReportData

if TYPE_CHECKING:
    from .. import ResultsInfo


class Report(BaseReport):
    """Immutable class representing a version 1 report."""

    SCHEMA: type[JSONSchema] = ReportSchema
    """The JSON schema class for version 1 reports."""

    TYPE: str = SCHEMA.TYPE
    """The JSON report type property value for version 1 reports."""

    VERSION: int = SCHEMA.VERSION
    """The JSON report version number."""

    ID: str = SCHEMA.ID
    """The JSON report ID property value for version 1 reports."""


    @classmethod
    def _data_params(cls) -> dict[str, Any]:
        """Get the constructor parameters for the schema data class.

        :return dict[str, Any]: A dictionary of constructor parameter names and types.
        """
        from simplebench.report.versions.v1 import ResultsInfo
        return {
            'hash_id': str,
            'timestamp': str,
            'group': str,
            'title': str,
            'description': str,
            'variation_cols': VariationCols,
            'results': Sequence[ResultsInfo],
            'machine': MachineInfo,
        }

    __slots__ = (
        '_timestamp',
        '_group',
        '_title',
        '_description',
        '_variation_cols',
        '_results',
        '_machine',
        '_hash_id',
        '_to_dict_cache',
    )

    def __init__(
        self,
        *,
        hash_id: str = '',
        timestamp: str,
        group: str,
        title: str,
        description: str,
        variation_cols: VariationCols,
        results: Sequence['ResultsInfo'],
        machine: MachineInfo,
    ) -> None:
        """Initialize a Report instance.

        :param str hash_id: The unique hash identifier for the report.
        :param str timestamp: ISO 8601 formatted timestamp string.
        :param str group: Group of the benchmark.
        :param str title: Title of the benchmark.
        :param str description: Description of the benchmark.
        :param VariationCols variation_cols: Variation columns dictionary.
        :param Sequence[ResultsInfo] results: Sequence of ResultsInfo instances.
        :param MachineInfo machine: MachineInfo instance.
        :raises SimpleBenchTypeError: If any parameter is of incorrect type.
        :raises SimpleBenchValueError: If any parameter has an invalid value.
        """
        self._timestamp: str = _validate.timestamp(timestamp)
        self._group: str = _validate.group(group)
        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._variation_cols: VariationCols = _validate.variation_cols(variation_cols)
        self._results: tuple[ResultsInfo, ...] = _validate.results(results)
        self._machine: MachineInfo = _validate.machine(machine)
        self._hash_id = _validate.hash_id(hash_id)
        if not self._hash_id:
            self._hash_id = self._hash_id_helper(ReportData)
        self._to_dict_cache: ImmutableReportDict | None = None
        """Private backing attribute for cached immutable dictionary representation of the Report instance.

        It is initialized to None and populated on the first call to to_dict().
        It is used to improve performance by avoiding redundant conversions
        and it is type cast to :class:`ImmutableReportDict` for
        static type checking.
        """

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'Report':
        """Create a Report instance from a dictionary.

        The input dictionary is validated against the rules for the version 1 report schema.

        :param Mapping[str, Any] data: Dictionary containing the JSON structured report data.
        :return Report: Report instance.
        :raises SimpleBenchValueError: If any field has an invalid value.
        :raises SimpleBenchTypeError: If any field is of an incorrect type.
        """
        from simplebench.report.versions.v1 import ResultsInfo

        allowed_keys = dict(cls._data_params())
        allowed_keys['type'] = str
        allowed_keys['version'] = int
        def process_results(value: Any) -> list[ResultsInfo]:
            """Process the results-info objects in the input sequence"""
            validated_list = validate_sequence_of_type(
                value,
                dict,
                'results',
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_NOT_A_SEQUENCE,
                _ReportErrorTag.INVALID_RESULTS_PROPERTY_ELEMENT_NOT_DICT,
                allow_empty=False,
            )
            return [ResultsInfo.from_dict(item) for item in validated_list]

        kwargs = cls.import_data(  # Hydrate instance arguments from dict
            data=data,
            allowed_fields=allowed_keys,
            skip_fields={'version', 'type'},
            optional_fields={'version', 'type', 'hash_id'},
            defaults={'version': cls.VERSION, 'type': cls.TYPE, 'hash_id': ''},
            match_on={'version': cls.VERSION, 'type': cls.TYPE},
            process_as={'results': process_results,
                        'machine': MachineInfo.from_dict,
                        'variation_cols': VariationCols},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableReportDict:
        """Convert the Report instance to a dictionary.

        The output dictionary conforms to the version 1 report schema
        and is suitable for serialization to JSON. It is immutable and cached
        for efficiency and is type cast to :class:`ImmutableReportDict` for
        static type checking.

        :return ImmutableReportDict: Immutable dictionary containing the JSON report data.
        """
        if self._to_dict_cache is None:
            self._to_dict_cache = CoreDataMapping({
                'timestamp': self.timestamp,
                'group': self.group,
                'title': self.title,
                'description': self.description,
                'variation_cols': self.variation_cols,
                'results': CoreDataSequence([result.to_dict() for result in self.results]),  # type: ignore
                'machine': self.machine.to_dict(),  # type: ignore
                'type': self.TYPE,
                'version': self.VERSION,
                'hash_id': self.hash_id,
            })  # type: ignore
        return self._to_dict_cache  # type: ignore

    def for_json(self) -> dict[str, Any]:
        """Convert the Report instance to a JSON-serializable dictionary.

        This method is used for JSON serialization and returns a standard
        dictionary representation of the report data. It is not cached and is
        not type cast to :class:`ImmutableReportDict` since it is intended for
        immediate serialization rather than long-term storage.

        :return dict[str, Any]: A JSON-serializable dictionary representation of the report.
        """

        return self.to_dict().thaw()  # type: ignore

    def as_json(self) -> str:
        """Convert the Report instance to a JSON string.

        This method is a convenience for directly obtaining a JSON string
        representation of the report. It uses the for_json method to get a
        JSON-serializable dictionary and then serializes it to a JSON string.

        :return str: A JSON string representation of the report.
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the unique hash identifier for the report.

        The hash_id is a unique identifier derived from the content of the report.
        It is used for hashing and equality comparisons.

        :return str: The unique hash identifier for the report.
        """
        return self._hash_id

    @property
    def timestamp(self) -> str:
        """Get the timestamp property.

        :return str: The ISO 8601 formatted timestamp string.
        """
        return self._timestamp

    @property
    def group(self) -> str:
        """Get the group property.

        :return str: The group string.
        """
        return self._group

    @property
    def title(self) -> str:
        """Get the title property.

        :return str: The title string.
        """
        return self._title

    @property
    def description(self) -> str:
        """Get the description property.

        :return str: The description string.
        """
        return self._description

    @property
    def variation_cols(self) -> VariationCols:
        """Return the variation_cols property.

        :return VariationCols: The variation_cols dictionary as an immutable mapping.
        """
        return self._variation_cols

    @property
    def results(self) -> tuple['ResultsInfo', ...]:
        """Get the results property.

        The results property is a tuple of ResultsInfo instances.

        :return tuple[ResultsInfo]: The results tuple.
        """
        return self._results

    @property
    def machine(self) -> MachineInfo:
        """Get the machine property."""
        return self._machine

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the Report instance
        is compact. It excludes calculated properties like `_to_dict_cache`.
        This decreases the pickled size by about 50%, which can significantly improve
        pickling and unpickling performance, especially for large reports. 

        This prioritizes a smaller pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # Sweep all slot attributes to force calculation of any lazy properties.
        # and collect any public attribute values for pickling. The non-public
        # attributes will be excluded from the pickled state and can be
        # recalculated on demand after unpickling. This keeps the pickled
        # representation minimal and about 50% smaller. Which is significant
        # for large datasets.
        # 'version' and 'type' are excluded as they are class constants not
        # instance attributes and can be inferred.
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
            object.__setattr__(self, slot, value)

    def __hash__(self) -> int:
        """Compute a hash value for the Report instance.

        The hash is based on the unique `hash_id` property, which is derived
        from the report's content. This ensures that reports with identical
        content will have the same hash value, while different reports will
        have different hash values.

        :return int: The hash value of the Report instance.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Report instance.

        Two Report instances are considered equal if their hash_id properties are equal.

        :param object other: The object to compare with.
        :return bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Report):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'Report':
        """Create a copy of the Report instance.

        Since the Report class is immutable, this method simply returns the same instance.

        :return Report: The same Report instance (since it's immutable).
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'Report':
        """Create a deep copy of the Report instance.

        Since the Report class is immutable, this method simply returns the same instance.

        :param dict[int, Any] memo: The memoization dictionary for deepcopy (ignored).
        :return Report: The same Report instance (since it's immutable).
        """
        return self

    def __repr__(self) -> str:
        """Return a string representation of the Report instance.

        :return str: A string representation of the Report instance.
        """
         # Get the init parameters excluding 'type' and 'version'
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'
