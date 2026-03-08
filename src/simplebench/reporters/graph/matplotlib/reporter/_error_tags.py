"""ErrorTags for MatPlotLibReporter exceptions in the
:mod:`~simplebench.reporters.graph.matplotlib.reporter` module.
"""

from enum import auto
from simplebench.doc_utils import enum_docstrings
from simplebench.exceptions import ErrorTag


@enum_docstrings
class _MatPlotLibReporterErrorTag(ErrorTag):
    """ErrorTags for exceptions in the :class:`~.MatPlotLibReporter` class."""

    RUN_REPORT_UNSUPPORTED_SECTION = auto()
    """The metric specified in the MatPlotLibReporter.run_report method is not supported."""
    IMAGE_TYPE_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.image_type method is not an ICase instance."""
    IMAGE_TYPE_INVALID_CHOICE_ARGTYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.image_type method is not a Choice instance."""
    IMAGE_TYPE_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.image_type method is not
    a MatPlotLibOptions subclass."""
    CASE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE = auto()
    """The image_type value specified in the Case().MatPlotLibOptions is not supported."""
    CHOICE_OPTIONS_UNSUPPORTED_IMAGE_TYPE_VALUE = auto()
    """The image_type value specified in the Choice().MatPlotLibOptions is not supported."""
    WIDTH_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.width method is not an ICase instance."""
    WIDTH_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.width method is not a Choice instance."""
    WIDTH_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.width method is not
    a MatPlotLibOptions subclass."""
    HEIGHT_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.height method is not an ICase instance."""
    HEIGHT_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.height method is not a Choice instance."""
    HEIGHT_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.height method is not
    a MatPlotLibOptions subclass."""
    DPI_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.dpi method is not an ICase instance."""
    DPI_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.dpi method is not a Choice instance."""
    DPI_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.dpi method is not
    a MatPlotLibOptions subclass."""
    X_LABELS_ROTATION_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.x_labels_rotation method is not an ICase instance."""
    X_LABELS_ROTATION_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.x_labels_rotation method is not a Choice instance."""
    X_LABELS_ROTATION_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.x_labels_rotation method is not
    a MatPlotLibOptions subclass."""
    Y_STARTS_AT_ZERO_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.y_starts_at_zero method is not an ICase instance."""
    Y_STARTS_AT_ZERO_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.y_starts_at_zero method is not a Choice instance."""
    Y_STARTS_AT_ZERO_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.y_starts_at_zero method is not
    a MatPlotLibOptions subclass."""
    THEME_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.theme method is not an ICase instance."""
    THEME_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.theme method is not a Choice instance."""
    THEME_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.theme method is not
    a MatPlotLibOptions subclass."""
    STYLE_INVALID_CASE_ARG_TYPE = auto()
    """The case argument passed to the MatPlotLibReporter.style method is not an ICase instance."""
    STYLE_INVALID_CHOICE_ARG_TYPE = auto()
    """The choice argument passed to the MatPlotLibReporter.style method is not a Choice instance."""
    STYLE_INVALID_OPTIONS_TYPE_ARG_TYPE = auto()
    """The options_type argument passed to the MatPlotLibReporter.style method is not
    a MatPlotLibOptions subclass."""
    PLOT_GRAPH_NOT_IMPLEMENTED = auto()
    """The plot_graph method has not been implemented by the subclass."""
