"""ErrorTags for MatPlotLibReporter exceptions in the reporters.graph.matplotlib.reporter module."""
from simplebench.exceptions import ErrorTag
from simplebench.enums import enum_docstrings


@enum_docstrings
class MatPlotLibReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the MatPlotLibReporter class."""
    RUN_REPORT_UNSUPPORTED_SECTION = "RUN_REPORT_UNSUPPORTED_SECTION"
    """The section specified in the MatPlotLibReporter.run_report method is not supported."""
    IMAGE_TYPE_INVALID_CASE_ARG_TYPE = "IMAGE_TYPE_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.image_type method is not an ICase instance."""
    IMAGE_TYPE_INVALID_CHOICE_ARGTYPE = "IMAGE_TYPE_INVALID_CHOICE_ARGTYPE"
    """The choice argument passed to the MatPlotLibReporter.image_type method is not a Choice instance."""
    IMAGE_TYPE_INVALID_OPTIONS_TYPE_ARG_TYPE = "IMAGE_TYPE_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.image_type method is not
    a MatPlotLibOptions subclass."""
    CASE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE = "CASE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE"
    """The image_type value specified in the Case().MatPlotLibOptions is not supported."""
    CHOICE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE = "CHOICE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE"
    """The image_type value specified in the Choice().MatPlotLibOptions is not supported."""
    WIDTH_INVALID_CASE_ARG_TYPE = "WIDTH_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.width method is not an ICase instance."""
    WIDTH_INVALID_CHOICE_ARG_TYPE = "WIDTH_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.width method is not a Choice instance."""
    WIDTH_INVALID_OPTIONS_TYPE_ARG_TYPE = "WIDTH_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.width method is not
    a MatPlotLibOptions subclass."""
    HEIGHT_INVALID_CASE_ARG_TYPE = "HEIGHT_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.height method is not an ICase instance."""
    HEIGHT_INVALID_CHOICE_ARG_TYPE = "HEIGHT_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.height method is not a Choice instance."""
    HEIGHT_INVALID_OPTIONS_TYPE_ARG_TYPE = "HEIGHT_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.height method is not
    a MatPlotLibOptions subclass."""
    DPI_INVALID_CASE_ARG_TYPE = "DPI_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.dpi method is not an ICase instance."""
    DPI_INVALID_CHOICE_ARG_TYPE = "DPI_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.dpi method is not a Choice instance."""
    DPI_INVALID_OPTIONS_TYPE_ARG_TYPE = "DPI_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.dpi method is not
    a MatPlotLibOptions subclass."""
    X_LABELS_ROTATION_INVALID_CASE_ARG_TYPE = "X_LABELS_ROTATION_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.x_labels_rotation method is not an ICase instance."""
    X_LABELS_ROTATION_INVALID_CHOICE_ARG_TYPE = "X_LABELS_ROTATION_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.x_labels_rotation method is not a Choice instance."""
    X_LABELS_ROTATION_INVALID_OPTIONS_TYPE_ARG_TYPE = "X_LABELS_ROTATION_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.x_labels_rotation method is not
    a MatPlotLibOptions subclass."""
    Y_STARTS_AT_ZERO_INVALID_CASE_ARG_TYPE = "Y_STARTS_AT_ZERO_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.y_starts_at_zero method is not an ICase instance."""
    Y_STARTS_AT_ZERO_INVALID_CHOICE_ARG_TYPE = "Y_STARTS_AT_ZERO_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.y_starts_at_zero method is not a Choice instance."""
    Y_STARTS_AT_ZERO_INVALID_OPTIONS_TYPE_ARG_TYPE = "Y_STARTS_AT_ZERO_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.y_starts_at_zero method is not
    a MatPlotLibOptions subclass."""
    THEME_INVALID_CASE_ARG_TYPE = "THEME_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.theme method is not an ICase instance."""
    THEME_INVALID_CHOICE_ARG_TYPE = "THEME_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.theme method is not a Choice instance."""
    THEME_INVALID_OPTIONS_TYPE_ARG_TYPE = "THEME_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.theme method is not
    a MatPlotLibOptions subclass."""
    STYLE_INVALID_CASE_ARG_TYPE = "STYLE_INVALID_CASE_ARG_TYPE"
    """The case argument passed to the MatPlotLibReporter.style method is not an ICase instance."""
    STYLE_INVALID_CHOICE_ARG_TYPE = "STYLE_INVALID_CHOICE_ARG_TYPE"
    """The choice argument passed to the MatPlotLibReporter.style method is not a Choice instance."""
    STYLE_INVALID_OPTIONS_TYPE_ARG_TYPE = "STYLE_INVALID_OPTIONS_TYPE_ARG_TYPE"
    """The options_type argument passed to the MatPlotLibReporter.style method is not
    a MatPlotLibOptions subclass."""
    PLOT_GRAPH_NOT_IMPLEMENTED = "PLOT_GRAPH_NOT_IMPLEMENTED"
    """The plot_graph method has not been implemented by the subclass."""
