"""Tests for git VCS module."""
import tarfile
from enum import Enum
from pathlib import Path

import pytest

from simplebench.vcs.git import Git, GitInfo
from simplebench.vcs.git.exceptions import _GitErrorTag

from ...factories.path import temp_dir
from ...testspec import Assert, TestAction, TestGet, TestSpec, idspec

_VCS_TEMP_DIR: Path | None = None
"""Temporary directory for VCS tests."""


def unpack_test_repo(tar_path: Path, extract_path: Path) -> None:
    """Helper function to unpack the test git repositories."""
    # Only unpack if the directory does not exist
    if not extract_path.exists():
        extract_path.mkdir(parents=True)
    with tarfile.open(tar_path.resolve(), "r:bz2") as tar:
        tar.extractall(path=extract_path)


def vcs_temp_dir() -> Path:
    """Path to temporary directory for VCS tests.

    This creates and unpacks the test repositories on first call.
    Subsequent calls return the same path.
    """
    global _VCS_TEMP_DIR  # pylint: disable=global-statement
    if _VCS_TEMP_DIR is not None:
        return _VCS_TEMP_DIR

    vcs_path = temp_dir() / "vcs_tests"
    if not vcs_path.exists():
        vcs_path.mkdir(parents=True)
    unpack_test_repo(tar_path=repos_archive_path(), extract_path=vcs_path)
    _VCS_TEMP_DIR = vcs_path
    return vcs_path


def repos_archive_path() -> Path:
    """Get the path to the test repos archive file."""
    return Path("tests", "fixtures", "test_repos.tar.bz2")


class Repo(str, Enum):
    """Enum for test repository directories."""
    CLEAN_EMPTY_REPO_NO_COMMITS = "clean_empty_repo_no_commits"
    CLEAN_REPO_ON_FEATURE_BRANCH = "clean_repo_on_feature_branch"
    CLEAN_REPO_ONE_COMMITTED_FILE = "clean_repo_one_committed_file"
    CLEAN_REPO_WITH_TAGS = "clean_repo_with_tags"
    DIRTY_REPO_MODIFIED_AND_STAGED = "dirty_repo_modified_and_staged"
    DIRTY_REPO_ONE_FILE_NO_COMMITS = "dirty_repo_one_file_no_commits"
    DIRTY_REPO_TWO_FILES_ONE_COMMITTED = "dirty_repo_two_files_one_committed"


_REPOS_INDEX: dict[Repo, Path] = {
    Repo.CLEAN_EMPTY_REPO_NO_COMMITS: Path(
        vcs_temp_dir(), "test_repos", "git", "clean_empty_repo_no_commits"),
    Repo.CLEAN_REPO_ON_FEATURE_BRANCH: Path(
        vcs_temp_dir(), "test_repos", "git", "clean_repo_on_feature_branch"),
    Repo.CLEAN_REPO_ONE_COMMITTED_FILE: Path(
        vcs_temp_dir(), "test_repos", "git", "clean_repo_one_committed_file"),
    Repo.CLEAN_REPO_WITH_TAGS: Path(
        vcs_temp_dir(), "test_repos", "git", "clean_repo_with_tags"),
    Repo.DIRTY_REPO_MODIFIED_AND_STAGED: Path(
        vcs_temp_dir(), "test_repos", "git", "dirty_repo_modified_and_staged"),
    Repo.DIRTY_REPO_ONE_FILE_NO_COMMITS: Path(
        vcs_temp_dir(), "test_repos", "git", "dirty_repo_one_file_no_commits"),
    Repo.DIRTY_REPO_TWO_FILES_ONE_COMMITTED: Path(
        vcs_temp_dir(), "test_repos", "git", "dirty_repo_two_files_one_committed"),
}


def repo_path(repo: Repo) -> Path:
    """Get the path to a test repository."""
    return _REPOS_INDEX[repo]


@pytest.mark.parametrize("testspec", [
    idspec("GA_001:is_available property", TestGet(
        name="Git is available on the system",
        obj=Git(),
        attribute="is_available",
        assertion=Assert.EQUAL,
        expected=True)),
    idspec("GA_002:cwd specified", TestGet(
        name="Git is available on the system (cwd specified)",
        obj=Git(cwd=repo_path(Repo.CLEAN_REPO_ONE_COMMITTED_FILE)),
        attribute="is_available",
        assertion=Assert.EQUAL,
        expected=True)),
])
def test_git_availability(testspec: TestSpec) -> None:
    """Test that git is available."""
    testspec.run()


def clean_one_commited_file_testspecs() -> list[TestSpec]:
    """Test that git status is clean for a known clean repo."""
    git_cwd = repo_path(Repo.CLEAN_REPO_ONE_COMMITTED_FILE)
    git = Git(cwd=git_cwd)

    testspecs: list[TestSpec] = [
        idspec("COCF_001:status()", TestAction(
            name="Git status is clean in clean repo with one committed file",
            action=git.status,
            assertion=Assert.EQUAL,
            expected="")),
        idspec("COCF_002:is_dirty()", TestAction(
            name="Git is_dirty() is False in clean repo with one committed file",
            action=git.is_dirty,
            assertion=Assert.EQUAL,
            expected=False)),
        idspec("COCF_003:get_info()", TestAction(
            name="Git get_info() in clean repo with one committed file",
            action=git.head,
            assertion=Assert.IS,
            expected=GitInfo)),
    ]
    return testspecs


@pytest.mark.parametrize("testspec", clean_one_commited_file_testspecs())
def test_git_clean_one_commited_file(testspec: TestSpec) -> None:
    """"Test Git in clean repo with one committed file."""
    testspec.run()
