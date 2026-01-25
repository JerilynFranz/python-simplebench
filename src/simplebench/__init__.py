"""Simple benchmarking framework.

Available imports:
- main: CLI entry point
- benchmark: benchmark decorator
- register_reporter: reporter registration decorator
- Case: Benchmark Case
- Mark: Benchmark Mark
- Results: Benchmark Results
- CSVOptions: CSV reporter options
- JSONOptions: JSON reporter options
- RichTableOptions: Rich Table reporter options
- Session: Benchmark Session
- Verbosity: Verbosity enum

Optional imports (may not be available if extras are not installed):
- ImageType: Image type enum (graph extra required)
- Style: Matplotlib style options (graph extra required)
- Theme: Matplotlib theme options (graph extra required)
- ScatterPlotOptions: Scatter plot reporter options (graph extra required)
- BenchmarkRegistrar: Pytest benchmark registrar (pytest extra required)

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

def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + list(_lazy_imports.keys()))

__all__ = list(set(_lazy_imports.keys()) - _optional_packages)  # type: ignore

for package, optional_attrs in _optional_imports.items():
    if all(importlib.util.find_spec(pkg) is not None for pkg in package):
        __all__ += optional_attrs  # type: ignore
