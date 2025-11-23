"""Exceptions for the simplebench.reporters.reporter module."""
from simplebench.enums import enum_docstrings
from simplebench.exceptions.base import ErrorTag


@enum_docstrings
class _ReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :mod:`simplebench.reporters.reporter` module."""
    # __init__()
    CONFIG_INVALID_ARG_TYPE = "CONFIG_INVALID_ARG_TYPE"
    """Invalid type for ``config`` argument in __init__()"""

    # log_report()
    LOG_REPORT_INVALID_TIMESTAMP_ARG_TYPE = "LOG_REPORT_INVALID_TIMESTAMP_ARG_TYPE"
    """Invalid type for ``timestamp`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.log_report`"""
    LOG_REPORT_INVALID_FILEPATH_ARG_TYPE = "LOG_REPORT_INVALID_FILEPATH_ARG_TYPE"
    """Invalid type for ``filepath`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.log_report`"""
    LOG_REPORT_INVALID_REPORTS_LOG_PATH_ARG_TYPE = "LOG_REPORT_INVALID_REPORTS_LOG_PATH_ARG_TYPE"
    """Invalid type for ``reports_log_path`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.log_report`"""
    LOG_REPORT_INVALID_CASE_ARG_TYPE = "LOG_REPORT_INVALID_CASE_ARG_TYPE"
    """Invalid type for ``case`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.log_report`"""
    LOG_REPORT_INVALID_CHOICE_ARG_TYPE = "LOG_REPORT_INVALID_CHOICE_ARG_TYPE"
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.log_report`"""
    # report()
    REPORT_INVALID_LOG_METADATA_ARG = "REPORT_INVALID_LOG_METADATA_ARG"
    """Invalid type for ``log_metadata`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report`"""

    # dispatch_to_targets()
    DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_LOG_METADATA_REPORTS_LOG_PATH_TYPE = (
        "DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_LOG_METADATA_REPORTS_LOG_PATH_TYPE")
    """Invalid type for ``log_metadata.reports_log_path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_LOG_METADATA_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_LOG_METADATA_ARG_TYPE")
    """Invalid type for ``log_metadata`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_PATH_TYPE = (
        "DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_PATH_TYPE")
    """Invalid type for ``path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_REPORTS_LOG_PATH_TYPE = (
        "DISPATCH_TO_TARGETS_FILESYSTEM_INVALID_REPORTS_LOG_PATH_TYPE")
    """Invalid type for ``reports_log_path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_REPORTS_LOG_PATH_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_REPORTS_LOG_PATH_ARG_TYPE")
    """Invalid type for ``reports_log_path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_ARGS_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_ARGS_ARG_TYPE")
    """Invalid type for ``args`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_OUTPUT_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_OUTPUT_ARG_TYPE")
    """Invalid type for ``output`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_TYPE")
    """Invalid type for ``filename_base`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_VALUE = (
        "DISPATCH_TO_TARGETS_INVALID_FILENAME_BASE_ARG_VALUE")
    """Invalid value for ``filename_base`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`
    - must be a non-empty, non-blank string."""
    DISPATCH_TO_TARGETS_INVALID_PATH_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_PATH_ARG_TYPE")
    """Invalid type for ``path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_CALLBACK_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_CALLBACK_ARG_TYPE")
    """Invalid type for ``callback`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_CASE_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_CASE_ARG_TYPE")
    """Invalid type for ``case`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_CHOICE_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_SECTION_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_SECTION_ARG_TYPE")
    """Invalid type for ``section`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_SESSION_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_SESSION_ARG_TYPE")
    """Invalid type for ``session`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_INVALID_PRIORITIZED_ARG_TYPE = (
        "DISPATCH_TO_TARGETS_INVALID_PRIORITIZED_ARG_TYPE")
    """Invalid type for ``prioritized`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets`"""
    DISPATCH_TO_TARGETS_UNSUPPORTED_TARGET = (
        "DISPATCH_TO_TARGETS_UNSUPPORTED_TARGET")
    """An unsupported Target was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin.dispatch_to_targets` method"""

    # get_prioritized_subdir()
    GET_PRIORITIZED_SUBDIR_INVALID_CHOICE_ARG_TYPE = (
        "GET_PRIORITIZED_SUBDIR_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_subdir`"""
    # get_prioritized_file_suffix()
    GET_PRIORITIZED_FILE_SUFFIX_INVALID_CHOICE_ARG_TYPE = (
        "GET_PRIORITIZED_FILE_SUFFIX_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_file_suffix`"""

    # get_prioritized_file_unique()
    GET_PRIORITIZED_FILE_UNIQUE_INVALID_CHOICE_ARG_TYPE = (
        "GET_PRIORITIZED_FILE_UNIQUE_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_file_unique`"""

    # get_prioritized_file_append()
    GET_PRIORITIZED_FILE_APPEND_INVALID_CHOICE_ARG_TYPE = (
        "GET_PRIORITIZED_FILE_APPEND_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_file_append`"""

    # get_prioritized_default_targets()
    GET_PRIORITIZED_DEFAULT_TARGETS_INVALID_CHOICE_ARG_TYPE = (
        "GET_PRIORITIZED_DEFAULT_TARGETS_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_default_targets`"""  # pylint: disable=line-too-long  # noqa: E501

    # _validate_render_by_args()
    VALIDATE_RENDER_BY_ARGS_INVALID_LOG_METADATA_ARG_TYPE = "VALIDATE_RENDER_BY_ARGS_INVALID_LOG_METADATA_ARG_TYPE"
    """Invalid type for ``log_metadata`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`
    """
    VALIDATE_RENDER_BY_ARGS_INVALID_TIMESTAMP_ARG_TYPE = "VALIDATE_RENDER_BY_ARGS_INVALID_TIMESTAMP_ARG_TYPE"
    """Invalid type for ``timestamp`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_MISSING_PATH_FOR_FILESYSTEM_TARGET = (
        "VALIDATE_RENDER_BY_ARGS_MISSING_PATH_FOR_FILESYSTEM_TARGET")
    """Missing ``path`` argument for FILESYSTEM target in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_MISSING_REPORTS_LOG_PATH_FOR_FILESYSTEM_TARGET = (
        "VALIDATE_RENDER_BY_ARGS_MISSING_REPORTS_LOG_PATH_FOR_FILESYSTEM_TARGET")
    """Missing ``reports_log_path`` argument for FILESYSTEM target in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_REPORTS_LOG_PATH_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_REPORTS_LOG_PATH_ARG_TYPE")
    """Invalid type for ``reports_log_path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_RENDERER_ARG_TYPE")
    """Invalid type for ``renderer`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_ARGS_ARG_TYPE")
    """Invalid type for ``args`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_CASE_ARG_TYPE")
    """Invalid type for ``case`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_CHOICE_ARG_TYPE")
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_SESSION_ARG_TYPE")
    """Invalid type for ``session`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_PATH_ARG_TYPE")
    """Invalid type for ``path`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""
    VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE = (
        "VALIDATE_RENDER_BY_ARGS_INVALID_CALLBACK_ARG_TYPE")
    """Invalid type for ``callback`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._orchestration.OrchestrationMixin._validate_render_by_args`"""

    # get_prioritized_options()
    GET_PRIORITIZED_OPTIONS_INVALID_CASE_ARG_TYPE = "GET_PRIORITIZED_OPTIONS_INVALID_CASE_ARG_TYPE"
    """Invalid type for ``case`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_options`"""
    GET_PRIORITIZED_OPTIONS_INVALID_CHOICE_ARG_TYPE = "GET_PRIORITIZED_OPTIONS_INVALID_CHOICE_ARG_TYPE"
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.get_prioritized_options`"""

    # select_targets_from_args()
    SELECT_TARGETS_FROM_ARGS_DEFAULT_TARGET_UNSUPPORTED = "SELECT_TARGETS_FROM_ARGS_DEFAULT_TARGET_UNSUPPORTED"
    """A default target specified is not supported by the choice in
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""
    SELECT_TARGETS_FROM_ARGS_INVALID_ARGS_ARG = "SELECT_TARGETS_FROM_ARGS_INVALID_ARGS_ARG"
    """Invalid type for ``args`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""
    SELECT_TARGETS_FROM_ARGS_INVALID_CHOICE_ARG = "SELECT_TARGETS_FROM_ARGS_INVALID_CHOICE_ARG"
    """Invalid type for ``choice`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""
    SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG = "SELECT_TARGETS_FROM_ARGS_INVALID_DEFAULT_TARGETS_ARG"
    """Invalid type or value for ``default_targets`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""

    # find_options_by_type()
    FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG = "FIND_OPTIONS_BY_TYPE_INVALID_OPTIONS_ARG"
    """Invalid type for ``options`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.find_options_by_type`
    - something other than None or an Iterable of ReporterOptions."""
    FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE = "FIND_OPTIONS_BY_TYPE_INVALID_CLS_ARG_TYPE"
    """Invalid type for ``cls`` argument in
    :meth:`~simplebench.reporters.reporter.mixins._prioritization.PrioritizationMixin.find_options_by_type`"""

    # _validate_subclass_config()
    VALIDATE_SUBCLASS_CONFIG_CANNOT_BE_REPORTER = (
        "VALIDATE_SUBCLASS_CONFIG_CANNOT_BE_REPORTER")
    """Subclass of Reporter cannot be the base Reporter class itself"""
    VALIDATE_SUBCLASS_CONFIG_MUST_BE_SUBCLASS_OF_REPORTER = (
        "VALIDATE_SUBCLASS_CONFIG_MUST_BE_SUBCLASS_OF_REPORTER")
    """Must be a subclass of Reporter"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_NOT_IMPLEMENTED = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_NOT_IMPLEMENTED")
    """_OPTION_TYPE class attribute must be implemented in subclass"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_INVALID_TYPE = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_INVALID_TYPE")
    """_OPTION_TYPE cannot be set to the base ReporterOptions class"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_MUST_BE_SUBCLASS = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_TYPE_MUST_BE_SUBCLASS")
    """_OPTION_TYPE must be set to a subclass of ReporterOptions"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_IMPLEMENTED = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_IMPLEMENTED")
    """_OPTIONS_KWARGS class attribute must be implemented in subclass"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_A_DICT = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_NOT_A_DICT")
    """_OPTIONS_KWARGS class attribute must be a dict in subclass"""
    VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_KEYS_MUST_BE_STR = (
        "VALIDATE_SUBCLASS_CONFIG_OPTIONS_KWARGS_KEYS_MUST_BE_STR")
    """_OPTIONS_KWARGS class attribute must be a dictionary with type str keys in subclass"""

    # set_default_options()
    SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE_BASE_CLASS_INSTANCE = (
        "SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE_BASE_CLASS_INSTANCE")
    """Invalid type for ``options`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.set_default_options` - cannot be ReporterOptions
    base class instance"""
    SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE = "SET_DEFAULT_OPTIONS_INVALID_OPTIONS_ARG_TYPE"
    """Invalid type for ``options`` argument in
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.set_default_options`"""

    # __init__()
    REPORTER_ABSTRACT_BASE_CLASS_INSTANTIATION = "REPORTER_ABSTRACT_BASE_CLASS_INSTANTIATION"
    """The Reporter class is an abstract base class and cannot be instantiated directly"""
    SECTIONS_ITEMS_ARG_VALUE = "SECTIONS_ITEMS_ARG_VALUE"
    """``sections`` is an empty iterable"""
    TARGETS_INVALID_ARG_TYPE = "INVALID_TARGETS_ARG_TYPE"
    """Something other than an iterable of Target enums was passed as the ``targets`` arg"""
    TARGETS_ITEMS_ARG_VALUE = "TARGETS_ITEMS_ARG_VALUE"
    """``targets`` is an empty iterable"""
    FORMATS_INVALID_ARG_TYPE = "INVALID_FORMATS_ARG_TYPE"
    """Something other than an iterable of Format enums was passed as the ``formats`` arg"""
    FORMATS_ITEMS_ARG_VALUE = "FORMATS_ITEMS_ARG_VALUE"
    """``formats`` is an empty iterable"""
    DEFAULT_TARGETS_ITEMS_ARG_VALUE = "DEFAULT_TARGETS_ITEMS_ARG_VALUE"
    """Placeholder for empty default targets - not used in practice"""
    FILE_UNIQUE_AND_FILE_APPEND_EXACTLY_ONE_REQUIRED = (
        "FILE_UNIQUE_AND_FILE_APPEND_EXACTLY_ONE_REQUIRED")
    """Exactly one of ``file_unique`` or ``file_append`` must be True"""
    DUPLICATE_CHOICE_NAMES_IN_CHOICES = "DUPLICATE_CHOICE_NAMES_IN_CHOICES"
    """Duplicate Choice names were found in the ``choices`` argument"""

    EMPTY_TARGETS_ARG_VALUE = "EMPTY_TARGETS_ARG_VALUE"
    """The ``targets`` arg cannot be an empty sequence"""
    DEFAULT_TARGETS_INVALID_ARG_TYPE = "DEFAULT_TARGETS_INVALID_ARG_TYPE"
    """Something other than a set of Target enums or None was passed as the ``default_targets`` arg"""
    DEFAULT_TARGETS_INVALID_ENTRY_TYPE = "DEFAULT_TARGETS_INVALID_ENTRY_TYPE"
    """Something other than a Target enum was found in the ``default_targets`` arg"""
    SUBDIR_INVALID_ARG_TYPE = "SUBDIR_INVALID_ARG_TYPE"
    """Something other than a string was passed as the default ``subdir`` arg"""
    SUBDIR_INVALID_ARG_VALUE = "SUBDIR_INVALID_ARG_VALUE"
    """The default ``subdir`` arg must be an alphanumeric string (a-z, A-Z, 0-9) or an empty string"""
    SUBDIR_TOO_LONG = "SUBDIR_TOO_LONG"
    """The ``subdir`` arg cannot be longer than 64 characters."""
    NAME_INVALID_ARG_TYPE = "NAME_INVALID_ARG_TYPE"
    """Something other than a string was passed as the ``name`` arg"""
    NAME_INVALID_ARG_VALUE = "NAME_INVALID_ARG_VALUE"
    """The ``name`` arg cannot be an empty string"""
    DESCRIPTION_INVALID_ARG_TYPE = "DESCRIPTION_INVALID_ARG_TYPE"
    """Something other than a string was passed as the ``description`` arg"""
    DESCRIPTION_INVALID_ARG_VALUE = "DESCRIPTION_INVALID_ARG_VALUE"
    """The ``description`` arg cannot be an empty string"""
    SECTIONS_INVALID_ARG_TYPE = "SECTIONS_INVALID_ARG_TYPE"
    """Something other than a sequence of Section enums was passed as the ``sections`` arg"""
    EMPTY_SECTIONS_ARG_VALUE = "EMPTY_SECTIONS_ARG_VALUE"
    """The ``sections`` arg cannot be an empty sequence (can be Section.NULL if needed)"""

    REPORTER_OPTIONS_NOT_IMPLEMENTED = "REPORTER_OPTIONS_NOT_IMPLEMENTED"
    """The ReporterOptions could not be found in the Case, Choice, or default options."""
    HARDCODED_DEFAULT_OPTIONS_NOT_IMPLEMENTED = "HARDCODED_DEFAULT_OPTIONS_NOT_IMPLEMENTED"
    """The Reporter.__HARDCODED_DEFAULT_OPTIONS property must be initialized with a
    ReporterOptions subclass instance by subclasses"""
    CHOICES_NOT_IMPLEMENTED = "CHOICES_NOT_IMPLEMENTED"
    """The Reporter.choices property must be implemented in subclasses"""
    NAME_NOT_IMPLEMENTED = "NAME_NOT_IMPLEMENTED"
    """The Reporter.name property must be initialized as a str by subclasses"""
    NAME_INVALID_VALUE = "NAME_INVALID_VALUE"
    """The Reporter.name property must be initialized as a non-empty string by subclasses"""
    OPTIONS_TYPE_INVALID_VALUE = "OPTIONS_TYPE_INVALID_VALUE"
    """The Reporter.options_type property must be a subclass type of ReporterOptions or None"""
    DESCRIPTION_NOT_IMPLEMENTED = "DESCRIPTION_NOT_IMPLEMENTED"
    """The Reporter.description property must be initialized as a str by subclasses"""
    DESCRIPTION_INVALID_VALUE = "DESCRIPTION_INVALID_VALUE"
    """The Reporter.description property must be initialized as a string by subclasses"""
    FILE_SUFFIX_INVALID_ARG_TYPE = "FILE_SUFFIX_INVALID_ARG_TYPE"
    """Something other than a str was passed as the ``file_suffix`` argument to the Reporter constructor"""
    FILE_SUFFIX_INVALID_ARG_VALUE = "FILE_SUFFIX_INVALID_ARG_VALUE"
    """The ``file_suffix`` argument passed to the Reporter constructor contained non-alphanumeric characters"""
    FILE_SUFFIX_ARG_TOO_LONG = "FILE_SUFFIX_ARG_TOO_LONG"
    """The ``file_suffix`` argument passed to the Reporter constructor exceeded the maximum length of 10 characters"""
    FILE_UNIQUE_INVALID_ARG_TYPE = "FILE_UNIQUE_INVALID_ARG_TYPE"
    """Something other than a bool was passed as the ``file_unique`` argument to the Reporter constructor"""
    FILE_APPEND_INVALID_ARG_TYPE = "FILE_APPEND_INVALID_ARG_TYPE"
    """Something other than a bool was passed as the ``file_append`` argument to the Reporter constructor"""
    FILE_UNIQUE_AND_APPEND_MUTUALLY_EXCLUSIVE = "FILE_UNIQUE_AND_APPEND_MUTUALLY_EXCLUSIVE"
    """``file_unique`` and ``file_append`` arguments are mutually exclusive and cannot both be True"""
    RUN_REPORT_NOT_IMPLEMENTED = "RUN_REPORT_NOT_IMPLEMENTED"
    """The Reporter.run_report() method must be implemented by subclasses"""
    ADD_FLAGS_UNSUPPORTED_FLAG_TYPE = "ADD_FLAGS_UNSUPPORTED_FLAG_TYPE"
    """The :meth:`~simplebench.reporters.reporter.mixins._argparse.ArgparseMixin.add_flags_to_argparse`
    method only supports flags of type FlagType.BOOLEAN or FlagType.TARGET_LIST"""
    ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE = (
        "ADD_LIST_OF_TARGETS_FLAGS_INVALID_CHOICE_ARG_TYPE")
    """Something other than a Choice instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._argparse.ArgparseMixin.add_list_of_targets_flags` method"""
    ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE = "ADD_BOOLEAN_FLAGS_INVALID_CHOICE_ARG_TYPE"
    """Something other than a Choice instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._argparse.ArgparseMixin.add_boolean_flags` method"""
    FORMATS_NOT_IMPLEMENTED = "FORMATS_NOT_IMPLEMENTED"
    """The Reporter.formats property must be implemented in subclasses"""
    INVALID_FORMATS_ENTRY_TYPE = "INVALID_FORMATS_ENTRY_TYPE"
    """Something other than a Format enum was found in the ``formats`` argument."""
    SECTIONS_NOT_IMPLEMENTED = "SECTIONS_NOT_IMPLEMENTED"
    """The Reporter.sections property must be implemented in subclasses"""
    INVALID_SECTIONS_ENTRY_TYPE = "INVALID_SECTIONS_ENTRY_TYPE"
    """Something other than a Section enum was found in the ``sections`` argument."""
    TARGETS_NOT_IMPLEMENTED = "TARGETS_NOT_IMPLEMENTED"
    """The Reporter.targets property must be implemented in subclasses"""
    INVALID_TARGETS_ENTRY_TYPE = "INVALID_TARGETS_ENTRY_TYPE"
    """Something other than a Target enum was found in the ``targets`` argument."""
    REPORT_INVALID_ARGS_ARG_TYPE = "REPORT_INVALID_ARGS_ARG_TYPE"
    """Something other than a Namespace instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method as the ``args`` argument"""
    REPORT_INVALID_CASE_ARG = "REPORT_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method"""
    REPORT_INVALID_CHOICE_ARG = "REPORT_INVALID_CHOICE_ARG"
    """Something other than a Choice instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method"""
    REPORT_INVALID_SESSION_ARG = "REPORT_INVALID_SESSION_ARG"
    """Something other than a Session instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method"""
    REPORT_INVALID_PATH_ARG = "REPORT_INVALID_PATH_ARG"
    """Something other than a Path instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method"""
    REPORT_INVALID_CALLBACK_ARG = "REPORT_INVALID_CALLBACK_ARG"
    """Something other than a callable was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method as the ``callback`` argument"""
    REPORT_UNSUPPORTED_SECTION = "REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method in the Choice.sections"""
    REPORT_UNSUPPORTED_TARGET = "REPORT_UNSUPPORTED_TARGET"
    """An unsupported Target was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method in the Choice.targets"""
    REPORT_UNSUPPORTED_FORMAT = "REPORT_UNSUPPORTED_FORMAT"
    """An unsupported Format was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method in the Choice.formats"""
    REPORT_INVALID_REPORTS_LOG_PATH_ARG = "REPORT_INVALID_REPORTS_LOG_PATH_ARG"
    """Something other than a Path instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.report` method as the ``reports_log_path`` argument"""
    CHOICES_INVALID_ARG_TYPE = "INVALID_CHOICES_ARG_TYPE"
    """Something other than a ChoicesConf instance was passed as the ``choices`` argument to the Reporter constructor"""
    CHOICES_INVALID_ARG_VALUE = "INVALID_CHOICES_ARG_VALUE"
    """The ``choices`` argument passed to the Reporter constructor must contain at least one ChoiceConf"""
    ADD_CHOICE_UNSUPPORTED_SECTION = "ADD_CHOICE_UNSUPPORTED_SECTION"
    """A Section in the Choice instance passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.add_choice` method is not supported by the Reporter"""
    ADD_CHOICE_INVALID_ARG_TYPE = "ADD_CHOICE_INVALID_ARG_TYPE"
    """Something other than a Choice instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.add_choice` method"""
    ADD_CHOICE_UNSUPPORTED_TARGET = "ADD_CHOICE_UNSUPPORTED_TARGET"
    """A Target in the Choice instance passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.add_choice` method is not supported by the Reporter"""
    ADD_CHOICE_UNSUPPORTED_FORMAT = "ADD_CHOICE_UNSUPPORTED_FORMAT"
    """A Format in the Choice instance passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.add_choice` method is not supported by the Reporter"""
    ADD_FLAGS_INVALID_PARSER_ARG_TYPE = "ADD_FLAGS_INVALID_PARSER_ARG_TYPE"
    """Something other than an ArgumentParser instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._argparse.ArgparseMixin.add_flags_to_argparse` method"""

    # target_filesystem()
    TARGET_FILESYSTEM_INVALID_LOG_METADATA_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_LOG_METADATA_ARG_TYPE"
    """Something other than a LogMetadata instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method"""
    TARGET_FILESYSTEM_INVALID_TIMESTAMP_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_TIMESTAMP_ARG_TYPE"
    """Something other than a float or int was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem`
    method as the ``timestamp`` argument"""
    TARGET_FILESYSTEM_INVALID_REPORTS_LOG_PATH_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_REPORTS_LOG_PATH_ARG_TYPE"
    """Something other than a Path instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method
    as the ``reports_log_path`` argument"""
    TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_PATH_ARG_TYPE"
    """Something other than a Path instance was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method"""
    TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_TYPE"
    """Something other than a string was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method as the ``subdir``
    argument"""
    TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_VALUE = "TARGET_FILESYSTEM_INVALID_SUBDIR_ARG_VALUE"
    """The ``subdir`` argument passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method
    contains non-alphanumeric characters"""
    TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_APPEND_ARG_TYPE"
    """Something other than a bool was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method as the ``append``
    argument"""
    TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_UNIQUE_ARG_TYPE"
    """Something other than a bool was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem` method as the ``unique``
    argument"""
    TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE = "TARGET_FILESYSTEM_INVALID_OUTPUT_ARG_TYPE"
    """Something other than a str, bytes, rich.Text, or rich.Table was passed to the
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.target_filesystem`
    method as the ``output`` argument"""
    TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS = (
        "TARGET_FILESYSTEM_APPEND_UNIQUE_INCOMPATIBLE_ARGS")
    """One, and only one, of ``append`` and ``unique`` must be True when writing to the filesystem"""
    TARGET_FILESYSTEM_OUTPUT_FILE_EXISTS = "TARGET_FILESYSTEM_OUTPUT_FILE_EXISTS"
    """The output file already exists and the ``append`` or ``unique`` options were not specified"""
    RUN_REPORT_UNSUPPORTED_SECTION = "RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the reporter's
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.run_report` method"""
    RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE = "RUN_REPORT_INVALID_CHOICE_OPTIONS_TYPE"
    """Something other than a RichTableChoiceOptions instance was set for a choice option"""
    SELECT_TARGETS_FROM_ARGS_UNKNOWN_TARGET_IN_ARGS = "SELECT_TARGETS_FROM_ARGS_UNKNOWN_TARGET_IN_ARGS"
    """An unknown target string was specified in the command-line arguments passed to
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""
    SELECT_TARGETS_FROM_ARGS_UNSUPPORTED_TARGET = "SELECT_TARGETS_FROM_ARGS_UNSUPPORTED_TARGET"
    """An unsupported target string was specified in the command-line arguments passed to
    :meth:`~simplebench.reporters.reporter.mixins._targets.TargetsMixin.select_targets_from_args`"""
    SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_TYPE = "SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_TYPE"
    """Invalid ``targets`` argument type:
    - must be of type `frozenset[Target]` or `None.`"""
    SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_VALUE = "SET_DEFAULT_TARGETS_INVALID_TARGETS_ARG_VALUE"
    """Invalid ``targets`` argument value:
    - must be a `frozenset` of `Target` enum members."""
    SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_TYPE = "SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_TYPE"
    """Invalid ``subdir`` argument type:
    - must be of type `str` or `None.`"""
    SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_VALUE = "SET_DEFAULT_SUBDIR_INVALID_SUBDIR_ARG_VALUE"
    """Invalid ``subdir`` argument value:
    - must be a `str` of only alphanumeric characters (A-Z, a-z, 0-9) or `None`."""
    GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE = "GET_OPTIONS_INVALID_OPTIONS_ARG_TYPE"
    """Invalid ``options`` argument type:
    - must be of type `Iterable[ReporterOptions]` or `None`."""
    GET_OPTIONS_INVALID_OPTIONS_ARG_VALUE = "GET_OPTIONS_INVALID_OPTIONS_ARG_VALUE"
    """Invalid ``options`` argument value:
    - ``options`` argument iterable contains something other than `ReporterOptions` instances."""
    RENDER_NOT_IMPLEMENTED = "RENDER_NOT_IMPLEMENTED"
    """The Reporter.render() method must be implemented by subclasses"""
    RICH_TEXT_TO_PLAIN_TEXT_INVALID_WIDTH_ARG_TYPE = "RICH_TEXT_TO_PLAIN_TEXT_INVALID_WIDTH_ARG_TYPE"
    """Something other than an int was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.rich_text_to_plain_text` method
    as the ``virtual_console_width`` argument"""
    RICH_TEXT_TO_PLAIN_TEXT_INVALID_WIDTH_ARG_VALUE = "RICH_TEXT_TO_PLAIN_TEXT_INVALID_WIDTH_ARG_VALUE"
    """The ``virtual_console_width`` argument passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.rich_text_to_plain_text` method
    is outside the valid range"""
    RICH_TEXT_TO_PLAIN_TEXT_INVALID_RICH_TEXT_ARG_TYPE = "RICH_TEXT_TO_PLAIN_TEXT_INVALID_RICH_TEXT_ARG_TYPE"
    """Something other than a rich.Text or rich.Table instance was passed to the
    :meth:`~simplebench.reporters.reporter.reporter.Reporter.rich_text_to_plain_text` method as the ``rich_text``
    argument"""
