"""simplebench.session KWArgs package for SimpleBench tests."""

from argparse import ArgumentParser
from pathlib import Path
from typing import Callable, Sequence

from rich.console import Console
from simplebench_tests.kwargs.kwargs import NO_DEFAULT_VALUE, KWArgs, NoDefaultValue

from simplebench.benchmark_runner import SimpleRunner
from simplebench.case import Case
from simplebench.enums import Verbosity
from simplebench.session import Session


class SessionKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Session instance.

    This class is used to facilitate testing of the Session class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.
    """

    def __init__(  # pylint: disable=unused-argument
        self,
        *,
        cases: Sequence[Case] | NoDefaultValue = NO_DEFAULT_VALUE,
        verbosity: Verbosity | NoDefaultValue = NO_DEFAULT_VALUE,
        default_runners: Sequence[type[SimpleRunner]] | NoDefaultValue = NO_DEFAULT_VALUE,
        args_parser: ArgumentParser | NoDefaultValue = NO_DEFAULT_VALUE,
        show_progress: bool | NoDefaultValue = NO_DEFAULT_VALUE,
        output_path: Path | NoDefaultValue = NO_DEFAULT_VALUE,
        console: Console | NoDefaultValue = NO_DEFAULT_VALUE,
        timer: Callable[[], int] | NoDefaultValue = NO_DEFAULT_VALUE,
        cpu_timer: Callable[[], int] | NoDefaultValue = NO_DEFAULT_VALUE,
    ) -> None:
        """Constructs a SessionKWArgs instance. This class is used to hold keyword arguments for
        initializing a Session instance in tests.

        All parameters are optional and default to NO_DEFAULT_VALUE, indicating that they were not provided.
        This allows for testing the Session class with various combinations of parameters, including those
        that are optional and those that have no default value.

        :param Sequence[Case] cases: A sequence of Case instances.
        :param Verbosity verbosity: The verbosity level for the session.
        :param Sequence[type[SimpleRunner]] default_runners: The default runner class to use for the session.
        :param ArgumentParser args_parser: The argument parser instance for the session.
        :param bool show_progress: Whether to show progress information during the session.
        :param Path output_path: The output path for the session results.
        :param Console console: The console instance to use for the session.
        :param Callable[[], int] timer: The timer function to use for the session.
        :param Callable[[], int] cpu_timer: The CPU timer function to use for the session.
        """
        super().__init__(call=Session.__init__, kwargs=locals())
