"""Bootstrap script to set up a development environment.

This script creates a local virtual environment in the `.venv` directory
and installs core development tools such as `uv` and `tox`.
"""
import os
import subprocess
import sys
from functools import cache
from pathlib import Path
from venv import create as create_venv


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


def confirmation_prompt() -> bool:
    """Prompts the user for confirmation to proceed."""
    try:
        git_root = get_git_root()
        print(f"Current working directory: {os.getcwd()}")
        print(f"Git repo root directory: {git_root}")
        choice = input(
            "This script will create a .venv directory in the git repo root "
            "directory and install tools for development. Continue? [Y/n] ")
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


def install_tools(python_exe: Path) -> None:
    """
    Installs core development tools into the virtual environment.
    :param python_exe Path: The path to the Python executable within the venv.
    """
    print("Installing/updating core tools (uv, tox) with uv...")
    run_command([python_exe, "-m", "pip", "install", "uv"])
    run_command([python_exe, "-m", "uv", "pip", "install", "--quiet", "-U", "tox"])


def print_instructions(is_windows: bool):
    """Prints instructions to the user on how to activate the virtual environment"""
    activate_script = "source .venv/bin/activate"
    if is_windows:
        activate_script = ".venv\\Scripts\\activate.bat"

    instructions = f"""
--- Bootstrap complete! ---

To activate the development environment, run:
  {activate_script}

You can then use 'tox' to run tasks, for example:
  tox -e lint
  tox -e docs

To deactivate the virtual environment, run:
  deactivate
"""
    print(instructions)


def main():
    """
    Creates a local, isolated virtual environment in ./.venv and installs
    core development tools (uv and tox) into it.
    """
    if not confirmation_prompt():
        print("Aborted by user.")
        sys.exit(0)

    git_root = get_git_root()
    os.chdir(git_root)

    print(f"--- Bootstrapping development environment (in {os.getcwd()}) ---")

    # --- Define Paths ---
    venv_dir = git_root / ".venv"
    is_windows = sys.platform == "win32"
    bin_dir = venv_dir / ("Scripts" if is_windows else "bin")
    python_exe = bin_dir / ("python.exe" if is_windows else "python")

    create_virtual_environment(venv_dir, python_exe)
    install_tools(python_exe)
    print_instructions(is_windows)


if __name__ == "__main__":
    main()
