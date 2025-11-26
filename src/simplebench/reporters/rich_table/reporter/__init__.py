"""Rich Table Reporter public API

Provides the following classes:
- :class:`~.RichTableConfig`
- :class:`~.RichTableOptions`
- :class:`~.RichTableReporter`
"""
from .config import RichTableConfig
from .options import RichTableOptions
from .reporter import RichTableReporter

__all__ = [
    "RichTableConfig",
    "RichTableOptions",
    "RichTableReporter",
]
