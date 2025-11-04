"""ErrorTags for simplebench.reporters.choices package."""
from simplebench.exceptions.base import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class ChoicesErrorTag(ErrorTag):
    """ErrorTags for simplebench.reporters.choices package."""
    CHOICES_INVALID_ARG_TYPE = "CHOICES_INVALID_ARG_TYPE"
    """Something other than a Iterable of correct type instances or a container
    instance was passed as the choices arg"""
    CHOICES_INVALID_ITEM_VALUE = "CHOICES_INVALID_ITEM_VALUE"
    """Something other than an instance of the correct type was found in the Iterable passed as the choices arg"""
    ADD_CHOICE_INVALID_ARG_TYPE = "ADD_CHOICE_INVALID_ARG_TYPE"
    """Something other than an instance of the correct type was passed as the choice arg"""
    EXTEND_CHOICES_INVALID_ARG_TYPE = "EXTEND_CHOICES_INVALID_ARG_TYPE"
    """Something other than a Iterable of instances of the correct type or a container
    instance was passed as the choices arg"""
    EXTEND_CHOICES_INVALID_ITEM_VALUE = "EXTEND_CHOICES_INVALID_ITEM_VALUE"
    """Something other than an instance of the correct type was found in the Iterable
    passed as the choices arg"""
    GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE = "GET_CHOICE_FOR_ARG_INVALID_ARG_TYPE"
    """Something other than a string was passed as the arg argument"""
    SETITEM_INVALID_VALUE_TYPE = "SETITEM_INVALID_VALUE_TYPE"
    """Something other than an instance of the correct type was assigned to a key in the container"""
    SETITEM_KEY_NAME_MISMATCH = "SETITEM_KEY_NAME_MISMATCH"
    """The key used to assign an instance does not match the name attribute"""
    SETITEM_INVALID_KEY_TYPE = "SETITEM_INVALID_KEY_TYPE"
    """Something other than a string was used as a key to assign an instance"""
    SETITEM_DUPLICATE_CHOICE_NAME = "SETITEM_DUPLICATE_CHOICE_NAME"
    """An instance with the same name already exists in the container"""
    SETITEM_DUPLICATE_CHOICE_FLAG = "SETITEM_DUPLICATE_CHOICE_FLAG"
    """A CLI flag in the instance being added already exists in another instance
    in the container"""
    DELITEM_UNKNOWN_CHOICE_NAME = "DELITEM_UNKNOWN_CHOICE_NAME"
    """No instance with the given name exists in the container"""
