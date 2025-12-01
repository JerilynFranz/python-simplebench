SimpleBench
===========

A framework for building and running benchmarks.

* 0.6.1-alpha.0 2025-12-1
  * Fix for failed imports related to optional [graphs] dependencies in default install
* 0.6.0-alpha.0 2025-12-1
  * Splitting of pypi install groups
    * default - all reporters except graph reporters
    * graph - add graph reporters to default install
    * all - all reporters including graph reporters
* 0.5.1-alpha.0 2025-11-30
  * Documentation updates
* 0.5.0-alpha.0 2025-11-30
  * Extended CSVReporter and RichTableReporter to allow customization
    of output columns using options.
  * Added checked support for explict parameters in benchmark functions.
  * Completed documentation for parameterized benchmarks.

* 0.4.1-alpha.0 2025-11-29 - Seventh alpha release
  * **Documentation Update**
    * Migration of README to .rst format
    * Addition of doctest support
    * Creation of first tutorials

* 0.4.0-alpha.0 2025-11-27 - Sixth alpha release
  * **Major Refactoring of Command-Line Interface (`cli.py`)**:
    * The main CLI logic has been significantly refactored for improved structure, robustness, and readability.
    * The `main()` function is now a high-level orchestrator, with argument parsing and session configuration moved into dedicated helper functions (`_create_parser`, `_configure_session_from_args`).
    * Implemented a robust `try...except...finally` pattern using a `final_message` variable. This ensures that terminal UI cleanup (e.g., stopping progress bars) always happens correctly before printing final error messages, preventing visual glitches.
    * The `argparse` setup now uses `add_mutually_exclusive_group` to properly handle conflicting verbosity flags (`--quiet`, `--verbose`, `--debug`).
  * **Improved Exception Handling**:
    * Added a new `SimpleBenchBenchmarkError` and a corresponding `BENCHMARK_ERROR` exit code to specifically handle and report exceptions that occur during the execution of a benchmark function itself.
    * The `Session.run()` method now wraps benchmark execution to catch these errors.
    * The CLI now explicitly catches `SimpleBenchTimeoutError` and `SimpleBenchBenchmarkError` to provide more specific feedback and exit codes to the user.
  * **API and Code Organization**:
    * The `enums` module was split into separate files for each enumeration (e.g., `ExitCode`, `Verbosity`), improving code organization.
    * The `add_reporter_flags()` method in `Session` is now called automatically by `parse_args()`, simplifying the API for programmatic use.
    * Removed the unused `group` argument from the internal `generate_benchmark_id()` function.
    * Removed the `section_mean()` method from `Case` and the `mean_change()` method from `JSONReporter` as being garbage metrics that should not exist.
  * **Documentation**:
    * Improved the visual styling of parameter lists in the Sphinx documentation for better readability.
    * Customized 'furo' theme for improved UX.
    * Added and improved module-level and function docstrings for clarity.
  * **Licensing**:
    * Updated `pyproject.toml` to use the modern SPDX license identifier (`Apache-2.0`).
  * **Testing**:
    * Added new unit tests for the `Session.report_keys()` method.
    * Added new unit tests for the `Session.add_reporter_flags()` method.
* 0.3.1-alpha.0 2025-11-25 - Fifth alpha release
  * Fixed bug in rich tables report caused by switch to floats for 'n' complexity weights
  * Switched to a furo derived theme for Sphinx documentation
* 0.3.0-alpha.0 2025-11-24 - Fourth alpha release
  * Added enforced timeouts for benchmark runs
  * Updated 'n' complexity handling to allow floats as well as int
  * Changed 'progress' init parameter for Session() to 'show_progress'
* 0.2.1-alpha.0 2025-11-23 - Third alpha release
  * Changed _report_log format to use 'benchmark_id', 'benchmark_title', and 'benchmark_group'
  * Fixed oversharing issue with building tarball in dist
* 0.2.0-alpha.0 2025-11-23 - Second alpha release
  * Added support for tracking git commits and stable case_ids.
  * Added JSON structured _report_log for filesystem reports.
  * Restructured filesystem output directory
  * Added benchmark environment to _report_log entries
* 0.1.0-alpha.0 2025-11-21 - First public release to PyPI. First alpha release.
