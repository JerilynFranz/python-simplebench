"""Module for TypedDict key information extraction.

This module defines the TypedDictKeyInfo class, which extracts and stores information
about a TypedDict key's required/optional/readonly status and its contained type.

:property bool | None is_required: True if Required, False if NotRequired, None if neither.
:property bool | None is_optional: True if NotRequired, False if Required, None if neither.
:property bool is_readonly: True if ReadOnly, False otherwise.
:property str key: The TypedDict key name.
:property object value_type: The value type argument contained in Required/NotRequired/ReadOnly,
    or the original value type.
"""

import logging
from typing import get_args, get_origin

from simplebench.exceptions import SimpleBenchRuntimeError
from simplebench.simplebench_types import NotRequired, ReadOnly, Required

from ._error_tags import _TypedDictKeyInfoErrorTag

__all__: list[str] = []


log = logging.getLogger(__name__)


class TypedDictKeyInfo:
    """Information about a TypedDict key's required/optional status and contained type.

    :property bool | None is_required: True if Required, False if NotRequired, None if neither.
    :property bool | None is_optional: True if NotRequired, False if Required, None if neither.
    :property bool is_readonly: True if ReadOnly, False otherwise.
    :property str key: The TypedDict key name.
    :property object value_type: The value type argument contained in Required/NotRequired, or the original value type.
    """

    def __init__(self, key: str, td_cls: type) -> None:
        """Initialize the TypedDictKeyInfo.

        :param str key: The TypedDict key name.
        :param type td_cls: The TypedDict subclass containing the key.
        """
        self._key: str = key
        self._is_readonly: bool = False

        # Set default required status based on the TypedDict's __total__ attribute.
        # This can be overridden by an explicit Required/NotRequired wrapper.
        self._is_required: bool = getattr(td_cls, '__total__', True)

        current_type = td_cls.__annotations__[key]

        # Loop to unwrap decorators like Required, NotRequired, and ReadOnly.
        # This handles nested wrappers like ReadOnly[Required[int]].
        while True:
            origin = get_origin(current_type)
            if origin in {Required, NotRequired, ReadOnly}:
                if origin is Required:
                    self._is_required = True
                elif origin is NotRequired:
                    self._is_required = False
                elif origin is ReadOnly:
                    self._is_readonly = True
                current_type = get_args(current_type)[0]
            else:
                # No more wrappers to unwrap, we've found the value type.
                break

        origin = get_origin(current_type)
        if origin in {Required, NotRequired, ReadOnly}:
            raise SimpleBenchRuntimeError(
                f"TypedDict key '{key}' in class {td_cls.__name__} has unprocessed "
                f"'{origin}' wrapper. Failed to 'unwrap' type.",
                tag=_TypedDictKeyInfoErrorTag.NESTED_REQUIRED_NOTREQUIRED_READONLY,
            )
        self._value_type: object = current_type

        log.debug(
            "TypedDictKeyInfo: Key '%s' in TypedDict '%s' - is_required: %s, is_readonly: %s, value_type: %s",
            key,
            td_cls.__name__,
            self._is_required,
            self._is_readonly,
            current_type,
        )

    @property
    def is_required(self) -> bool:
        """Get whether the key is Required.

        :return bool: True if Required, False otherwise.
        """
        return self._is_required

    @property
    def is_optional(self) -> bool:
        """Get whether the key is NotRequired.

        :return bool: True if NotRequired, False otherwise.
        """
        return not self._is_required

    @property
    def is_readonly(self) -> bool:
        """Get whether the key is ReadOnly.

        :return bool: True if ReadOnly, False otherwise.
        """
        return self._is_readonly

    @property
    def key(self) -> str:
        """Get the TypedDict key name.

        :return str: The TypedDict key name.
        """
        return self._key

    @property
    def value_type(self) -> object:
        """Get the contained value type.

        :return object: The value type argument contained in Required/NotRequired,
                        or the original value type if neither.
        """
        return self._value_type

    @classmethod
    def get_all_keys(cls, td_cls: type) -> set[str]:
        """Get all keys defined in the TypedDict subclass.

        .. code-block:: python

            class MyTypedDict(TypedDict):
                a: int
                b: NotRequired[str]
                c: ReadOnly[float]

            keys_info = TypedDictKeyInfo.get_all_keys(MyTypedDict)
            # keys_info will be a set containing 'a', 'b', 'c'.

        :param td_cls: The TypedDict subclass to extract keys from.
        :type td_cls: type
        :return: A set of all defined keys.
        :rtype: set[str]
        """
        return set(td_cls.__annotations__.keys())
