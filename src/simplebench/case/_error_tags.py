"""ErrorTags for simplebench.case related exceptions in SimpleBench."""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _CaseErrorTag(ErrorTag):
    """ErrorTags for case-related exceptions."""
    INVALID_CALIBRATE_TYPE = auto()
    """The calibrate argument passed to the Case() constructor is not of type Calibrate."""
    INVALID_ACTION_TOO_MANY_PARAMETERS = auto()
    """The action function has more than two parameters."""
    INVALID_ACTION_MISSING_VARIATION_MARKS_PARAMETER = auto()
    """The action function is missing the required 'variation_marks' parameter."""
    INVALID_ACTION_VARIATION_MARKS_PARAMETER_WRONG_TYPE = auto()
    """The 'variation_marks' parameter in the action function is not annotated with VariationMarks."""
    INVALID_NODE = auto()
    """The node being accessed is not of the expected type of :class:`str` or :obj:`None`."""
    INVALID_TIMER_FIELD_NAME_TYPE = auto()
    """The field_name argument passed to the timer validation function is not of type str."""
    INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_CANNOT_CONVERT_TO_STRING = (
        'INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_CANNOT_CONVERT_TO_STRING')
    """The kwargs_variations dictionary contains a value that cannot be converted to a string."""
    INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_ELEMENT_COLLECTION = (
        'INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_NOT_ELEMENT_COLLECTION')
    """The kwargs_variations dictionary contains a value that is not an ElementCollection."""
    INVALID_RUNNERS_NOT_ELEMENT_COLLECTION = auto()
    """The runners argument passed to the Case() constructor is not an ElementCollection."""
    INVALID_REPORT_INCLUDE_RAW_DATA_NOT_BOOL = auto()
    """The include_raw_data argument passed to Case.report() is not a bool."""
    HAVE_NOT_RUN_CASE_YET = auto()
    """An action depending on the benchmark having been run was requested before running the benchmarks in the Case."""
    INVALID_CPU_TIMER_NOT_CALLABLE = auto()
    """The CPU timer argument passed to the Case() constructor is not a callable."""
    INVALID_CPU_TIMER_RETURN_TYPE = auto()
    """The CPU timer callable passed to the Case() constructor does not return an int."""
    INVALID_TIMER_NOT_CALLABLE = auto()
    """The timer argument passed to the Case() constructor is not a callable."""
    INVALID_TIMER_RETURN_TYPE = auto()
    """The timer callable passed to the Case() constructor does not return a float or int."""
    INVALID_ACTION_KWARGS_VARIATIONS_KEY_NOT_IN_PARAMETERS = auto()
    """A key in kwargs_variations was not found in the action function parameters."""
    INVALID_ACTION_PARAMETER_NOT_IN_KWARGS_VARIATIONS = auto()
    """A keyword-only parameter in the action function was not found in kwargs_variations."""
    INVALID_ACTION_NON_KEYWORD_ONLY_PARAMETERS = auto()
    """The action function contains non-keyword-only parameters other than the required '_bench' parameter."""
    INVALID_ACTION_BENCH_PARAMETER_NOT_ANNOTATED = auto()
    """The '_bench' parameter in the action function is not annotated with SimpleRunner."""
    INVALID_ACTION_BENCH_PARAMETER_WRONG_TYPE = auto()
    """The '_bench' parameter in the action function is not annotated with SimpleRunner."""
    INVALID_ACTION_BENCH_PARAMETER_NOT_POSITIONAL_ONLY = auto()
    """The '_bench' parameter in the action function is not positional-only."""
    INVALID_TIMEOUT_TYPE = auto()
    """Invalid timeout argument type passed to the Case() constructor"""
    INVALID_TIMEOUT_VALUE = auto()
    """Invalid timeout argument value passed to the Case() constructor"""
    INVALID_TIMEOUT_LESS_EQUAL_MAX_TIME = auto()
    """Timeout argument value passed to the Case() constructor is less than or equal to max_time"""
    INVALID_VCS_INFO_ARG_TYPE = auto()
    """Invalid vcs_info argument type passed to the Case() constructor"""
    INVALID_BENCHMARK_ID_TYPE = auto()
    """Invalid benchmark_id argument type passed to the Case() constructor"""
    INVALID_BENCHMARK_ID_VALUE = auto()
    """Invalid benchmark_id argument value passed to the Case() constructor"""
    INVALID_GROUP_TYPE = auto()
    """Invalid group argument type passed to the Case() constructor"""
    INVALID_GROUP_VALUE = auto()
    """Invalid group argument value passed to the Case() constructor"""
    INVALID_TITLE_TYPE = auto()
    """Invalid title argument type passed to the Case() constructor"""
    INVALID_TITLE_VALUE = auto()
    """Invalid title argument value passed to the Case() constructor"""
    INVALID_DESCRIPTION_TYPE = auto()
    """Invalid description argument type passed to the Case() constructor"""
    INVALID_DESCRIPTION_VALUE = auto()
    """Invalid description argument value passed to the Case() constructor"""
    INVALID_ITERATIONS_TYPE = auto()
    """Invalid iterations argument type passed to the Case() constructor"""
    INVALID_ITERATIONS_VALUE = auto()
    """Invalid iterations argument value passed to the Case() constructor"""
    INVALID_WARMUP_ITERATIONS_TYPE = auto()
    """Invalid warmup_iterations argument type passed to the Case() constructor"""
    INVALID_WARMUP_ITERATIONS_VALUE = auto()
    """Invalid warmup_iterations argument value passed to the Case() constructor"""
    INVALID_MIN_TIME_TYPE = auto()
    """Invalid min_time argument type passed to the Case() constructor"""
    INVALID_MIN_TIME_VALUE = auto()
    """Invalid min_time argument value passed to the Case() constructor"""
    INVALID_MAX_TIME_TYPE = auto()
    """Invalid max_time argument type passed to the Case() constructor"""
    INVALID_MAX_TIME_VALUE = auto()
    """Invalid max_time argument value passed to the Case() constructor"""
    INVALID_TIME_RANGE = auto()
    """max_time must be greater than or equal to min_time in the Case() constructor"""
    INVALID_NAME = auto()
    """Something other than a non-empty string was passed to the Case() constructor as the name arg"""
    INVALID_DESCRIPTION = auto()
    """Something other than a string was passed to the Case() constructor as the description arg"""
    INVALID_RUNNER_NOT_CALLABLE_OR_NONE = auto()
    """Something other than a callable (function or method) was passed to the Case() constructor as the runner arg"""
    INVALID_ACTION_NOT_CALLABLE = auto()
    """Something other than a callable (function or method) was passed to the Case() constructor as the action arg"""
    INVALID_SETUP = auto()
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the setup arg"""
    INVALID_TEARDOWN = auto()
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the teardown arg"""
    INVALID_VARIATION_COLS_NOT_MAPPING = auto()
    """Something other than a :class:`~collections.abc.Mapping` was passed to the
    Case() constructor as the variation_cols arg"""
    INVALID_VARIATION_COLS_ENTRY_NOT_STRINGS = auto()
    """Something other than string keys and string or number values were found in the dictionary passed to
    the Case() constructor as the variation_cols arg"""
    INVALID_KWARGS_VARIATIONS_NOT_MAPPING = auto()
    """Something other than a :class:`~collections.abc.Mapping` was passed to the Case()
    constructor as the kwargs_variations arg"""
    INVALID_OPTIONS_NOT_ELEMENT_COLLECTION = auto()
    """Something other than an ElementCollection was passed to the Case() constructor as the options arg"""
    INVALID_OPTIONS_ENTRY_NOT_REPORTER_OPTION = auto()
    """Something other than a ReporterOptions instance was found in the iterable passed to the Case() constructor
    as the options arg"""
    INVALID_CALLBACK_NOT_CALLABLE_OR_NONE = auto()
    """Something other than a callable (function or method) or None was passed to the Case() constructor as
    the callback arg"""
    SECTION_MEAN_INVALID_SECTION_TYPE_ARGUMENT = auto()
    """Something other than a Metric instance was passed to the Case() constructor as the metric arg"""
    SECTION_MEAN_INVALID_SECTION_ARGUMENT = auto()
    """Something other than Metric.OPS or Metric.TIMING was passed to the Case.metric_mean() method"""
    INVALID_RUNNER_NOT_SUBCLASS_OF_RUNNER = auto()
    """Attempted to set a runner for Case that is not a subclass of BenchmarkRunner."""
    INVALID_ACTION_MISSING_BENCH_PARAMETER = auto()
    """The action function is missing the required 'bench' parameter."""
    INVALID_ACTION_MISSING_KWARGS_PARAMETER = auto()
    """The action function is missing the required '**kwargs' parameter."""
    INVALID_VARIATION_COLS_ENTRY_KEY_TYPE = auto()
    """The variation_cols dictionary contains a key that is not type str"""
    INVALID_VARIATION_COLS_ENTRY_KEY_NOT_IN_KWARGS = auto()
    """The variation_cols dictionary contains a key that does not appear in kwargs_variations."""
    INVALID_VARIATION_COLS_ENTRY_VALUE_NOT_STRING = auto()
    """The variation_cols dictionary contains a value that is not a string."""
    INVALID_VARIATION_COLS_ENTRY_VALUE_BLANK = auto()
    """The variation_cols dictionary contains a value that is a blank string."""
    INVALID_KWARGS_VARIATIONS_ENTRY_KEY_TYPE = auto()
    """The kwargs_variations dictionary contains a key that is not type str"""
    INVALID_KWARGS_VARIATIONS_ENTRY_KEY_NOT_IDENTIFIER = auto()
    """The kwargs_variations dictionary contains a key that is not a valid Python identifier."""
    INVALID_KWARGS_VARIATIONS_ENTRY_VALUE_EMPTY_LIST = auto()
    """The kwargs_variations dictionary contains a value that is an empty list."""
    INVALID_CALLBACK_INCORRECT_NUMBER_OF_PARAMETERS = auto()
    """The callback function must accept exactly four parameters: the Case instance, a Metric instance,
    a Format instance, and a value (which may be of any type.)"""
    INVALID_ACTION_INCORRECT_SIGNATURE = auto()
    """The action function must accept two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    INVALID_ACTION_PARAMETER_COUNT = auto()
    """The action function must accept exactly two parameters: a 'bench' parameter and a '**kwargs' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_CASE_PARAMETER'
    )
    """The callback function is missing the required 'case' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_TYPE'
    )
    """The callback function's 'case' parameter must be type Case."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_CASE_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """The callback function's 'case' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_SECTION_PARAMETER'
    )
    """The callback function is missing the required 'metric' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_TYPE'
    )
    """The callback function's 'metric' parameter must be type Metric."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """The callback function's 'metric' parameter must be a keyword-only parameter."""
    SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY = (
        'SECTION_INVALID_CALLBACK_INCORRECT_SIGNATURE_SECTION_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """The callback function's 'metric' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_FORMAT_PARAMETER'
    )
    """The callback function is missing the required 'output_format' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_TYPE'
    )
    """The callback function's 'output_format' parameter must be type Format."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_FORMAT_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """The callback function's 'output_format' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_OUTPUT_PARAMETER'
    )
    """The callback function is missing the required 'output' parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """The callback function's 'output' parameter must be a keyword-only parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_OUTPUT_PARAMETER_TYPE'
    )
    """The callback function's 'output' parameter must have a type annotation."""
    MODIFY_READONLY_GROUP = auto()
    """The group attribute is read-only and cannot be modified."""
    MODIFY_READONLY_TITLE = auto()
    """The title attribute is read-only and cannot be modified."""
    MODIFY_READONLY_DESCRIPTION = auto()
    """The description attribute is read-only and cannot be modified."""
    MODIFY_READONLY_NAME = auto()
    """The name attribute is read-only and cannot be modified."""
    MODIFY_READONLY_RUNNER = auto()
    """The runner attribute is read-only and cannot be modified."""
    MODIFY_READONLY_ACTION = auto()
    """The action attribute is read-only and cannot be modified."""
    MODIFY_READONLY_ITERATIONS = auto()
    """The iterations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_WARMUP_ITERATIONS = auto()
    """The warmup_iterations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_MIN_TIME = auto()
    """The min_time attribute is read-only and cannot be modified."""
    MODIFY_READONLY_MAX_TIME = auto()
    """The max_time attribute is read-only and cannot be modified."""
    MODIFY_READONLY_VARIATION_COLS = auto()
    """The variation_cols attribute is read-only and cannot be modified."""
    MODIFY_READONLY_KWARGS_VARIATIONS = auto()
    """The kwargs_variations attribute is read-only and cannot be modified."""
    MODIFY_READONLY_OPTIONS = auto()
    """The options attribute is read-only and cannot be modified."""
    MODIFY_READONLY_CALLBACK = auto()
    """The callback attribute is read-only and cannot be modified."""
    MODIFY_READONLY_RESULTS = auto()
    """The results attribute is read-only and cannot be modified."""
    INVALID_RESULTS_NOT_LIST = auto()
    """Something other than a list was assigned to the results attribute"""
    INVALID_RESULTS_ENTRY_NOT_RESULTS_INSTANCE = auto()
    """Something other than a Results instance was found in the list assigned to the results attribute"""
    INVALID_CALLBACK_UNRESOLVABLE_HINTS = auto()
    """The type hints for the callback function could not be resolved."""
    INVALID_DEFAULT_RUNNER_NOT_SIMPLE_RUNNER_SUBCLASS = auto()
    """Attempted to set a default runner for Case that is not a SimpleRunner or a subclass."""
    BENCHMARK_ACTION_RAISED_EXCEPTION = auto()
    """The action function raised an exception during execution."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_MISSING_PARAMETER = auto()
    """The callback function is missing a required parameter."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_TYPE = auto()
    """A parameter in the callback function has an incorrect type."""
    INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY = (
        'INVALID_CALLBACK_INCORRECT_SIGNATURE_PARAMETER_NOT_KEYWORD_ONLY'
    )
    """A parameter in the callback function is not keyword-only."""
    ADD_RESULT_INVALID_RESULT_TYPE = auto()
    """Something other than a Results instance was passed to the Case.add_result() method"""
    INVALID_ROUNDS_TYPE = auto()
    """Invalid rounds argument type passed to the Case() constructor"""
    INVALID_ROUNDS_VALUE = auto()
    """Invalid rounds argument value passed to the Case() constructor"""
    BENCHMARK_ACTION_TIMEOUT_OCCURRED = auto()
    """A timeout occurred while running the benchmark action."""
    INVALID_RUNNER_NOT_BENCHMARK_RUNNER_SUBCLASS = auto()
    """Attempted to set a runner for Case that is not a subclass of BenchmarkRunner."""
    INVALID_DEFAULT_RUNNER_NOT_BENCHMARK_RUNNER_SUBCLASS = auto()
    """Attempted to set a default runner for Case that is not a BenchmarkRunner or a subclass."""
    INVALID_VARIATION_COLS_NOT_VARIATION_COLS = auto()
    """Something other than a VariationCols instance was passed to the Case() constructor as the variation_cols arg."""
    INVALID_KWARGS_VARIATIONS_NOT_KWARGS_VARIATIONS = auto()
    """Something other than a KWArgsVariations instance was passed to the Case() constructor as the
    kwargs_variations arg."""
    BENCHMARK_MAX_TIME_LESS_THAN_MIN_TIME = auto()
    """The max_time parameter is less than the min_time parameter."""
    BENCHMARK_N_TYPE = auto()
    """The 'n' parameter is not of type float or int."""
    BENCHMARK_N_VALUE = auto()
    """The 'n' parameter is not positive."""
