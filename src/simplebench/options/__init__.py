"""Reporter options package.

Public interface for reporter options.

Public API
----------

- :class:`~simplebench.options.CSVOptions`
    Class for holding CSV reporter specific options.
- :class:`~simplebench.options.JSONOptions`
    Class for holding JSON reporter specific options.
- :class:`~simplebench.options.RichTableOptions`
    Class for holding Rich Table reporter specific options.
- :class:`~simplebench.options.ScatterPlotOptions`
    Class for holding Scatter Plot reporter specific options. (requires 'graph' extras)
"""
# ruff: noqa F401

from .csv import CSVOptions
from .json import JSONOptions
from .rich_table import RichTableOptions

try:
    from .scatterplot import ScatterPlotOptions
except ImportError:
    pass

# No * exports defined
__all__: list[str] = []
