"""Rich Table Reporter public API

Provides the following classes:
- :class:`~.RichTableConfig`
- :class:`~.RichTableField`
- :class:`~.RichTableOptions`
- :class:`~.RichTableReporter`
"""
from .config import RichTableConfig
from .options import RichTableField, RichTableOptions
from .reporter import RichTableReporter

__all__ = [
    "RichTableConfig",
    "RichTableField",
    "RichTableOptions",
    "RichTableReporter",
]
