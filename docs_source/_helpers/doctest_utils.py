"""Helpers for running doctest benchmarks and validating their output."""
import difflib
import os
import re
import subprocess
import sys
from typing import List

# --- Path Configuration ---
# The 'documentation' directory is our consistent root for all paths.
HELPER_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_ROOT = os.path.dirname(HELPER_DIR)
# --------------------------


def _sanitize_output(raw_text: str) -> str:
    """Internal helper to sanitize benchmark output text."""
    sanitized_lines = []
    for line in raw_text.splitlines():
        if line.strip().startswith('│'):
            line = re.sub(r'\b\d[\d.,]*%?\b', '...', line)
        sanitized_lines.append(line)
    return "\n".join(sanitized_lines)


def run_script_and_get_raw_output(script_path: str, args: List[str]) -> str:
    """
    Executes a script and returns its raw, unsanitized stdout.
    The script path is relative to the 'documentation' directory.
    """
    command = [sys.executable, script_path] + args
    env = os.environ.copy()
    env['COLUMNS'] = '500'

    # The subprocess needs the project root in its PYTHONPATH to find 'simplebench'.
    project_root = os.path.dirname(DOCS_ROOT)
    env['PYTHONPATH'] = f"{project_root}{os.pathsep}{env.get('PYTHONPATH', '')}"

    # Run the subprocess from the documentation root for consistent pathing.
    result = subprocess.run(
        command, capture_output=True, text=True, check=False,
        cwd=DOCS_ROOT, env=env
    )
    if result.stderr:
        return f"--- STDERR ---\n{result.stderr}"
    return result.stdout


def assert_benchmark_output(actual_raw: str, expected_output_file: str):
    """
    Sanitizes and compares benchmark output against an expected output file.
    The file path is relative to the 'documentation' directory.
    """
    # Construct the full path to the expected output file from the docs root.
    full_expected_path = os.path.join(DOCS_ROOT, expected_output_file)

    with open(full_expected_path, encoding="utf-8") as fh:
        expected_raw = fh.read()

    actual_sanitized = _sanitize_output(actual_raw)
    expected_sanitized = _sanitize_output(expected_raw)

    # To compare, normalize all whitespace in both strings.
    actual_normalized = " ".join(actual_sanitized.split())
    expected_normalized = " ".join(expected_sanitized.split())

    if actual_normalized != expected_normalized:
        diff = difflib.unified_diff(
            expected_sanitized.splitlines(keepends=True),
            actual_sanitized.splitlines(keepends=True),
            fromfile=f'expected (from {expected_output_file})',
            tofile='actual (live output)',
        )
        error_message = "Sanitized output does not match expected output (ignoring whitespace):\n" + "".join(diff)
        raise AssertionError(error_message)


if __name__ == "__main__":
    # This block allows the script to be used as a command-line tool to
    # generate the "golden master" output files for doctests.
    # Run this script from the 'documentation' directory.
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <output_file> <script_to_run> [args...]")
        print("  (Run from 'documentation/' directory, paths are relative to it)")
        sys.exit(1)

    output_file_path = sys.argv[1]
    script_to_run = sys.argv[2]
    script_args = sys.argv[3:]

    print(f"Generating golden master for '{script_to_run}'...")

    raw_output = run_script_and_get_raw_output(script_to_run, script_args)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(raw_output)

    print(f"Successfully generated golden master file: {output_file_path}")
