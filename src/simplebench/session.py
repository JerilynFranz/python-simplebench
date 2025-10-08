"""Session management for SimpleBench."""
from __future__ import annotations
from argparse import ArgumentParser, ArgumentError, Namespace
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence, TYPE_CHECKING

from rich.console import Console
from rich.progress import Progress

from .enums import Verbosity, Target
from .exceptions import ErrorTag, SimpleBenchArgumentError, SimpleBenchTypeError
from .metaclasses import ISession
from .protocols import ReporterCallback
from .reporters import ReporterManager
from .reporters.choices import Choice, Choices
from .runners import SimpleRunner
from .tasks import RichProgressTasks, RichTask
from .case import Case
from .utils import sanitize_filename, platform_id


if TYPE_CHECKING:
    from .reporters import Reporter


class Session(ISession):
    """Container for session related information while running benchmarks.

    Properties:
        args: (Namespace): The command line arguments for the session.
        cases: (Sequence[Case]): Sequence of benchmark cases for the session.
        output_path: (Optional[Path]): The output path for reports.
        console: (Console): A Rich Console instance for displaying output.
        verbosity: (Verbosity): Verbosity level for console output (default: Verbosity.NORMAL)
        default_runner: (Optional[type[SimpleRunner]]): The default runner class to use for Cases
            that do not specify a runner. If None, SimpleRunner will be used. (default: None)
        show_progress: (bool): Whether to show progress bars during execution.
        progress: (Progress): Rich Progress instance for displaying progress bars. (read only)
        tasks: (ProgressTasks): The ProgressTasks instance for managing progress tasks. (read only)
        reporter_manager: (ReporterManager): The ReporterManager instance for managing reporters. (read only)
    """
    def __init__(self,
                 *,
                 cases: Optional[Sequence[Case]] = None,
                 verbosity: Verbosity = Verbosity.NORMAL,
                 default_runner: Optional[type[SimpleRunner]] = None,
                 args_parser: Optional[ArgumentParser] = None,
                 progress: bool = False,
                 output_path: Optional[Path] = None,
                 console: Optional[Console] = None) -> None:
        """Create a new Session.

        Args:
            cases (Sequence[Case]): A Sequence of benchmark cases for the session (default: empty list).
            verbosity (Verbosity): The verbosity level for console output (default: Verbosity.NORMAL)
            default_runner (Optional[type[SimpleRunner]]): The default runner class to use for Cases
                that do not specify a runner. If None, SimpleRunner will be used. (default: None)
            args_parser (Optional[ArgumentParser]): The ArgumentParser instance for the session. If None,
                a new ArgumentParser will be created. (default: None)
            progress (bool): Whether to show progress bars during execution. (default: False)
            output_path (Optional[Path]): The output path for reports. (default: None)
            console: (Optional[Console]): A Rich Console instance for displaying output. If None, a new Console
                will be created. (default: None)

        Raises:
            SimpleBenchTypeError: If the arguments are of the wrong type.
        """
        # public read/write properties with private backing fields
        self.default_runner = default_runner
        self.args_parser = args_parser if args_parser is not None else ArgumentParser()
        self.cases = cases if cases is not None else []
        self.verbosity = verbosity if verbosity is not None else Verbosity.NORMAL
        self.show_progress = progress if progress is not None else False
        self.output_path = output_path
        self.console = console if console is not None else Console()

        # private attributes
        self._progress_tasks: RichProgressTasks = RichProgressTasks(verbosity=verbosity, console=self.console)
        """ProgressTasks instance for managing progress tasks - backing field for the 'tasks' attribute."""
        self._progress: Progress = self._progress_tasks._progress
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
        """Parse the command line arguments using the session's ArgumentParser.

        This method parses the command line arguments and stores them in the session's args property.
        By default, it parses the arguments from sys.argv. If args is provided, it will parse
        the arguments from the provided sequence of strings instead.

        Args:
            args (Optional[Sequence[str]]): A list of command line arguments to parse. If None,
                the arguments will be taken from sys.argv. (default: None)

        Raises:
            SimpleBenchTypeError: If the args_parser is not set.
        """
        if args is not None:
            if not isinstance(args, Sequence):
                raise SimpleBenchTypeError(
                    "'args' argument must either be None or a list of str: "
                    f"type of passed 'args' was {type(args).__name__}",
                    tag=ErrorTag.SESSION_PARSE_ARGS_INVALID_ARGS_TYPE)
            args = tuple(args)
            if not all(isinstance(arg, str) for arg in args):
                raise SimpleBenchTypeError(
                    "'args' argument must either be None or a list of str: A non-str item was found in the passed list",
                    tag=ErrorTag.SESSION_PARSE_ARGS_INVALID_ARGS_TYPE)
        self._args = self._args_parser.parse_args(args=args)

    @property
    def reporter_manager(self) -> ReporterManager:
        """Return the ReporterManager instance for managing reporters.

        Returns:
            ReporterManager: The ReporterManager instance for managing reporters.
        """
        return self._reporter_manager

    def add_reporter_flags(self) -> None:
        """Adds the command line flags for all registered reporters to the session's ArgumentParser.

        Any conflicts in flag names with already declared ArgumentParser flags will have to be
        handled by the reporters themselves.

        This method should be called before parse_args().

        It is placed in its own method so that a user can customize the ArgumentParser
        before or after adding the reporter flags as needed.

        It also allows the user to unregister reporters before adding the reporter flags if they
        want to omit specific built-in reporters entirely.


        Raises:
            SimpleBenchArgumentError: If there is a conflict or other error in reporter flag names.
        """
        try:
            self._reporter_manager.add_reporters_to_argparse(self._args_parser)
        except ArgumentError as arg_err:
            raise SimpleBenchArgumentError(
                argument_name=arg_err.argument_name,
                message=f'Error adding reporter flags to ArgumentParser: {arg_err.message}',
                tag=ErrorTag.REPORTER_MANAGER_ARGUMENT_ERROR_ADDING_FLAGS
            ) from arg_err

    def run(self) -> None:
        """Run all benchmark cases in the session."""
        if self._verbosity > Verbosity.NORMAL:
            self._console.print(f'Running {len(self.cases)} benchmark case(s)...')
        self._progress_tasks.clear()
        task_name: str = 'cases'
        task: RichTask | None = None
        if self.show_progress and self.verbosity > Verbosity.QUIET and self.tasks:
            self._progress_tasks.start()
            task = self.tasks.get(task_name)
            if not task:
                if self._verbosity >= Verbosity.DEBUG:
                    self._console.print(f"[DEBUG] Creating task '{task_name}'")
                task = self.tasks.new_task(
                    name=task_name,
                    description='Running benchmark cases',
                    completed=0,
                    total=len(self.cases))

        case_counter: int = 0
        if task:
            task.reset()
            task.update(
                completed=0,
                description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(self.cases)})'
            )
            task.start()
        for case in self.cases:
            if self.verbosity >= Verbosity.QUIET and self.show_progress and task is not None:
                task.update(
                    description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(self.cases)})',
                    completed=case_counter,
                    refresh=True)
                task.refresh()
            case_counter += 1
            case.run(session=self)
        if task:
            task.stop()
            self._progress_tasks.stop()
            self._progress_tasks.clear()

    def report(self) -> None:
        """Generate reports for all benchmark cases in the session."""

        # all_choice_args returns a set of all Namespace args from all Choice instances
        # we check each arg to see if it is set in self.args.
        # The logic here is that if the arg is set, the user wants that report. By
        # making the lookup go from the defined Choices to the args, we ensure
        # that we only consider valid args that are associated with a Choice.
        if self.verbosity > Verbosity.NORMAL:
            self._console.print(f"Generating reports for {len(self.cases)} case(s)...")
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        platform_name = sanitize_filename(platform_id())
        processed_choices: set[str] = set()
        n_reports: int = 0
        report_keys: list[str] = []
        for key in self._choices.all_choice_args():
            # skip all Choices that are not set in self.args
            if not getattr(self.args, key, None):
                continue
            n_reports += 1
            report_keys.append(key)

        self._progress_tasks.clear()
        task_name: str = 'reports'
        task: RichTask | None = None
        if self.show_progress and self.verbosity > Verbosity.QUIET and self.tasks:
            self._progress_tasks.start()
            task = self.tasks.get(task_name)
            if not task:
                if self._verbosity >= Verbosity.DEBUG:
                    self._console.print(f"[DEBUG] Creating task '{task_name}'")
                task = self.tasks.new_task(
                    name=task_name,
                    description='Running reports',
                    completed=0,
                    total=n_reports)
        if task:
            task.reset()
            task.update(completed=0)
            task.start()

        report_counter: int = 0
        for key in report_keys:
            report_counter += 1
            if self.verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Checking report for arg '{key}'")

            choice: Choice | None = self._choices.get_choice_for_arg(key)
            if not isinstance(choice, Choice):
                raise SimpleBenchTypeError(
                    "choice must be a Choice instance",
                    tag=ErrorTag.SESSION_REPORT_INVALID_CHOICE_RETRIEVED
                )
            # If we have already processed this Choice (there can be multiple
            # possible valid triggering args defined for a single Choice), then skip it.
            if choice and choice.name in processed_choices:
                continue
            processed_choices.add(choice.name)

            if task is not None:
                task.update(
                    description=f'Running report {choice.name} ({report_counter:2d}/{n_reports})',
                    completed=report_counter - 1,
                    refresh=True)
                task.refresh()

            cases_task_name = 'cases'
            cases_task: RichTask | None = None
            if task is not None:
                cases_task = self.tasks.get(cases_task_name)
                if not cases_task:
                    if self._verbosity >= Verbosity.DEBUG:
                        self._console.print(f"[DEBUG] Creating task '{cases_task_name}'")
                    cases_task = self.tasks.new_task(
                        name=cases_task_name,
                        description='Generating reports for cases',
                        completed=0,
                        total=len(self.cases))
            if cases_task:
                cases_task.reset()
                cases_task.update(completed=0)
                cases_task.start()
            for case_counter, case in enumerate(self.cases, start=1):
                if self.verbosity > Verbosity.QUIET and self.show_progress and cases_task is not None:
                    cases_task.update(
                        description=(f'Generating reports for case {case.title} '
                                     f'(case {case_counter:2d}/{len(self.cases)})'),
                        completed=case_counter - 1,
                        refresh=True)
                    cases_task.refresh()
                callback: Optional[ReporterCallback] = case.callback
                reporter: Reporter = choice.reporter
                output_path: Optional[Path] = self._output_path
                if Target.FILESYSTEM in choice.targets:
                    if output_path is None:
                        flag: str = '--' + key.replace('_', '-')
                        raise SimpleBenchTypeError(
                            f'output_path must be set to generate Choice {choice.name} / {flag} report',
                            tag=ErrorTag.SESSION_REPORT_OUTPUT_PATH_NOT_SET
                        )
                    group_path = sanitize_filename(case.group)
                    output_path = output_path / platform_name / group_path / timestamp
                    if self.verbosity >= Verbosity.DEBUG:
                        self._console.print(f"[DEBUG] Output path for report: {output_path}")
                reporter.report(
                    case=case,
                    choice=choice,
                    path=output_path,
                    session=self,
                    callback=callback)
            if cases_task is not None:
                cases_task.stop()
        if task is not None:
            task.stop()
            self._progress_tasks.stop()
            self._progress_tasks.clear()

    @property
    def default_runner(self) -> type[SimpleRunner] | None:
        """The default runner class to use for Cases that do not specify a runner. If None,
        SimpleRunner will be used."""
        return self._default_runner

    @default_runner.setter
    def default_runner(self, value: type[SimpleRunner] | None) -> None:
        """Set the default runner class to use for Cases that do not specify a runner.

        Args:
            value (type[SimpleRunner] | None): The default runner class to use for Cases that do
                not specify a runner. If None, SimpleRunner will be used.
        Raises:
            SimpleBenchTypeError: If the value is not a subclass of SimpleRunner or None.
        """
        if value is not None and not (isinstance(value, type) and issubclass(value, SimpleRunner)):
            raise SimpleBenchTypeError(
                f'default_runner must be a subclass of SimpleRunner or None - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_DEFAULT_RUNNER_ARG
            )
        self._default_runner = value

    @property
    def args_parser(self) -> ArgumentParser:
        """The ArgumentParser instance for the session."""
        return self._args_parser

    @args_parser.setter
    def args_parser(self, value: ArgumentParser) -> None:
        """Set the ArgumentParser instance for the session.

        Args:
            value (ArgumentParser): The ArgumentParser instance for the session.
        """
        if not isinstance(value, ArgumentParser):
            raise SimpleBenchTypeError(
                f'args_parser must be an ArgumentParser instance - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_ARGSPARSER_ARG
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

        Args:
            value (Namespace): The command line arguments for the session.
        """
        if not isinstance(value, Namespace):
            raise SimpleBenchTypeError(
                f'args must be a Namespace instance - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_ARGS_ARG
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

        Args:
            value (bool): Whether to show progress bars during execution.

        Raises:
            SimpleBenchTypeError: If the value is not a bool.
        """
        if not isinstance(value, bool):
            raise SimpleBenchTypeError(
                f'progress must be a bool - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_PROGRESS_ARG
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

        Args:
            value (Verbosity): The new verbosity level for the session.

        Raises:
            SimpleBenchTypeError: If the value is not a Verbosity instance.
        """
        if not isinstance(value, Verbosity):
            raise SimpleBenchTypeError(
                f'verbosity must be a Verbosity instance - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_VERBOSITY_ARG
            )
        self._verbosity = value

    @property
    def cases(self) -> Sequence[Case]:
        """Sequence of Cases for this session."""
        return self._cases

    @cases.setter
    def cases(self, value: Sequence[Case]) -> None:
        """Set the Sequence of Cases for this session.

        Args:
            value (Sequence[Case]): Sequence of Cases for the Session

        Raises:
            SimpleBenchTypeError: If the value is not a Sequence of Cases.
        """
        if not isinstance(value, Sequence):
            raise SimpleBenchTypeError(
                f'value must be a Sequence of Case - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
            )
        for case in value:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    tag=ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = value

    def add(self, case: Case) -> None:
        """Add a Case to the Sequence of Cases for this session.

        Args:
            case (Case): Case to add to the Session

        Raises:
            SimpleBenchTypeError: If the value is not a Case instance.
        """
        if not isinstance(case, Case):
            raise SimpleBenchTypeError(
                f'case must be a Case instance - cannot be a {type(case)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG
            )
        self._cases = list(self._cases) + [case]

    def extend(self, cases: Sequence[Case]) -> None:
        """Extend the Sequence of Cases for this session.

        Args:
            cases (Sequence[Case]): Sequence of Cases to add to the Session

        Raises:
            SimpleBenchTypeError: If the value is not a Sequence of Cases.
        """
        if not isinstance(cases, Sequence):
            raise SimpleBenchTypeError(
                f'cases must be a Sequence of Case - cannot be a {type(cases)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
            )
        for case in cases:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    tag=ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = list(self._cases) + list(cases)

    @property
    def output_path(self) -> Path | None:
        """The output path for reports."""
        return self._output_path

    @output_path.setter
    def output_path(self, value: Path | None) -> None:
        """Set the output path for reports.

        Args:
            value (Path | None): The output path for reports.
        """
        if value is not None and not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f'output_path must be a Path instance - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG
            )
        self._output_path = value

    @property
    def console(self) -> Console:
        """The Rich Console instance for displaying output."""
        return self._console

    @console.setter
    def console(self, value: Console) -> None:
        """Set the Rich Console instance for displaying output.

        Args:
            value (Console): The Rich Console instance for displaying output.
        """
        if not isinstance(value, Console):
            raise SimpleBenchTypeError(
                f'console must be a Console instance - cannot be a {type(value)}',
                tag=ErrorTag.SESSION_PROPERTY_INVALID_CONSOLE_ARG
            )
        self._console = value
