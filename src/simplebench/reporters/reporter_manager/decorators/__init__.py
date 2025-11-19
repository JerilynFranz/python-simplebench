"""Decorators for ReporterManager.

Exportable:
- `register_reporter`
- `get_registered_reporters`
- `clear_registered_reporters`
- `RegisterReporterErrorTag`
"""
from simplebench.reporters.reporter_manager.decorators.register_reporter.exceptions import _RegisterReporterErrorTag
from simplebench.reporters.reporter_manager.decorators.register_reporter.register_reporter import (
    clear_registered_reporters,
    get_registered_reporters,
    register_reporter,
)

__all__ = [
    "register_reporter",
    "get_registered_reporters",
    "clear_registered_reporters",
    "_RegisterReporterErrorTag",
]
"""'*' exportable identifiers for ReporterManager decorators.
- `register_reporter`
- `get_registered_reporters`
- `clear_registered_reporters`
- `RegisterReporterErrorTag`
"""
