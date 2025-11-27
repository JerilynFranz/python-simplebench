"""CLI script support for SimpleBench.

This module provides the main entry point for running benchmarks via a command-line
interface (CLI).

It defines the `main` function, which sets up argument parsing, configures the benchmarking
session, and executes the benchmarks based on user-specified options.

It provides functionality to list available benchmarks, select specific benchmarks to run,
configure output verbosity, and specify output paths.
"""
from __future__ import annotations

import pathlib
import sys
from argparse import ArgumentParser, Namespace
from typing import TYPE_CHECKING, Optional, Sequence

from rich.console import Console

from .decorators import get_registered_cases
from .doc_utils import format_docstring
from .enums import ExitCode, Verbosity
from .exceptions import (
    SimpleBenchArgumentError,
    SimpleBenchBenchmarkError,
    SimpleBenchTimeoutError,
    SimpleBenchTypeError,
    SimpleBenchUsageError,
    _CLIErrorTag,
)
from .session import Session

if TYPE_CHECKING:
    from .case import Case


def _create_parser() -> ArgumentParser:
    """Create the ArgumentParser instance for the SimpleBench CLI.

    :return: An ArgumentParser instance configured for the SimpleBench CLI.
    """
    parser = ArgumentParser(description='Run benchmarks and output results in various formats.')

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('--verbose', action='store_true', help='Enable verbose output')
    verbosity_group.add_argument('--quiet', action='store_true', help='Enable quiet output')
    verbosity_group.add_argument('--debug', action='store_true', help='Enable debug output')

    parser.add_argument('--progress', action='store_true', help='Enable progress display during benchmarking')
    parser.add_argument('--list', action='store_true', help='List all available benchmarks')
    parser.add_argument(
        '--run', nargs="+", default='all', metavar='<benchmark>',
        help='Run specific benchmarks selected by group name or "all" for all benchmarks (default: all)')
    parser.add_argument('--output_path', default='.benchmarks', metavar='<path>', type=pathlib.Path,
                        help='Output destination directory (default: .benchmarks)')
    return parser


def _configure_session_from_args(
        session: Session,
        cases: Sequence[Case],
        args: Namespace | None) -> None:
    """Configure the Session instance based on parsed command-line arguments.

    :param session: The Session instance to configure.
    :param cases: The available benchmark Case instances.
    :param args: The parsed command-line arguments.
    :raises SimpleBenchUsageError:
        If no benchmarks match the specified --run options or if no
        reporters are selected via command-line flags
    """
    if args is None:
        args = Namespace()

    if args.run:
        if 'all' in args.run:
            session.cases = cases
        else:
            session.cases = [
                case for case in cases if case.group in args.run
            ]
            if not session.cases:
                error_msg = 'No matching benchmarks found for the specified --run options'
                raise SimpleBenchUsageError(
                    error_msg, tag=_CLIErrorTag.NO_MATCHING_CASES)

    if args.output_path:
        session.output_path = args.output_path

    session.verbosity = Verbosity.NORMAL
    if args.quiet:
        session.verbosity = Verbosity.QUIET
    if args.verbose:
        session.verbosity = Verbosity.VERBOSE
    if args.debug:
        session.verbosity = Verbosity.DEBUG  # pyright: ignore[reportAttributeAccessIssue]

    session.show_progress = args.progress

    report_keys: list[str] = session.report_keys()
    if len(report_keys) == 0:
        error_msg = 'Please specify at least one reporter via command-line flags'
        session.args_parser.print_usage()
        raise SimpleBenchUsageError(error_msg,
                                    tag=_CLIErrorTag.NO_REPORTERS_SPECIFIED)


@format_docstring(KEYBOARD_INTERRUPT=ExitCode.KEYBOARD_INTERRUPT.value,
                  RUNTIME_ERROR=ExitCode.RUNTIME_ERROR.value,
                  CLI_ARGUMENTS_ERROR=ExitCode.CLI_ARGUMENTS_ERROR.value,
                  SUCCESS=ExitCode.SUCCESS.value,
                  BENCHMARK_TIMED_OUT=ExitCode.BENCHMARK_TIMED_OUT.value,
                  BENCHMARK_ERROR=ExitCode.BENCHMARK_ERROR.value)
def main(benchmark_cases: Optional[Sequence[Case]] = None,
         *,
         argv: Optional[list[str]] = None,
         extra_args: Optional[list[str]] = None,
         no_exit: bool = False) -> ExitCode:
    """Main entry point for running benchmarks via a command-line interface.

    This function is responsible for setting up the command-line interface,
    parsing arguments, and executing the benchmark cases.

    :func:`@benchmark <simplebench.decorators.benchmark>` decorated benchmark cases
    are automatically included and added to the list of benchmark cases passed to this function.

    Call this function from a script or the command line to execute benchmarks.

    If passed a list of :class:`Case <simplebench.case.Case>` instances via the
    ``benchmark_cases`` argument, those cases will be benchmarked in addition to any
    cases registered via the :func:`@benchmark <simplebench.decorators.benchmark>` decorator.

    If ``argv`` is provided, it will be used as the list of command-line arguments
    instead of ``sys.argv``.

    If ``extra_args`` is provided, those arguments will be appended to the command-line
    arguments before parsing.

    If the ``no_exit`` argument is set to True, the function will return the exit code
    instead of calling sys.exit(). This is useful for testing or embedding the CLI functionality
    in other applications.

    :param benchmark_cases: A Sequence of SimpleBench.Case instances to be benchmarked.
    :param argv: A list of command-line arguments to parse. If None, defaults to sys.argv.
    :param extra_args: Additional command-line arguments to include.
    :param no_exit: If True, the function will not call sys.exit() and will return the exit code instead.
    :return:
        - ``ExitCode.SUCCESS`` ({SUCCESS}) on success
        - ``ExitCode.RUNTIME_ERROR`` ({RUNTIME_ERROR}) runtime errors during execution.
        - ``ExitCode.CLI_ARGUMENTS_ERROR`` ({CLI_ARGUMENTS_ERROR}) for errors during CLI argument processing
        - ``ExitCode.KEYBOARD_INTERRUPT`` ({KEYBOARD_INTERRUPT}) if interrupted by keyboard interrupt
        - ``ExitCode.BENCHMARK_TIMED_OUT`` ({BENCHMARK_TIMED_OUT}) if a timeout occurs during execution of a benchmark.
        - ``ExitCode.BENCHMARK_ERROR`` ({BENCHMARK_ERROR}) if an error occurs during execution of a benchmark.
    :raises SimpleBenchTypeError: If the ``extra_args`` argument is not ``None`` or a list of strings or
        if ``argv`` is not ``None`` or a list of strings.
    """
    # These are outside the try-except to ensure type validation occurs before session creation
    # This is to avoid masking calling errors with session-related exceptions
    # Errors here indicate incorrect usage of the CLI function itself.
    if extra_args is not None:
        if not isinstance(extra_args, Sequence):
            raise SimpleBenchTypeError(
                "'extra_args' argument must either be None or a list of str: "
                f"type of passed 'extra_args' was {type(extra_args).__name__}",
                tag=_CLIErrorTag.CLI_INVALID_EXTRA_ARGS_TYPE)
        extra_args = list(extra_args)
        if not all(isinstance(item, str) for item in extra_args):
            raise SimpleBenchTypeError(
                "'extra_args' argument must either be None or a list of str: "
                "A non-str item was found in the passed list",
                tag=_CLIErrorTag.CLI_INVALID_EXTRA_ARGS_ITEM_TYPE)

    effective_argv = argv if argv is not None else sys.argv[1:]
    if extra_args:
        effective_argv.extend(extra_args)

    exit_code: ExitCode = ExitCode.SUCCESS
    session = None  # type: ignore[assignment]  # just to make sure it's defined in the outer scope

    final_message: str = ''
    try:
        parser = _create_parser()
        session = Session(args_parser=parser)
        session.add_reporter_flags()
        session.parse_args(effective_argv)
        args: Namespace = session.args if session.args else Namespace()
        console: Console = session.console

        if benchmark_cases is None:
            benchmark_cases = []
        available_cases = list(benchmark_cases) + get_registered_cases()

        if args.list:
            console.print('Available benchmarks:')
            for case in available_cases:
                console.print('  - ', f'[green]{case.group:<40s}[/green]', f'{case.title}')
            if no_exit:
                return ExitCode.SUCCESS
            sys.exit(int(ExitCode.SUCCESS))

        _configure_session_from_args(
            session=session, args=session.args, cases=available_cases)

        session.run()
        session.report()

    except KeyboardInterrupt:
        final_message = '\nBenchmarking interrupted by keyboard interrupt'
        exit_code = ExitCode.KEYBOARD_INTERRUPT
    except SimpleBenchUsageError as e:
        final_message = f'Usage error: {e}'
        exit_code = ExitCode.CLI_ARGUMENTS_ERROR
    except SimpleBenchArgumentError as e:
        final_message = f'CLI argument processing error: {e}'
        exit_code = ExitCode.CLI_ARGUMENTS_ERROR
    except SimpleBenchTimeoutError as e:
        final_message = f'Timeout occurred during a benchmark: {e}'
        exit_code = ExitCode.BENCHMARK_TIMED_OUT
    except SimpleBenchBenchmarkError as e:
        final_message = f'An error occurred while running a benchmark: {e}'
        exit_code = ExitCode.BENCHMARK_ERROR
    except Exception as e:  # pylint: disable=broad-exception-caught
        final_message = f'An unexpected error occurred: {e}'
        exit_code = ExitCode.RUNTIME_ERROR
    finally:
        if session and session.tasks:
            session.tasks.stop()
        if final_message:
            print(final_message)

    if no_exit:
        return exit_code
    sys.exit(int(exit_code))
