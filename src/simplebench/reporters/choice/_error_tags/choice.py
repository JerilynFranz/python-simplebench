"""ErrorTags for Choice() class related exceptions."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions.error_tag import ErrorTag


@enum_docstrings
class _ChoiceErrorTag(ErrorTag):
    """ErrorTags for Choice() class related exceptions."""

    REPORTER_INVALID_ARG_TYPE = auto()
    """The 'reporter' argument is not a Reporter subclass instance."""
    CHOICE_CONF_INVALID_ARG_TYPE = auto()
    """The 'choice_conf' argument is not a ChoiceConf instance."""
