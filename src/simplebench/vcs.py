"""Version Control System utilities using Dulwich."""
from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dulwich import porcelain
from dulwich.errors import NotGitRepository  # <-- Import this
from dulwich.objects import Commit
from dulwich.repo import Repo


@dataclass
class GitInfo:
    """Dataclass to hold Git repository information.

    Attributes:
        commit (str): The current commit hash.
        date (str): The date of the current commit in ISO format.
        dirty (bool): Whether there are uncommitted changes in the working directory.
    """
    commit: str
    date: str
    dirty: bool

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def get_git_info(search_path: Path | None = None) -> GitInfo | None:
    """Fetch Git repository information using Dulwich.

    :param search_path: The path to start searching for the git repository.
                        If None, defaults to the directory of the main script
                        or the current working directory.
    :type search_path: Path | None
    :return: A dictionary with git info, or None if not a git repository.
    :rtype: dict[str, Any] | None
    """
    # Determine the starting path for the repo search
    has_modules_main = sys.modules.get('__main__') is not None
    has_main_file = has_modules_main and hasattr(sys.modules['__main__'], '__file__')
    main_file = getattr(sys.modules['__main__'], '__file__') if has_main_file else None
    if search_path:
        start_dir = search_path.parent if search_path.is_file() else search_path
    elif isinstance(main_file, str):
        start_dir = Path(main_file).parent.resolve()
    else:
        start_dir = Path.cwd()

    try:
        # Dulwich's Repo.discover() walks up the tree to find the .git dir
        repo = Repo.discover(str(start_dir))  # type: ignore[reportPossiblyUnboundVariable]

        # Get the HEAD commit
        head_sha = repo.head()
        commit = repo[head_sha]
        if not isinstance(commit, Commit):
            return None

        # Parse Date
        # commit_time is seconds since epoch
        commit_time = commit.commit_time
        dt = datetime.fromtimestamp(commit_time, tz=timezone.utc)
        date_str = dt.isoformat()

        # Check for dirty status (uncommitted changes)
        # status returns (staged, unstaged, untracked)
        staged, unstaged, _ = porcelain.status(repo)
        is_dirty = bool(staged or unstaged)

        return GitInfo(
            commit=head_sha.decode('utf-8'),
            date=date_str,
            dirty=is_dirty,
        )
    except NotGitRepository:
        # Standard case: code is not running inside a git repo
        return None
    except Exception:  # pylint: disable=broad-exception-caught
        # Fallback: Repo exists but is corrupt, unreadable, or other unexpected error.
        # We swallow this to prevent crashing the benchmark.
        return None
