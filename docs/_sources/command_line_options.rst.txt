======================
Command-Line Options
======================

.. _command_line_options:

SimpleBench provides a variety of command-line options to customize the behavior
of your benchmark.

General Options
===============

These options control the overall behavior of the SimpleBench framework.

.. option:: -h, --help

   Show a help message and exit.

.. option:: --version

   Show SimpleBench's version and exit.

.. option:: --verbose

   Enable verbose output for more detailed information during execution.

.. option:: --quiet

   Suppress most output. This is useful for automated environments.

.. option:: --progress

   Display a progress bar during benchmark execution.

Reporting Options
=================

These options control which benchmarks are run and where results are saved.

.. option:: --list

   List all available benchmarks by group and name, then exit.

.. option:: --run <benchmark-group, ...>

   Run specified benchmarks selected by group. Multiple groups can be specified
   by separating them with spaces. You can see a list of available benchmark
   groups by using the :option:`--list` option.

   Defaults to running all benchmark groups if not specified.

   Example of running specific benchmark groups:

   .. code-block:: shell
     :caption: Running specific benchmark groups
     :name: run-specific-benchmark-groups

       python my_script.py --run group1 group2

.. option:: --output-path <path>

   Set the output directory for reports saved to the filesystem.
   Defaults to ``.benchmarks``.

Report Types
============

The following sections detail the options for each report type. Most reports can
be sent to one or more destinations using space separated values from the following list:

- ``console``: Print the report to the terminal.
- ``filesystem``: Save the report to a file in the output path.
- ``callback``: Pass the report object to a user-defined callback function.

Each report type has an appropriate default destination if none is explicitly specified.

This example report type option generates a rich table report with all result types,
printing it to the console and saving it to the filesystem.

.. code-block:: shell
  :caption: Report Type Destination Selection Example
  :name: report-destinations-example

    --rich-table console filesystem

Reports can often be filtered to only include specific result types, such as
operations-per-second, timing, or memory usage.

This example generates a rich table report with only operations-per-second results,
saving it to the filesystem

.. code-block:: shell
  :caption: Report Type Result Filtering Example
  :name: report-result-filtering-example

    --rich-table.ops filesystem

Rich Table Reports
------------------

Generates formatted tables for display in the console. The default destination
is ``console``.

.. option:: --rich-table [{callback,console,filesystem} ...]

   Generate tables for all result types.

.. option:: --rich-table.ops [{callback,console,filesystem} ...]

   Generate tables only for operations-per-second results.

.. option:: --rich-table.timing [{callback,console,filesystem} ...]

   Generate tables only for timing results.
.. option:: --rich-table.memory [{callback,console,filesystem} ...]

   Generate tables only for memory usage results.

CSV Reports
-----------

Exports results to CSV format.

These are easily imported into spreadsheet applications or data analysis tools.
The default destination is ``filesystem``.

.. option:: --csv [{callback,console,filesystem} ...]

    Generate CSV reports for all results.

.. option:: --csv.ops [{callback,console,filesystem} ...]

    Generate CSV reports only for operations-per-second results.

.. option:: --csv.timing [{callback,console,filesystem} ...]

    Generate CSV reports only for timing results.

.. option:: --csv.memory [{callback,console,filesystem} ...]

    Generate CSV reports only for memory usage results.

Graph Reports
-------------

Graph reports generate visual representations of benchmark results,
including line graphs and scatter plots. These visualizations can help you
better understand statistical characteristics and comparisons across parameterized
inputs.

They can only be saved to the filesystem or handled via a callback function.

The default destination for all graph reports is ``filesystem``.

Scatter Plot Reports
~~~~~~~~~~~~~~~~~~~~

Scatter plot reports display individual benchmark results as points on a graph,
allowing for easy comparison of performance across different benchmark
parameter values.

.. option:: --scatter-plot [{callback,filesystem} ...]

    Generate scatter plot graphs for all results.   

.. option:: --scatter-plot.ops [{callback,filesystem} ...]

    Generate scatter plot graphs only for operations-per-second results.

.. option:: --scatter-plot.timing [{callback,filesystem} ...]

    Generate scatter plot graphs only for timing results.

.. option:: --scatter-plot.memory [{callback,filesystem} ...]

    Generate scatter plot graphs only for memory usage results.

JSON Reports
------------

JSON report options allow you to export benchmark results in JSON format,
which is useful for programmatic consumption and integration with other tools.

The default destination is ``filesystem``.

.. option:: --json [{callback,console,filesystem} ...]

   Generate JSON reports only for statistical results. 

.. option:: --json-data [{callback,console,filesystem} ...]

   Generate JSON reports for statistical results and the full raw data.
