"""Protocols for the Reporter class and its mixins."""
# pylint: disable=unnecessary-ellipsis
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Iterable, Protocol, TypeVar, runtime_checkable

from rich.table import Table
from rich.text import Text

from simplebench.enums import Format, Section, Target
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer

if TYPE_CHECKING:
    from simplebench.case import Case
    from simplebench.reporters.choice.choice import Choice
    from simplebench.reporters.choices.choices import Choices
    from simplebench.reporters.reporter.options import ReporterOptions
    from simplebench.session import Session

T = TypeVar('T')


@runtime_checkable
class ReporterProtocol(Protocol):
    """Protocol for the Reporter class and its mixins."""
    _OPTIONS_TYPE: ClassVar[type[ReporterOptions]]
    _OPTIONS_KWARGS: ClassVar[dict[str, Any]]

    @property
    def name(self) -> str:
        """Return the name of the reporter."""
        ...

    @property
    def description(self) -> str:
        """Return the description of the reporter."""
        ...

    def supported_sections(self) -> frozenset[Section]:
        """Return the supported sections for this reporter."""
        ...

    def supported_targets(self) -> frozenset[Target]:
        """Return the supported targets for this reporter."""
        ...

    def supported_formats(self) -> frozenset[Format]:
        """Return the supported formats for this reporter."""
        ...

    _name: str
    """The name of the reporter (private backend attribute)."""
    _description: str
    """The description of the reporter (private backend attribute)."""
    _sections: frozenset[Section]
    """The supported sections for this reporter (private backend attribute)."""
    _targets: frozenset[Target]
    """The supported targets for this reporter (private backend attribute)."""
    _formats: frozenset[Format]
    """The supported formats for this reporter (private backend attribute)."""
    _choices: Choices
    """The choices for this reporter (private backend attribute)."""
    _default_targets: frozenset[Target]
    """The default targets for this reporter (private backend attribute)."""
    _subdir: str
    """The default subdirectory for this reporter (private backend attribute)."""
    _file_suffix: str
    """The default file suffix for this reporter (private backend attribute)."""
    _file_unique: bool
    """The default file unique flag for this reporter (private backend attribute)."""
    _file_append: bool
    """The default file append flag for this reporter (private backend attribute)."""

    @property
    def choices(self) -> Choices:
        """The Choices instance for this reporter."""
        ...

    @property
    def default_targets(self) -> frozenset[Target]:
        """The default set of Targets for the reporter."""
        ...

    @property
    def subdir(self) -> str:
        """The subdirectory where report files will  be saved."""
        ...

    @property
    def file_suffix(self) -> str:
        """The file suffix for report files."""
        ...

    @property
    def file_unique(self) -> bool:
        """Indicates whether report files should have unique names."""
        ...

    @property
    def file_append(self) -> bool:
        """Indicates whether report files should be appended to if they exist."""
        ...

    @classmethod
    def get_hardcoded_default_options(cls) -> ReporterOptions:
        """Get the hardcoded default options for the reporter."""
        ...

    @classmethod
    def set_default_options(cls, options: ReporterOptions | None = None) -> None:
        """Set the default options for the reporter."""
        ...

    @classmethod
    def get_default_options(cls) -> ReporterOptions:
        """Get the default options for the reporter."""
        ...

    @staticmethod
    def find_options_by_type(options: Iterable[ReporterOptions] | None, cls: type[T]) -> T | None:
        """Find and return the first ReporterOptions instance of the specified type."""
        ...

    def add_choice(self, choice: Choice) -> None:
        """Add a Choice instance to the reporter's choices."""
        ...

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add the reporter's command-line flags to an ArgumentParser."""
        ...

    def add_list_of_targets_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Add a Choice's command-line flags to an ArgumentParser."""
        ...

    def add_boolean_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Add boolean flags for a Choice to an ArgumentParser."""
        ...

    def select_targets_from_args(
        self, *, args: Namespace, choice: Choice, default_targets: Iterable[Target]
    ) -> set[Target]:
        """Select output targets based on command-line arguments and choice."""
        ...

    def get_prioritized_default_targets(self, choice: Choice) -> frozenset[Target]:
        """Get the prioritized default targets from the choice or reporter defaults."""
        ...

    def get_prioritized_subdir(self, choice: Choice) -> str:
        """Get the prioritized subdirectory from the choice or reporter defaults."""
        ...

    def get_prioritized_options(self, case: Case, choice: Choice) -> ReporterOptions:
        """Get the prioritized ReporterOptions for the given case and choice."""
        ...

    def get_prioritized_file_suffix(self, choice: Choice) -> str:
        """Get the prioritized file suffix from the choice or reporter."""
        ...

    def get_prioritized_file_unique(self, choice: Choice) -> bool:
        """Get the prioritized file unique flag from the choice or reporter."""
        ...

    def get_prioritized_file_append(self, choice: Choice) -> bool:
        """Get the prioritized file append flag from the choice or reporter."""
        ...

    def report(
        self,
        *,
        args: Namespace,
        case: Case,
        choice: Choice,
        path: Path | None = None,
        session: Session | None = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Generate the report for the given case and choice."""
        ...

    def render(self, *, case: "Case", section: "Section", options: "ReporterOptions") -> str | bytes | Text | Table:
        """Render the report for a specific case and section.

        Args:
            case (Case): The Case instance representing the benchmarked code.
            section (Section): The section to render the report for.
            options (ReporterOptions): The options for rendering the report.

        Returns:
            str | bytes | Text | Table: The rendered report output.
        """
        raise NotImplementedError

    def run_report(
        self,
        *,
        args: Namespace,
        case: Case,
        choice: Choice,
        path: Path | None = None,
        session: Session | None = None,
        callback: ReporterCallback | None = None,
    ) -> None:
        """Run the report generation process for the given case and choice."""
        ...

    def render_by_section(self, *,
                          renderer: ReportRenderer,
                          args: Namespace,
                          case: Case,
                          choice: Choice,
                          path: Path | None = None,
                          session: Session | None = None,
                          callback: ReporterCallback | None = None) -> None:
        """Render the report by section for the given case and choice."""
        ...

    def render_by_case(self, *,
                       renderer: ReportRenderer,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
        """Render the report by case for the given case and choice."""
        ...

    def target_filesystem(
        self,
        *,
        path: Path | None,
        subdir: str,
        filename: str,
        output: str | bytes | Text | Table,
        unique: bool,
        append: bool,
    ) -> None:
        """Helper method to write report data to the filesystem."""
        ...

    def target_callback(
        self,
        callback: ReporterCallback | None,
        case: Case,
        section: Section,
        output_format: Format,
        output: str | bytes | Text | Table,
    ) -> None:
        """Helper method to send report data to a callback function."""
        ...

    def target_console(self, session: Session | None, output: str | bytes | Text | Table) -> None:
        """Helper method to output report data to the console."""
        ...

    def rich_text_to_plain_text(self, rich_text: Text | Table) -> str:
        """Convert rich text or table to plain text."""
        ...

    def get_base_unit_for_section(self, section: Section) -> str:
        """Get the base unit for the given section."""
        ...

    def get_all_stats_values(self, results: list, section: Section) -> list[float]:
        """Get all statistical values for the given results and section."""
        ...

    def _validate_render_by_args(
        self, *,
        renderer: ReportRenderer,
        args: Namespace,
        case: Case,
        choice: Choice,
        path: Path | None = None,
        session: Session | None = None,
        callback: ReporterCallback | None = None
    ) -> None:
        """Validate common arguments for render_by_case and render_by_section methods."""
        ...

    def dispatch_to_targets(
            self, *,
            output: str | bytes | Text | Table,
            filename_base: str,
            args: Namespace,
            choice: Choice,
            case: Case,
            section: Section,
            path: Path | None = None,
            session: Session | None = None,
            callback: ReporterCallback | None = None) -> None:
        """Deliver the rendered output to the specified targets."""
        ...
