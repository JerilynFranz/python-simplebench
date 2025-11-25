"""Session management for SimpleBench."""
from __future__ import annotations

from argparse import ArgumentError, ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence

from rich.console import Console
from rich.progress import Progress

from simplebench.case import Case
from simplebench.enums import Color, Target, Verbosity
from simplebench.exceptions import SimpleBenchArgumentError, SimpleBenchTypeError, _SessionErrorTag
from simplebench.reporters.choice import Choice
from simplebench.reporters.choices import Choices
from simplebench.reporters.log.report_log_metadata import ReportLogMetadata
from simplebench.reporters.protocols import ReporterCallback
from simplebench.reporters.reporter_manager import ReporterManager
from simplebench.runners import SimpleRunner
from simplebench.tasks import ProgressTracker, RichProgressTasks
from simplebench.utils import sanitize_filename

if TYPE_CHECKING:
    from simplebench.reporters.reporter import Reporter


class Session():
    """Container for session related information while running benchmarks.

    :ivar args: The command line arguments for the session.
    :vartype args: Namespace
    :ivar cases: Sequence of benchmark cases for the session.
    :vartype cases: Sequence[Case]
    :ivar output_path: The output path for reports.
    :vartype output_path: Path, optional
    :ivar console: A Rich Console instance for displaying output.
    :vartype console: Console
    :ivar verbosity: Verbosity level for console output (default: :attr:`Verbosity.NORMAL`)
    :vartype verbosity: Verbosity
    :ivar default_runner: The default runner class to use for Cases
        that do not specify a runner. Defaults to :class:`~.runners.SimpleRunner`.
    :vartype default_runner: type[SimpleRunner]
    :ivar show_progress: Whether to show progress bars during execution. Defaults to False.
    :vartype show_progress: bool
    :ivar progress: Rich Progress instance for displaying progress bars. (read only)
    :vartype progress: Progress
    :ivar tasks: The ProgressTasks instance for managing progress tasks. (read only)
    :vartype tasks: RichProgressTasks
    :ivar reporter_manager: The ReporterManager instance for managing reporters. (read only)
    :vartype reporter_manager: ReporterManager
    """
    def __init__(self,
                 *,
                 cases: Optional[Sequence[Case]] = None,
                 verbosity: Verbosity = Verbosity.NORMAL,
                 default_runner: type[SimpleRunner] | None = None,
                 args_parser: Optional[ArgumentParser] = None,
                 show_progress: bool = False,
                 output_path: Optional[Path] = None,
                 console: Optional[Console] = None) -> None:
        """Create a new Session.

        :param cases: A Sequence of benchmark cases for the session.
            If None, an empty list will be created. Defaults to None.
        :type cases: Sequence[Case], optional
        :param verbosity: The verbosity level for console output.
            Defaults to :attr:`Verbosity.NORMAL`.
        :type verbosity: Verbosity, optional
        :param default_runner: The default runner class to use
            for Cases that do not specify a runner. If None, the default :class:`~.runners.SimpleRunner` is used.
            Defaults to None.
        :type default_runner: type[SimpleRunner], optional
        :param args_parser: The :class:`~argparse.ArgumentParser` instance for the
            session. If None, a new :class:`~argparse.ArgumentParser` will be automatically created.
            Defaults to None.
        :type args_parser: ArgumentParser, optional
        :param show_progress: Whether to show progress bars during execution.
            Defaults to False.
        :type show_progress: bool, optional
        :param output_path: The output path for reports. Defaults to None.
        :type output_path: Path, optional
        :param console: A Rich Console instance for displaying output. If None,
            a new Console will be automatically created. Defaults to None.
        :type console: Console, optional
        :raises SimpleBenchTypeError: If the arguments are of the wrong type.
        """
        # public read/write properties with private backing fields
        self.default_runner = default_runner
        self.args_parser = ArgumentParser() if args_parser is None else args_parser
        self.cases = [] if cases is None else cases
        self.verbosity = verbosity
        self.show_progress = show_progress
        self.output_path = output_path
        self.console = Console() if console is None else console

        # private attributes
        self._progress_tasks: RichProgressTasks = RichProgressTasks(verbosity=verbosity, console=self.console)
        """ProgressTasks instance for managing progress tasks - backing field for the 'tasks' attribute."""
        self._progress: Progress = self.tasks.progress
        """Rich Progress instance for displaying progress bars - backing field for the 'progress' attribute."""
        self._reporter_manager: ReporterManager = ReporterManager()
        """The ReporterManager instance for managing reporters."""
        self._choices: Choices = self._reporter_manager.choices
        """The Choices instance for managing registered reporters."""

        # backing fields for public read-only properties
        self._args: Optional[Namespace] = None
        """The command line arguments - backing field for the 'args' attribute."""
        self._console: Console = self._progress.console
        """Rich Console instance for displaying output - backing field for the 'console' attribute."""

    def parse_args(self, args: Sequence[str] | None = None) -> None:
        """Parse the command line arguments using the session's :class:`~argparse.ArgumentParser`.

        This method parses the command line arguments and stores them in the session's :attr:`args` property.
        By default, it parses the arguments from :data:`sys.argv`. If ``args`` is provided, it will parse
        the arguments from the provided sequence of strings instead.

        :param args: A list of command line arguments to parse. If None,
            the arguments will be taken from :data:`sys.argv`. Defaults to None.
        :type args: Sequence[str], optional
        :raises SimpleBenchTypeError: If the ``args_parser`` is not set.
        """
        if args is not None:
            if not isinstance(args, Sequence):
                raise SimpleBenchTypeError(
                    "'args' argument must either be None or a list of str: "
                    f"type of passed 'args' was {type(args).__name__}",
                    tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE)
            args = tuple(args)
            if not all(isinstance(arg, str) for arg in args):
                raise SimpleBenchTypeError(
                    "'args' argument must either be None or a list of str: A non-str item was found in the passed list",
                    tag=_SessionErrorTag.PARSE_ARGS_INVALID_ARGS_TYPE)

        self._args = self._args_parser.parse_args(args=args)

    @property
    def reporter_manager(self) -> ReporterManager:
        """Return the :class:`~.reporters.reporter_manager.ReporterManager` instance for managing reporters.

        :return: The :class:`~.reporters.reporter_manager.ReporterManager` instance for managing reporters.
        :rtype: ReporterManager
        """
        return self._reporter_manager

    def add_reporter_flags(self) -> None:
        """Add the command line flags for all registered reporters to the session's ArgumentParser.

        Any conflicts in flag names with already declared :class:`~argparse.ArgumentParser` flags will have to be
        handled by the reporters themselves.

        This method should be called before :meth:`parse_args`.

        It is placed in its own method so that a user can customize the :class:`~argparse.ArgumentParser`
        before or after adding the reporter flags as needed.

        It also allows the user to unregister reporters before adding the reporter flags if they
        want to omit specific built-in reporters entirely.


        :raises SimpleBenchArgumentError: If there is a conflict or other error in reporter flag names.
        """
        try:
            # Add reporter flags to the ArgumentParser based on command line args defined in each registered Choice
            self._reporter_manager.add_reporters_to_argparse(self._args_parser)
        except ArgumentError as arg_err:
            raise SimpleBenchArgumentError(
                argument_name=arg_err.argument_name,
                message=f'Error adding reporter flags to ArgumentParser: {arg_err.message}',
                tag=_SessionErrorTag.ARGUMENT_ERROR_ADDING_FLAGS
            ) from arg_err

    def run(self) -> None:
        """Run all benchmark cases in the session."""
        if self._verbosity > Verbosity.NORMAL:
            self._console.print(f'Running {len(self.cases)} benchmark case(s)...')
        self.tasks.clear()
        progress_tracker = ProgressTracker(
            session=self,
            task_name='Session:cases',
            progress_max=len(self.cases),
            description='Running benchmark cases',
            color=Color.WHITE
        )

        if self.show_progress and self.verbosity > Verbosity.QUIET and self.tasks:
            self.tasks.start()

        case_counter: int = 0
        progress_tracker.reset()
        progress_tracker.update(
            completed=0,
            description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(self.cases)})')
        progress_tracker.start()

        for case in self.cases:
            progress_tracker.update(
                description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(self.cases)})',
                completed=case_counter,
                refresh=True)
            case_counter += 1
            case.run(session=self)
        progress_tracker.stop()
        self.tasks.stop()
        self.tasks.clear()

    def report_keys(self) -> list[str]:
        """Get a list of report keys for all reports to be generated in this session.

        This filters the report choices based on the command line arguments
        that were set and parsed when the session was created and returns a list of
        report keys for the reports that should be generated.

        :return: A list of report keys for all reports to be generated in this session.
        :rtype: list[str]
        """
        report_keys: list[str] = []
        for key in self._choices.all_choice_args():
            # skip all Choices that are not set in self.args
            if not getattr(self.args, key, None):
                continue
            report_keys.append(key)
        return report_keys

    def report(self) -> None:
        """Generate reports for all benchmark cases in the session."""

        # all_choice_args returns a set of all Namespace args from all Choice instances
        # we check each arg to see if it is set in self.args.
        # The logic here is that if the arg is set, the user wants that report. By
        # making the lookup go from the defined Choices to the args, we ensure
        # that we only consider valid args that are associated with a Choice.
        if self.verbosity > Verbosity.NORMAL:
            self._console.print(f"Generating reports for {len(self.cases)} case(s)...")
        now = datetime.now()
        epoch_timestamp = now.timestamp()
        timestamp = now.strftime('%Y%m%d%H%M%S')

        processed_choices: set[str] = set()
        report_keys: list[str] = self.report_keys()
        n_reports = len(report_keys)

        self.tasks.clear()
        reports_progress_tracker = ProgressTracker(
            session=self,
            task_name='Session:reports',
            progress_max=n_reports,
            description='Running reports',
            color=Color.WHITE
        )

        cases_progress_tracker = ProgressTracker(
            session=self,
            task_name='Session:cases',
            progress_max=len(self.cases),
            description='Generating reports for cases',
            color=Color.CYAN)

        reports_progress_tracker.start()
        report_counter: int = 0
        for key in report_keys:
            report_counter += 1
            if self.verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Checking report for arg '{key}'")

            choice: Choice | None = self._choices.get_choice_for_arg(key)
            if not isinstance(choice, Choice):
                raise SimpleBenchTypeError(
                    "choice must be a Choice instance",
                    tag=_SessionErrorTag.REPORT_INVALID_CHOICE_RETRIEVED
                )
            # If we have already processed this Choice (there can be multiple
            # possible valid triggering args defined for a single Choice), then skip it.
            if choice and choice.name in processed_choices:
                continue
            processed_choices.add(choice.name)

            reports_progress_tracker.update(
                description=f'Running report {choice.name} ({report_counter:2d}/{n_reports})',
                completed=report_counter - 1,
                refresh=True)

            cases_progress_tracker.reset()
            for case_counter, case in enumerate(self.cases, start=1):
                cases_progress_tracker.update(
                    description=(
                        f'Generating reports for case {case.title} (case {case_counter:2d}/{len(self.cases)})'),
                    completed=case_counter - 1,
                    refresh=True)

                callback: Optional[ReporterCallback] = case.callback
                reporter: Reporter = choice.reporter
                output_path: Path | None = self._output_path
                report_log_path: Path | None = output_path / "_reports_log" if output_path is not None else None
                if Target.FILESYSTEM in choice.targets:
                    if output_path is None:
                        flag: str = '--' + key.replace('_', '-')
                        raise SimpleBenchTypeError(
                            f'output_path must be set to generate Choice {choice.name} / {flag} report',
                            tag=_SessionErrorTag.REPORT_OUTPUT_PATH_NOT_SET
                        )
                    group_path = sanitize_filename(case.group)
                    output_path = output_path / timestamp / group_path
                    if self.verbosity >= Verbosity.DEBUG:
                        self._console.print(f"[DEBUG] Output path for report: {output_path}")
                log_metadata = ReportLogMetadata(
                    timestamp=epoch_timestamp,
                    case=case,
                    choice=choice,
                    reports_log_path=report_log_path)
                if self.args:  # mypy guard
                    reporter.report(
                        log_metadata=log_metadata,
                        args=self.args,
                        case=case,
                        choice=choice,
                        path=output_path,
                        session=self,
                        callback=callback)
            cases_progress_tracker.stop()
        reports_progress_tracker.stop()

        self.tasks.stop()
        self.tasks.clear()

    @property
    def default_runner(self) -> type[SimpleRunner] | None:
        """The session scoped default runner class to use for Cases that do not specify a runner."""
        return self._default_runner

    @default_runner.setter
    def default_runner(self, value: type[SimpleRunner] | None) -> None:
        """Set the session scoped default runner class to use for Cases that do not specify a runner.

        Example:

        .. code-block:: python

            from simplebench import Session
            from mybenchmark.runners import MyCustomRunner

            session = Session(default_runner=MyCustomRunner)

        :param value: The default runner class to use for Cases that do
            not specify a runner. Default is :class:`~.runners.SimpleRunner`.
        :type value: type[SimpleRunner] or None
        :raises SimpleBenchTypeError: If the value is not a subclass of :class:`~.runners.SimpleRunner` or None.
        """
        if value is not None and not (isinstance(value, type) and issubclass(value, SimpleRunner)):
            raise SimpleBenchTypeError(
                f'default_runner must be a subclass of SimpleRunner or None - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_DEFAULT_RUNNER_ARG
            )
        self._default_runner = value

    @property
    def args_parser(self) -> ArgumentParser:
        """The ArgumentParser instance for the session."""
        return self._args_parser

    @args_parser.setter
    def args_parser(self, value: ArgumentParser) -> None:
        """Set the :class:`~argparse.ArgumentParser` instance for the session.

        :param value: The :class:`~argparse.ArgumentParser` instance for the session.
        :type value: ArgumentParser
        """
        if not isinstance(value, ArgumentParser):
            raise SimpleBenchTypeError(
                f'args_parser must be an ArgumentParser instance - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_ARGSPARSER_ARG
            )
        self._args_parser = value

    @property
    def args(self) -> Optional[Namespace]:
        """The command line arguments for the session. This will be None until the parse_args()
        method has been called."""
        return self._args

    @args.setter
    def args(self, value: Namespace) -> None:
        """Set the command line arguments for the session.

        :param value: The command line arguments for the session.
        :type value: Namespace
        """
        if not isinstance(value, Namespace):
            raise SimpleBenchTypeError(
                f'args must be a Namespace instance - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_ARGS_ARG
            )
        self._args = value

    @property
    def progress(self) -> Progress:
        """The Rich Progress instance for displaying progress bars."""
        return self._progress

    @property
    def show_progress(self) -> bool:
        """Whether to show progress bars during execution."""
        return self._show_progress

    @show_progress.setter
    def show_progress(self, value: bool) -> None:
        """Set whether to show progress bars during execution.

        :param value: Whether to show progress bars during execution.
        :type value: bool
        :raises SimpleBenchTypeError: If the value is not a bool.
        """
        if not isinstance(value, bool):
            raise SimpleBenchTypeError(
                f'progress must be a bool - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_PROGRESS_ARG
            )
        self._show_progress = value

    @property
    def tasks(self) -> RichProgressTasks:
        """The RichProgressTasks instance for managing progress tasks."""
        return self._progress_tasks

    @property
    def verbosity(self) -> Verbosity:
        """The Verbosity level for this session."""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, value: Verbosity) -> None:
        """Set the Verbosity level for this session.

        :param value: The new verbosity level for the session.
        :type value: Verbosity
        :raises SimpleBenchTypeError: If the value is not a :class:`~.enums.Verbosity` instance.
        """
        if not isinstance(value, Verbosity):
            raise SimpleBenchTypeError(
                f'verbosity must be a Verbosity instance - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_VERBOSITY_ARG
            )
        self._verbosity = value

    @property
    def cases(self) -> tuple[Case]:
        """Tuple of Cases for this session."""
        return self._cases  # type: ignore[return-value]

    @cases.setter
    def cases(self, value: Sequence[Case]) -> None:
        """Set the tuple of :class:`~simplebench.Cases` for this session.

        This replaces all existing Cases in the session.

        :param value: Sequence of Cases for the Session
        :type value: Sequence[Case]
        :raises SimpleBenchTypeError: If the value is not a :class:`Sequence` of :class:`~simplebench.Case` instances.
        """
        if not isinstance(value, Sequence):
            raise SimpleBenchTypeError(
                f'value must be a Sequence of Case - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_CASES_ARG
            )
        for case in value:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    tag=_SessionErrorTag.PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = tuple(value)

    def add(self, case: Case) -> None:
        """Add a :class:`~.case.Case` to the Sequence of Cases for this session.

        :param case: :class:`~.case.Case` to add to the Session
        :type case: Case
        :raises SimpleBenchTypeError: If the value is not a :class:`~.case.Case` instance.
        """
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                f'case must be a Case instance - cannot be a {type(case)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_CASE_ARG
            )
        self._cases = list(self._cases) + [case]

    def extend(self, cases: Sequence[Case]) -> None:
        """Extend the Sequence of Cases for this session.

        :param cases: Sequence of Cases to add to the Session
        :type cases: Sequence[Case]
        :raises SimpleBenchTypeError: If the value is not a Sequence of Cases.
        """
        if not isinstance(cases, Sequence):
            raise SimpleBenchTypeError(
                f'cases must be a Sequence of Case - cannot be a {type(cases)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_CASES_ARG
            )
        for case in cases:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    tag=_SessionErrorTag.PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = list(self._cases) + list(cases)

    @property
    def output_path(self) -> Path | None:
        """The output path for reports."""
        return self._output_path

    @output_path.setter
    def output_path(self, value: Path | None) -> None:
        """Set the output path for reports.

        :param value: The output path for reports.
        :type value: Path or None
        """
        if value is not None and not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f'output_path must be a Path instance - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_OUTPUT_PATH_ARG
            )
        self._output_path = value

    @property
    def console(self) -> Console:
        """The Rich Console instance for displaying output."""
        return self._console

    @console.setter
    def console(self, value: Console) -> None:
        """Set the Rich Console instance for displaying output.

        :param value: The Rich Console instance for displaying output.
        :type value: Console
        """
        if not isinstance(value, Console):
            raise SimpleBenchTypeError(
                f'console must be a Console instance - cannot be a {type(value)}',
                tag=_SessionErrorTag.PROPERTY_INVALID_CONSOLE_ARG
            )
        self._console = value
