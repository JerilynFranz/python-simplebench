CSV Report
==========

.. _csv-report:

CSV (Comma-Separated Values) reports are designed for machine readability and
are ideal for importing benchmark results into spreadsheet applications like
Microsoft Excel or Google Sheets, or for analysis with data processing tools
like Pandas.

To generate a CSV report, you can use an option like `--csv.ops` when running
your benchmarks. By default, this will save a CSV file to the output directory
(which defaults to ``.benchmarks``).

Here is an example of how to run a benchmark script and generate a CSV report:

.. code-block:: shell
  :caption: Running a benchmark with a CSV report
  :name: run-benchmark-csv

    python my_benchmark_script.py --csv.ops

This command executes the benchmarks in `my_benchmark_script.py` and saves a
CSV file containing the operations-per-second results. A basic CSV output file
will look something like this:

.. code-block:: text
  :caption: Sample CSV Output
  :name: sample-csv-output

    # title: addition_benchmark
    # description: A simple addition benchmark of Python's built-in sum function.
    # unit: Ops/s
    N,Iterations,Rounds,Elapsed Seconds,mean (kOps/s),median (kOps/s),min (kOps/s),max (kOps/s),5th (kOps/s),95th (kOps/s),std dev (kOps/s),rsd (%)
    1,42801,1,0.291715587,147.0,148.0,22.0,153.0,142.0,151.0,6.77,4.6

Which corresponds to the following table:

.. csv-table::
   :header-rows: 1
   :align: center

   N,Iterations,Rounds,Elapsed Seconds,mean (kOps/s),median (kOps/s),min (kOps/s),max (kOps/s),5th (kOps/s),95th (kOps/s),std dev (kOps/s),rsd (%)
   1,42801,1,0.291715587,147.0,148.0,22.0,153.0,142.0,151.0,6.77,4.6



.. note::
   **Interpreting Outliers in Benchmark Results**

   In the sample output, you may notice that the ``min (Ops/s)`` value is an
   extreme outlier. This is a realistic reflection of real-world benchmarking,
   where system events like garbage collection can cause individual iterations
   to be significantly slower. This is why SimpleBench provides a full suite of
   statistics like the **median** (which is resistant to outliers) and **RSD%**
   (which quantifies inconsistency) to help you get a complete and honest
   picture of your code's performance.

.. note::
   To avoid "false precision", statistical results are output with three significant digits.
   Due to the inherent variability of performance measurement, any further digits are
   typically meaningless statistical noise.

   This is not an issue with SimpleBench itself, but rather a fundamental aspect of benchmarking and performance
   measurement in the real world.

Report Variations and Destinations
----------------------------------

SimpleBench provides several variations of the CSV report:

- ``--csv``: Generates a CSV file with all result types (ops, timing, and memory).
- ``--csv.ops``: Generates a CSV file only for operations-per-second results.
- ``--csv.timing``: Generates a CSV file only for timing results.
- ``--csv.memory``: Generates a CSV file only for memory usage results.

By default, CSV reports are saved to the ``filesystem``. You can send a report to
other destinations, such as the console, by appending the destination name. For
example, to print the CSV content directly to the terminal:

.. code-block:: shell
  :caption: Printing a CSV report to the console
  :name: csv-report-console

    python my_benchmark_script.py --csv.ops console

The generated files are named based on the benchmarked function name and report type.
To prevent collisions between identical benchmark names, a numeric prefix is added to
ensure uniqueness.

Examples

.. code-block:: shell
  :caption: Output file names for different CSV report types
  :name: csv-report-filenames

    001_addition_benchmark-memory_usage.csv
    001_addition_benchmark-peak_memory_usage.csv
    001_addition_benchmark-operations_per_second.csv
    001_addition_benchmark-timing.csv


Advanced Features
-----------------

Parameterized Benchmarks
~~~~~~~~~~~~~~~~~~~~~~~~

When running parameterized benchmarks, the CSV report includes additional
columns for each parameter variation. This makes it easy to sort, filter, and
analyze how different input parameters affect performance.

For more information on creating parameterized benchmarks, see the
:doc:`../advanced_usage` documentation.

Custom Complexity Weightings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``N`` column in the CSV report represents the complexity weighting of the
benchmark. This is particularly useful for analyzing the scalability of your
code with different input sizes.

For more details on how to use this feature, see the :doc:`../advanced_usage`
documentation.

.. include:: reports/csv_report_field_definitions.rst
