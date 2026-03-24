"""Metric class to represent the metric for evaluation.

The Metric class represents a metric definition used in the benchmarking report.

It includes attibutes such as :attr:`label`, :attr:`title`, :attr:`description`,
and :attr:`metric_type`. It is immutable and provides methods for serialization
to and from dictionaries.

The MetricType field properties (unit, scale, category, semantic_type, type_label, type_description) are
exposed as properties on the Metric class for convenient access, but they are derived from the MetricType instance.

The Metric class also implements the Mapping interface, allowing access to its fields using dictionary-like syntax.
The MetricType properties are not directly accessible as keys in the mapping interface,
but the 'metric_type' key returns the dictionary representation of
the MetricType instance (a :class:`CoreDataMapping` that is type cast to
:class:`ImmutableMetricTypeDict`) to ensure that the mapping interface returns
only serializable data.
"""
from collections.abc import Iterator, KeysView, Mapping, ValuesView
from types import MappingProxyType
from typing import Any

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.report._error_tags import _MetricErrorTag
from simplebench.report.base import JSONSchema, ReportElement
from simplebench.simplebench_types import Never

from ..metric_type import ImmutableMetricTypeDict, MetricType, MetricTypeData
from . import _validate
from .metric_schema import MetricSchema
from .metric_dict import ImmutableMetricDict, MetricData

__all__: list[str] = []


class Metric(ReportElement, Mapping[str, str | int | ImmutableMetricTypeDict]):
    """Metric class to define a metric for use."""

    SCHEMA: type[JSONSchema] = MetricSchema
    """JSON schema class for the metric type."""

    VERSION: int = SCHEMA.VERSION
    """Version of the metric schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the metric schema."""

    ID: str = SCHEMA.ID
    """ID of the metric schema."""

    _init_params_cache: MappingProxyType[str, Any] = MappingProxyType({})
    """Cache for the constructor parameters of the MetricType class."""

    @classmethod
    def _data_params(cls) -> MappingProxyType[str, Any]:
        """Get the constructor parameters for the schema data class.

        The parameters are cached after the first call for performance.

        It is returned as a read-only mapping and includes 'type' and 'version'.

        :return MappingProxyType[str, Any]: A read-only mapping of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(MetricData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ['_label', '_title', '_description', '_metric_type', '_hash_id', '_dict_cache']

    def __init__(self, *,
                 hash_id: str = '',
                 label: str,
                 title: str,
                 description: str,
                 metric_type: MetricType) -> None:
        self._label: str = _validate.label(label)
        self._title: str = _validate.title(title)
        self._description: str = _validate.description(description)
        self._metric_type: MetricType = _validate.metric_type(metric_type)
        self._hash_id: str = _validate.hash_id(hash_id) or self._hash_id_helper(MetricData)
        self._dict_cache: ImmutableMetricDict = self._to_dict_helper(ImmutableMetricDict)

    @classmethod
    def from_dict(cls, data: Mapping[str, int | str | MetricTypeData]) -> 'Metric':
        """Initialize the Metric instance from a dictionary.

        :param data: The dictionary containing the metric data.
        :type data: dict
        """
        init_params = cls._data_params()
        kwargs = cls.import_data(
            data=data,
            allowed_fields=init_params,
            skip_fields={'type', 'version'},
            optional_fields={'type', 'version', 'hash_id'},
            defaults={'type': cls.TYPE, 'version': cls.VERSION},
            match_on={'type': cls.TYPE, 'version': cls.VERSION},
            process_as={'metric_type': MetricType.from_dict},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableMetricDict:
        """Convert the Metric instance to a dictionary.

        Returns an immutable dictionary representation of the Metric instance.
        It is actually a :class:`~simplebench.simplebench_types.CoreDataMapping` instance, but it is cast to an
        :class:`~simplebench.report.versions.v1.metric.ImmutableMetricDict` for type checking purposes.

        :return: A dictionary representation of the Metric instance.
        :rtype: ImmutableMetricDict
        """
        return self._dict_cache

    def for_json(self) -> ImmutableMetricDict:
        """Convert the Metric instance to a JSON-serializable dictionary.

        This is the same as `to_dict` since the output of `to_dict` is already JSON-serializable.

        :return: A JSON-serializable dictionary representation of the Metric instance.
        :rtype: ImmutableMetricDict
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Convert the Metric instance to a JSON string.

        :return: A JSON string representation of the Metric instance.
        :rtype: str
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def hash_id(self) -> str:
        """Get the hash_id of the metric.

        :return: The hash_id of the metric.
        :rtype: str
        """
        return self._hash_id

    @property
    def label(self) -> str:
        """Get the label of the metric.

        :return: The label of the metric.
        :rtype: str
        """
        return self._label

    @property
    def title(self) -> str:
        """Get the title of the metric.

        :return: The title of the metric.
        :rtype: str
        """
        return self._title

    @property
    def description(self) -> str:
        """Get the description of the metric.

        :return: The description of the metric.
        :rtype: str
        """
        return self._description

    @property
    def unit(self) -> str:
        """Get the unit of the metric.

        :return: The unit of the metric.
        :rtype: str
        """
        return self.metric_type.unit

    @property
    def scale(self) -> float:
        """Get the scale of the metric.

        :return: The scale of the metric.
        :rtype: float
        """
        return self.metric_type.scale

    @property
    def category(self) -> str:
        """Get the category of the metric.

        :return: The category of the metric.
        :rtype: str

        """
        return self.metric_type.category.value

    @property
    def semantic_type(self) -> str:
        """Get the semantic type of the metric.

        :return: The semantic type of the metric.
        :rtype: str
        """
        return self.metric_type.semantic_type

    @property
    def type_label(self) -> str:
        """Get the type label of the metric.

        :return: The type label of the metric.
        :rtype: str
        """
        return self.metric_type.label

    @property
    def type_description(self) -> str:
        """Get the type description of the metric.

        :return: The type description of the metric.
        :rtype: str
        """
        return self.metric_type.description

    @property
    def metric_type(self) -> MetricType:
        """Get the metric type of the metric.

        :return: The metric type of the metric.
        :rtype: MetricType
        """
        return self._metric_type

    def __repr__(self) -> str:
        """Get the string representation of the Metric instance.

        :return: The string representation of the Metric instance.
        :rtype: str
        """
        # Get the init parameters excluding 'type' and 'version' since they are fixed for this class
        init_params = dict(self._data_params())
        init_params.pop('type', None)
        init_params.pop('version', None)

        # Build the key-value argument string. Accessing the properties via getattr
        # will trigger their lazy calculation if they haven't been computed yet.
        calling_args = ', '.join(f'{key}={getattr(self, key)!r}' for key in init_params)
        return f'{self.__class__.__name__}({calling_args})'

    def __hash__(self) -> int:
        """Get the hash of the Metric instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two Metric instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        :rtype: bool
        :raises SimpleBenchTypeError: If the other value is not a Metric instance.
        """
        if not isinstance(other, Metric):
            raise SimpleBenchTypeError(
                f'Cannot compare Metric with {type(other).__name__!r}',
                tag=_MetricErrorTag.COMPARISON_TYPE_ERROR)
        return self.hash_id == other.hash_id

    def __lt__(self, other: object) -> bool:
        """Less than comparison between two Metric instances based on their labels.

        :param other: The other Metric instance to compare with.
        :type other: object
        :returns: True if this Metric's label is less than the other Metric's label, False otherwise.
        :rtype: bool
        :raises SimpleBenchTypeError: If the other value is not a Metric instance.
        """

        if not isinstance(other, Metric):
            raise SimpleBenchTypeError(
                f'Cannot compare Metric with {type(other).__name__!r}',
                tag=_MetricErrorTag.COMPARISON_TYPE_ERROR)
        return self.label < other.label

    def __copy__(self) -> 'Metric':
        """Create a copy of the Metric instance.

        It returns self since the Metric instance is immutable and can be shared safely.

        :return: The Metric instance.
        :rtype: Metric
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'Metric':
        """Create a deep copy of the Metric instance.

        It returns self since the Metric instance is immutable and can be shared safely.

        """
        return self

    def __getitem__(self, key: str) -> str | int | ImmutableMetricTypeDict:
        """Get the value for the given key.

        It only allows keys that are defined in MetricData.
        For the 'metric_type' field, it returns the dictionary representation
        of the MetricType instance instead of the instance itself.
        This is to ensure that the mapping interface returns only serializable data.

        It also allows 'type' and 'version' as keys, which return the class-level
        TYPE and VERSION attributes, respectively. It does not allow any other keys and will raise a
        SimpleBenchKeyError if the key is not found.

        :param key: The key.
        :type key: str
        :returns: The corresponding value
        :rtype: str | int | ImmutableMetricTypeDict
        :raises SimpleBenchKeyError: If the key is not found.
        """
        if key not in self._dict_cache:
            raise SimpleBenchKeyError(
                f'Key {key!r} not found in Metric. Valid keys are: {self._dict_cache.keys()}',
                tag=_MetricErrorTag.MAPPING_KEY_ERROR)
        return self._dict_cache[key]  # type: ignore

    def get(self, key: str) -> str | int | ImmutableMetricTypeDict:  # type: ignore
        """Get the value for the given key, or raise an error if the key is not found.

        It does not support a default value since Metric is immutable and all valid keys should
        always be present. This is a deliberate design choice to ensure that any access
        to a key that is not defined results in an error.

        If a key is accessed that is not defined, it indicates a bug in the code
        that needs to be fixed, rather than a case where a default value would be appropriate.

        :param key: The key.
        :type key: str
        :returns: The corresponding value.
        :rtype: str | int | ImmutableMetricTypeDict
        """
        return self.__getitem__(key)

    def __setitem__(self, key: str, value: Never) -> None:
        """Always raises an error since Metric is immutable and does
        not support item assignment.

        :param key: The key to set.
        :type key: str
        :param value: The value to set.
        :type value: Never
        :raises SimpleBenchTypeError: Always, since Metric is immutable.
        """
        raise SimpleBenchTypeError(
            'Metric is immutable and does not support item assignment.',
            tag=_MetricErrorTag.MAPPING_IMMUTABLE)

    def __contains__(self, key: object) -> bool:
        """Check if the Metric contains the given key.

        :param key: The key to check.
        :type key: object
        :returns: True if the key is in the Metric, False otherwise.
        :rtype: bool
        """
        return key in self._dict_cache

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the Metric.

        This iterates over the keys defined in :class:`MetricData`,
        which are the valid fields for the Metric.

        :returns: An iterator over the keys in the Metric.
        :rtype: Iterator[str]
        """
        yield from self._dict_cache.keys()

    def __len__(self) -> int:
        """Return the number of elements in the Metric.

        :returns: The number of elements in the Metric.
        :rtype: int
        """
        return len(self._dict_cache)

    def keys(self) -> KeysView[str]:
        """Return the set of keys in the Metric.

        This returns the keys defined in :class:`MetricData`,
        which are the valid fields for the Metric.
        :returns: The keys in the Metric.
        :rtype: KeysView[str]
        """
        return self._dict_cache.keys()  # type: ignore

    def values(self) -> ValuesView[str | int | ImmutableMetricTypeDict]:
        """Return the values in the Metric.

        This returns the values corresponding to the keys defined in :class:`MetricData
        which are the valid fields for the Metric. For the 'metric_type' field, it returns the dictionary
        representation of the MetricType instance instead of the instance itself.
        :returns: The values in the Metric.
        :rtype: ValuesView[str | int | ImmutableMetricTypeDict]
        """
        return self._dict_cache.values()  # type: ignore
