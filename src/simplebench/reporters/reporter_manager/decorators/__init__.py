"""Decorators for ReporterManager.

Exportable:
- `register_reporter`
- `get_registered_reporters`
- `clear_registered_reporters`
- `RegisterReporterErrorTag`
"""
from simplebench.reporters.reporter_manager.decorators.register_reporter.register_reporter import (
    register_reporter, get_registered_reporters, clear_registered_reporters)
from simplebench.reporters.reporter_manager.decorators.register_reporter.exceptions import RegisterReporterErrorTag

__all__ = [
    "register_reporter",
    "get_registered_reporters",
    "clear_registered_reporters",
    "RegisterReporterErrorTag",
]
"""'*' exportable identifiers for ReporterManager decorators.
- `register_reporter`
- `get_registered_reporters`
- `clear_registered_reporters`
- `RegisterReporterErrorTag`
"""
