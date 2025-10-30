"""simplebench.reporters.validators.exceptions package."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class ReportersValidatorsErrorTag(ErrorTag):
    """ErrorTags for simplebench.reporters.validators exceptions."""
    # validate_reporter_callback() tags
    REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE = "INVALID_REPORTER_CALLBACK_NOT_CALLABLE_OR_NONE"
    """The reporter callback is neither a callable nor None"""
    REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = (
        "INVALID_REPORTER_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS")
    """The reporter callback does not have the correct number of parameters"""

    # validate_callback() tags
    INVALID_CALLBACK_UNRESOLVABLE_HINTS = "INVALID_CALLBACK_UNRESOLVABLE_HINTS"
    """The type hints for the callback function could not be resolved"""
    REPORTER_CALLBACK_MISSING_RETURN_ANNOTATION = "REPORTER_CALLBACK_MISSING_RETURN_ANNOTATION"
    """The reporter callback is missing a return type annotation"""
    REPORTER_CALLBACK_INCORRECT_RETURN_ANNOTATION_TYPE = "REPORTER_CALLBACK_INCORRECT_RETURN_ANNOTATION_TYPE"
    """The reporter callback has an incorrect return annotation type"""

    # validate_reporter_call_parameter() tags
    INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER")
    """The callback function is missing a required parameter"""
    INVALID_CALL_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER_TYPE_HINT")
    """The callback function is missing a required parameter type hint"""
    INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE")
    """The callback function has a parameter with an incorrect type annotation"""
    INVALID_CALL_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function has a parameter that is not keyword-only"""

    # validate_report_renderer() tags
    REPORT_RENDERER_NOT_CALLABLE = "REPORT_RENDERER_NOT_CALLABLE"
    """The renderer parameter is not callable"""
    REPORT_RENDERER_INCORRECT_NUMBER_OF_PARAMETERS = "REPORTER_RENDERER_INCORRECT_NUMBER_OF_PARAMETERS"
    """The renderer does not have the correct number of parameters"""
    REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE = "REPORT_RENDERER_INCORRECT_RETURN_ANNOTATION_TYPE"
    """The renderer has an incorrect return annotation type"""
    REPORT_RENDERER_MISSING_RETURN_ANNOTATION = "REPORT_RENDERER_MISSING_RETURN_ANNOTATION"
    """The renderer is missing a return type annotation"""
    REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE = "REPORT_RENDERER_UNEXPECTED_RETURN_ANNOTATION_TYPE"
    """The renderer has an unexpected return annotation type"""
