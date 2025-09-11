"""Session management for SimpleBench."""
from __future__ import annotations
from argparse import ArgumentParser, ArgumentError, Namespace
from importlib.resources import path
from pathlib import Path
from typing import Any, Callable, Optional, Sequence, TYPE_CHECKING

from rich.console import Console
from rich.progress import Progress

from .enums import Verbosity
from .exceptions import ErrorTag, SimpleBenchArgumentError, SimpleBenchTypeError
from .reporters import ReporterManager
from .reporters.choices import Choice, Choices, Format, Section, Target
from .tasks import RichProgressTasks, RichTask
from .case import Case


if TYPE_CHECKING:
    from .reporters import Reporter


class Session:
    """Container for session related information while running benchmarks.

    Arguments:
        cases: (Sequence[Case]): A Sequence of benchmark cases for the session.
        verbosity: (Verbosity): The verbosity level for console output (default: Verbosity.NORMAL)

    Properties:
        args: (Namespace): The command line arguments for the session.
        cases: (Sequence[Case]): Sequence of benchmark cases for the session.
        verbosity: (Verbosity): Verbosity level for console output (default: Verbosity.NORMAL)
        progress: (Progress): Rich Progress instance for displaying progress bars. (read only)
        console: (Console): Rich Console instance for displaying output. (read only)
        tasks: (ProgressTasks): The ProgressTasks instance for managing progress tasks. (read only)
    """
    def __init__(self,
                 args_parser: Optional[ArgumentParser] = None,
                 cases: Optional[Sequence[Case]] = None,
                 verbosity: Verbosity = Verbosity.NORMAL,
                 progress: bool = False,
                 output_path: Optional[Path] = None) -> None:
        """Create a new Session.

        Args:
            args_parser (Optional[ArgumentParser]): The ArgumentParser instance for the session. If None,
            a new ArgumentParser will be created. (default: None)
            cases (Sequence[Case]): A Sequence of benchmark cases for the session (default: empty list).
            verbosity (Verbosity): The verbosity level for console output (default: Verbosity.NORMAL)
            progress (bool): Whether to show progress bars during execution. (default: False)
            output_path (Optional[Path]): The output path for reports. (default: None)

        Raises:
            SimpleBenchTypeError: If the arguments are of the wrong type.
        """
        if args_parser is not None and not isinstance(args_parser, ArgumentParser):
            raise SimpleBenchTypeError(
                f'args_parser must be an ArgumentParser instance - cannot be a {type(args_parser)}',
                ErrorTag.SESSION_INIT_INVALID_ARGSPARSER_ARG
            )
        self._args_parser: ArgumentParser = args_parser if args_parser else ArgumentParser()
        """The ArgumentParser instance for the session."""
        self._args: Optional[Namespace] = None
        """The command line arguments for the session."""
        self._cases: Sequence[Case] = [] if cases is None else cases
        """The Sequence of benchmark cases for the session."""
        self._verbosity: Verbosity = Verbosity.NORMAL
        """The verbosity level for console output."""
        self._show_progress: bool = progress
        """Whether to show progress bars during execution."""
        self._progress_tasks: RichProgressTasks = RichProgressTasks(verbosity=verbosity)
        """ProgressTasks instance for managing progress tasks."""
        self._progress: Progress = self._progress_tasks._progress
        """Rich Progress instance for displaying progress bars."""
        self._console: Console = self._progress.console
        """Rich Console instance for displaying output."""
        self._reporter_manager: ReporterManager = ReporterManager()
        """The ReporterManager instance for managing reporters."""
        self._choices: Choices = self._reporter_manager.choices
        """The Choices instance for managing registered reporters."""
        if output_path is not None and not isinstance(output_path, Path):
            raise SimpleBenchTypeError(
                f'output_path must be a Path instance - cannot be a {type(path)}',
                ErrorTag.SESSION_INIT_INVALID_OUTPUT_PATH_ARG
            )
        self._output_path: Optional[Path] = output_path
        """The output path for reports."""

        if not cases:
            cases = []
        if not isinstance(cases, Sequence):
            raise SimpleBenchTypeError(
                f'cases must be a Sequence of Case instances - cannot be a {type(cases)}',
                ErrorTag.SESSION_INIT_INVALID_CASES_SEQUENCE_ARG
            )
        for entry in cases:
            if not isinstance(entry, Case):
                error_text = f'case items must be Case instances - cannot be a {type(entry)}'
                raise SimpleBenchTypeError(error_text,
                                           ErrorTag.SESSION_INIT_INVALID_CASE_ARG_IN_SEQUENCE)
        self._cases = cases
        """The Sequence of benchmark cases for the session."""

        if not isinstance(verbosity, Verbosity):
            raise SimpleBenchTypeError(
                f'verbosity must be a Verbosity instance - cannot be a {type(verbosity)}',
                ErrorTag.SESSION_INIT_INVALID_VERBOSITY_ARG
            )
        self._verbosity = verbosity
        """The verbosity level for console output."""

    def parse_args(self) -> None:
        """Parse the command line arguments using the session's ArgumentParser.

        This method parses the command line arguments and stores them in the session's args property.

        Raises:
            SimpleBenchTypeError: If the args_parser is not set.
        """
        self._args = self._args_parser.parse_args()

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
        if self._verbosity >= Verbosity.NORMAL:
            self._console.print(f'Running {len(self.cases)} benchmark case(s)...')
        task_name: str = 'cases'
        task: RichTask | None = None
        if self.show_progress and self.tasks:
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
            if self.verbosity >= Verbosity.NORMAL and task is not None:
                task.update(
                    description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(self.cases)})',
                    completed=case_counter,
                    refresh=True)
                task.refresh()
            case_counter += 1
            case.run(session=self)
        if task:
            task.terminate_and_remove()
            self._progress_tasks.stop()

    def report(self) -> None:
        """Generate reports for all benchmark cases in the session."""

        # all_choice_args returns a set of all Namespace args from all Choice instances
        # we check each arg to see if it is set in self.args.
        # The logic here is that if the arg is set, the user wants that report. By
        # making the lookup go from the defined Choices to the args, we ensure
        # that we only consider valid args that are associated with a Choice.
        if self.verbosity >= Verbosity.DEBUG:
            self._console.print(f"[DEBUG] Generating reports for session with {len(self.cases)} case(s)")
        processed_choices: set[str] = set()
        for key in self._choices.all_choice_args():
            if self.verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Checking report for arg '{key}'")
            # skip all Choices that are not set in self.args
            if not getattr(self.args, key, None):
                continue
            if self.verbosity >= Verbosity.DEBUG:
                self._console.print(f"[DEBUG] Processing report for arg '{key}'")
            choice: Choice | None = self._choices.get_choice_for_arg(key)
            if not isinstance(choice, Choice):
                raise SimpleBenchTypeError(
                    "choice must be a Choice instance",
                    ErrorTag.SESSION_REPORT_INVALID_CHOICE_RETRIEVED
                )
            # If we have already processed this Choice (there can be multiple
            # possible valid triggering args defined for a single Choice), then skip it.
            if choice and choice.name in processed_choices:
                continue
            processed_choices.add(choice.name)

            for case in self.cases:
                callback: Optional[Callable[[Case, Section, Format, Any], None]] = case.callback
                reporter: Reporter = choice.reporter
                output_path: Optional[Path] = self._output_path
                if output_path is None and Target.FILESYSTEM in choice.targets:
                    flag: str = '--' + key.replace('_', '-')
                    raise SimpleBenchTypeError(
                        f'output_path must be set to generate Choice {choice.name} / {flag} report',
                        ErrorTag.SESSION_REPORT_OUTPUT_PATH_NOT_SET
                    )
                reporter.report(
                    case=case,
                    choice=choice,
                    path=output_path,
                    session=self,
                    callback=callback)

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
                ErrorTag.SESSION_PROPERTY_INVALID_ARGS_ARG
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
                ErrorTag.SESSION_PROPERTY_INVALID_PROGRESS_ARG
            )
        self._show_progress = value

    @property
    def console(self) -> Console:
        """The Rich Console instance for displaying output."""
        return self._console

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
                ErrorTag.SESSION_PROPERTY_INVALID_VERBOSITY_ARG
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
                ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
            )
        for case in value:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
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
                ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG
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
                ErrorTag.SESSION_PROPERTY_INVALID_CASES_ARG
            )
        for case in cases:
            if not isinstance(case, Case):
                error_text = f'items in Sequence must be Case instances - cannot be a {type(case)}'
                raise SimpleBenchTypeError(
                    error_text,
                    ErrorTag.SESSION_PROPERTY_INVALID_CASE_ARG_IN_SEQUENCE
                )
        self._cases = list(self._cases) + list(cases)

    @property
    def output_path(self) -> Optional[Path]:
        """The output path for reports."""
        return self._output_path

    @output_path.setter
    def output_path(self, value: Path) -> None:
        """Set the output path for reports.

        Args:
            value (Path): The output path for reports.
        """
        if not isinstance(value, Path):
            raise SimpleBenchTypeError(
                f'output_path must be a Path instance - cannot be a {type(value)}',
                ErrorTag.SESSION_PROPERTY_INVALID_OUTPUT_PATH_ARG
            )
        self._output_path = value
