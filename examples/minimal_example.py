#!python3
"""A minimal example of using simplebench.

**Purpose**

This example demonstrates how to define and run simple benchmarks
using the @benchmark decorator with minimal configuration.

**Code Explanation**

This file includes two benchmark functions registered with the `@benchmark` decorator:
1. `addition_benchmark`: A basic benchmark with no parameters.
2. `string_concatenation_benchmark`: A benchmark with a custom group and title.

The `@benchmark` decorator is used to register functions as benchmark cases.

The `if __name__ == '__main__':` block shows how to programmatically pass
default arguments to simplebench. In this case, we add `--progress` to
show the progress bar by default.

You must specify a report and output target(s) when running the benchmarks.

**Available Reports and Output Targets**

Reports are selected via command-line flags, and each report supports
various output targets. The available reports and their default targets are:

- Rich Table Report:
    - Flag: `--rich-table`
    - Available Output Targets: `console`, `filesystem`, `callback`
    - Default Target: `console`
- JSON Reports:
    - Flags: `--json`, `--json-data`
    - Available Output Targets: `console`, `filesystem`, `callback`
    - Default Target: `filesystem`
- CSV Report:
    - Flag: `--csv`
    - Available Output Targets: `console`, `filesystem`, `callback`
    - Default Target: `filesystem`
- Scatter Plot Report:
    - Flag: `--scatter-plot`
    - Available Output Targets: `filesystem`, `callback`
    - Default Target: `filesystem`

**Usage Examples**

Generate a rich table report to the default target (console):

    python examples/minimal_example.py --rich-table

Generate a rich table report specifically to the console:

    python examples/minimal_example.py --rich-table console

Generate a rich table report specifically to filesystem and console:

    python examples/minimal_example.py --rich-table filesystem console

Run only a specific group of benchmarks (e.g., string operations) with a rich table:

    python examples/minimal_example.py --run string_ops --rich-table console

See all available command-line options:

    python examples/minimal_example.py --help
"""
import simplebench


@simplebench.benchmark
def addition_benchmark():
    '''A simple addition benchmark of Python's built-in sum function.'''
    sum(range(1000))


@simplebench.benchmark('string_ops',
                       title='String Concatenation Benchmark',)
def string_concatenation_benchmark():
    '''A simple string concatenation benchmark with a custom group and title.'''
    result = ''
    for i in range(1000):
        result += str(i)


if __name__ == '__main__':
    extra_args = ['--progress']
    simplebench.main(extra_args=extra_args)
