"""ErrorTags for the graph scatter module in the reporters package."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class ScatterPlotReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the ScatterPlotReporter class."""
    RUN_REPORT_UNSUPPORTED_OUTPUT_FORMAT = "GRAPH_REPORTER_RUN_REPORT_UNSUPPORTED_OUTPUT_FORMAT"
    """The output format specified in the GraphOptions is not supported.

    Supported formats are:
      - `ImageType.SVG`
      - `ImageType.PNG`
    """
    RUN_REPORT_UNSUPPORTED_SECTION = "RUN_REPORT_UNSUPPORTED_SECTION"
    """An unsupported Section was passed to the ScatterPlotReporter.run_report() method in the Choice.sections"""
    PLOT_GRAPH_INVALID_CASE_ARG = "PLOT_GRAPH_INVALID_CASE_ARG"
    """Something other than a Case instance was passed to the ScatterPlotReporter._plot_graph() method"""
    PLOT_GRAPH_INVALID_GRAPHPATH_ARG = "PLOT_GRAPH_INVALID_GRAPHPATH_ARG"
    """Something other than a Path instance was passed to the ScatterPlotReporter._plot_graph() method"""
    PLOT_GRAPH_INVALID_SECTION_ARG = "PLOT_GRAPH_INVALID_SECTION_ARG"
    """Something other than a valid Section was passed to the ScatterPlotReporter._plot_graph() method"""


@enum_docstrings
class ScatterPlotChoiceOptionsErrorTag(ErrorTag):
    """ErrorTags for exceptions in the ScatterPlotChoiceOptions class."""
    DEFAULT_TARGETS_NOT_ITERABLE = "DEFAULT_TARGETS_NOT_ITERABLE"
    """The default targets specified in the ScatterPlotChoiceOptions must be an iterable of Target enum members."""
    INVALID_DEFAULT_TARGETS_TYPE = "INVALID_DEFAULT_TARGETS_TYPE"
    """The default targets specified in the ScatterPlotChoiceOptions are not valid Target enum members."""
    INVALID_DEFAULT_TARGETS_VALUE = "INVALID_DEFAULT_TARGETS_VALUE"
    """The default targets specified in the ScatterPlotChoiceOptions cannot be empty."""
    INVALID_SUBDIR_TYPE = "INVALID_SUBDIR_TYPE"
    """The subdir specified in the ScatterPlotChoiceOptions must be a string."""
    INVALID_SUBDIR_VALUE = "INVALID_SUBDIR_VALUE"
    """The subdir specified in the ScatterPlotChoiceOptions cannot be an empty string."""
    INVALID_DEFAULT_WIDTH_TYPE = "INVALID_DEFAULT_WIDTH_TYPE"
    """The width specified in the ScatterPlotChoiceOptions must be an integer."""
    INVALID_DEFAULT_WIDTH_VALUE = "INVALID_DEFAULT_WIDTH_VALUE"
    """The width specified in the ScatterPlotChoiceOptions must be greater than zero."""
    INVALID_DEFAULT_HEIGHT_TYPE = "INVALID_DEFAULT_HEIGHT_TYPE"
    """The height specified in the ScatterPlotChoiceOptions must be an integer."""
    INVALID_DEFAULT_HEIGHT_VALUE = "INVALID_DEFAULT_HEIGHT_VALUE"
    """The height specified in the ScatterPlotChoiceOptions must be greater than zero."""
    INVALID_DEFAULT_DPI_TYPE = "INVALID_DEFAULT_DPI_TYPE"
    """The DPI specified in the ScatterPlotChoiceOptions must be an integer."""
    INVALID_DEFAULT_DPI_VALUE = "INVALID_DEFAULT_DPI_VALUE"
    """The DPI specified in the ScatterPlotChoiceOptions must be between 75 and 400 (inclusive)."""


@enum_docstrings
class ScatterPlotOptionsErrorTag(ErrorTag):
    """ErrorTags for exceptions in the ScatterPlotOptions class."""
    INVALID_THEME_TYPE = "INVALID_THEME_TYPE"
    """The theme specified in the GraphOptions has an invalid type. It must be a dict or None."""
    UNSUPPORTED_STYLE = "UNSUPPORTED_STYLE"
    """The style specified in the GraphOptions is not supported. Supported styles are 'darkgrid' and 'default'"""
    UNSUPPORTED_OUTPUT_FORMAT = "UNSUPPORTED_OUTPUT_FORMAT"
    """The output format specified in the GraphOptions is not supported. Supported formats are 'svg' and 'png'"""
    INVALID_ASPECT_RATIO = "INVALID_ASPECT_RATIO"
    """The aspect ratio specified in the GraphOptions is invalid. It must be a positive number."""
    INVALID_X_LABELS_ROTATION_TYPE = (
        "INVALID_X_LABELS_ROTATION_TYPE")
    """The x_labels_rotation specified in the GraphOptions has an invalid type. It must be a float."""
    INVALID_Y_STARTS_AT_ZERO_TYPE = (
        "INVALID_Y_STARTS_AT_ZERO_TYPE")
    """The y_starts_at_zero value specified in the GraphOptions has an invalid type. It must be a bool."""
