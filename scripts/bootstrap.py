"""Zero-dependency, cross-platform bootstrap script to set up a Python
development environment.

License
-------

Licensed under the Apache License, Version 2.0 (SPDX-License-Identifier: Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0.txt
Copyright [2025] Jerilyn Franz

See https://github.com/JerilynFranz/python-env-bootstrap/blob/main/LICENSE
for details.

You can get the most recent version of this script for your own use
in a project at https://github.com/JerilynFranz/python-env-bootstrap

Description
-----------

It is designed to be run after cloning a git or Mercurial repository, to create
a local virtual environment (.venvtools), and install necessary development tools.

It relies only on the Python standard library and network access to PyPI and
does not require any pre-installed packages or change your system Python installation.

This example project requires Python 3.8 or later, so this script
checks the Python version meets that requirement before proceeding.

The minimum Python version can be changed as needed for your project and
the lowest supported version is Python 3.8.

This example script installs the following tools by default:
- uv (for managing Python packages and dependencies)
- tox (for running tests, linters, and building documentation)
- tox-uv (to integrate uv with tox)
 
That is the minimum set of tools required to start development for this example project.

The minimum supported Python version, virtual environment directory name,
and list of tools to install can be customized by modifying the
corresponding constants in this script. The script can also be extended to
perform additional setup steps as needed via the run_post_install_steps() function
such as installing additional packages from requirements.txt files 
or configuring settings.

The choices of installing 'uv' and 'tox' for the bootstrap are just examples;
you can modify the BOOTSTRAP_MODULES list to only include any packages you need
for your development bootstrap workflow.

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
# pylint: disable=wrong-import-position
import sys

# Check for minimum supported Python version before importing anything else
# this ensures that users get a clear error message if they try to run
# the script with an unsupported Python version.
#
# The minimum version of Python this bootstrap script can support is 3.8+
# This can be changed as needed for your project.
if sys.version_info < (3, 8):
    major, minor = sys.version_info.major, sys.version_info.minor
    print("Error: Python 3.8 or later is required to run this project. "
          f"You are using Python {major}.{minor}.")
    sys.exit(2)

import argparse
import os
import subprocess
from functools import lru_cache as cache
from pathlib import Path
from typing import List, NamedTuple, Optional, Union
from venv import create as create_venv

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

VENV_DIR: str = ".venvtools"
"""The name of the virtual environment directory to create in the repository root for the bootstrap."""

ACTIVATED_VENV_DIR: str = 'venv'
"""The name of the virtual environment directory when the project virtual environment is activated."""

class InstallSpec(NamedTuple):
    """Specification for modules required to be installed.

    :param str name: The name of the module to install.
    :param str version: An optional version specifier (e.g., ">=1.0.0").
    :param str extras: An optional extras specifier (e.g., "[dev]").
    """
    name: str
    version: str = ''
    extras: str = ''

    def __str__(self):
        return f"{self.name}{self.extras}{self.version or ' (latest)'}"


# --- Modules to install during bootstrap ---

BOOTSTRAP_MODULES: List[InstallSpec] = [
    InstallSpec(name="uv", version=">=0.9.18"),
    InstallSpec(name="tox", version=">=4.22.0"),
    InstallSpec(name="tox-uv", version=">=1.13.1"),
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

  deactivate

{TOOL_USAGE_INSTRUCTIONS}
"""

# --- Confirmation prompt message ---

CONFIRMATION_PROMPT_MESSAGE = f"""
This script will create a {VENV_DIR} directory in the root
of the current repository.

It will install required tools into it for development, 
and install the project as an editable package into the
virtual environment.

No changes will be made to your system install of Python.

Continue? [y/n] """

# --- Global flags for output control ---

# These are defined here only for declaration purposes; they are actually set
# in main() after parsing command-line arguments.
# Changing these variables directly has no effect: Set DEFAULT_DEBUG and
# DEFAULT_QUIET instead to change the default behavior.
DEBUG: bool = False
QUIET: bool = False

def run_post_install_steps(python_exe: Path, root_path: Path, bin_dir: Path) -> None:
    """Runs any post-installation steps required after installing tools.

    This function is called automatically after the core development tools are installed.
    It is intended as a customization point for project-specific setup tasks, such as:
    - Installing the current project in editable mode
    - Setting up pre-commit hooks
    - Installing packages from requirements.txt files
    - Any other project-specific initialization

    The default example implementation here runs 'tox devenv -e dev' to set up and activate
    the development environment, and then installs the current project in editable mode
    with 'uv pip install -e .'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param root_path Path: The path to the root of the repository.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_path(root_path, "root_path", exists=True)
    controlled_print("--> Running initial 'tox devenv -e dev' to setup and activate the development environment...")
    run_command([python_exe, str(bin_dir / "tox"), "devenv", "-e", "dev"], cwd=root_path, check=True)
    controlled_print("--> Installing the current project in editable mode within the development environment...")
    run_command([bin_dir / "uv", "pip", "install", "-e", "."], cwd=root_path, check=True)

def _is_windows() -> bool:
    """Determines if the current platform is Windows."""
    return sys.platform == "win32"

def _validate_string(value: str, name: str) -> None:
    """Validates that the input is a string.

    :param value str: The value to validate.
    :param name str: The name of the value (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")

def _validate_string_list(lst: List[str], name: str) -> None:
    """Validates that the input is a list of strings.

    :param lst List[str]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(lst, list):
        raise TypeError(f"{name} must be a list")
    if not all(isinstance(item, str) for item in lst):
        raise TypeError(f"all items in {name} must be strings")

def _validate_module_list(modules: List[InstallSpec], name: str) -> None:
    """Validates that the input is a list of InstallSpec instances.

    :param modules List[InstallSpec]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(modules, list):
        raise TypeError(f"{name} must be a list")
    for module in modules:
        if not isinstance(module, InstallSpec):
            raise TypeError(f"all items in {name} must be InstallSpec instances")

def _validate_command(lst: List[Union[str, Path]], name: str) -> None:
    """Validates that the input is a list of that starts with
    either a string or Path, and contains only strings for all other items.

    It must contain at least one item.

    :param lst List[Union[str, Path]]: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(lst, list):
        raise TypeError(f"{name} must be a list")
    if not lst:
        raise ValueError(f"{name} must not be empty")
    if not isinstance(lst[0], (str, Path)):
        raise TypeError(f"the first item in {name} must be a string or Path")
    if not all(isinstance(item, str) for item in lst[1:]):
        raise TypeError(f"all items after the first in {name} must be strings")

def _validate_boolean(value: bool, name: str) -> None:
    """Validates that the input is a boolean.

    :param value bool: The value to validate.
    :param name str: The name of the value (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean")

def _validate_kwarg_keys_are_strings(kwargs: dict, name: str) -> None:
    """Validates that all keys in the input dictionary are strings.

    :param kwargs dict: The dictionary to validate.
    :param name str: The name of the dictionary (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(kwargs, dict):
        raise TypeError(f"{name} must be a dictionary")
    if not all(isinstance(k, str) for k in kwargs.keys()):
        raise TypeError(f"all keys in {name} must be strings")


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
        raise TypeError(f"{name} must be a Path instance")
    if exists and not path.exists():
        raise FileNotFoundError(f"{name} does not exist: {path}")

def run_command(command: List[Union[str, Path]], *,
                check: bool = True,
                cwd: Optional[Union[str, Path]] = None,
                **kwargs):
    """Helper to run a command and print its output.

    If the command is not found, or returns a non-zero exit code,
    prints an error message and exits the script.

    :param command List[Union[str, Path]]: The command to run as a list.
    :param check bool: Whether to raise an exception on non-zero exit code.
    :param cwd Optional[str, Path]: The working directory for the command.
    :param kwargs: Additional keyword arguments to pass to subprocess.run().
    """
    _validate_command(command, "command")
    _validate_boolean(check, "check")
    if cwd:
        _validate_path(Path(cwd), "cwd", exists=True)
    _validate_kwarg_keys_are_strings(kwargs, "kwargs")

    try:
        if DEBUG:
            debug_kwargs = kwargs.copy()
            if cwd:
                debug_kwargs['cwd'] = cwd
            print(f"DEBUG: Running {command} with kwargs: {debug_kwargs}")
        # Suppress output if QUIET is True and not already overridden
        if QUIET:
            kwargs.setdefault('stdout', subprocess.DEVNULL)
            kwargs.setdefault('stderr', subprocess.DEVNULL)
        subprocess.run(command, check=check, cwd=cwd, **kwargs)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Is it in your PATH?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command {command} failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def controlled_print(message: str) -> None:
    """Prints a message if not in quiet mode."""
    _validate_string(message, "message")
    if not QUIET:
        print(message)

def confirmation_prompt(message: str) -> bool:
    """Prompts the user for confirmation to proceed."""
    try:
        repo_root = get_repo_root()
        controlled_print(f"Current working directory: {os.getcwd()}")
        controlled_print(f"Repository root directory: {repo_root}")
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
    """
    try:
        git_root_bytes = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.PIPE
        )
        return Path(git_root_bytes.decode('utf-8').strip())
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Try Mercurial CLI
        try:
            hg_root_bytes = subprocess.check_output(
                ['hg', 'root'],
                stderr=subprocess.PIPE
            )
            return Path(hg_root_bytes.decode('utf-8').strip())
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback to directory search...
            current_dir = Path.cwd()
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / ".git").is_dir():
                    return parent

            # Check for Mercurial repository instead
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / ".hg").is_dir():
                    return parent

            controlled_print("Error: No Git or Mercurial repository found in any parent directories.")
            sys.exit(1)


def path_to_venv_python(venv_dir: Path) -> Path:
    """Returns the path to the Python executable within the virtual environment.

    :param venv_dir Path: The directory of the virtual environment.
    :param is_windows bool: Whether the platform is Windows.
    :return: The path to the Python executable.
    """
    _validate_path(venv_dir, "venv_dir", exists=False)
    is_windows = _is_windows()
    bin_dir = venv_dir / ("Scripts" if is_windows else "bin")
    python_exe = bin_dir / ("python.exe" if is_windows else "python")
    return python_exe


@cache
def pip_module_is_available(python_exe: Path) -> bool:
    """Checks if 'pip' is available in the given Python executable.

    :param python_exe Path: The path to the Python executable.
    :return: True if 'pip' is available, False otherwise.
    """
    _validate_path(python_exe, "python_exe", exists=True)

    stdout = subprocess.PIPE if not QUIET else subprocess.DEVNULL
    stderr = subprocess.PIPE if not QUIET else subprocess.DEVNULL
    try:
        if DEBUG:
            controlled_print(f"DEBUG: Running '{python_exe} -m pip --version' to check "
                  "for pip availability")
        subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            check=True,
            stdout=stdout,
            stderr=stderr
        )
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
    _validate_path(venv_dir, "venv_dir", exists=False)
    _validate_path(python_exe, "python_exe", exists=False)

    if not venv_dir.exists():
        controlled_print(f"Creating virtual environment in '{venv_dir}'...")
        create_venv(venv_dir, with_pip=True)
        controlled_print("---> Ensuring pip CLI script is installed in the virtual environment...")
        run_command([python_exe, "-m", "ensurepip", "--upgrade"])

        controlled_print("---> Upgrading pip in the virtual environment to latest version...")
        if not pip_module_is_available(python_exe):
            pip_path = venv_dir / "Scripts" / "pip.exe" if _is_windows() else venv_dir / "bin" / "pip"
            if not pip_path.exists():
                controlled_print("Error: 'pip' is not available in the virtual environment after ensurepip.")
                controlled_print("Please check your Python installation.")
                sys.exit(1)
            run_command([pip_path, "install", "--upgrade", "pip"])
        else:
            run_command([
                python_exe, "-m", "pip", "install", "--upgrade", "pip", "--require-virtualenv"])
    else:
        controlled_print(f"Virtual environment '{venv_dir}' already exists. Skipping creation.")

def install_tools(python_exe: Path, modules: List[InstallSpec]) -> None:
    """Installs core development tools into the virtual environment.

    If 'uv' is specified in the modules, it is bootstrapped with pip
    and used to install all the other modules; otherwise, the installation
    falls back to 'pip' for all modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules List[InstallSpec]: A list of InstallSpec objects to install.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_module_list(modules, "modules")

    if not modules:
        return

    controlled_print("Installing/updating core development tools...")
    using_uv = any(mod.name == "uv" for mod in modules)
    if using_uv:
        install_with_uv(python_exe, modules)
    else:
        install_with_pip(python_exe, modules)

def install_with_uv(python_exe: Path, modules: List[InstallSpec]) -> None:
    """Installs 'uv' using pip, then uses 'uv' to install the specified modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules List[InstallSpec]: A list of InstallSpec objects to install.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_module_list(modules, "modules")

    uv_module: InstallSpec = [mod for mod in modules if mod.name == "uv"][0]
    other_modules: List[InstallSpec] = [mod for mod in modules if mod.name != "uv"]

    bootstrap_message = (
        f"--> Bootstrapping 'uv' using 'pip': {uv_module}, "
        f"{uv_module.version or 'latest'}")
    install_with_pip(python_exe, [uv_module], message=bootstrap_message)

    if not other_modules:
        return

    controlled_print("--> Installing remaining modules using 'uv pip'")
    command = _build_install_command(
        [python_exe, "-m", "uv", "pip"], other_modules
    )
    run_command(command)

def install_with_pip(python_exe: Path, modules: List[InstallSpec], message: str = '') -> None:
    """Installs the specified modules using 'pip'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    :param message str: An optional message to print before installation.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_module_list(modules, "modules")
    _validate_string(message, "message")

    if message:
        controlled_print(message)
    else:
        controlled_print("--> Installing modules using 'pip'")
    command = _build_install_command([python_exe, "-m", "pip", "--require-virtualenv"], modules)
    run_command(command)

def _build_install_command(base_command: List[Union[str, Path]],
                           modules: List[InstallSpec]) -> List[Union[str, Path]]:
    """Builds a complete installation command list for either 'pip' or 'uv pip'.

    :param base_command List[Union[str, Path]]: The base command to start with (e.g., pip or uv pip).
    :param modules List[InstallSpec]: A list of InstallSpec objects to install.
    :return List[Union[str, Path]]: The complete command list to run.
    """
    _validate_command(base_command, "base_command")
    _validate_module_list(modules, "modules")

    command = base_command + ["install", "-U"]
    for module in modules:
        spec_str = module.name
        if module.extras:
            spec_str += module.extras
        if module.version:
            spec_str += module.version
        command.append(spec_str)
    return command

def print_instructions(template: str) -> None:
    """Prints instructions to the user on how to activate the virtual environment
    and use the installed tools.

    :param template str: The instructions template to use.
    """
    _validate_string(template, "template")

    activate_script = f"source {ACTIVATED_VENV_DIR}/bin/activate"
    if _is_windows():
        activate_script = f"{ACTIVATED_VENV_DIR}\\Scripts\\activate.bat"

    instructions = template.format(activate=activate_script)
    controlled_print(instructions)


def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    arg_parser = argparse.ArgumentParser(
        description="Bootstrap the development environment by creating a "
                    "virtual environment and installing required tools."
    )
    arg_parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help="Automatically confirm and proceed without prompting."
    )

    debug_group = arg_parser.add_mutually_exclusive_group()
    debug_group.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        help="Enable debug output."
    )
    debug_group.add_argument(
        '--no-debug',
        dest='debug',
        action='store_false',
        help="Disable debug output."
    )

    # Mutually exclusive group for verbosity
    verbosity_group = arg_parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '-q', '--quiet',
        dest='quiet',
        action='store_true',
        help="Suppress non-error output."
    )
    verbosity_group.add_argument(
        '-v', '--verbose',
        dest='quiet',
        action='store_false',
        help="Enable verbose output (default)."
    )
    arg_parser.set_defaults(quiet=DEFAULT_QUIET, debug=DEFAULT_DEBUG)

    return arg_parser.parse_args()

def main():
    """
    Checks for required development tools and bootstraps a local virtual
    environment with them if necessary.
    """
    args = parse_arguments()
    global DEBUG, QUIET  # pylint: disable=global-statement
    DEBUG = args.debug
    QUIET = args.quiet

    if QUIET and not args.yes:
        print("Note: You can use --yes/-y to skip confirmation prompts.")
    if not args.yes and not confirmation_prompt(CONFIRMATION_PROMPT_MESSAGE):
        print("Aborted by user.")
        sys.exit(0)

    repo_root = get_repo_root()

    controlled_print(f"--- Bootstrapping development environment (in {repo_root}) ---")

    venv_dir = repo_root / VENV_DIR
    python_exe = path_to_venv_python(venv_dir)
    create_virtual_environment(venv_dir, python_exe)
    install_tools(python_exe, BOOTSTRAP_MODULES)

    bin_dir = venv_dir / ("Scripts" if _is_windows() else "bin")
    run_post_install_steps(python_exe=python_exe, root_path=repo_root, bin_dir=bin_dir)
    print_instructions(POST_INSTALL_MESSAGE)


if __name__ == "__main__":
    main()
