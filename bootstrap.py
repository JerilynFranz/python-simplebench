"""Zero-dependency, cross-platform bootstrap script to set up a Python
development environment.

This is the development bootstrap script for the 'simplebench' project.

The bootstrap script is NOT intended to be run with Python versions earlier than 3.10
and will exit with an error if attempted.

It has been tested with Python 3.10 through 3.14 as of January 2025.

This script is part of the 'python-env-bootstrap' project available at
https://github.com/JerilynFranz/python-env-bootstrap

License
-------

Licensed under the Apache License, Version 2.0 (SPDX-License-Identifier: Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0.txt
Copyright [2025] Jerilyn Franz

Based on 'python-env-bootstrap' (https://github.com/JerilynFranz/python-env-bootstrap).

Description
-----------

It is designed to be run after cloning a git or Mercurial repository, to create
a local virtual environment (.venv for example), and install necessary development tools.

It relies only on the Python standard library and network access to PyPI and
does not require any pre-installed packages or change your system Python installation.

This script installs the following tools by default:
- uv (for managing Python packages and dependencies)

That is the minimum set of tools required to start development for this project.

The minimum supported Python version, virtual environment directory name,
and list of tools to install can be customized by modifying the
corresponding constants in this script. The script can also be extended to
perform additional setup steps as needed via the run_post_install_steps() function
such as installing additional packages from requirements.txt files
or configuring settings.

Settable Options
----------------

- VENV_DIR: The name of the virtual environment directory to create.
- BOOTSTRAP_MODULES: A list of InstallSpec instances specifying the packages
  to install into the virtual environment during bootstrap.
- Post-install steps: You can customize the `run_post_install_steps()`
  function to perform additional setup tasks after installing the core tools.
- Output control: You can set `DEFAULT_DEBUG` and `DEFAULT_QUIET` constants
  to control whether debug output or quiet mode is enabled by default.
- Command-line options: You can use '--debug'/'--no-debug' and '--quiet'/'--verbose'
  to control output verbosity when running the script.
- Automatic confirmation: You can use '--yes'/'-y' to skip confirmation prompts.
- You can configure the supported Python versions by modifying
  the version check ("if sys.version_info") at the start of the script.

Usage
-----

python bootstrap.py [-h] [--yes] [--debug | --no-debug] [-q | -v]

CLI Help
--------
  -h, --help     show this help message and exit
  --yes, -y      Automatically confirm and proceed without prompting.
  --debug        Enable debug output.
  --no-debug     Disable debug output.
  -q, --quiet    Suppress non-error output.
  -v, --verbose  Enable verbose output (default).
"""

__version__ = '1.3.0'

# pylint: disable=wrong-import-position,C0103,too-many-lines

import sys

# Check for minimum supported Python version before importing anything else
# this ensures that users get a clear error message if they try to run
# the script with an unsupported Python version.
#
# The minimum version of Python this bootstrap script can support is 3.10+
# This can be changed as needed for your project.
if sys.version_info < (3, 10):
    major, minor = sys.version_info.major, sys.version_info.minor
    print(f'Error: Python 3.10 or later is required to run this script. You are using Python {major}.{minor}.')
    sys.exit(2)

import argparse
import os
import shutil
import stat
import subprocess
from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple
from venv import create as create_venv


def _is_windows() -> bool:
    """Determines if the current platform is Windows."""
    return sys.platform == 'win32'


DEFAULT_DEBUG: bool = False
"""Enable debug output only if --debug is specified.

To enable debug output by default, set this to True
and then --no-debug can be used to disable it.
"""

DEFAULT_QUIET: bool = False
"""Suppress non-error output only if --quiet is specified.

To enable quiet output by default, set this to True
and then --verbose can be used to disable it.
"""

# Whether to remove the bootstrapvirtual environment directory on script exit.
# This is useful for cleaning up the bootstrap venv after installation
# if desired. Set to False to keep the venv for inspection or reuse.
#
# Removing it on exit is not the default behavior to avoid accidental loss
# of the created environment. But it can be enabled as needed.
# Default is False because most users will want to keep the venv.
REMOVE_BOOTSTRAP_VENV_ON_EXIT: bool = False
"""Whether to remove the virtual environment directory on script exit."""

VENV_DIR: str = '.venv'
"""The name of the virtual environment directory to create in the repository root for the bootstrap."""

# The name of the final virtual environment directory when activated.
#
# This can be changed as needed for your project. If you are using 'tox'
# or another tool such as 'poetry' that creates its own venv,
# you may want to change this to 'venv' or another appropriate name depending on
# your project's virtual environment management.
ACTIVATED_VENV_DIR: str = '.venv'
"""The name of the virtual environment directory where the project's virtual environment is kept."""


class InstallSpec(NamedTuple):
    """Specification for modules required to be installed.

    :param str name: The name of the module to install.
    :param str version: An optional version specifier (e.g., ">=1.0.0").
    :param str extras: An optional extras specifier (e.g., "[dev]").
    """

    name: str
    version: str = ''
    extras: str = ''

    def __str__(self) -> str:
        return f'{self.name}{self.extras}{self.version or " (latest)"}'


# --- Modules to install during bootstrap ---

BOOTSTRAP_MODULES: list[InstallSpec] = [
    InstallSpec(name='uv', version='>=0.9.18'),
]

# --- Tool usage instructions template ---

TOOL_USAGE_INSTRUCTIONS = """
You use 'tox' to run tasks that set up and manage the development environment,
run tests, linters, and build documentation:

Examples:

  tox run -e lint     # Run linters on the codebase
  tox run -e docs     # Build documentation
  tox run -e py310    # Run the test suite using Python 3.10
  tox run -e py314    # Run the test suite using Python 3.14
  tox devenv -e dev   # Start an interactive dev environment with Python 3.12

The list of available 'tox' environments can be found by running:

  tox list

If you are not familiar with using 'tox' see https://tox.wiki/en/latest/

You use 'uv' to manage Python packages within the virtual environment and to
update pyproject dependencies:

Examples:

  # Add a new package to the 'dev' dependency group
  uv add --dev --group=dev 'package_name>=1.2.3'

  # Add a new package to the default dependency group
  uv add 'package_name>=1.2.3'

  # Add a package to specified extras
  uv add 'package_name[extra1,extra2]'

  # install a package from PyPI to the virtual environment
  uv pip install 'package_name>=1.2.3'

See https://docs.astral.sh/uv/ for more information on using 'uv'.
"""

# --- Post-install instructions template ---

POST_INSTALL_MESSAGE = f"""
--- Bootstrap complete! ---

The development environment has been set up in the '{ACTIVATED_VENV_DIR}' directory,
and the project has been installed in editable mode.

To activate the project's development virtual environment, run:

{{activate}}

To deactivate the virtual environment, run:

{{deactivate}}

{TOOL_USAGE_INSTRUCTIONS}
"""



# Platform-specific configs and messages

if _is_windows():
    PLATFORM_PROMPT_MESSAGE = """
************************************************************
If you are using PowerShell, the script will attempt to set
the execution policy to allow running scripts in the virtual
environment. This is required to activate the virtual
environment in PowerShell.

The execution policy will be set only for the current user.
************************************************************

"""

    # Use ; as path separator on Windows
    # Also use backslashes for paths in .env on Windows
    # Set to '' to disable .env creation
    DOT_ENV_CONTENT="""
PYTHONPATH={repo_root}\\src;{repo_root}\\tests
"""

# POSIX (Linux, macOS, etc.)
else:
    PLATFORM_PROMPT_MESSAGE = ''

    # Use : as path separator on POSIX systems
    # Also use forward slashes for paths in .env on POSIX
    # Set to '' to disable .env creation
    DOT_ENV_CONTENT="""
PYTHONPATH={repo_root}/src:{repo_root}/tests
"""

CONFIRMATION_PROMPT_MESSAGE = f"""
This script will create a {VENV_DIR} directory in the root
of the current repository.

It will install required tools into it for development,
and install the project as an editable package into the
virtual environment.

It will also install a git pre-commit hook for the repository.

{PLATFORM_PROMPT_MESSAGE}
No other changes will be made to your system install of Python.

Continue? [y/n] """

# --- Global flags for output control ---

# These are defined here only for declaration purposes; they are actually set
# in main() after parsing command-line arguments.
# Changing these variables directly has no effect: Set DEFAULT_DEBUG and
# DEFAULT_QUIET instead to change the default behavior.
DEBUG: bool = False
QUIET: bool = False


# --- Version Control System (VCS) Hook Names ---

# Standard Git and Mercurial hook names. If you need custom hooks,
# you can modify these sets as needed. Only names included in these
# sets will be installed by the install_vcs_hooks() function.
GIT_HOOK_NAMES = {
    'applypatch-msg',
    'commit-msg',
    'fsmonitor-watchman',
    'post-update',
    'pre-applypatch',
    'pre-commit',
    'pre-merge-commit',
    'pre-push',
    'pre-rebase',
    'pre-receive',
    'prepare-commit-msg',
    'update',
}

HG_HOOK_NAMES = {
    'precommit',
    'commit',
    'prepush',
    'push',
    'preupdate',
    'update',
    'prechangegroup',
    'changegroup',
    'pretag',
    'tag',
}


class VCS(NamedTuple):
    """Specification for version control systems.

    :param str name: The name of the VCS (e.g., 'git', 'hg', 'none').
    """

    name: str
    repo_root: Path | None = None

    def is_git(self) -> bool:
        """Returns True if the VCS is git."""
        return self.name == 'git'

    def is_hg(self) -> bool:
        """Returns True if the VCS is Mercurial."""
        return self.name == 'hg'

    def is_none(self) -> bool:
        """Returns True if no VCS is detected."""
        return self.name == 'none'

    def __str__(self) -> str:
        return self.name


DETECTED_VCS: VCS = VCS(name='none', repo_root=Path('.'))
"""The detected version control system in use (git, hg, or none)."""


_powershell_execution_policy_set: bool = False

def run_post_install_steps(python_exe: Path, root_path: Path, bin_dir: Path) -> None:
    """Runs any post-installation steps required after installing tools.

    This function is called automatically after the core development tools are installed.
    It is intended as a customization point for project-specific setup tasks, such as:
    - Installing the current project in editable mode
    - Setting up pre-commit hooks
    - Installing packages from requirements.txt files
    - Any other project-specific initialization

    The example here installs the current project in editable mode with 'uv pip install -e .'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param root_path Path: The path to the root of the repository.
    """
    _validate_path(python_exe, 'python_exe', exists=True)
    _validate_path(root_path, 'root_path', exists=True)

    controlled_print('--> Installing the current project and syncing all dependency groups...')
    # We use --all-groups to ensure 'tools' (tox), 'test', etc. defined in
    # pyproject.toml are installed. uv sync also handles installing the
    # project itself in editable mode.
    run_command([bin_dir / 'uv', 'sync', '--all-groups'], cwd=root_path, check=True)


class FatalBootstrapError(Exception):
    """Exception raised for fatal errors during the bootstrap process."""

    def __init__(self, message: str, error_code: int = 1) -> None:
        super().__init__(message)
        self.error_code = error_code



def _validate_string(value: str, name: str) -> None:
    """Validates that the input is a string.

    :param value str: The value to validate.
    :param name str: The name of the value (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(value, str):
        raise TypeError(f'{name} must be a string')


def _validate_string_list(lst: list[str], name: str) -> None:
    """Validates that the input is a list of strings.

    :param lst list[str]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(lst, list):
        raise TypeError(f'{name} must be a list')
    if not all(isinstance(item, str) for item in lst):
        raise TypeError(f'all items in {name} must be strings')


def _validate_module_list(modules: list[InstallSpec], name: str) -> None:
    """Validates that the input is a list of InstallSpec instances.

    :param modules list[InstallSpec]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(modules, list):
        raise TypeError(f'{name} must be a list')
    for module in modules:
        if not isinstance(module, InstallSpec):
            raise TypeError(f'all items in {name} must be InstallSpec instances')


def _validate_command(lst: list[str | Path], name: str) -> None:
    """Validates that the input is a list of that starts with
    either a string or Path, and contains only strings for all other items.

    It must contain at least one item.

    :param lst list[str | Path]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(lst, list):
        raise TypeError(f'{name} must be a list')
    if not lst:
        raise ValueError(f'{name} must not be empty')
    if not isinstance(lst[0], (str, Path)):
        raise TypeError(f'the first item in {name} must be a string or Path')
    if not all(isinstance(item, str) for item in lst[1:]):
        raise TypeError(f'all items after the first in {name} must be strings')


def _validate_boolean(value: bool, name: str) -> None:
    """Validates that the input is a boolean.

    :param value bool: The value to validate.
    :param name str: The name of the value (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(value, bool):
        raise TypeError(f'{name} must be a boolean')


def _validate_kwarg_keys_are_strings(kwargs: dict, name: str) -> None:
    """Validates that all keys in the input dictionary are strings.

    :param kwargs dict: The dictionary to validate.
    :param name str: The name of the dictionary (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(kwargs, dict):
        raise TypeError(f'{name} must be a dictionary')
    if not all(isinstance(k, str) for k in kwargs.keys()):
        raise TypeError(f'all keys in {name} must be strings')


def _validate_path(path: Path, name: str, exists: bool = False) -> None:
    """Validates that the input is a Path instance.

    Optionally checks that the path exists.

    :param path Path: The path to validate.
    :param name str: The name of the path (for error messages).
    :param exists bool: Whether to check that the path exists.
    :raises TypeError: If validation fails.
    :raises FileNotFoundError: If exists is True and the path does not exist.
    """
    if not isinstance(path, Path):
        raise TypeError(f'{name} must be a Path instance')
    if exists and not path.exists():
        raise FileNotFoundError(f'{name} does not exist: {path}')


def run_command(
    command: list[str | Path],
    *,
    check: bool = True,
    cwd: str | Path | None = None,
    **kwargs,  # noqa: ANN003
) -> None:
    """Helper to run a command and print its output.

    If the command is not found, or returns a non-zero exit code,
    prints an error message and exits the script.

    :param command list[str | Path]: The command to run as a list.
    :param check bool: Whether to raise an exception on non-zero exit code.
    :param cwd str | Path | None: The working directory for the command.
    :param kwargs: Additional keyword arguments to pass to subprocess.run().
    """
    _validate_command(command, 'command')
    _validate_boolean(check, 'check')
    if cwd:
        _validate_path(Path(cwd), 'cwd', exists=True)
    _validate_kwarg_keys_are_strings(kwargs, 'kwargs')

    try:
        if DEBUG:
            debug_kwargs = kwargs.copy()
            if cwd:
                debug_kwargs['cwd'] = cwd
            print(f'DEBUG: Running {command} with kwargs: {debug_kwargs}')
        # Suppress output if QUIET is True and not already overridden
        if QUIET:
            kwargs.setdefault('stdout', subprocess.DEVNULL)
            kwargs.setdefault('stderr', subprocess.DEVNULL)
        subprocess.run(command, check=check, cwd=cwd, **kwargs)
    except FileNotFoundError as e:
        print(f"Error: Command '{command[0]}' not found. Is it in your PATH?")
        raise FatalBootstrapError(f"Command '{command[0]}' not found.", error_code=1) from e
    except subprocess.CalledProcessError as e:
        print(f'Error: Command {command} failed with exit code {e.returncode}')
        raise FatalBootstrapError(
            f'Command {command} failed with exit code {e.returncode}', error_code=e.returncode
        ) from e


def controlled_print(message: str) -> None:
    """Prints a message if not in quiet mode."""
    _validate_string(message, 'message')
    if not QUIET:
        print(message)


def confirmation_prompt(message: str) -> bool:
    """Prompts the user for confirmation to proceed."""
    try:
        repo_root = get_repo_root()
        controlled_print(f'Current working directory: {os.getcwd()}')
        controlled_print(f'Repository root directory: {repo_root}')
        choice = ''
        while choice.lower().strip() not in ('y', 'yes', 'n', 'no'):
            choice = input(message)
    except KeyboardInterrupt:
        controlled_print('')
        return False

    return choice.lower().strip() in ('', 'y', 'yes')


@cache
def get_repo_root() -> Path:
    """Finds the root directory of the repository and caches the result.

    If not in a repository, prints an error message and exits.

    It tries to use 'git rev-parse --show-toplevel' first, and falls back
    to searching parent directories for a '.git' folder if the git command
    is not found.

    If a .git directory is not found, it looks for a Mercurial repository
    by searching for a '.hg' folder instead.

    :raises FatalBootstrapError: If no repository is found.
    """
    global DETECTED_VCS  # pylint: disable=global-statement
    try:
        git_root_bytes = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.PIPE)
        root_dir = git_root_bytes.decode('utf-8').strip()
        DETECTED_VCS = VCS(name='git', repo_root=Path(root_dir))
        return Path(root_dir)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Try Mercurial CLI
        try:
            hg_root_bytes = subprocess.check_output(['hg', 'root'], stderr=subprocess.PIPE)
            root_dir = hg_root_bytes.decode('utf-8').strip()
            DETECTED_VCS = VCS(name='hg', repo_root=Path(root_dir))
            return Path(root_dir)
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback to directory search...
            current_dir = Path.cwd()
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / '.git').is_dir():
                    DETECTED_VCS = VCS(name='git', repo_root=parent)
                    return parent

            # Check for Mercurial repository instead
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / '.hg').is_dir():
                    DETECTED_VCS = VCS(name='hg', repo_root=parent)
                    return parent

            controlled_print('Error: No Git or Mercurial repository found in any parent directories.')
            raise FatalBootstrapError('No repository found.', error_code=1)  # noqa: B904


def install_vcs_hooks(repo_root: Path, forced: bool) -> None:
    """Install pre-commit and pre-push hooks for git or hg if present.

    It uses the 'hooks/' directory in the repository root
    to find the hook scripts to install to the auto-detected VCS
    metadata directory.

    :param repo_root Path: The root directory of the repository.
    :param forced bool: Whether to force overwrite of existing hooks.
    """
    _validate_path(repo_root, 'repo_root', exists=True)

    if DETECTED_VCS.is_none():
        controlled_print('No version control system detected; skipping VCS hook installation.')
        return

    hooks_dir = repo_root / 'hooks'
    if not hooks_dir.exists():
        controlled_print('No hooks/ directory found; skipping VCS hook installation.')
        return

    if DETECTED_VCS.is_git():
        _install_git_hooks(repo_root, forced)
    elif DETECTED_VCS.is_hg():
        _install_hg_hooks(repo_root, forced)
    else:
        controlled_print('Unsupported VCS for hook installation; skipping.')


def _is_valid_git_hook_name(name: str) -> bool:
    """Checks if the given name is a valid Git hook name.

    :param name str: The hook name to check.
    :return bool: True if valid, False otherwise.
    """
    return name in GIT_HOOK_NAMES


def _is_valid_hg_hook_name(name: str) -> bool:
    """Checks if the given name is a valid Mercurial hook name.

    :param name str: The hook name to check.
    :return bool: True if valid, False otherwise.
    """
    return name in HG_HOOK_NAMES


def _install_git_hooks(repo_root: Path, forced: bool) -> None:
    """Installs git hooks from the 'hooks/' directory in the repository root.

    :param repo_root Path: The root directory of the repository.
    :param forced bool: Whether to force overwrite existing hooks.
    """
    _validate_path(repo_root, 'repo_root', exists=True)

    git_dir = repo_root / '.git'
    hooks_dir = git_dir / 'hooks'
    source_hooks_dir = repo_root / 'hooks'

    if not source_hooks_dir.exists():
        controlled_print('No hooks/ directory found; skipping Git hook installation.')
        return

    if not hooks_dir.exists():
        controlled_print(f'Git hooks directory does not exist at {hooks_dir}; creating it.')
        try:
            hooks_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            controlled_print(f'Error: Could not create Git hooks directory at {hooks_dir}: {e}')
            controlled_print('Skipping Git hooks installation.')
            return

    try:
        for hook_file in source_hooks_dir.iterdir():
            if hook_file.is_file():
                hook_name = hook_file.name
                if not _is_valid_git_hook_name(hook_name):
                    controlled_print(f'Skipping non-standard Git hook: {hook_name}')
                    continue
                dest_hook = hooks_dir / hook_file.name
                if dest_hook.exists():
                    if forced:
                        controlled_print(f'Overwriting existing git hook: {dest_hook}')
                    else:
                        controlled_print(f'Git hook already exists, skipping: {dest_hook}')
                        continue
                try:
                    shutil.copy2(hook_file, dest_hook)
                except Exception as e:
                    controlled_print(f'Error: Could not copy hook {hook_file} to {dest_hook}: {e}')
                    controlled_print('Skipping this hook.')
                    continue
                try:
                    dest_hook.chmod(dest_hook.stat().st_mode | stat.S_IEXEC)
                except Exception:
                    controlled_print(f'Warning: Could not set executable permission for {dest_hook}')
                controlled_print(f'Installed git hook: {dest_hook}')
    except Exception as e:
        controlled_print(f'Error while installing Git hooks: {e}')
        controlled_print('Skipping Git hooks installation. Some hooks may not be installed.')


def _install_hg_hooks(repo_root: Path, forced: bool) -> None:
    """Installs Mercurial hooks from the 'hooks/' directory in the repository root.

    :param repo_root Path: The root directory of the repository.
    :param forced bool: Whether to force overwrite existing hooks.
    """
    _validate_path(repo_root, 'repo_root', exists=True)

    hg_dir = repo_root / '.hg'
    hgrc_file = hg_dir / 'hgrc'
    source_hooks_dir = repo_root / 'hooks'
    relative_hooks_path = '../hooks'

    if not source_hooks_dir.exists():
        controlled_print('No hooks/ directory found; skipping Mercurial hook installation.')
        return

    try:
        if not hgrc_file.exists():
            controlled_print(f'No hgrc file found at {hgrc_file}; creating a new one.')
            hgrc_file.touch()
    except Exception as e:
        controlled_print(f'Error: Could not create hgrc file at {hgrc_file}: {e}')
        controlled_print('Skipping Mercurial hooks installation.')
        return

    try:
        installed_hooks: set[str] = _already_installed_hg_hooks(repo_root)
        hook_entries = []
        hook_names = set()
        for hook_file in source_hooks_dir.iterdir():
            if hook_file.is_file():
                hook_name = hook_file.name
                if not _is_valid_hg_hook_name(hook_name):
                    controlled_print(f'Skipping non-standard Mercurial hook: {hook_name}')
                    continue
                if hook_name in installed_hooks and not forced:
                    controlled_print(f'Mercurial hook already configured, skipping: {hook_name}')
                    continue
                hook_entries.append(f'{hook_name} = {relative_hooks_path}/{hook_name}\n')
                hook_names.add(hook_name)
    except Exception as e:
        controlled_print(f'Error while preparing Mercurial hooks: {e}')
        controlled_print('Skipping Mercurial hooks installation.')
        return

    if not hook_entries:
        controlled_print('No Mercurial hooks to install; skipping.')
        return

    try:
        uniquifier = 1
        new_hgrc_file = hgrc_file.with_name(hgrc_file.name + f'new_{uniquifier}')
        while new_hgrc_file.exists():
            uniquifier += 1
            new_hgrc_file = hgrc_file.with_name(hgrc_file.name + f'new_{uniquifier}')

        if hook_entries:
            hgrc_content: list[str] = hgrc_file.read_text().splitlines(keepends=True)
            found_hooks_section = False
            with new_hgrc_file.open('w') as hgrc:
                in_hooks_section = False
                for line in hgrc_content:
                    # Find [hooks] section
                    stripped_line = line.strip()
                    if stripped_line.startswith('[hooks]'):
                        in_hooks_section = True
                        found_hooks_section = True
                        hgrc.write(line)
                        continue

                    # Process lines in [hooks] section
                    if in_hooks_section:
                        # end of [hooks] section
                        if stripped_line.startswith('[') and stripped_line.endswith(']'):
                            in_hooks_section = False
                            # Add any remaining hooks before leaving section
                            for name in hook_names:
                                hgrc.write(f'{name} = {relative_hooks_path}/{name}\n')

                        # A hook entry
                        elif '=' in line:
                            hook_name_key, hook_file_value = line.split('=', 1)
                            hook_name_key = hook_name_key.strip()
                            if hook_name_key in hook_names:
                                hook_names.remove(hook_name_key)
                                if forced:
                                    controlled_print(f'Overwriting existing Mercurial hook: {hook_name_key}')
                                    line = f'{hook_name_key} = {relative_hooks_path}/{hook_name_key}\n'
                                else:
                                    controlled_print(f'Mercurial hook already configured, skipping: {hook_name_key}')
                    hgrc.write(line)

                # If no [hooks] section was found, add it at the end
                if not found_hooks_section:
                    hgrc.write('[hooks]\n')
                    hgrc.writelines(hook_entries)

            # Replace original hgrc with new one (backup original)
            backup_suffix: str = '.bak.'
            backup_uniquifier: int = 1
            backup_file = hgrc_file.with_name(hgrc_file.name + f'{backup_suffix}{backup_uniquifier}')
            while backup_file.exists():
                backup_uniquifier += 1
                backup_file = hgrc_file.with_name(hgrc_file.name + f'{backup_suffix}{backup_uniquifier}')
            shutil.copy2(hgrc_file, backup_file)
            shutil.move(new_hgrc_file, hgrc_file)

    except Exception as e:
        controlled_print(f'Error while installing Mercurial hooks: {e}')
        controlled_print('Skipping Mercurial hooks installation.')
        return

    controlled_print(f'Configured Mercurial hooks in {hgrc_file}')


def _already_installed_hg_hooks(repo_root: Path) -> set[str]:
    """Returns a set of already installed Mercurial hook names from hgrc.

    :param repo_root Path: The root directory of the repository.
    :return set[str]: A set of installed hook names.
    """
    _validate_path(repo_root, 'repo_root', exists=True)

    hg_dir: Path = repo_root / '.hg'
    hgrc_file: Path = hg_dir / 'hgrc'
    installed_hooks: set[str] = set()

    if not hgrc_file.exists():
        return installed_hooks

    with hgrc_file.open('r') as hgrc:
        in_hooks_section = False
        for line in hgrc:
            line = line.strip()
            if line.startswith('[hooks]'):
                in_hooks_section = True
                continue
            if in_hooks_section:
                if line.startswith('[') and line.endswith(']'):
                    break  # End of hooks section
                if '=' in line:
                    hook_name = line.split('=')[0].strip()
                    installed_hooks.add(hook_name)

    return installed_hooks


def path_to_venv_python(venv_dir: Path) -> Path:
    """Returns the path to the Python executable within the virtual environment.

    :param venv_dir Path: The directory of the virtual environment.
    :param is_windows bool: Whether the platform is Windows.
    :return: The path to the Python executable.
    """
    _validate_path(venv_dir, 'venv_dir', exists=False)
    is_windows = _is_windows()
    bin_dir = venv_dir / ('Scripts' if is_windows else 'bin')
    python_exe = bin_dir / ('python.exe' if is_windows else 'python')
    return python_exe


@cache
def pip_module_is_available(python_exe: Path) -> bool:
    """Checks if 'pip' is available in the given Python executable.

    :param python_exe Path: The path to the Python executable.
    :return: True if 'pip' is available, False otherwise.
    """
    _validate_path(python_exe, 'python_exe', exists=True)

    stdout = subprocess.PIPE if not QUIET else subprocess.DEVNULL
    stderr = subprocess.PIPE if not QUIET else subprocess.DEVNULL
    try:
        if DEBUG:
            controlled_print(f"DEBUG: Running '{python_exe} -m pip --version' to check for pip availability")
        subprocess.run([python_exe, '-m', 'pip', '--version'], check=True, stdout=stdout, stderr=stderr)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def create_virtual_environment(venv_dir: Path, python_exe: Path) -> None:
    """
    Creates a virtual environment at the specified directory.
    If the directory already exists, it skips creation.
    :param venv_dir Path: The directory to create the virtual environment in.
    :param python_exe Path: The path to the Python executable within the venv.
    """
    _validate_path(venv_dir, 'venv_dir', exists=False)
    _validate_path(python_exe, 'python_exe', exists=False)

    if not venv_dir.exists():
        controlled_print(f"Creating temporary virtual environment in '{venv_dir}'...")
        create_venv(venv_dir, with_pip=True)
        controlled_print('---> Ensuring pip CLI script is installed in the virtual environment...')
        run_command([python_exe, '-m', 'ensurepip', '--upgrade'])

        controlled_print('---> Upgrading pip in the virtual environment to latest version...')
        if not pip_module_is_available(python_exe):
            pip_path = venv_dir / 'Scripts' / 'pip.exe' if _is_windows() else venv_dir / 'bin' / 'pip'
            if not pip_path.exists():
                controlled_print("Error: 'pip' is not available in the virtual environment after ensurepip.")
                controlled_print('Please check your Python installation.')
                raise FatalBootstrapError("'pip' not available in virtual environment.", error_code=1)
            run_command([pip_path, 'install', '--upgrade', 'pip'])
        else:
            run_command([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip', '--require-virtualenv'])
    else:
        controlled_print(f"Virtual environment '{venv_dir}' already exists. Skipping creation.")


def remove_virtual_environment(venv_dir: Path, quiet: bool = False) -> None:
    """Removes the temporary virtual environment directory.

    :param venv_dir Path: The directory of the virtual environment to remove.
    """
    if not quiet:
        controlled_print(f"Removing temporary virtual environment at '{venv_dir}'...")
    if venv_dir.exists():
        if sys.version_info >= (3, 12):
            shutil.rmtree(venv_dir, onexc=_remove_readonly)
        else:  # error handler deprecated in 3.12+
            shutil.rmtree(venv_dir, onerror=_remove_readonly)


def _remove_readonly(func: Callable[[str | Path], None], path: str | Path, _: Any) -> None:
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)


def install_tools(python_exe: Path, modules: list[InstallSpec]) -> None:
    """Installs core development tools into the virtual environment.

    If 'uv' is specified in the modules, it is bootstrapped with pip
    and used to install all the other modules; otherwise, the installation
    falls back to 'pip' for all modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules list[InstallSpec]: A list of InstallSpec objects to install.
    """
    _validate_path(python_exe, 'python_exe', exists=True)
    _validate_module_list(modules, 'modules')

    if not modules:
        return

    controlled_print('Installing/updating core development tools...')
    using_uv = any(mod.name == 'uv' for mod in modules)
    if using_uv:
        install_with_uv(python_exe, modules)
    else:
        install_with_pip(python_exe, modules)


def install_with_uv(python_exe: Path, modules: list[InstallSpec]) -> None:
    """Installs 'uv' using pip, then uses 'uv' to install the specified modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules list[InstallSpec]: A list of InstallSpec objects to install.
    """
    _validate_path(python_exe, 'python_exe', exists=True)
    _validate_module_list(modules, 'modules')

    uv_module: InstallSpec = [mod for mod in modules if mod.name == 'uv'][0]
    other_modules: list[InstallSpec] = [mod for mod in modules if mod.name != 'uv']

    bootstrap_message = f"--> Bootstrapping 'uv' using 'pip': {uv_module}, {uv_module.version or 'latest'}"
    install_with_pip(python_exe, [uv_module], message=bootstrap_message)

    if not other_modules:
        return

    controlled_print("--> Installing remaining modules using 'uv pip'")
    command = _build_install_command([python_exe, '-m', 'uv', 'pip'], other_modules)
    run_command(command)


def install_with_pip(python_exe: Path, modules: list[InstallSpec], message: str = '') -> None:
    """Installs the specified modules using 'pip'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    :param message str: An optional message to print before installation.
    """
    _validate_path(python_exe, 'python_exe', exists=True)
    _validate_module_list(modules, 'modules')
    _validate_string(message, 'message')

    if message:
        controlled_print(message)
    else:
        controlled_print("--> Installing modules using 'pip'")
    command = _build_install_command([python_exe, '-m', 'pip', '--require-virtualenv'], modules)
    run_command(command)


def _build_install_command(base_command: list[str | Path], modules: list[InstallSpec]) -> list[str | Path]:
    """Builds a complete installation command list for either 'pip' or 'uv pip'.

    :param base_command list[str | Path]: The base command to start with (e.g., pip or uv pip).
    :param modules list[InstallSpec]: A list of InstallSpec objects to install.
    :return list[str | Path]: The complete command list to run.
    """
    _validate_command(base_command, 'base_command')
    _validate_module_list(modules, 'modules')

    command = base_command + ['install', '-U']
    for module in modules:
        spec_str = module.name
        if module.extras:
            spec_str += module.extras
        if module.version:
            spec_str += module.version
        command.append(spec_str)
    return command


def set_powershell_execution_policy() -> None:
    """Sets the PowerShell execution policy to RemoteSigned for the current user if on Windows."""
    if not _is_windows():
        return

    controlled_print('--> Configuring PowerShell execution policy...')
    try:
        global _powershell_execution_policy_set  # pylint: disable=global-statement

        # Check current policy
        check_command = ['powershell', '-Command', 'Get-ExecutionPolicy']
        result = subprocess.run(check_command, capture_output=True, text=True, check=False)
        current_policy = result.stdout.strip()

        if current_policy == 'RemoteSigned':
            controlled_print('PowerShell execution policy is already set to RemoteSigned.')
            _powershell_execution_policy_set = True
            return

        controlled_print('Setting PowerShell execution policy to RemoteSigned for the current user.')
        # This command requires user confirmation if run interactively in a PS prompt,
        # but it should proceed without a prompt when called via subprocess from a non-interactive script.
        # Using -Force to be certain.
        set_command: list[str | Path] = [
            'powershell',
            '-Command',
            'Set-ExecutionPolicy',
            '-ExecutionPolicy',
            'RemoteSigned',
            '-Scope',
            'CurrentUser',
            '-Force',
        ]
        run_command(set_command)
        controlled_print('PowerShell execution policy has been set to RemoteSigned.')
        _powershell_execution_policy_set = True

    except (subprocess.CalledProcessError, FileNotFoundError, FatalBootstrapError) as e:
        controlled_print(f'Warning: Failed to set PowerShell execution policy: {e}')
        controlled_print('You may need to run the following command in PowerShell manually:')
        controlled_print('Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser')


def install_dot_env(repo_root: Path) -> None:
    """Installs a .env file into the root directory of the repository.

    It can substitute the {repo_root} placeholder with the actual
    repository root path if defined in the :data:`DOT_ENV_CONTENT`.

    It will skip installation if the .env file already exists or if
    :data:`DOT_ENV_CONTENT` is empty.

    :param repo_root Path: The root directory of the repository.
    :param bin_dir Path: The bin/Scripts directory of the virtual environment.
    """
    _validate_path(repo_root, 'repo_root', exists=True)
    dot_env_path = repo_root / '.env'
    if not DOT_ENV_CONTENT:
        controlled_print('.env installation is disabled; skipping .env installation.')
        return

    if dot_env_path.exists():
        controlled_print(f".env file already exists at '{dot_env_path}'; skipping installation.")
        return

    controlled_print(f"Installing .env file at '{dot_env_path}'...")
    env_content = DOT_ENV_CONTENT.replace('{repo_root}', str(repo_root))
    try:
        with dot_env_path.open('w') as dot_env_file:
            dot_env_file.write(env_content)
    except Exception as e:
        controlled_print(f'Error: Could not write .env file at {dot_env_path}: {e}')
        controlled_print('Skipping .env installation.')


def print_instructions(template: str) -> None:
    """Prints instructions to the user on how to activate the virtual environment
    and use the installed tools.

    :param template str: The instructions template to use.
    """
    _validate_string(template, 'template')

    activate_script = f"""
Unix/macOS/Linux:

    source {ACTIVATED_VENV_DIR}/bin/activate

If you use fish:

    source {ACTIVATED_VENV_DIR}/bin/activate.fish
"""

    if _is_windows():
        activate_script = f"""
Windows Command Prompt:

    {ACTIVATED_VENV_DIR}\\Scripts\\activate

PowerShell:

    .\\{ACTIVATED_VENV_DIR}\\Scripts\\Activate.ps1

Note: For PowerShell, you may need to adjust your execution policy to run scripts.
You can do this by running PowerShell and executing:

    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
"""
    deactivate_script: str = """
To deactivate the virtual environment, run:

Unix/macOS/Linux/fish/Windows Command Prompt/PowerShell:

    deactivate

"""
    instructions = template.format(activate=activate_script, deactivate=deactivate_script)
    controlled_print(instructions)

    if _is_windows() and not _powershell_execution_policy_set:
        controlled_print('\n' + '*' * 60)
        controlled_print('Warning: Failed to set PowerShell execution policy.')
        controlled_print('This may prevent you from activating the virtual environment in PowerShell.')
        controlled_print('To fix this, open PowerShell and run:')
        controlled_print('    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser')
        controlled_print('For more information, see the Microsoft documentation on execution policies.')
        controlled_print('*')


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    arg_parser = argparse.ArgumentParser(
        description='Bootstrap the development environment by creating a '
        'virtual environment and installing required tools.'
    )
    arg_parser.add_argument(
        '--yes', '-y', action='store_true', help='Automatically confirm and proceed without prompting.'
    )

    debug_group = arg_parser.add_mutually_exclusive_group()
    debug_group.add_argument('--debug', dest='debug', action='store_true', help='Enable debug output.')
    debug_group.add_argument('--no-debug', dest='debug', action='store_false', help='Disable debug output.')

    # Mutually exclusive group for verbosity
    verbosity_group = arg_parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '-q',
        '--quiet',
        '--ci',
        dest='quiet',
        action='store_true',
        help='Suppress non-error output. This is useful for CI environments.',
    )
    verbosity_group.add_argument(
        '-v', '--verbose', dest='quiet', action='store_false', help='Enable verbose output (default).'
    )

    # Forced hook installation option
    arg_parser.add_argument(
        '--force-hooks', action='store_true', help='Force overwrite of existing VCS hooks during installation.'
    )
    arg_parser.set_defaults(quiet=DEFAULT_QUIET, debug=DEFAULT_DEBUG)

    return arg_parser.parse_args()


def main() -> None:
    """
    Checks for required development tools and bootstraps a local virtual
    environment with them if necessary.
    """
    args = parse_arguments()
    global DEBUG, QUIET  # pylint: disable=global-statement
    DEBUG = args.debug
    QUIET = args.quiet

    if QUIET and not args.yes:
        print('Note: You can use --yes/-y to skip confirmation prompts.')
    if not args.yes and not confirmation_prompt(CONFIRMATION_PROMPT_MESSAGE):
        print('Aborted by user.')
        sys.exit(0)

    try:
        repo_root = get_repo_root()

        controlled_print(f'--- Bootstrapping development environment (in {repo_root}) ---')

        venv_dir = repo_root / VENV_DIR
    except FatalBootstrapError as e:
        controlled_print(f'Fatal error during bootstrap: {e}')
        sys.exit(e.error_code)

    try:
        python_exe = path_to_venv_python(venv_dir)
        create_virtual_environment(venv_dir, python_exe)
        install_tools(python_exe, BOOTSTRAP_MODULES)
        install_vcs_hooks(repo_root, forced=args.force_hooks)
        install_dot_env(repo_root)
        set_powershell_execution_policy()

        bin_dir = venv_dir / ('Scripts' if _is_windows() else 'bin')
        run_post_install_steps(python_exe=python_exe, root_path=repo_root, bin_dir=bin_dir)
        if REMOVE_BOOTSTRAP_VENV_ON_EXIT:
            remove_virtual_environment(venv_dir)
        print_instructions(POST_INSTALL_MESSAGE)

    except KeyboardInterrupt:
        remove_virtual_environment(venv_dir, quiet=True)
        controlled_print('')
        controlled_print('Aborted by user.')
        sys.exit(2)

    except FatalBootstrapError as e:
        remove_virtual_environment(venv_dir, quiet=True)
        controlled_print(f'Fatal error during bootstrap: {e}')
        sys.exit(e.error_code)

    except Exception as e:
        remove_virtual_environment(venv_dir, quiet=True)
        controlled_print(f'Fatal error during bootstrap: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
