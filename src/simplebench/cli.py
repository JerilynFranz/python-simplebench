# -*- coding: utf-8 -*-
"""CLI script support for SimpleBench."""
from __future__ import annotations
from argparse import Namespace, ArgumentParser
import pathlib
from typing import Any, Sequence, TYPE_CHECKING

from rich.console import Console

from .enums import Verbosity
from .session import Session


if TYPE_CHECKING:
    from .case import Case


def run_benchmarks(session: Session):
    """Run the benchmark tests and print the results.
    """
    benchmark_cases: Sequence[Case] = session.cases
    for case in benchmark_cases:
        case.verbose = args.verbose
        case.progress = args.progress

    cases_to_run: list[Case] = []
    for case in benchmark_cases:
        if 'all' in args.run or case.group in args.run:
            cases_to_run.append(case)

    if args.progress:
        PROGRESS.start()
    case_counter: int = 0
    data_export: list[dict[str, Any]] = []
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_dir: Path = Path(args.output_dir)
    benchmark_run_dir: Path = output_dir.joinpath(f'run_{timestamp}')
    if args.json or args.json_data or args.csv or args.graph:
        output_dir.mkdir(parents=True, exist_ok=True)
        benchmark_run_dir.mkdir(parents=True, exist_ok=True)

    utils = BenchmarkUtils()
    try:
        task_name: str = 'cases'
        if task_name not in TASKS and args.progress:
            TASKS[task_name] = PROGRESS.add_task(
                description='Running benchmark cases',
                total=len(cases_to_run))

        for case_counter, case in enumerate(cases_to_run):
            if task_name in TASKS:
                PROGRESS.reset(TASKS[task_name])
                PROGRESS.update(
                    task_id=TASKS[task_name],
                    completed=case_counter,
                    description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(cases_to_run)})')
            case.run()
            if case.results:
                if args.json or args.json_data:
                    data_export.append(case.as_dict(args=args))

                if args.graph:
                    if args.ops:
                        graph_file: Path = benchmark_run_dir.joinpath(f'benchmark_graph_ops_{case.group[:60]}.svg')
                        case.plot_ops_results(graph_file)
                    if args.timing:
                        graph_file: Path = benchmark_run_dir.joinpath(f'benchmark_graph_timing_{case.group[:60]}.svg')
                        case.plot_timing_results(graph_file)

                if args.csv:
                    output_targets: list[str] = []
                    if args.ops:
                        output_targets.append('ops')
                    if args.timing:
                        output_targets.append('timing')
                    for target in output_targets:
                        partial_filename: str = utils.sanitize_filename(f'benchmark_{target}_{case.group[:60]}')
                        uniquifier: int = 1
                        csv_file: Path = benchmark_run_dir.joinpath(f'{uniquifier:0>4d}_{partial_filename}.csv')
                        while csv_file.exists():
                            uniquifier += 1
                            csv_file = benchmark_run_dir.joinpath(f'{uniquifier:0>4d}_{partial_filename}.csv')
                        if target == 'ops':
                            case.output_ops_results_to_csv(csv_file)
                        elif target == 'timing':
                            case.output_timing_results_to_csv(csv_file)

                if args.console:
                    if args.ops:
                        case.ops_results_as_rich_table()
                    if args.timing:
                        case.timing_results_as_rich_table()
            else:
                PROGRESS.console.print('No results available')
        if args.json or args.json_data:
            filename = 'benchmark_results.json'
            full_path: Path = benchmark_run_dir.joinpath(filename)
            with full_path.open('w', encoding='utf-8') as json_file:
                json.dump(data_export, json_file, indent=4)
            PROGRESS.console.print(f'Benchmark results exported as JSON to [green]{str(full_path)}[/green]')
        if task_name in TASKS:
            PROGRESS.update(
                task_id=TASKS[task_name],
                completed=len(cases_to_run),
                description=f'Running benchmark cases (case {case_counter + 1:2d}/{len(cases_to_run)})')
        TASKS.clear()
    except KeyboardInterrupt:
        PROGRESS.console.print('Benchmarking interrupted by keyboard interrupt')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        PROGRESS.console.print(f'Error occurred while running benchmarks: {exc}')
    finally:
        if args.progress:
            TASKS.clear()
            PROGRESS.stop()
            for task in PROGRESS.task_ids:
                PROGRESS.remove_task(task)


def main(benchmark_cases: Sequence[Case]) -> int:
    """Main entry point for running benchmarks.

    Usage:
        This function serves as the main entry point for running benchmarks.

    Args:
        benchmark_cases (Sequence[Case]): A Sequence of SimpleBench.Case instances to be benchmarked.

    Returns:
        An integer exit code.
    """
    try:
        parser = ArgumentParser(description='Run benchmarks and output results in various formats.')
        parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
        parser.add_argument('--quiet', action='store_true', help='Enable quiet output')
        parser.add_argument('--debug', action='store_true', help='Enable debug output')
        parser.add_argument('--progress', action='store_true', help='Enable progress output')
        parser.add_argument('--list', action='store_true', help='List all available benchmarks')
        parser.add_argument('--run', nargs="+", default='all', metavar='<benchmark>', help='Run specific benchmarks')
        parser.add_argument('--output_path', default='.benchmarks', metavar='<path>', type=pathlib.Path,
                            help='Output destination directory (default: .benchmarks)')
        session: Session = Session(args_parser=parser)
        session.add_reporter_flags()
        session.parse_args()
        args: Namespace = session.args if session.args else Namespace()
        console: Console = session.console
        if args.list:
            console.print('Available benchmarks:')
            for case in benchmark_cases:
                console.print('  - ', f'[green]{case.group:<40s}[/green]', f'{case.title}')
            return 0

        if args.progress and session.verbosity == Verbosity.QUIET:
            console.print('Error: Cannot use both --progress and --quiet options together')
            parser.print_usage()
            return 1

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
            session.verbosity = Verbosity.DEBUG

        session.show_progress = args.progress

        if args.run:
            if 'all' in args.run:
                session.cases = benchmark_cases
            else:
                selected_cases: list[Case] = []
                for case in benchmark_cases:
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
