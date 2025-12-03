"""Timer information functions for simplebench"""

from .info import is_valid_timer, timer_overhead_ns, timer_precision_ns

__all__ = [
    "is_valid_timer",
    "timer_overhead_ns",
    "timer_precision_ns",
]
