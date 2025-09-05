# -*- coding: utf-8 -*-
"""CLI script support for SimpleBench."""


from argparse import Namespace, ArgumentParser
from typing import Any, Sequence

from rich.console import Console

from .case import Case
from .session import Session, Verbosity


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
        benchmark_cases (Sequence[Case]): A Sequence of benchmark cases.

    Returns:
        An integer exit code.

    """
    parser = ArgumentParser(description='Run GeneralizedTrie benchmarks.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--progress', action='store_true', help='Enable progress output')
    parser.add_argument('--list', action='store_true', help='List all available benchmarks')
    parser.add_argument('--run', nargs="+", default='all', metavar='<benchmark>', help='Run specific benchmarks')
    parser.add_argument('--console', action='store_true', help='Enable console output')
    parser.add_argument('--json', action='store_true', help='Enable JSON file statistics output to files')
    parser.add_argument('--json-data',
                        action='store_true',
                        help='Enable JSON file statistics and data output to files')
    parser.add_argument('--csv', action='store_true', help='Enable tagged CSV statistics output to files')
    parser.add_argument('--graph', action='store_true', help='Enable graphical output (e.g., plots)')
    parser.add_argument('--output_dir', default='.benchmarks',
                        help='Output destination directory (default: .benchmarks)')
    parser.add_argument('--ops',
                        action='store_true',
                        help='Enable operations per second output to console or csv')
    parser.add_argument('--timing', action='store_true', help='Enable operations timing output to console or csv')

    args: Namespace = parser.parse_args()
    session: Session = Session(args=args, cases=benchmark_cases)
    console: Console = session.console
    if args.list:
        console.print('Available benchmarks:')
        for case in benchmark_cases:
            console.print('  - ', f'[green]{case.group:<40s}[/green]', f'{case.title}')
        return 0

    if args.quiet and args.verbose:
        console.print('Error: Cannot use both --quiet and --verbose options together')
        parser.print_usage()
        return 1

    session.verbosity = Verbosity.NORMAL
    if args.quiet:
        session.verbosity = Verbosity.QUIET

    if args.verbose:
        session.verbosity = Verbosity.VERBOSE

    if not (args.console or args.json or args.csv or args.json or args.json_data):
        session.console.print('No output format(s) selected, using console output by default')
        session.reporters.add(ConsoleReporter(session.console))
        args.console = True

    if args.json and args.json_data:
        session.console.print('Warning: Both --json and --json-data are enabled, using --json-data')
        args.json = False
    if (args.graph or args.json or args.json_data or args.csv) and not args.output_dir:
        session.console.print('No output directory specified, using default: .benchmarks')

    if args.console and not (args.ops or args.timing):
        session.console.print(
            'No benchmark result type selected for --console: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return 1

    if args.csv and not (args.ops or args.timing):
        session.console.print(
            'No benchmark result type selected for --csv: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return 1

    if args.graph and not (args.ops or args.timing):
        PROGRESS.console.print(
            'No benchmark result type selected for --graph: At least one of --ops or --timing must be enabled')
        parser.print_usage()
        return 1

    run_benchmarks(cases=benchmark_cases, args=args)

    return 0
