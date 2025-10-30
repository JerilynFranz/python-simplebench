"""simplebench.session KWArgs package for SimpleBench tests."""
from __future__ import annotations
import inspect
from typing import Any, Sequence, TYPE_CHECKING

from tests.kwargs.helpers import NoDefaultValue


if TYPE_CHECKING:
    from argparse import ArgumentParser
    from pathlib import Path

    from rich.console import Console

    from simplebench.enums import Verbosity
    from simplebench.case import Case
    from simplebench.runners import SimpleRunner


class SessionKWArgs(dict):
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
            progress: bool | NoDefaultValue = NoDefaultValue(),
            output_path: Path | NoDefaultValue = NoDefaultValue(),
            console: Console | NoDefaultValue = NoDefaultValue()) -> None:
        """Constructs a SessionKWArgs instance. This class is used to hold keyword arguments for
        initializing a Session instance in tests.

        Args:
            cases (Sequence[Case]): A sequence of Case instances.
            verbosity (Verbosity): The verbosity level for the session.
            default_runner (type[SimpleRunner]): The default runner class to use for the session.
            args_parser (ArgumentParser): The argument parser instance for the session.
            progress (bool): Whether to show progress information during the session.
            output_path (Path): The output path for the session results.
            console (Console): The console instance to use for the session.
        """
        kwargs_sig = inspect.signature(self.__init__)  # type: ignore[misc]
        params = set(kwargs_sig.parameters.keys()) - {'self'}
        kwargs: dict[str, Any] = {}
        for key in params:
            value = locals()[key]
            if not isinstance(value, NoDefaultValue):
                kwargs[key] = value
        super().__init__(**kwargs)
