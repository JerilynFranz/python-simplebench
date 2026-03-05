"""Definition for a metric for the simplebench library."""
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any, cast

from simplebench.report.base import JSONSchema, ReportElement
from simplebench.simplebench_types import CoreDataMapping

from ..metric_category import MetricCategory
from . import _validate
from .metric_type_schema import MetricTypeSchema
from .typed_dict import ImmutableMetricTypeDict, MetricTypeData

__all__: list[str] = []

class MetricType(ReportElement):
    """Definition for a metric type.

    This class defines a metric type with a name, semantic type, label, description, unit, scale and category.
    It includes validation logic for each field and can be initialized from a dictionary or converted to a
    dictionary for JSON serialization.

    Metrics types define the semantics of the metric, including its meaning, how it should be interpreted,
    units, and how it should be scaled. They are used to provide context and meaning to the metric data.

    :ivar str semantic_type: The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'
    :ivar str label: The label of the metric, e.g. 'OPS_PER_SEC'
    :ivar str description: The description of the metric, e.g. 'Operations per second'
    :ivar str unit: The unit of the metric, e.g. 'ops/s'
    :ivar float scale: The scale of the metric, e.g. 1.0. Accepts an int or float and converts it to a float.
    :ivar MetricCategory category: The type of the metric
        - :attr:`MetricCategory.VALUE`
        - :attr:`MetricCategory.STATS`
        - :attr:`MetricCategory.RAW_DATA`
    """

    SCHEMA: type[JSONSchema] = MetricTypeSchema
    """JSON schema class for the metric type."""

    VERSION: int = SCHEMA.VERSION
    """Version of the metric type schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the metric type schema."""

    ID: str = SCHEMA.ID
    """ID of the metric type schema."""

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
            params = cls.init_params(MetricTypeData)
            cls._init_params_cache = MappingProxyType(params)
        return cls._init_params_cache

    __slots__ = ('_semantic_type', '_label', '_description', '_unit', '_scale', '_category', '_hash_id')

    def __init__(self, *,
                 hash_id: str = '',
                 semantic_type: str,
                 label: str,
                 description: str,
                 unit: str,
                 scale: float | int,
                 category: MetricCategory) -> None:
        """Initialize a MetricType instance.

        :param hash_id: The hash ID of the metric type. This is an optional field that can be used to uniquely
            identify the metric type.
        :type hash_id: str
        :param semantic_type: The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'
        :type semantic_type: str
        :param label: The label of the metric, e.g. 'OPS_PER_SEC'
        :type label: str
        :param description: The description of the metric, e.g. 'Operations per second'
        :type description: str
        :param unit: The unit of the metric, e.g. 'ops/s'
        :type unit: str
        :param scale: The scale of the metric, e.g. 1.0. Accepts an int or float and converts it to a float.
        :type scale: float | int
        :param category: The type of the metric
            - :attr:`MetricCategory.VALUE`
            - :attr:`MetricCategory.STATS`
            - :attr:`MetricCategory.RAW_DATA`
        :type category: MetricCategory
        """
        self._label: str = _validate.label(label)
        self._description: str = _validate.description(description)
        self._unit: str = _validate.unit(unit)
        self._scale: float = _validate.scale(scale)
        self._semantic_type: str = _validate.semantic_type(semantic_type)
        self._category: MetricCategory = _validate.category(category)
        self._hash_id : str = _validate.hash_id(hash_id) or self._hash_id_helper(MetricTypeData)

    @staticmethod
    def _metric_category_helper(category: str) -> MetricCategory:
        """Helper function to convert a MetricCategory value to an enum.

        :param category: The category value to convert.
        :type category: str
        :return: The corresponding MetricCategory enum value.
        :rtype: MetricCategory
        """
        return MetricCategory[category]

    @classmethod
    def from_dict(cls, data: Mapping[str, float | int | str]) -> 'MetricType':
        """Initialize the MetricType instance from a dictionary.

        :param data: The dictionary containing the metric type data.
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
            process_as={'category': cls._metric_category_helper},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableMetricTypeDict:
        """Convert the MetricType instance to a dictionary.

        Returns an immutable dictionary representation of the MetricType instance.
        It is actually a :class:`~simplebench.simplebench_types.CoreDataMapping` instance, but it is cast to an
        :class:`~simplebench.report.versions.v1.metric_type.ImmutableMetricTypeDict` for type checking purposes.

        :return: A dictionary representation of the MetricType instance.
        :rtype: ImmutableMetricTypeDict
        """
        return cast(ImmutableMetricTypeDict,
            CoreDataMapping({
                'type': self.TYPE,
                'version': self.VERSION,
                'hash_id': self.hash_id,
                'semantic_type': self.semantic_type,
                'label': self.label,
                'description': self.description,
                'unit': self.unit,
                'scale': self.scale,
                'category': self.category.value,
            }))

    def for_json(self) -> ImmutableMetricTypeDict:
        """Convert the MetricType instance to a JSON-serializable dictionary.

        This is the same as `to_dict` since the output of `to_dict` is already JSON-serializable.

        :return: A JSON-serializable dictionary representation of the MetricType instance.
        :rtype: ImmutableMetricTypeDict
        """
        return self.to_dict().for_json()  # type: ignore

    def as_json(self) -> str:
        """Convert the MetricType instance to a JSON string.

        :return: A JSON string representation of the MetricType instance.
        :rtype: str
        """
        return self.to_dict().as_json()  # type: ignore

    @property
    def semantic_type(self) -> str:
        """The semantic type of the metric, e.g. 'simplebench_std::operations_per_second'
        """
        return self._semantic_type

    @property
    def label(self) -> str:
        """The label of the metric, e.g. 'OPS_PER_SEC'"""
        return self._label

    @property
    def description(self) -> str:
        """The description of the metric, e.g. 'Operations per second'"""
        return self._description

    @property
    def unit(self) -> str:
        """The unit of the metric, e.g. 'ops/s'"""
        return self._unit

    @property
    def scale(self) -> float:
        """The scale of the metric, e.g. 1.0"""
        return self._scale

    @property
    def category(self) -> MetricCategory:
        """The type of the metric, e.g. :attr:`MetricCategory.VALUE`, :attr:`MetricCategory.STATS`
        or :attr:`MetricCategory.RAW_DATA`"""
        return self._category

    @property
    def hash_id(self) -> str:
        """The hash ID of the metric type."""
        return self._hash_id

    def __repr__(self) -> str:
        """Get the string representation of the MetricType instance.

        :return: The string representation of the MetricType instance.
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
        """Get the hash of the MetricType instance.

        :return: The hash value.
        """
        return hash(self.hash_id)

    def __eq__(self, other: object) -> bool:
        """Check equality between two MetricType instances.

        :param other: The other object to compare.
        :return: True if equal, False otherwise.
        """
        if not isinstance(other, MetricType):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __copy__(self) -> 'MetricType':
        """Create a copy of the MetricType instance.

        It returns self since the MetricType instance is immutable and can be shared safely.

        :return: The MetricType instance.
        :rtype: MetricType
        """
        return self

    def __deepcopy__(self, memo: dict[int, Any]) -> 'MetricType':
        """Create a deep copy of the MetricType instance.

        It returns self since the MetricType instance is immutable and can be shared safely.

        """
        return self
