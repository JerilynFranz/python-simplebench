# -*- coding: utf-8 -*-
"""CLI script support for SimpleBench."""
from __future__ import annotations
from argparse import Namespace, ArgumentParser
import pathlib
import sys
from typing import Optional, Sequence, TYPE_CHECKING

from rich.console import Console

from .decorators import get_registered_cases
from .exceptions import SimpleBenchTypeError, ErrorTag
from .enums import Verbosity
from .session import Session


if TYPE_CHECKING:
    from .case import Case


def main(benchmark_cases: Optional[Sequence[Case]] = None,
         *,
         argv: Optional[list[str]] = None,
         extra_args: Optional[list[str]] = None) -> int:
    """Main entry point for running benchmarks via a command-line interface.

    This function is responsible for setting up the command-line interface,
    parsing arguments, and executing the benchmark cases.

    @benchmark() decorated cases are automatically included and added to the
    list of benchmark cases passed to this function.

    Usage:
        This function serves as the main entry point for running benchmarks.

    Args:
        benchmark_cases (Optional[Sequence[Case]]): A Sequence of SimpleBench.Case instances to be benchmarked.
        argv (Optional[list[str]]): A list of command-line arguments to parse. If None, defaults to sys.argv.
        extra_args (Optional[list[str]]): Additional command-line arguments to include.

    Returns:
        An integer exit code.
    """
    if extra_args is not None:
        if not isinstance(extra_args, Sequence):
            raise SimpleBenchTypeError(
                "'extra_args' argument must either be None or a list of str: "
                f"type of passed 'extra_args' was {type(extra_args).__name__}",
                tag=ErrorTag.CLI_INVALID_EXTRA_ARGS_TYPE)
        extra_args = list(extra_args)
        if not all(isinstance(item, str) for item in extra_args):
            raise SimpleBenchTypeError(
                "'extra_args' argument must either be None or a list of str: "
                "A non-str item was found in the passed list",
                tag=ErrorTag.CLI_INVALID_EXTRA_ARGS_ITEM_TYPE)

    if extra_args is not None:
        if argv is None:
            sys.argv.extend(extra_args)
        else:
            argv = list(argv)
            argv.extend(extra_args)

    try:
        parser = ArgumentParser(description='Run benchmarks and output results in various formats.')
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
        parser.add_argument('--quiet', action='store_true', help='Enable quiet output')
        parser.add_argument('--debug', action='store_true', help='Enable debug output')
        parser.add_argument('--progress', action='store_true', help='Enable progress output')
        parser.add_argument('--list', action='store_true', help='List all available benchmarks')
        parser.add_argument(
            '--run', nargs="+", default='all', metavar='<benchmark>',
            help='Run specific benchmarks selected by group name or "all" for all benchmarks (default: all)')
        parser.add_argument('--output_path', default='.benchmarks', metavar='<path>', type=pathlib.Path,
                            help='Output destination directory (default: .benchmarks)')
        session: Session = Session(args_parser=parser)
        session.add_reporter_flags()
        session.parse_args(argv)
        args: Namespace = session.args if session.args else Namespace()
        console: Console = session.console
        if benchmark_cases is None:
            benchmark_cases = []
        available_cases = list(benchmark_cases) + get_registered_cases()

        if args.list:
            console.print('Available benchmarks:')
            for case in available_cases:
                console.print('  - ', f'[green]{case.group:<40s}[/green]', f'{case.title}')
            return 0

        if args.quiet and args.verbose:
            console.print('Error: Cannot use both --quiet and --verbose options together')
            parser.print_usage()
            return 1

        if args.quiet and args.debug:
            console.print('Error: Cannot use both --quiet and --debug options together')
            parser.print_usage()
            return 1

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
            console.print('Error: No reporters selected. Please specify at least one reporter via command-line flags.')
            parser.print_usage()
            return 1

        if args.run:
            if 'all' in args.run:
                session.cases = available_cases
            else:
                selected_cases: list[Case] = []
                for case in available_cases:
                    if case.group in args.run:
                        selected_cases.append(case)
                if not selected_cases:
                    console.print('Error: No matching benchmarks found for the specified --run options')
                    parser.print_usage()
                    return 1
                session.cases = selected_cases

        session.run()
        session.report()
    except KeyboardInterrupt:
        print('')
        print('Benchmarking interrupted by keyboard interrupt')
        return 1
    return 0
