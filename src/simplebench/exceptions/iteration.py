"""ErrorTags for simplebench.iterations in SimpleBench."""
from ..enums import enum_docstrings
from .base import ErrorTag


@enum_docstrings
class _IterationErrorTag(ErrorTag):
    """ErrorTags for simplebench.iterations in SimpleBench."""
    N_ARG_TYPE = "N_ARG_TYPE"
    """Invalid n argument passed to the Iteration() constructor - must be an int"""
    N_ARG_VALUE = "N_ARG_VALUE"
    ROUNDS_ARG_TYPE = "ROUNDS_ARG_TYPE"
    """Invalid rounds argument passed to the Iteration() constructor - must be an int"""
    ROUNDS_ARG_VALUE = "ROUNDS_ARG_VALUE"
    """Invalid rounds argument passed to the Iteration() constructor - must be greater than zero"""
    ELAPSED_ARG_TYPE = "ELAPSED_ARG_TYPE"
    """Invalid elapsed argument passed to the Iteration() constructor - must be an int"""
    ELAPSED_ARG_VALUE = "ELAPSED_ARG_VALUE"
    """Invalid elapsed argument passed to the Iteration() constructor - must be zero or greater"""
    MEMORY_ARG_TYPE = "MEMORY_ARG_TYPE"
    """Invalid memory argument passed to the Iteration() constructor - must be an int"""
    PEAK_MEMORY_ARG_TYPE = "PEAK_MEMORY_ARG_TYPE"
    """Invalid peak_memory argument passed to the Iteration() constructor - must be an int"""
    UNIT_ARG_TYPE = "UNIT_ARG_TYPE"
    """Invalid unit argument passed to the Iteration() constructor - must be a str"""
    UNIT_ARG_VALUE = "UNIT_ARG_VALUE"
    """Invalid unit argument passed to the Iteration() constructor - must be a non-empty str"""
    SCALE_ARG_TYPE = "SCALE_ARG_TYPE"
    """Invalid scale argument passed to the Iteration() constructor - must be a float"""
    SCALE_ARG_VALUE = "SCALE_ARG_VALUE"
    """Invalid scale argument passed to the Iteration() constructor - must be greater than zero"""
    ITERATION_SECTION_INVALID_SECTION_ARG_TYPE = "ITERATION_SECTION_INVALID_SECTION_ARG_TYPE"
    """Something other than a Section enum was passed as the iteration_sections arg"""
    ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE = (
            "ITERATION_SECTION_UNSUPPORTED_SECTION_ARG_VALUE")
    """Something other than a Section.OPS or Section.TIMING was passed to the Iteration.iteration_section() method"""
