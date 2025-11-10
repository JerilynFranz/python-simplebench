"""Protocols for the Reporter class and its mixins."""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import (TYPE_CHECKING, Iterable, Protocol, TypeVar,
                    runtime_checkable)

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

    @property
    def name(self) -> str:
        ...

    @property
    def description(self) -> str:
        ...

    @property
    def options_type(self) -> type[ReporterOptions]:
        ...

    def supported_sections(self) -> frozenset[Section]:
        ...

    def supported_targets(self) -> frozenset[Target]:
        ...

    def supported_formats(self) -> frozenset[Format]:
        ...

    _name: str
    _description: str
    _options_type: type[ReporterOptions]
    _sections: frozenset[Section]
    _targets: frozenset[Target]
    _formats: frozenset[Format]
    _choices: Choices
    _default_targets: frozenset[Target]
    _subdir: str
    _file_suffix: str
    _file_unique: bool
    _file_append: bool

    @property
    def choices(self) -> Choices:
        ...

    @classmethod
    def get_hardcoded_default_options(cls) -> ReporterOptions:
        ...

    @classmethod
    def set_default_options(cls, options: ReporterOptions | None = None) -> None:
        ...

    @classmethod
    def get_default_options(cls) -> ReporterOptions:
        ...

    @staticmethod
    def find_options_by_type(options: Iterable[ReporterOptions] | None, cls: type[T]) -> T | None:
        ...

    def add_choice(self, choice: Choice) -> None:
        ...

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        ...

    def add_list_of_targets_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        ...

    def add_boolean_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        ...

    def select_targets_from_args(
        self, *, args: Namespace, choice: Choice, default_targets: Iterable[Target]
    ) -> set[Target]:
        ...

    def get_prioritized_default_targets(self, choice: Choice) -> frozenset[Target]:
        ...

    def get_prioritized_subdir(self, choice: Choice) -> str:
        ...

    def get_prioritized_options(self, case: Case, choice: Choice) -> ReporterOptions:
        ...

    def get_prioritized_file_suffix(self, choice: Choice) -> str:
        ...

    def get_prioritized_file_unique(self, choice: Choice) -> bool:
        ...

    def get_prioritized_file_append(self, choice: Choice) -> bool:
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
        ...

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
        ...

    def render_by_section(self, *,
                          renderer: ReportRenderer,
                          args: Namespace,
                          case: Case,
                          choice: Choice,
                          path: Path | None = None,
                          session: Session | None = None,
                          callback: ReporterCallback | None = None) -> None:
        ...

    def render_by_case(self, *,
                       renderer: ReportRenderer,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
        ...

    def target_filesystem(
        self,
        *,
        path: Path | None,
        subdir: str,
        filename: str,
        output: str | bytes | Text | Table,
        unique: bool = False,
        append: bool = False,
    ) -> None:
        ...

    def target_callback(
        self,
        callback: ReporterCallback | None,
        case: Case,
        section: Section,
        output_format: Format,
        output: str | bytes | Text | Table,
    ) -> None:
        ...

    def target_console(self, session: Session | None, output: str | bytes | Text | Table) -> None:
        ...

    def rich_text_to_plain_text(self, rich_text: Text | Table) -> str:
        ...

    def get_base_unit_for_section(self, section: Section) -> str:
        ...

    def get_all_stats_values(self, results: list, section: Section) -> list[float]:
        ...
