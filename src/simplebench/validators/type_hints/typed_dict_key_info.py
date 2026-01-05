"""Module for TypedDict key information extraction.

This module defines the TypedDictKeyInfo class, which extracts and stores information
about a TypedDict key's required/optional/readonly status and its contained type.

:property bool | None is_required: True if Required, False if NotRequired, None if neither.
:property bool | None is_optional: True if NotRequired, False if Required, None if neither.
:property bool is_readonly: True if ReadOnly, False otherwise.
:property str key: The TypedDict key name.
:property object value_type: The value type argument contained in Required/NotRequired, or the original value type.
"""
from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _TypedDictKeyInfoErrorTag

__all__ = ('TypedDictKeyInfo',)

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
            typ_type = type(current_type)
            module: str = typ_type.__module__
            qualname: str = typ_type.__qualname__

            if qualname in {"Required", "NotRequired", "ReadOnly"}:
                if module not in {"typing", "typing_extensions"}:
                    raise SimpleBenchTypeError(
                        f"TypedDict key '{key}' in class {td_cls.__name__} has unexpected type wrapper "
                        f"'{qualname}' from module '{module}', expected 'typing' or 'typing_extensions'.",
                        tag=_TypedDictKeyInfoErrorTag.UNEXPECTED_TYPEDDICT_WRAPPER_MODULE)

                if qualname == "Required":
                    self._is_required = True
                elif qualname == "NotRequired":
                    self._is_required = False
                elif qualname == "ReadOnly":
                    self._is_readonly = True

                current_type = current_type.__args__[0]
            else:
                # No more wrappers to unwrap, we've found the value type.
                break

        self._value_type: object = current_type

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
