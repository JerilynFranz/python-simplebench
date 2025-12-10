"""Utility functions for version control system operations."""

import sys
from pathlib import Path


def resolve_vcs_path(search_path: Path | None = None) -> Path:
    """Identify the starting path for repository search.

    This function determines the appropriate starting directory
    for searching for a version control repository based on the provided path,
    the main script's location, or the current working directory.

    Resolution order:
    1. If `search_path` is provided, use its parent if it's a file,
       otherwise use `search_path` itself.
    2. If the main script's file is available, use its parent directory.
    3. Fallback to the current working directory.

    :param search_path: The path to start searching for the repository.
                        If None, defaults to the directory of the main script
                        or the current working directory.
    :return: The starting Path object.
    """
    has_modules_main = sys.modules.get('__main__') is not None
    has_main_file = has_modules_main and hasattr(sys.modules['__main__'], '__file__')
    main_file = getattr(sys.modules['__main__'], '__file__') if has_main_file else None
    if search_path:
        start_dir = search_path.parent if search_path.is_file() else search_path
    elif isinstance(main_file, str):
        start_dir = Path(main_file).parent.resolve()
    else:
        start_dir = Path.cwd()
    return start_dir
