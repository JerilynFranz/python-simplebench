"""Error tags for prioritized reporter exceptions."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _PrioritizedErrorTag(ErrorTag):
    """Error tags for prioritized reporter configurations"""
    INIT_INVALID_REPORTER_ARG_TYPE = "INIT_INVALID_REPORTER_ARG_TYPE"
    """The reporter argument provided to Prioritized.__init__() is not a Reporter instance."""
    INIT_INVALID_CHOICE_ARG_TYPE = "INIT_INVALID_CHOICE_ARG_TYPE"
    """The choice argument provided to Prioritized.__init__() is not a Choice instance."""
    INIT_INVALID_CASE_ARG_TYPE = "INIT_INVALID_CASE_ARG_TYPE"
    """The case argument provided to Prioritized.__init__() is not a Case instance."""
