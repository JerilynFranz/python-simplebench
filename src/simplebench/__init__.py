"""Simple benchmarking framework.

Available imports:

- :func:`~simplebench.main`: CLI entry point
- :decor:`~simplebench.benchmark`: benchmark decorator
- :class:`~simplebench.BenchmarkRunner`: Benchmark Runner base class
- :func:`~simplebench.register_reporter`: reporter registration decorator
- :class:`~simplebench.Case`: Benchmark Case
- :class:`~simplebench.case.Results`: Benchmark Results
- :class:`~simplebench.options`: Options module
- :class:`~simplebench.CSVOptions`: CSV reporter options
- :class:`~simplebench.JSONOptions`: JSON reporter options
- :class:`~simplebench.RichTableOptions`: Rich Table reporter options
- :class:`~simplebench.Session`: Benchmark Session
- :class:`~simplebench.Mark`: Mark type
- :class:`~simplebench.VariationMarks`: Variation Marks type
- :class:`~simplebench.Verbosity`: Verbosity enum

Optional imports (may not be available if extras are not installed):

Graph related imports (requires ``graph`` extra)
------------------------------------------------

- :class:`~simplebench.ImageType`: Image type enum
- :class:`~simplebench.Style`: Matplotlib style options
- :class:`~simplebench.Theme`: Matplotlib theme options
- :class:`~simplebench.options.ScatterPlotOptions`: Scatter plot reporter options

Pytest related imports (requires ``pytest`` extra)
--------------------------------------------------

- :class:`~simplebench._pytest.BenchmarkRegistrar`: Pytest benchmark registrar
"""
# ruff: noqa: F401

from simplebench import options
from simplebench.benchmark import benchmark
from simplebench.benchmark_runner import BenchmarkRunner
from simplebench.case import Case, Results
from simplebench.cli import main
from simplebench.enums import Verbosity
from simplebench.reporters.reporter_manager.decorators.register_reporter import register_reporter
from simplebench.session import Session
from simplebench.simplebench_types import Mark, VariationMarks

try:
    from simplebench._pytest import BenchmarkRegistrar
except ImportError:
    pass

try:
    from simplebench.reporters.graph.matplotlib import Style, Theme
except ImportError:
    pass

try:
    from simplebench.reporters.graph import ImageType
except ImportError:
    pass


# No * exports defined
__all__: list[str] = []
