"""Protocols for the Reporter class and its mixins."""
# pylint: disable=unnecessary-ellipsis,line-too-long
# noqa: E501
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Iterable, Protocol, TypeVar, runtime_checkable

from rich.table import Table
from rich.text import Text

from simplebench.enums import Format, Section, Target
from simplebench.reporters.protocols import ReporterCallback, ReportRenderer
from simplebench.reporters.reporter.config import ReporterConfig

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
        """The unique identifying name of the reporter."""
        ...

    @property
    def description(self) -> str:
        """A brief description of the reporter."""
        ...

    def supported_sections(self) -> frozenset[Section]:
        """The set of supported :class:`~simplebench.enums.Section` for the reporter.

        This is the set of :class:`~simplebench.enums.Section` that the reporter can include
        in its reports.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.enums.Section` that are declared in this set.
        """
        ...

    def supported_targets(self) -> frozenset[Target]:
        """The set of supported :class:`~simplebench.enums.Target` for the reporter.

        This is the set of :class:`~simplebench.enums.Target` that the reporter can output to.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.enums.Target` that are declared in this set.
        """
        ...

    def supported_formats(self) -> frozenset[Format]:
        """The set of supported :class:`~simplebench.enums.Format` for the reporter.

        This is the set of :class:`~simplebench.enums.Format` that the reporter can output in.

        Defined :class:`~simplebench.reporters.choice.choice.Choice` can only include
        :class:`~simplebench.enums.Format` that are declared in this set.
        """
        ...

    _config: ReporterConfig
    """The configuration object for the reporter (private backing field)."""
    _choices: Choices
    """An instance of `Choices` containing the `Choice` instances for the `Reporter`.

        This is constructed from an iterable of `Choice` instances (private backing field)"""

    @property
    def config(self) -> ReporterConfig:
        """The configuration object for the reporter."""
        ...

    @property
    def choices(self) -> Choices:
        """The :class:`~simplebench.reporters.choices.choices.Choices` for the reporter.

        The :class:`~simplebench.reporters.choices.choices.Choices` instance contains one or more
        :class:`~simplebench.reporters.choice.choice.Choice` instances, each representing a
        specific combination of sections, targets, and formats, command line flags,
        and descriptions.

        This property allows access to the reporter's choices for generating reports
        and customizing report output and available options.

        :return: The :class:`~simplebench.reporters.choices.choices.Choices` instance for the reporter.
        :rtype: :class:`~simplebench.reporters.choices.choices.Choices`
        """
        ...

    @property
    def default_targets(self) -> frozenset[Target]:
        """The default set of Targets for the reporter."""
        ...

    @property
    def subdir(self) -> str:
        """The subdirectory where report files will be saved."""
        ...

    @property
    def file_suffix(self) -> str:
        """The file suffix for reporter output files."""
        ...

    @property
    def file_unique(self) -> bool:
        """Whether output files should have unique names."""
        ...

    @property
    def file_append(self) -> bool:
        """Whether output files should be appended to."""
        ...

    @classmethod
    def get_hardcoded_default_options(cls) -> ReporterOptions:
        """Get the built-in hardcoded default options for the reporter.

        This abstract method must be implemented by all :class:`~.Reporter` subclasses.
        It defines the base class default options for a reporter and must
        be available in all :class:`~.Reporter` subclasses.

        It returns the hardcoded default :class:`~.ReporterOptions` sub-class instance
        specific to the reporter.

        Sub-classes must implement the following class variables:

            _OPTIONS_TYPE: ClassVar[type[MyOptions]] = MyOptions
            _OPTIONS_KWARGS: ClassVar[dict[str, Any]] = {...}

        or the method will raise an exception.

        :return: The built-in hardcoded default :class:`~.ReporterOptions` instance.
        :raises SimpleBenchNotImplementedError: If required class variables are not implemented
            or are of incorrect types.
        """
        ...

    @classmethod
    def set_default_options(cls, options: ReporterOptions | None = None) -> None:
        """Set the default options for the reporter.

        :param options: The options to set as the default, defaults to None
        :type options: :class:`~.ReporterOptions` or None, optional
        """
        ...

    @classmethod
    def get_default_options(cls) -> ReporterOptions:
        """Get the default options for the reporter.

        Returns the default options set via :meth:`~.set_default_options` if set,
        otherwise returns the built-in hardcoded default options from
        :meth:`~.get_hardcoded_default_options`.

        :return: The default options.
        :rtype: :class:`~.ReporterOptions`
        """
        ...

    @staticmethod
    def find_options_by_type(options: Iterable[ReporterOptions] | None, cls: type[T]) -> T | None:
        """Retrieve an instance of type ``cls`` (if present) from a collection of :class:`~.ReporterOptions`.

        This is used to extract reporter specific options from an iterable container of generic
        :class:`~.ReporterOptions` such as those associated with a
        :class:`~simplebench.reporters.choice.choice.Choice` or :class:`~simplebench.case.Case`.

        For example, a ``CSVReporter`` may define a ``CSVReporterOptions`` class that extends
        :class:`~.ReporterOptions` and use this method to extract the ``CSVReporterOptions`` instance
        from the options iterable:

            options = Reporter.find_options_by_type(case.options, CSVReporterOptions)

        :param options: An iterable of :class:`~.ReporterOptions` instances.
        :type options: Iterable[:class:`~.ReporterOptions`]
        :param cls: The specific subclass type of :class:`~.ReporterOptions` to find.
        :type cls: type[T]
        :return: The instance of the class ``cls`` if found, otherwise ``None``.
        :rtype: T | None
        """
        ...

    def add_choice(self, choice: Choice) -> None:
        """Add a :class:`~simplebench.reporters.choice.choice.Choice` to the reporter's choices.

        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance to add.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :raises SimpleBenchTypeError: If the provided choice is not a
            :class:`~simplebench.reporters.choice.choice.Choice` instance.
        :raises SimpleBenchValueError: If the choice's sections, targets, or formats
            are not supported by the reporter.
        """
        ...

    def add_flags_to_argparse(self, parser: ArgumentParser) -> None:
        """Add command-line flags for the reporter's choices to an :class:`~argparse.ArgumentParser`.

        This method iterates through the reporter's choices and adds the appropriate
        command-line flags for each choice to the provided :class:`~argparse.ArgumentParser`.

        :param parser: The :class:`~argparse.ArgumentParser` to add the flags to.
        :type parser: :class:`~argparse.ArgumentParser`
        """
        ...

    def add_list_of_targets_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Add a list of target flags for a :class:`~simplebench.reporters.choice.choice.Choice` \
            to an :class:`~argparse.ArgumentParser`.

        This method adds a ``--<choice.flag>-targets`` flag to the parser, allowing users
        to specify a comma-separated list of output targets for the choice.

        :param parser: The :class:`~argparse.ArgumentParser` to add the flags to.
        :type parser: :class:`~argparse.ArgumentParser`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` to add the flags for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        """
        ...

    def add_boolean_flags_to_argparse(self, parser: ArgumentParser, choice: Choice) -> None:
        """Add boolean flags for a :class:`~simplebench.reporters.choice.choice.Choice` to an \
            :class:`~argparse.ArgumentParser`.

        This method adds a ``--<choice.flag>`` flag to the parser, which acts as a boolean
        switch to enable the choice.

        :param parser: The :class:`~argparse.ArgumentParser` to add the flags to.
        :type parser: :class:`~argparse.ArgumentParser`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` to add the flags for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        """
        ...

    def select_targets_from_args(
        self, *, args: Namespace, choice: Choice, default_targets: Iterable[Target]
    ) -> set[Target]:
        """Select output targets based on command-line arguments and \
            :class:`~simplebench.reporters.choice.choice.Choice` configuration.

        This method determines the final set of output targets for a given choice by
        prioritizing command-line arguments over the choice's default targets.

        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` to select targets for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param default_targets: The default targets to use if no command-line arguments are provided.
        :type default_targets: Iterable[:class:`~simplebench.enums.Target`]
        :return: A set of the selected output targets.
        :rtype: set[:class:`~simplebench.enums.Target`]
        """
        ...

    def get_prioritized_default_targets(self, choice: Choice) -> frozenset[Target]:
        """Get the prioritized default targets from the choice or reporter defaults.

        :param choice: The choice to get the prioritized default targets for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized default targets.
        :rtype: frozenset[:class:`~simplebench.enums.Target`]
        """
        ...

    def get_prioritized_subdir(self, choice: Choice) -> str:
        """Get the prioritized subdirectory from the choice or reporter defaults.

        :param choice: The choice to get the prioritized subdirectory for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized subdirectory.
        :rtype: str
        """
        ...

    def get_prioritized_options(self, case: Case, choice: Choice) -> ReporterOptions:
        """Get the prioritized :class:`~.ReporterOptions` for the given case and choice.

        :param case: The case to get the prioritized options for.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The choice to get the prioritized options for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized options.
        :rtype: :class:`~.ReporterOptions`
        """
        ...

    def get_prioritized_file_suffix(self, choice: Choice) -> str:
        """Get the prioritized file suffix from the choice or reporter.

        :param choice: The choice to get the prioritized file suffix for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized file suffix.
        :rtype: str
        """
        ...

    def get_prioritized_file_unique(self, choice: Choice) -> bool:
        """Get the prioritized file unique flag from the choice or reporter.

        :param choice: The choice to get the prioritized file unique flag for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized file unique flag.
        :rtype: bool
        """
        ...

    def get_prioritized_file_append(self, choice: Choice) -> bool:
        """Get the prioritized file append flag from the choice or reporter.

        :param choice: The choice to get the prioritized file append flag for.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :return: The prioritized file append flag.
        :rtype: bool
        """
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
        """Generate a report based on the benchmark results.

        This method performs validation and then calls the subclass's :meth:`~.run_report` method.

        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance containing benchmark results.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance specifying
                       the report configuration.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The path to the directory where the report can be saved if needed.
                     Leave as ``None`` if not saving to the filesystem. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance containing benchmark results.
                        Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for additional processing of the report. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        ...

    def render(self, *, case: "Case", section: "Section", options: "ReporterOptions") -> str | bytes | Text | Table:
        """Render the report for a specific case and section.

        This abstract method must be implemented by all :class:`~.Reporter` subclasses.
        It is responsible for generating the actual report content for a given case and section,
        based on the provided options.

        The output can be a string, bytes, or a Rich object (:class:`~rich.text.Text` or
        :class:`~rich.table.Table`).

        :param case: The :class:`~simplebench.case.Case` instance containing the benchmark results.
        :type case: :class:`~simplebench.case.Case`
        :param section: The specific :class:`~simplebench.enums.Section` of the results to render.
        :type section: :class:`~simplebench.enums.Section`
        :param options: The reporter-specific :class:`~.ReporterOptions` for rendering.
        :type options: :class:`~.ReporterOptions`
        :return: The rendered report content.
        :rtype: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        :raises NotImplementedError: If the method is not implemented in a subclass.
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
        """Orchestration hook for report generation.

        This method is the primary customization point for controlling how a report is generated.
        It is called by the public :meth:`~.report` method after all inputs have been validated.

        The default implementation calls :meth:`~._ReporterOrchestrationMixin.render_by_section`,
        which is suitable for most reporters. Subclasses can override this method to provide
        alternative orchestration, such as calling
        :meth:`~._ReporterOrchestrationMixin.render_by_case` for reports that are generated
        once per case.

        .. note::
            This is also the correct place to implement custom logic for non-standard
            targets like :attr:`~simplebench.enums.Target.CUSTOM`.

        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance representing the benchmarked code.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance specifying
                       the report configuration.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The path to the directory where report files will be saved. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance containing benchmark results.
                        Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for additional processing. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        ...

    def render_by_section(self, *,
                          renderer: ReportRenderer,
                          args: Namespace,
                          case: Case,
                          choice: Choice,
                          path: Path | None = None,
                          session: Session | None = None,
                          callback: ReporterCallback | None = None) -> None:
        """Render a report by iterating through each section specified in the choice.

        This method is suitable for reporters that generate a separate output for each
        section of the benchmark results (e.g., OPS, TIMING, MEMORY).

        :param renderer: A callable that takes a case, section, and options, and returns the rendered output.
        :type renderer: :class:`~simplebench.reporters.protocols.report_renderer.ReportRenderer`
        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance for the report.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance for the report.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The output path for filesystem targets. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance for the report. Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for callback targets. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        ...

    def render_by_case(self, *,
                       renderer: ReportRenderer,
                       args: Namespace,
                       case: Case,
                       choice: Choice,
                       path: Path | None = None,
                       session: Session | None = None,
                       callback: ReporterCallback | None = None) -> None:
        """Render a single report for the entire case.

        This method is suitable for reporters that generate a single, consolidated output
        for all sections of the benchmark results.

        :param renderer: A callable that takes a case, section (which will be ``None``), and options,
                         and returns the rendered output.
        :type renderer: :class:`~simplebench.reporters.protocols.report_renderer.ReportRenderer`
        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance for the report.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance for the report.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The output path for filesystem targets. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance for the report. Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for callback targets. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
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
        """Write report data to the filesystem.

        This method handles the logic for writing report output to a file, including
        creating directories, handling unique filenames, and appending to existing files.

        :param path: The base output path.
        :type path: :class:`~pathlib.Path` | None
        :param subdir: The subdirectory within the base path to write to.
        :type subdir: str
        :param filename: The name of the file to write.
        :type filename: str
        :param output: The content to write to the file.
        :type output: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        :param unique: Whether to generate a unique filename if the file already exists.
        :type unique: bool
        :param append: Whether to append to the file if it already exists.
        :type append: bool
        """
        ...

    def target_callback(
        self,
        callback: ReporterCallback | None,
        case: Case,
        section: Section,
        output_format: Format,
        output: str | bytes | Text | Table,
    ) -> None:
        """Send report data to a callback function.

        :param callback: The callback function to call.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None
        :param case: The :class:`~simplebench.case.Case` instance for the report.
        :type case: :class:`~simplebench.case.Case`
        :param section: The :class:`~simplebench.enums.Section` of the report.
        :type section: :class:`~simplebench.enums.Section`
        :param output_format: The :class:`~simplebench.enums.Format` of the output.
        :type output_format: :class:`~simplebench.enums.Format`
        :param output: The report content to send.
        :type output: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        """
        ...

    def target_console(self, session: Session | None, output: str | bytes | Text | Table) -> None:
        """Output report data to the console.

        This method uses the console associated with the :class:`~simplebench.session.Session`
        to print the report output.

        :param session: The :class:`~simplebench.session.Session` instance containing the console.
        :type session: :class:`~simplebench.session.Session` | None
        :param output: The content to print to the console.
        :type output: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        """
        ...

    def rich_text_to_plain_text(self, rich_text: Text | Table) -> str:
        """Convert a Rich :class:`~rich.text.Text` or :class:`~rich.table.Table` object to plain text.

        :param rich_text: The Rich object to convert.
        :type rich_text: :class:`~rich.text.Text` | :class:`~rich.table.Table`
        :return: The plain text representation of the Rich object.
        :rtype: str
        """
        ...

    def get_base_unit_for_section(self, section: Section) -> str:
        """Return the base unit for the specified section.

        :param section: The section to get the base unit for.
        :type section: :class:`~simplebench.enums.Section`
        :return: The base unit for the section.
        :rtype: str
        """
        ...

    def get_all_stats_values(self, results: list, section: Section) -> list[float]:
        """Gathers all primary statistical values for a given section across multiple results.

        It collects mean, median, minimum, maximum, 5th percentile, and 95th percentile,
        from each :class:`~simplebench.results.Results` instance for the specified section.

        This method is useful in determining appropriate scaling factors or units
        for reporting by analyzing the range of values across all results.

        Adjusted standard deviation is not included in this collection because it can
        be ``NaN`` for results with insufficient data points, or orders of magnitude different
        from the other statistics, which can skew scaling calculations.

        :param results: A list of :class:`~simplebench.results.Results` instances to gather
                        statistics from.
        :type results: list[:class:`~simplebench.results.Results`]
        :param section: The section to gather statistics for.
        :type section: :class:`~simplebench.enums.Section`
        :return: A list of all gathered statistical values.
        :rtype: list[float]
        """
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
        """Validate common arguments for render_by_case and render_by_section methods.

        :param renderer: The renderer callable to validate.
        :type renderer: :class:`~simplebench.reporters.protocols.report_renderer.ReportRenderer`
        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param case: The :class:`~simplebench.case.Case` instance.
        :type case: :class:`~simplebench.case.Case`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param path: The output path. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance. Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: The callback function. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
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
        """Deliver the rendered output to the specified targets.

        This method orchestrates sending the generated report content to the various
        output targets (console, filesystem, callback) based on the selected options.

        :param output: The rendered report content.
        :type output: str | bytes | :class:`~rich.text.Text` | :class:`~rich.table.Table`
        :param filename_base: The base name for the output file.
        :type filename_base: str
        :param args: The parsed command-line arguments.
        :type args: :class:`~argparse.Namespace`
        :param choice: The :class:`~simplebench.reporters.choice.choice.Choice` instance for the report.
        :type choice: :class:`~simplebench.reporters.choice.choice.Choice`
        :param case: The :class:`~simplebench.case.Case` instance for the report.
        :type case: :class:`~simplebench.case.Case`
        :param section: The :class:`~simplebench.enums.Section` of the report.
        :type section: :class:`~simplebench.enums.Section`
        :param path: The output path for filesystem targets. Defaults to ``None``.
        :type path: :class:`~pathlib.Path` | None, optional
        :param session: The :class:`~simplebench.session.Session` instance for the report. Defaults to ``None``.
        :type session: :class:`~simplebench.session.Session` | None, optional
        :param callback: A callback function for callback targets. Defaults to ``None``.
        :type callback: :class:`~simplebench.reporters.protocols.reporter_callback.ReporterCallback` | None, optional
        """
        ...
