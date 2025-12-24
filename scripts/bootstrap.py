"""Zero-dependency, cross-platform bootstrap script to set up a Python development environment.

It is designed to be run after cloning a git repository, to ensure that
all necessary development tools for working with this project are installed.

It relies only on the Python standard library and network access to PyPI.

If the required python tools are not found in the system environment,
the script creates a local virtual environment in the git repository
root directory (in a folder named `.venv`) and installs the tools there.

If the necessary tools are already installed in the system environment,
no action is taken.

Requires Python 3.8 or later.

This does not mean that it will use Python 3.8 for development; the virtual
environment can use any Python version installed on the system and any
modules and versions that support that Python version.

It only means that the bootstrap script itself needs at least Python 3.8 to run,
due to its use of certain language features.
"""
# pylint: disable=wrong-import-position
import sys

# Check for minimum Python version
if sys.version_info < (3, 8):
    major, minor = sys.version_info.major, sys.version_info.minor
    print(f"Error: Python 3.8 or later is required to run this script. You are using Python {major}.{minor}.")
    sys.exit(2)

import os
import re
import subprocess
from functools import lru_cache as cache
from pathlib import Path
from typing import List, NamedTuple, Union
from venv import create as create_venv

DEBUG: bool = False
"""Enable debug output if True."""


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
    InstallSpec(name="tox", version=">=4.32.0"),
    InstallSpec(name="tox-uv", version=">=1.29.0"),
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

To activate the development environment, run:

  {{activate}}

To deactivate the virtual environment, run:

  deactivate

{TOOL_USAGE_INSTRUCTIONS}
"""


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


def _validate_string_list(lst: list, name: str) -> None:
    """Validates that the input is a list of strings.

    :param lst list: The list to validate.
    :param name str: The name of the list (for error messages).
    :raises TypeError: If validation fails.
    """
    if not isinstance(lst, list):
        raise TypeError(f"{name} must be a list")
    if not all(isinstance(item, str) for item in lst):
        raise TypeError(f"all items in {name} must be strings")


def _validate_module_list(modules: List[InstallSpec], name: str) -> None:
    """Validates that the input is a list of InstallSpec instances.

    :param modules list: The list to validate.
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


def run_command(command: List[Union[str, Path]], check=True, **kwargs):
    """Helper to run a command and print its output.

    If the command is not found, or returns a non-zero exit code,
    prints an error message and exits the script.

    :param command List[Union[str, Path]]: The command to run as a list.
    :param check bool: Whether to raise an exception on non-zero exit code.
    :param kwargs: Additional keyword arguments to pass to subprocess.run().
    """
    _validate_command(command, "command")
    _validate_boolean(check, "check")
    _validate_kwarg_keys_are_strings(kwargs, "kwargs")

    try:
        if DEBUG:
            print(f"DEBUG: Running {command} with kwargs: {kwargs}")
        subprocess.run(command, check=check, **kwargs)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Is it in your PATH?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def modules_already_installed(python_exe: Path, modules: List[InstallSpec]) -> bool:
    """Checks if the required modules are already installed in the system environment.

    Tries to use 'pip install ... --dry-run' to simulate installation
    and checks if all required modules are already satisfied.

    If 'pip' is not available or returns errors, assumes modules are not installed.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to check.
    :return: True if all modules are installed, False otherwise.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_module_list(modules, "modules")

    # '--break-system-packages' is used to allow checking in system envs
    # where packages may be managed by the system package manager.
    # It prevents pip from refusing to run in such environments.
    # We only want to check, not actually install anything.
    command = _build_install_command([python_exe, "-m", "pip"], modules) + ["--dry-run", "--break-system-packages"]

    required_mods: set[str] = set(mod.name for mod in modules)
    print("--> Checking for required modules in the system environment...")
    try:
        if DEBUG:
            print(f"DEBUG: Running {command} to check installed modules")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
        output_lines = output.splitlines()
        already_satisfied_re: re.Pattern = re.compile(
            r"Requirement\s+already\s+satisfied:\s+(?P<mod_name>[^\s<>=!~\[]+)[\s<>=!~\[]")
        for line in output_lines:
            match = already_satisfied_re.search(line)
            if match:
                mod_name = match.group("mod_name")
                required_mods.discard(mod_name)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # 'pip' command not found or returned non-zero exit code; treat as not installed
        print(" - 'pip' command not found or failed. Assuming required modules are not installed.")
        return False
    for mod in sorted(modules):
        if mod.name not in required_mods:
            print(f" - Module '{mod}' already installed.")
        else:
            print(f" - Module '{mod}' NOT already installed.")

    return not required_mods  # True if all required modules are installed


def confirmation_prompt() -> bool:
    """Prompts the user for confirmation to proceed."""
    try:
        git_root = get_git_root()
        print(f"Current working directory: {os.getcwd()}")
        print(f"Git repo root directory: {git_root}")
        choice = ''
        while choice.lower().strip() not in ('y', 'yes', 'n', 'no'):
            choice = input(
                "This script will create a .venv directory in the git repo root "
                "directory and install tools into it for development. Continue? [y/n] ")
    except KeyboardInterrupt:
        print()
        return False

    return choice.lower().strip() in ('', 'y', 'yes')


@cache
def get_git_root() -> Path:
    """Finds the root directory of the git repository and caches the result.

    If not in a git repository, prints an error message and exits.

    It tries to use 'git rev-parse --show-toplevel' first, and falls back
    to searching parent directories for a '.git' folder if the git command is not found.
    """
    try:
        git_root_bytes = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.PIPE
        )
        git_root = Path(git_root_bytes.decode('utf-8').strip())
        return git_root
    except FileNotFoundError:
        # No git command found...so we do it the hard way
        current_dir = Path.cwd()
        for parent in [current_dir] + list(current_dir.parents):
            if (parent / ".git").is_dir():
                return parent

        print("Error: .git directory not found in any parent directories.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: This does not appear to be a git repository. "
              "Please run from within the cloned project directory.")
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

    try:
        if DEBUG:
            print(f"DEBUG: Running '{python_exe} -m pip --version' to check for pip availability")
        subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
        print(f"Creating virtual environment in '{venv_dir}'...")
        create_venv(venv_dir, with_pip=True)
        print("---> Ensuring pip CLI script is installed in the virtual environment...")
        run_command([python_exe, "-m", "ensurepip", "--upgrade"])

        print("---> Upgrading pip in the virtual environment to latest version...")
        if not pip_module_is_available(python_exe):
            pip_path = venv_dir / "Scripts" / "pip.exe" if _is_windows() else venv_dir / "bin" / "pip"
            if not pip_path.exists():
                print("Error: 'pip' is not available in the virtual environment after ensurepip.")
                print("Please check your Python installation.")
                sys.exit(1)
            run_command([pip_path, "install", "--upgrade", "pip"])
        else:
            run_command([
                python_exe, "-m", "pip", "install", "--upgrade", "pip", "--require-virtualenv"])
    else:
        print(f"Virtual environment '{venv_dir}' already exists. Skipping creation.")


def install_tools(python_exe: Path, modules: List[InstallSpec]) -> None:
    """Installs core development tools into the virtual environment.

    If 'uv' is specified in the modules, it is bootstrapped with pip
    and used to install all the other modules; otherwise, the installation
    falls back to 'pip' for all modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    """
    _validate_path(python_exe, "python_exe", exists=True)
    _validate_module_list(modules, "modules")

    if not modules:
        return

    print("Installing/updating core development tools...")
    using_uv = any(mod.name == "uv" for mod in modules)
    if using_uv:
        install_with_uv(python_exe, modules)
    else:
        install_with_pip(python_exe, modules)


def install_with_uv(python_exe: Path, modules: List[InstallSpec]) -> None:
    """Installs 'uv' using pip, then uses 'uv' to install the specified modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
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

    print("--> Installing remaining modules using 'uv pip'")
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
        print(message)
    else:
        print("--> Installing modules using 'pip'")
    command = _build_install_command([python_exe, "-m", "pip", "--require-virtualenv"], modules)
    run_command(command)


def _build_install_command(base_command: List[Union[str, Path]], modules: List[InstallSpec]) -> List:
    """Builds a complete installation command list for either 'pip' or 'uv pip'.

    :param base_command List[Union[str, Path]]: The base command to start with (e.g., pip or uv pip).
    :param modules: A list of InstallSpec objects to install.
    :return: The complete command list to run.
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

    activate_script = "source .venv/bin/activate"
    if _is_windows():
        activate_script = ".venv\\Scripts\\activate.bat"

    instructions = template.format(activate=activate_script)
    print(instructions)


def main():
    """
    Checks for required development tools and bootstraps a local virtual
    environment with them if necessary.
    """
    if modules_already_installed(
            python_exe=Path(sys.executable),
            modules=BOOTSTRAP_MODULES):
        print("All required development tools are already installed in the system environment.")
        print("No action is necessary.")
        print()
        print(TOOL_USAGE_INSTRUCTIONS)
        return

    if not confirmation_prompt():
        print("Aborted by user.")
        sys.exit(0)

    git_root = get_git_root()

    print(f"--- Bootstrapping development environment (in {git_root}) ---")

    venv_dir = git_root / ".venv"
    python_exe: Path = path_to_venv_python(venv_dir)
    create_virtual_environment(venv_dir, python_exe)
    install_tools(python_exe, BOOTSTRAP_MODULES)
    print_instructions(POST_INSTALL_MESSAGE)


if __name__ == "__main__":
    main()
