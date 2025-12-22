"""System memory information utility functions."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MemoryInfo:
    """A snapshot of the system's static memory configuration.

    This class attempts to use the 'psutil' library to gather information
    about the total physical and swap memory. If 'psutil' is not installed,
    all values will be 0.

    To enable memory reporting, you can install it as an extra:
        pip install simplebench[memory]

    :param total_physical: Total physical memory in bytes. 0 if psutil is not installed.
    :param total_swap: Total configured swap memory in bytes. 0 if psutil is not installed.
    """
    total_physical: int
    total_swap: int

    def __init__(self) -> None:
        """Initializes the MemoryInfo object by querying psutil.

        If psutil is not available, all memory values are set to 0.
        """
        try:
            import psutil  # pylint: disable=import-outside-toplevel
            vmem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            # Uses object.__setattr__ because the class is frozen
            object.__setattr__(self, 'total_physical', vmem.total)
            object.__setattr__(self, 'total_swap', swap.total)
        except ImportError:
            # psutil is not installed, set defaults
            object.__setattr__(self, 'total_physical', 0)
            object.__setattr__(self, 'total_swap', 0)
