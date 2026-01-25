"""Simple benchmarking framework.

Available imports:

- :func:`~simplebench.cli.main`: CLI entry point
- :func:`~simplebench.benchmark.benchmark`: benchmark decorator
- :func:`~simplebench.reporters.reporter_manager.decorators.register_reporter`: reporter registration decorator
- :class:`~simplebench.case.Case`: Benchmark Case
- :class:`~simplebench.case.Mark`: Benchmark Mark
- :class:`~simplebench.case.Results`: Benchmark Results
- :class:`~simplebench.reporters.csv.reporter.options.CSVOptions`: CSV reporter options
- :class:`~simplebench.reporters.json.reporter.options.JSONOptions`: JSON reporter options
- :class:`~simplebench.reporters.rich_table.reporter.options.RichTableOptions`: Rich Table reporter options
- :class:`~simplebench.session.Session`: Benchmark Session
- :class:`~simplebench.enums.Verbosity`: Verbosity enum

Optional imports (may not be available if extras are not installed):

- :class:`~simplebench.reporters.graph.enums.ImageType`: Image type enum (``graph`` extra required)
- :class:`~simplebench.reporters.graph.matplotlib.Style`: Matplotlib style options (``graph`` extra required)
- :class:`~simplebench.reporters.graph.matplotlib.Theme`: Matplotlib theme options (``graph`` extra required)
- :class:`~simplebench.reporters.graph.scatterplot.reporter.ScatterPlotOptions`: Scatter plot reporter options
    (``graph`` extra required)
- :class:`~simplebench._pytest.BenchmarkRegistrar`: Pytest benchmark registrar (``pytest`` extra required)
"""

import importlib
import importlib.util

# Lazy submodule imports prevent mass importing of all submodules when importing simplebench modules
# This improves import times and reduces unnecessary dependencies being loaded during
# simplebench usage and tests.

_lazy_imports: dict[str, tuple[str, str]] = {
    'main': ('simplebench.cli', 'main'),
    'benchmark': ('simplebench.benchmark', 'benchmark'),
    'register_reporter': ('simplebench.reporters.reporter_manager.decorators', 'register_reporter'),
    'Case': ('simplebench.case', 'Case'),
    'Mark': ('simplebench.case', 'Mark'),
    'Results': ('simplebench.case', 'Results'),
    'CSVOptions': ('simplebench.reporters.csv.reporter.options', 'CSVOptions'),
    'JSONOptions': ('simplebench.reporters.json.reporter.options', 'JSONOptions'),
    'RichTableOptions': ('simplebench.reporters.rich_table.reporter.options', 'RichTableOptions'),
    'Session': ('simplebench.session', 'Session'),
    'Verbosity': ('simplebench.enums', 'Verbosity'),
    # Optionals
    'ImageType': ('simplebench.reporters.graph.enums', 'ImageType'),
    'Style': ('simplebench.reporters.graph.matplotlib', 'Style'),
    'Theme': ('simplebench.reporters.graph.matplotlib', 'Theme'),
    'ScatterPlotOptions': ('simplebench.reporters.graph.scatterplot.reporter', 'ScatterPlotOptions'),
    'BenchmarkRegistrar': ('simplebench._pytest', 'BenchmarkRegistrar'),
}

_optional_imports: dict[tuple[str, ...], list[str]] = {
    ('pytest',): ['BenchmarkRegistrar'],
    ('matplotlib', 'pandas', 'seaborn'): [
        'ImageType',
        'Style',
        'Theme',
        'ScatterPlotOptions'],
}
"""List of optional packages and their corresponding attributes.

Attributes are only added to __all__ if all packages in the tuple are available.
"""

_optional_packages: set[str] = {item for sublist in _optional_imports.values() for item in sublist}

def __getattr__(name: str) -> object:
    """Import submodules and attributes lazily.

    :param name: Name of the attribute to import.
    :return: Imported attribute.
    :raises AttributeError: If the attribute does not exist.
    """
    if name in _lazy_imports:
        module_name, attr = _lazy_imports[name]
        try:
            module = importlib.import_module(module_name)
            value = getattr(module, attr)
            globals()[name] = value
            return value
        except ImportError as e:
            raise ImportError(f'Could not import {name} from {module_name}') from e
    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = list(set(_lazy_imports.keys()) - _optional_packages)  # type: ignore

# Add optional attributes to __all__ if their packages are available
for package, optional_attrs in _optional_imports.items():
    if all(importlib.util.find_spec(pkg) is not None for pkg in package):
        __all__ += optional_attrs  # type: ignore


def __dir__() -> list[str]:
    """List available attributes for the module.

    :return: List of available attribute names.
    :rtype: list[str]
    """
    return sorted(list(globals().keys()) + __all__)
