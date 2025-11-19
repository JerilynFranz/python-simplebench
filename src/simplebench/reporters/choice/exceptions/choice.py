"""ErrorTags for Choice() class related exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions.base import ErrorTag


@enum_docstrings
class _ChoiceErrorTag(ErrorTag):
    """ErrorTags for Choice() class related exceptions."""
    REPORTER_INVALID_ARG_TYPE = "REPORTER_INVALID_ARG_TYPE"
    """The 'reporter' argument is not a Reporter subclass instance."""
    CHOICE_CONF_INVALID_ARG_TYPE = "CHOICE_CONF_INVALID_ARG_TYPE"
    """The 'choice_conf' argument is not a ChoiceConf instance."""
