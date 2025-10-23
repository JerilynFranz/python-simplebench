"""ErrorTags for simplebench.case related exceptions in SimpleBench."""
from .base import ErrorTag
from ..enums import enum_docstrings


@enum_docstrings
class CaseErrorTag(ErrorTag):
    """ErrorTags for case-related exceptions."""
    INVALID_GROUP_TYPE = "INVALID_GROUP_TYPE"
    """Invalid group argument type passed to the Case() constructor"""
    INVALID_GROUP_VALUE = "INVALID_GROUP_VALUE"
    """Invalid group argument value passed to the Case() constructor"""
    INVALID_TITLE_TYPE = "INVALID_TITLE_TYPE"
    """Invalid title argument type passed to the Case() constructor"""
    INVALID_TITLE_VALUE = "INVALID_TITLE_VALUE"
    """Invalid title argument value passed to the Case() constructor"""
    INVALID_DESCRIPTION_TYPE = "INVALID_DESCRIPTION_TYPE"
    """Invalid description argument type passed to the Case() constructor"""
    INVALID_DESCRIPTION_VALUE = "INVALID_DESCRIPTION_VALUE"
    """Invalid description argument value passed to the Case() constructor"""
    INVALID_ITERATIONS_TYPE = "INVALID_ITERATIONS_TYPE"
    """Invalid iterations argument type passed to the Case() constructor"""
    INVALID_ITERATIONS_VALUE = "INVALID_ITERATIONS_VALUE"
    """Invalid iterations argument value passed to the Case() constructor"""
    INVALID_WARMUP_ITERATIONS_TYPE = "INVALID_WARMUP_ITERATIONS_TYPE"
    """Invalid warmup_iterations argument type passed to the Case() constructor"""
    INVALID_WARMUP_ITERATIONS_VALUE = "INVALID_WARMUP_ITERATIONS_VALUE"
    """Invalid warmup_iterations argument value passed to the Case() constructor"""
    INVALID_MIN_TIME_TYPE = "INVALID_MIN_TIME_TYPE"
    """Invalid min_time argument type passed to the Case() constructor"""
    INVALID_MIN_TIME_VALUE = "INVALID_MIN_TIME_VALUE"
    """Invalid min_time argument value passed to the Case() constructor"""
    INVALID_MAX_TIME_TYPE = "INVALID_MAX_TIME_TYPE"
    """Invalid max_time argument type passed to the Case() constructor"""
    INVALID_MAX_TIME_VALUE = "INVALID_MAX_TIME_VALUE"
    """Invalid max_time argument value passed to the Case() constructor"""
    INVALID_TIME_RANGE = "INVALID_TIME_RANGE"
    """max_time must be greater than or equal to min_time in the Case() constructor"""
    INVALID_NAME = "INVALID_NAME"
    """Something other than a non-empty string was passed to the Case() constructor as the name arg"""
    INVALID_DESCRIPTION = "INVALID_DESCRIPTION"
    """Something other than a string was passed to the Case() constructor as the description arg"""
    INVALID_RUNNER_NOT_CALLABLE_OR_NONE = "INVALID_RUNNER_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the runner arg"""
    INVALID_ACTION_NOT_CALLABLE = "INVALID_ACTION_NOT_CALLABLE"
    """Something other than a callable (function or method) was passed to the Case() constructor as the action arg"""
    INVALID_SETUP = "INVALID_SETUP"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the setup arg"""
    INVALID_TEARDOWN = "INVALID_TEARDOWN"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the teardown arg"""
    INVALID_VARIATION_COLS_NOT_DICT = "INVALID_VARIATION_COLS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the variation_cols arg"""
    INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS = "INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS"
    """Something other than string keys and string or number values were found in the dictionary passed to
    the Case() constructor as the variation_cols arg"""
    INVALID_KWARGS_VARIATIONS_NOT_DICT = "INVALID_KWARGS_VARIATIONS_NOT_DICT"
    """Something other than a dictionary was passed to the Case() constructor as the kwargs_variations arg"""
    INVALID_OPTIONS_NOT_LIST = "INVALID_OPTIONS_NOT_LIST"
    """Something other than a list was passed to the Case() constructor as the options arg"""
    INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION = "INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION"
    """Something other than a ReporterOptions instance was found in the list passed to the Case() constructor
    as the options arg"""
    INVALID_CALLBACK_NOT_CALLABLE_OR_NONE = "INVALID_CALLBACK_NOT_CALLABLE_OR_NONE"
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the callback arg"""
    SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT = "SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT"
    """Something other than a Section instance was passed to the Case() constructor as the section arg"""
    SECTION_MEAN_INVALID_SECTION_ARGUMENT = "SECTION_MEAN_INVALID_SECTION_ARGUMENT"
    """Something other than Section.OPS or Section.TIMING was passed to the Case.section_mean() method"""
    INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS = "INVALID_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS"
    """Something other than a SimpleRunner or a subclass was passed to the Case() constructor as the runner arg"""
    INVALID_ACTION_MISSING_BENCH_PARAMETER = "INVALID_ACTION_MISSING_BENCH_PARAMETER"
    """The action function is missing the required 'bench' parameter."""
    INVALID_ACTION_MISSING_KWARGS_PARAMETER = "INVALID_ACTION_MISSING_KWARGS_PARAMETER"
    """The action function is missing the required '**kwargs' parameter."""
    INVALID_VARIATION_COLS_ENTRY_KEY_TYPE = "INVALID_VARIATION_COLS_ENTRY_KEY_TYPE"
    """The variation_cols dictionary contains a key that is not type str"""
    INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS = "INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS"
    """The variation_cols dictionary contains a key that does not appear in kwargs_variations."""
    INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING = "INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING"
    """The variation_cols dictionary contains a value that is not a string."""
    INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK = "INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK"
    """The variation_cols dictionary contains a value that is a blank string."""
    INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE = "INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE"
    """The kwargs_variations dictionary contains a key that is not type str"""
    INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER = "INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER"
    """The kwargs_variations dictionary contains a key that is not a valid Python identifier."""
    INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST = "INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_LIST"
    """The kwargs_variations dictionary contains a value that is not a list."""
    INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST = "INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST"
    """The kwargs_variations dictionary contains a value that is an empty list."""
    INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = "INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS"
    """The callback function must accept exactly four parameters: the Case instance, a Section instance,
    a Format instance, and a value (which may be of any type.)"""
    INVALID_ACTION_INCORRECT_SIGNATURE = "INVALID_ACTION_INCORRECT_SIGNATURE"
    """The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    INVALID_ACTION_PARAMETER_COUNT = "INVALID_ACTION_PARAMETER_COUNT"
    """The action function must accept exactly two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER")
    """The callback function is missing the required 'case' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE")
    """The callback function's 'case' parameter must be type Case."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'case' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER")
    """The callback function is missing the required 'section' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE")
    """The callback function's 'section' parameter must be type Section."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'section' parameter must be a keyword-only parameter."""
    SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        "SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'section' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER")
    """The callback function is missing the required 'output_format' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE")
    """The callback function's 'output_format' parameter must be type Format."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'output_format' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER")
    """The callback function is missing the required 'output' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY")
    """The callback function's 'output' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE")
    """The callback function's 'output' parameter must have a type annotation."""
    MODIFY_READONLY_GROUP = "MODIFY_READONLY_GROUP"
    """The group attribute is read-only and cannot be modified."""
    MODIFY_READONLY_TITLE = "MODIFY_READONLY_TITLE"
    """The title attribute is read-only and cannot be modified."""
    MODIFY_READONLY_DESCRIPTION = "MODIFY_READONLY_DESCRIPTION"
    """The description attribute is read-only and cannot be modified."""
    MODIFY_READONLY_NAME = "MODIFY_READONLY_NAME"
    """The name attribute is read-only and cannot be modified."""
    MODIFY_READONLY_RUNNER = "MODIFY_READONLY_RUNNER"
    """The runner attribute is read-only and cannot be modified."""
    MODIFY_READONLY_ACTION = "MODIFY_READONLY_ACTION"
    """The action attribute is read-only and cannot be modified."""
    MODIFY_READONLY_ITERATIONS = "MODIFY_READONLY_ITERATIONS"
    """The iterations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_WARMUP_ITERATIONS = "MODIFY_READONLY_WARMUP_ITERATIONS"
    """The warmup_iterations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_MIN_TIME = "MODIFY_READONLY_MIN_TIME"
    """The min_time attribute is read-only and cannot be modified."""
    MODIFY_READONLY_MAX_TIME = "MODIFY_READONLY_MAX_TIME"
    """The max_time attribute is read-only and cannot be modified."""
    MODIFY_READONLY_VARIATION_COLS = "MODIFY_READONLY_VARIATION_COLS"
    """The variation_cols attribute is read-only and cannot be modified."""
    MODIFY_READONLY_KWARGS_VARIATIONS = "MODIFY_READONLY_KWARGS_VARIATIONS"
    """The kwargs_variations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_OPTIONS = "MODIFY_READONLY_OPTIONS"
    """The options attribute is read-only and cannot be modified."""
    MODIFY_READONLY_CALLBACK = "MODIFY_READONLY_CALLBACK"
    """The callback attribute is read-only and cannot be modified."""
    MODIFY_READONLY_RESULTS = "MODIFY_READONLY_RESULTS"
    """The results attribute is read-only and cannot be modified."""
    INVALID_RESULTS_NOT_LIST = "INVALID_RESULTS_NOT_LIST"
    """Something other than a list was assigned to the results attribute"""
    INVALID_RESULTS_ENTRY_NOT_RESULTS_INSTANCE = "INVALID_RESULTS_ENTRY_NOT_RESULTS_INSTANCE"
    """Something other than a Results instance was found in the list assigned to the results attribute"""
    INVALID_CALLBACK_UNRESOLVABLE_HINTS = "INVALID_CALLBACK_UNRESOLVABLE_HINTS"
    """The type hints for the callback function could not be resolved."""
    INVALID_DEFAULT_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS = "INVALID_DEFAULT_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS"
    """Attempted to set a default runner for Case that is not a SimpleRunner or a subclass."""
    BENCHMARK_ACTION_RAISED_EXCEPTION = "BENCHMARK_ACTION_RAISED_EXCEPTION"
    """The action function raised an exception during execution."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER")
    """The callback function is missing a required parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE")
    """A parameter in the callback function has an incorrect type."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY = (
        "INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY")
    """A parameter in the callback function is not keyword-only."""
    ADD_RESULT_INVALID_RESULT_TYPE = "ADD_RESULT_INVALID_RESULT_TYPE"
    """Something other than a Results instance was passed to the Case.add_result() method"""
    INVALID_ROUNDS_TYPE = "INVALID_ROUNDS_TYPE"
    """Invalid rounds argument type passed to the Case() constructor"""
    INVALID_ROUNDS_VALUE = "INVALID_ROUNDS_VALUE"
    """Invalid rounds argument value passed to the Case() constructor"""
