"""Mixins for the Reporter class.

This package contains mixin classes that provide additional functionality
to the Reporter class in the simplebench framework. These mixins encapsulate
specific behaviors such as argument parsing, target selection, prioritization,
and orchestration of reporting tasks.

    - _ReporterArgparseMixin: Provides methods for integrating reporter
      options with argparse for command-line interfaces.
    - _ReporterTargetMixin: Contains methods for determining and validating
      output targets for reports.
    - _ReporterPrioritizationMixin: Implements logic for prioritizing
      reporter options based on case-specific, choice-specific, and default settings.
    - _ReporterOrchestrationMixin: Manages the overall orchestration of
      report generation, including rendering and callback execution.
"""

from ._argparse import _ReporterArgparseMixin
from ._orchestration import _ReporterOrchestrationMixin
from ._prioritization import _ReporterPrioritizationMixin
from ._targets import _ReporterTargetMixin

__all__ = [
    "_ReporterArgparseMixin",
    "_ReporterOrchestrationMixin",
    "_ReporterPrioritizationMixin",
    "_ReporterTargetMixin",
]
