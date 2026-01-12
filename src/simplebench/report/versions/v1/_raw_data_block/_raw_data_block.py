"""Class for JSON raw data block representation."""

from collections.abc import Mapping, Sequence
from copy import copy
from typing import Any

from simplebench.report.base import BaseRawDataBlock, JSONSchema
from simplebench.types import Values

from . import _validate
from ._raw_data_block_dict import ImmutableRawDataBlockDict, RawDataBlockData
from ._raw_data_block_schema import RawDataBlockSchema


class RawDataBlock(BaseRawDataBlock):
    """Class representing a raw data block (V1).
    :param str semantic_type: The semantic type string for the raw data block. ('type' field in JSON data)
    :param (str | None) timer: The timer string or None.
    :param str unit: The unit of measurement.
    :param float scale: The scale factor.
    :param Values data: The raw data values of the block.
    :raise SimpleBenchTypeError: If any parameter is of incorrect type.
    :raise SimpleBenchValueError: If any parameter has an invalid value.
    """

    SCHEMA: type[JSONSchema] = RawDataBlockSchema
    """JSON schema class for the raw data block."""

    VERSION: int = SCHEMA.VERSION
    """Version of the raw data block schema."""

    TYPE: str = SCHEMA.TYPE
    """Type of the raw data block schema."""

    ID: str = SCHEMA.ID
    """ID of the raw data block schema."""

    _init_params_cache: dict[str, Any] = {}
    """Cache for the constructor parameters of the RawDataBlock class."""

    @classmethod
    def _raw_data_block_params(cls) -> dict[str, Any]:
        """Get the constructor parameters for the RawDataBlock class.
        The parameters are cached after the first call for performance.

        :return dict[str, Any]: A dictionary of constructor parameter names and types.
        """
        if not cls._init_params_cache:
            params = cls.init_params(RawDataBlockData)
            params.pop('type', None)
            params.pop('version', None)
            cls._init_params_cache = params

        return cls._init_params_cache

    __slots__ = ('_hash_id', '_semantic_type', '_timer', '_unit', '_scale', '_data', '_to_dict_cache')

    def __init__(
        self,
        *,
        hash_id: str = '',
        semantic_type: str,
        timer: str | None = None,
        unit: str,
        scale: float,
        data: Sequence[int | float] | Values,
    ) -> None:
        """Initialize RawDataBlock class.

        :param str hash_id: The hash ID string for the raw data block.
        :param str semantic_type: The semantic type string for the raw data block.
        :param (str | None) timer: The timer string or None.
        :param str unit: The unit of measurement.
        :param float scale: The scale factor.
        :param Values data: The raw data values of the block.
        :param (str | None) timer: The timer string or None.
        :raise SimpleBenchTypeError: If any parameter is of incorrect type.
        :raise SimpleBenchValueError: If any parameter has an invalid value.
        """
        self._hash_id: str = _validate.hash_id(hash_id)
        self._semantic_type: str = _validate.semantic_type(semantic_type)
        self._timer: str | None = _validate.timer(timer)
        self._unit: str = _validate.unit(unit)
        self._scale: float = _validate.scale(scale)
        self._data: Values = _validate.data(data)
        if self._hash_id == '':
            self._hash_id = self._hash_id_helper(RawDataBlockData)

        self._to_dict_cache: ImmutableRawDataBlockDict | None = None  # Cache for to_dict output

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> 'RawDataBlock':
        """Create a RawDataBlock instance from a dictionary that represents the
        JSON raw data block. It must conform to the :class:`RawDataBlockSchema`.

        :param data: Dictionary containing the JSON raw data block data.
        :return RawDataBlock: A RawDataBlock instance.
        """
        init_params = cls._raw_data_block_params()
        init_params['type'] = str
        init_params['version'] = int
        kwargs = cls.import_data(
            data=data,
            allowed_fields=init_params,
            skip_fields={'type', 'version'},
            optional_fields={'timer', 'type', 'version', 'hash_id'},
            defaults={'type': cls.TYPE, 'version': cls.VERSION},
            match_on={'type': cls.TYPE, 'version': cls.VERSION},
            process_as={'data': Values},
        )
        return cls(**kwargs)

    def to_dict(self) -> ImmutableRawDataBlockDict:
        """Convert the RawDataBlock instance to a dictionary.

        The returned dictionary conforms to the 'shape' of the :class:`RawDataBlockDict` type,
        is immutable, and can be serialized to JSON.

        :return ImmutableRawDataBlockDict: Dictionary representation of the RawDataBlock instance.
        """
        if self._to_dict_cache is None:
            self._to_dict_cache = self._to_dict_helper(ImmutableRawDataBlockDict)
        return self._to_dict_cache

    @property
    def hash_id(self) -> str:
        """Get the hash ID of the raw data block.

        :return str: The hash ID of the raw data block.
        """
        return self._hash_id

    @property
    def semantic_type(self) -> str:
        """Get the semantic type value.

        :return str: The semantic type value.
        """
        return self._semantic_type

    @property
    def unit(self) -> str:
        """Get the unit of measurement.

        :return str: The unit of measurement.
        """
        return self._unit

    @property
    def scale(self) -> float:
        """Get the scale factor.

        :return float: The scale factor.
        :raise SimpleBenchTypeError: If scale is not a float.
        """
        return self._scale

    @property
    def timer(self) -> str | None:
        """Get the timer.

        :return str | None: The timer.
        """
        return self._timer

    @property
    def data(self) -> Values:
        """Get the data.

        :return Values: The data.
        """
        return self._data

    def __repr__(self) -> str:
        """Get the string representation of the RawDataBlock instance.

        :return str: String representation of the RawDataBlock instance.
        """
        return (
            f'RawDataBlock(hash_id={self.hash_id!r}, '
            f'semantic_type={self.semantic_type!r}, '
            f'timer={self.timer!r}, '
            f'unit={self.unit!r}, scale={self.scale!r}, '
            f'data={self.data!r})'
        )

    def __eq__(self, other: object) -> bool:
        """Check equality between two RawDataBlock instances.

        :param other: The other object to compare with.
        :return bool: `True` if both instances are equal, `False` otherwise.
        """
        if not isinstance(other, RawDataBlock):
            return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self) -> int:
        """Get the hash of the RawDataBlock instance.

        :return int: Hash of the RawDataBlock instance.
        """
        return hash(self.hash_id)

    def __getstate__(self) -> tuple[dict[str, Any] | None, tuple[Any, ...]]:
        """Prepare the object's state for pickling, prioritizing size.

        This method ensures that the pickled representation of the RawDataBlock
        is compact. It achieves this by forcing the calculation of any lazy-evaluated
        statistical properties and then excluding any attributes that are not part of the
        public interface of the RawDataBlock from the pickled state. Those excluded attributes
        can be recalculated upon unpickling on demand and do not need to be stored.

        This prioritizes a smaller pickled size and fast subsequent unpickling over
        preserving the lazy-evaluation state across serialization.

        :return: A state tuple for pickling.
        :rtype: tuple[dict[str, Any] | None, tuple[Any, ...]]
        """
        # Sweep all slot attributes to force calculation of any lazy properties.
        # and collect any public attribute values for pickling.
        public_attrs = self._raw_data_block_params()
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
        for slot, value in zip(self.__slots__, slot_values):
            # Use object.__setattr__ to bypass our immutable setters.
            object.__setattr__(self, slot, value)

    def __deepcopy__(self, memo: dict[int, Any]) -> 'RawDataBlock':
        """Return a shallow copy of the instance as an optimized deep copy.

        Since the RawDataBlock instance is immutable and composed of immutable components,
        a shallow copy is functionally identical to a deep copy. This method overrides
        the default `copy.deepcopy` behavior to perform a more efficient shallow copy instead.

        :param memo: The memoization dictionary used by `copy.deepcopy`.
                     It is not used in this optimized implementation.
        :return RawDataBlock: A new, shallow-copied instance of the RawDataBlock.
        """
        # because the RawDataBlock is immutable, we can return a copy of self
        return copy(self)
