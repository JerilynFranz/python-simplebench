"""simplebench.session KWArgs package for SimpleBench tests."""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Sequence

from simplebench.session import Session

from .kwargs import KWArgs, NoDefaultValue

if TYPE_CHECKING:
    from argparse import ArgumentParser
    from pathlib import Path

    from rich.console import Console

    from simplebench.case import Case
    from simplebench.enums import Verbosity
    from simplebench.runners import SimpleRunner


class SessionKWArgs(KWArgs):
    """A class to hold keyword arguments for initializing a Session instance.

    This class is used to facilitate testing of the Session class initialization
    with various combinations of parameters, including those that are optional and those
    that have no default value.
    """
    def __init__(  # pylint: disable=unused-argument
            self, *,
            cases: Sequence[Case] | NoDefaultValue = NoDefaultValue(),
            verbosity: Verbosity | NoDefaultValue = NoDefaultValue(),
            default_runner: type[SimpleRunner] | NoDefaultValue = NoDefaultValue(),
            args_parser: ArgumentParser | NoDefaultValue = NoDefaultValue(),
            show_progress: bool | NoDefaultValue = NoDefaultValue(),
            output_path: Path | NoDefaultValue = NoDefaultValue(),
            console: Console | NoDefaultValue = NoDefaultValue(),
            timer: Callable[[], float | int] | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a SessionKWArgs instance. This class is used to hold keyword arguments for
        initializing a Session instance in tests.

        :param cases: A sequence of Case instances.
        :param verbosity: The verbosity level for the session.
        :param default_runner: The default runner class to use for the session.
        :param args_parser: The argument parser instance for the session.
        :param show_progress: Whether to show progress information during the session.
        :param output_path: The output path for the session results.
        :param console: The console instance to use for the session.
        :param timer: The timer function to use for the session.
        """
        super().__init__(call=Session.__init__, kwargs=locals())
