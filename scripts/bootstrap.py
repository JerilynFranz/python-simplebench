"""Bootstrap script to set up a development environment.

If necessary, creates a local virtual environment and installs core
development tools into it.

If the tools are already installed in the system environment, no action is taken.
"""
import os
import subprocess
import sys
from functools import cache
from pathlib import Path
from typing import NamedTuple
from venv import create as create_venv


class InstallSpec(NamedTuple):
    """Specification for modules to install in the virtual environment.

    :param str name: The name of the module to install.
    :param str version: An optional version specifier (e.g., ">=1.0.0").
    :param str extras: An optional extras specifier (e.g., "[dev]").
    """
    name: str
    version: str = ''
    extras: str = ''


# --- Modules to install during bootstrap ---

BOOTSTRAP_MODULES: list[InstallSpec] = [
    InstallSpec(name="uv", version=">=0.9.18"),
    InstallSpec(name="tox", version=">=4.32.0"),
    InstallSpec(name="tox-uv", version=">=1.29.0"),
]


TOX_INSTRUCTIONS = """
You use 'tox' to run tasks that set up and manage your development environment,
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
"""

# --- Post-install instructions template ---

POST_INSTALL_MESSAGE = f"""
--- Bootstrap complete! ---
To activate the development environment, run:

  {{activate}}

To deactivate the virtual environment, run:
  deactivate

{TOX_INSTRUCTIONS}
"""


def run_command(command, check=True, **kwargs):
    """Helper to run a command and print its output."""
    print(f"--> Running: {' '.join(map(str, command))}")
    try:
        subprocess.run(command, check=check, **kwargs)
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Is it in your PATH?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def check_requirements() -> None:
    """Checks that required system dependencies are available."""
    try:
        subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: 'git' command not found. Please install Git and ensure it is in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: 'git' command is not functioning properly.")
        sys.exit(1)


def modules_already_installed(python_exe: Path, modules: list[InstallSpec]) -> bool:
    """Checks if the specified modules are already installed in the system environment.

    Tries to use 'pip freeze' to get the list of installed packages
    and checks if the required modules are present with satisfying versions.

    If 'pip' is not available or returns errors, assumes modules are not installed.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to check.
    :return: True if all modules are installed, False otherwise.
    """
    command = _build_install_command([python_exe, "-m", "pip"], modules) + ["--dry-run"]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout + result.stderr
        if result.returncode != 0 or "ERROR:" in output:
            return False

    # any errors and we assume pip and/or modules are not installed
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

    return True


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
    """Finds the root directory of the git repository and caches the result."""
    try:
        git_root_bytes = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            stderr=subprocess.PIPE
        )
        git_root = Path(git_root_bytes.decode('utf-8').strip())
        return git_root
    except FileNotFoundError:
        print("Error: 'git' command not found. Please install Git and ensure it is in your PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: This does not appear to be a git repository. "
              "Please run from within the cloned project directory.")
        sys.exit(1)


def create_virtual_environment(venv_dir: Path, python_exe: Path) -> None:
    """
    Creates a virtual environment at the specified directory.
    If the directory already exists, it skips creation.
    :param venv_dir Path: The directory to create the virtual environment in.
    :param python_exe Path: The path to the Python executable within the venv.
    """
    if not venv_dir.exists():
        print(f"Creating virtual environment in '{venv_dir}'...")
        # Create venv without default pip; we ensure it ourselves for robustness.
        create_venv(venv_dir, with_pip=False)

        print("Ensuring pip is installed in the virtual environment...")
        run_command([python_exe, "-m", "ensurepip", "--upgrade"])
    else:
        print(f"Virtual environment '{venv_dir}' already exists. Skipping creation.")


def install_tools(python_exe: Path, modules: list[InstallSpec]) -> None:
    """Installs core development tools into the virtual environment.

    If 'uv' is specified in the modules, it is bootstrapped with pip
    and used to install all the other modules; otherwise, the installation
    falls back to 'pip' for all modules.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    """
    if not modules:
        return

    print("Installing/updating core development tools...")
    using_uv = any(mod.name == "uv" for mod in modules)
    if using_uv:
        install_with_uv(python_exe, modules)
    else:
        install_with_pip(python_exe, modules)


def install_with_uv(python_exe: Path, modules: list[InstallSpec]) -> None:
    """Installs 'uv' using pip, then uses 'uv' to install the specified modules.

    If modules with uv tools are specified, they are installed using 'uv tool install'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    """
    uv_module: InstallSpec = [mod for mod in modules if mod.name == "uv"][0]
    other_modules: list[InstallSpec] = [mod for mod in modules if mod.name != "uv"]

    bootstrap_message = (
        f"--> Bootstrapping 'uv' using 'pip': {uv_module.name}, "
        f"{uv_module.version or 'latest'}")
    install_with_pip(python_exe, [uv_module], message=bootstrap_message)

    if not other_modules:
        return

    print("--> Installing remaining modules using 'uv pip'")
    command = _build_install_command(
        [python_exe, "-m", "uv", "pip"], other_modules
    )
    run_command(command)


def install_with_pip(python_exe: Path, modules: list[InstallSpec], message: str = '') -> None:
    """Installs the specified modules using 'pip'.

    :param python_exe Path: The path to the Python executable within the venv.
    :param modules: A list of InstallSpec objects to install.
    :param message str: An optional message to print before installation.
    """
    if message:
        print(message)
    else:
        print("--> Installing modules using 'pip'")
    command = _build_install_command([python_exe, "-m", "pip"], modules)
    run_command(command)


def _build_install_command(base_command: list, modules: list[InstallSpec]) -> list:
    """Builds a complete installation command list.

    :param base_command list: The base command to start with (e.g., pip or uv pip).
    :param modules: A list of InstallSpec objects to install.
    :return: The complete command list to run.
    """
    command = base_command + ["install", "--quiet", "-U"]
    for module in modules:
        extras_str = f", extras: {module.extras}" if module.extras else ""
        print(f"  - {module.name}, {module.version or 'latest'}{extras_str}")
        spec_str = module.name
        if module.extras:
            spec_str += module.extras
        if module.version:
            spec_str += module.version
        command.append(spec_str)
    return command


def print_instructions(is_windows: bool, template: str) -> None:
    """Prints instructions to the user on how to activate the virtual environment
    and use the installed tools.

    :param is_windows bool: Whether the current platform is Windows.
    :param template str: The instructions template to use.
    """
    activate_script = "source .venv/bin/activate"
    if is_windows:
        activate_script = ".venv\\Scripts\\activate.bat"

    instructions = template.format(activate=activate_script)
    print(instructions)


def main():
    """
    Checks for required development tools and bootstraps a local virtual
    environment with them if necessary.
    """
    check_requirements()
    if modules_already_installed(
            python_exe=Path(sys.executable),
            modules=BOOTSTRAP_MODULES):
        print("All required development tools are already installed in the system environment.")
        print("No action is necessary.")
        print(TOX_INSTRUCTIONS)
        return

    if not confirmation_prompt():
        print("Aborted by user.")
        sys.exit(0)

    git_root = get_git_root()

    print(f"--- Bootstrapping development environment (in {git_root}) ---")

    venv_dir = git_root / ".venv"
    is_windows = sys.platform == "win32"
    bin_dir = venv_dir / ("Scripts" if is_windows else "bin")
    python_exe = bin_dir / ("python.exe" if is_windows else "python")

    create_virtual_environment(venv_dir, python_exe)
    install_tools(python_exe, BOOTSTRAP_MODULES)
    print_instructions(is_windows, POST_INSTALL_MESSAGE)


if __name__ == "__main__":
    main()
