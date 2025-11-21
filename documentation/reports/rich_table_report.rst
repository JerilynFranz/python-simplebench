Rich Table Report
=================

.. _rich-table-report:

Rich Tables are a popular way to display benchmark results in a clear and
concise manner. SimpleBench leverages the `rich <https://github.com/Textualize/rich>`_
library to generate these tables, providing visually appealing and easy-to-read reports.

.. note::

   Rich Table reports are just one of several reporting options available in SimpleBench.
   You can also generate CSV reports, graph reports, and JSON reports, each providing
   different perspectives on your benchmark results.

   Refer to the :doc:`command_line_options` section for more details on how to
   generate and customize these reports.

To generate a Rich Table report, you can use an option like `--rich-table.ops`
when running your benchmarks. For example:

.. code-block:: shell
  :caption: Running a benchmark with a Rich Table report
  :name: run-benchmark-rich-table

    python my_benchmark_script.py --rich-table.ops --progress

This command executes the benchmarks in `my_benchmark_script.py` and generates
a Rich Table in the terminal displaying the operations-per-second results.
A basic output will look something like this:

.. code-block:: text
  :caption: Sample Rich Table Output (operations per second)
  :name: sample-rich-table-output

                                                                     addition_benchmark
                                                                  operations per second

                                             A simple addition benchmark of Python's built-in sum function.
   ┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┓
   ┃        ┃            ┃        ┃ Elapsed ┃             ┃               ┃            ┃            ┃            ┃             ┃                ┃        ┃
   ┃   N    ┃ Iterations ┃ Rounds ┃ Seconds ┃ mean kOps/s ┃ median kOps/s ┃ min kOps/s ┃ max kOps/s ┃ 5th kOps/s ┃ 95th kOps/s ┃ std dev kOps/s ┃  rsd%  ┃
   ┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━┩
   │      1 │    44872   │      1 │  0.32   │    143.00   │     144.00    │      1.07  │    153.00  │    140.00  │    150.00   │        9.28    │  6.51% │
   └────────┴────────────┴────────┴─────────┴─────────────┴───────────────┴────────────┴────────────┴────────────┴─────────────┴────────────────┴────────┘

.. note::
   To avoid "false precision", statistical results are shown to three significant digits.
   Due to the inherent variability of performance measurement, any further digits are
   typically meaningless statistical noise.

   This is not an issue with SimpleBench itself, but rather a fundamental aspect of benchmarking and performance
   measurement in the real world.

.. note::
   **Interpreting Outliers in Benchmark Results**

   In the sample output above, you may notice that the ``min kOps/s`` value is
   an extreme outlier, far from the ``mean`` and ``median``. This is a realistic
   reflection of real-world benchmarking. System events like garbage collection,
   process scheduling, or I/O interrupts can cause individual iterations to be
   significantly slower than the typical case.

   This is precisely why SimpleBench provides a full suite of statistics. Instead
   of relying solely on the ``mean``, you should also consider:

   - The **median**, which is resistant to outliers and often gives a better
     sense of "typical" performance.
   - The **5th and 95th percentiles**, which show the range of performance
     for the vast majority of iterations, excluding the most extreme outliers.
   - The **standard deviation (std dev)** and **RSD%**, which quantify the
     level of inconsistency in the results. A high value indicates significant
     variability.

   By providing these metrics, SimpleBench allows you to get a complete and
   honest picture of your code's performance, including its variability.

Report Variations and Destinations
----------------------------------

The example above shows an operations-per-second report printed to the console.
SimpleBench provides several variations:

- `--rich-table`: Generates tables for all result types (ops, timing, and memory).
- `--rich-table.ops`: Generates tables only for operations-per-second results.
- `--rich-table.timing`: Generates tables only for timing results.
- `--rich-table.memory`: Generates tables only for memory usage results.

By default, reports are displayed in the console. You can send a report to other
destinations, such as the filesystem, by appending the destination name. For example,
to save the report to a file instead of printing it to the terminal:

.. code-block:: shell
  :caption: Saving a Rich Table report to the filesystem
  :name: rich-table-ops-filesystem

    python my_benchmark_script.py --rich-table.ops filesystem


Advanced Features
-----------------

Beyond the basic fields shown above, the reports also support advanced features such as:

Parameterized Benchmarks
  Including esults for benchmarks that take parameters,
  allowing for analysis of performance across different input sizes or configurations.

Custom Complexity Weightings:
  Including Big-O complexity weight/size annotations to help analyze how performance
  scales with input size.

These features make these reports a powerful tool for understanding
the performance characteristics of your code in a clear and structured manner.

Parameterized Benchmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When benchmarks are parameterized, SimpleBench generates additional columns in the
report for each parameter value requested for generation.

This allows you to easily compare performance across different configurations.
For example, if you have a benchmark that takes an input size
parameter, the report can include how performance varies with different input sizes.

See the :doc:`defining_benchmarks` section for more details on defining and using
parameterized benchmarks.

Custom Complexity Weightings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Related to parameterized benchmarks, SimpleBench allows you to specify
custom complexity weightings (number/size weighting)for your benchmarks.

These weightings are included in the report as the N column value, helping you analyze
how performance scales with input size and parameterization.

For example, you might specify that a benchmark set covers input sizes 1, 20, 100, 1000,
which will be indicated in the N column of the report with a row for each size.

When defining a parameterized benchmark, you can provide complexity weightings that
reflect the expected performance characteristics of the code being benchmarked and
are matched with the parameters being used. This helps in understanding how the performance
of the benchmarked code changes as the input size or other parameters vary.

These advanced features make these reports a powerful tool for analyzing
the performance of parameterized benchmarks and understanding the scalability
of your code.

.. include:: reports/rich_table_field_definitions.rst
