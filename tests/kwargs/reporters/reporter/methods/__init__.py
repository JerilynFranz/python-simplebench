"""KWArgs package for tests of simplebench.reporters.reporter methods."""
from .dispatch_to_targets_method_kwargs import DispatchToTargetsMethodKWArgs
from .render_by_case_method_kwargs import RenderByCaseMethodKWArgs
from .render_by_section_method_kwargs import RenderBySectionMethodKWArgs
from .target_callback_method_kwargs import TargetCallbackMethodKWArgs
from .target_console_method_kwargs import TargetConsoleMethodKWArgs
from .target_filesystem_method_kwargs import TargetFilesystemMethodKWArgs

__all__ = [
    "DispatchToTargetsMethodKWArgs",
    "RenderByCaseMethodKWArgs",
    "RenderBySectionMethodKWArgs",
    "TargetCallbackMethodKWArgs",
    "TargetConsoleMethodKWArgs",
    "TargetFilesystemMethodKWArgs",
]
"""'*' imports for simplebench.reporters.reporter method KWArgs packages."""
