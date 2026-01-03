"""Module for TypedDict key information extraction.

This module defines the _TypedDictKeyInfo class, which extracts and stores information
about a TypedDict key's required/optional status and its contained type.

:property bool | None is_required: True if Required, False if NotRequired, None if neither.
:property bool | None is_optional: True if NotRequired, False if Required, None if neither.
:property object value_type: The value type argument contained in Required/NotRequired, or the original value type.
"""
from simplebench.exceptions import SimpleBenchTypeError

from ._error_tags import _TypedDictKeyInfoErrorTag


class _TypedDictKeyInfo:
    """Information about a TypedDict key's required/optional status and contained type.

    :property bool | None is_required: True if Required, False if NotRequired, None if neither.
    :property bool | None is_optional: True if NotRequired, False if Required, None if neither.
    :property object value_type: The value type argument contained in Required/NotRequired, or the original value type.
    """
    def __init__(self, key: str, td_cls: type) -> None:
        """Initialize the TypedDictKeyInfo.

        :param str key: The TypedDict key name.
        :param type td_cls: The TypedDict subclass containing the key.
        """
        self._key: str = key
        self._is_required: bool = False
        self._value_type: object = None
        typ = td_cls.__annotations__[key]
        typ_type = type(typ)
        module: str = typ_type.__module__
        qualname: str = typ_type.__qualname__

        match qualname:
            case "Required":
                if not module in {"typing", "typing_extensions"}:
                    raise SimpleBenchTypeError(
                        f"TypedDict key '{key}' in class {td_cls.__name__} has unexpected type wrapper "
                        f"from module '{module}', expected either 'typing' or 'typing_extensions'.",
                        tag=_TypedDictKeyInfoErrorTag.UNEXPECTED_TYPEDDICT_WRAPPER_MODULE)
                self._is_required = True
                self._value_type = typ.__args__[0]
            case "NotRequired":
                if not module in {"typing", "typing_extensions"}:
                    raise SimpleBenchTypeError(
                        f"TypedDict key '{key}' in class {td_cls.__name__} has unexpected type wrapper "
                        f"from module '{module}', expected either 'typing' or 'typing_extensions'.",
                        tag=_TypedDictKeyInfoErrorTag.UNEXPECTED_TYPEDDICT_WRAPPER_MODULE)
                self._is_required = False
                self._value_type = typ.__args__[0]
            case _:  # bare type without Required/NotRequired wrapper
                is_total: bool = getattr(td_cls, '__total__', True)
                if is_total:
                    self._is_required = True
                else:
                    self._is_required = False
                self._value_type = typ

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

__all__ = ["_TypedDictKeyInfo"]
