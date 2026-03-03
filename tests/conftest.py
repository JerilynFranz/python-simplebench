import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest import Session

def pytest_sessionstart(session: "Session") -> None:
    """
    Clears the module cache to defeat VS Code's persistent test worker.
    This forces a fresh import, allowing coverage to capture module-level code.
    """
    target = "simplebench"

    # Create a list of all cached modules associated with the target package
    to_delete = [
        mod_name for mod_name in sys.modules
        if mod_name == target or mod_name.startswith(f"{target}.")
    ]

    # Purge them from the cache so Python is forced to re-execute them
    for mod_name in to_delete:
        del sys.modules[mod_name]
