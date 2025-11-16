"""Reporter Priority class for managing prioritized reporter options."""
from __future__ import annotations

from typing import TYPE_CHECKING

from simplebench.enums import Target
from simplebench.exceptions import SimpleBenchTypeError
from simplebench.reporters.reporter.exceptions import PrioritizedErrorTag
from simplebench.reporters.reporter.options import ReporterOptions
from simplebench.reporters.reporter.protocols import ReporterProtocol
from simplebench.type_proxies import is_case, is_choice, is_reporter

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.reporters.reporter import Reporter


class Prioritized:
    """Class for managing prioritized reporter options.

    This class encapsulates the prioritized options for a reporter,
    determining the effective configuration based on the choice and case
    provided. It retrieves prioritized settings such as default targets,
    subdirectory, file suffix, uniqueness, append mode, and reporter options
    based on the hierarchy of case-specific, choice-specific, and reporter default values.

    It collates the relevant values from the various Reporter().get_prioritized_... methods
    and makes them accessible as proxied attributes of the Prioritized instance.

    Attributes:
        default_targets (frozenset[Target]): The prioritized default targets.
        subdir (str): The prioritized subdirectory for report files.
        file_suffix (str): The prioritized file suffix for report files.
        file_unique (bool): The prioritized uniqueness flag for report files.
        file_append (bool): The prioritized append mode flag for report files.
        options (ReporterOptions): The prioritized reporter options.
    """
    def __init__(self, *,
                 reporter: ReporterProtocol | Reporter,
                 choice: Choice,
                 case: Case) -> None:
        """Initialize the Prioritized class with choice and case.

        Args:
            reporter (Reporter): The Reporter instance.
            choice (Choice): The Choice instance specifying the report configuration.
            case (Case): The Case instance for which the report is being generated.
        """

        if not is_reporter(reporter) or not isinstance(reporter, ReporterProtocol):
            raise SimpleBenchTypeError(
                f"Invalid reporter argument: expected Reporter instance, got {type(reporter).__name__}",
                tag=PrioritizedErrorTag.INIT_INVALID_REPORTER_ARG_TYPE)
        if not is_choice(choice):
            raise SimpleBenchTypeError(
                f"Invalid choice argument: expected Choice instance, got {type(choice).__name__}",
                tag=PrioritizedErrorTag.INIT_INVALID_CHOICE_ARG_TYPE)
        if not is_case(case):
            raise SimpleBenchTypeError(
                f"Invalid case argument: expected Case instance, got {type(case).__name__}",
                tag=PrioritizedErrorTag.INIT_INVALID_CASE_ARG_TYPE)
        self._reporter: Reporter = reporter
        self._choice: Choice = choice
        self._case: Case = case

    @property
    def default_targets(self) -> frozenset[Target]:
        """Get the prioritized default targets."""
        return self._reporter.get_prioritized_default_targets(choice=self._choice)

    @property
    def subdir(self) -> str:
        """Get the prioritized subdirectory for report files."""
        return self._reporter.get_prioritized_subdir(choice=self._choice)

    @property
    def file_suffix(self) -> str:
        """Get the prioritized file suffix for report files."""
        return self._reporter.get_prioritized_file_suffix(choice=self._choice)

    @property
    def file_unique(self) -> bool:
        """Get the prioritized uniqueness flag for report files."""
        return self._reporter.get_prioritized_file_unique(choice=self._choice)

    @property
    def file_append(self) -> bool:
        """Get the prioritized append mode flag for report files."""
        return self._reporter.get_prioritized_file_append(choice=self._choice)

    @property
    def options(self) -> ReporterOptions:
        """Get the prioritized reporter options."""
        return self._reporter.get_prioritized_options(case=self._case, choice=self._choice)
