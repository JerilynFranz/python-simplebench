"""Common utilities and definitions for CoreData types. """
from typing import TYPE_CHECKING

from simplebench.exceptions import SimpleBenchAssertionError

from ._error_tags import _CoreDataErrorTag

if TYPE_CHECKING:
    from ._types import ImmutableCoreDataTypes


def rich_compare_value(value: 'ImmutableCoreDataTypes') -> str:
        """Returns a string representation for rich comparison purposes.

        We don't actually care about the comparision value, just that
        it is consistent and largely guaranteed to be unique for
        each item value.

        Since in a set the order is not guaranteed, we generate a reproducible
        and consistent value by their string representation or content
        hash if they are immutable core data types. This ensures that
        two sets with the same content will have the same
        representation for comparison.

        Since it is only used in generating a cached content hash, this is
        efficient enough for our purposes.

        .. note:: This is a helper method for internal use only. It
              should not be used outside of this class. It's also
              vulnerable to infinite recursion if used on recursive
              data structure since it would never find a base case to stop.

              However, since CoreDataSet is immutable and cannot contain
              recursive references during construction, this should not be an issue in practice.

        :returns: A sorted list of the set items.
        :rtype: list[CoreDataTypes]
        """
        from ._core_data_mapping import CoreDataMapping
        from ._core_data_sequence import CoreDataSequence
        from ._core_data_set import CoreDataSet
        from ._types import CORE_DATA_PRIMITIVE_TYPES_TUPLE

        if value is None:
            return ''
        if isinstance(value, CORE_DATA_PRIMITIVE_TYPES_TUPLE):
            return repr(value)
        if isinstance(value, (CoreDataSequence, CoreDataMapping, CoreDataSet)):
            return value.content_hash()

        raise SimpleBenchAssertionError(
            f'Unsupported CoreData type for rich comparison: {type(value)!r}',
            tag=_CoreDataErrorTag.CORE_DATA_COMPARISON_UNSUPPORTED_TYPE)


def data_url(data: bytes, mime_type: str = 'application/octet-stream') -> str:
    """Generates a data URL for the given bytes data.

    :param data: The bytes data to encode in the data URL.
    :type data: bytes
    :param mime_type: The MIME type of the data. Defaults to 'application/octet-stream'.
    :type mime_type: str
    :returns: A data URL representing the bytes data.
    :rtype: str
    """
    import base64
    encoded_data = base64.b64encode(data).decode('ascii')
    return f'data:{mime_type};base64,{encoded_data}'
