JSON Report
===========

.. _json-report:

JSON is a popular way to export data for programmatic consumption. SimpleBench leverages
JSON reports to provide structured benchmark results that can be easily parsed and analyzed
by other tools or scripts.

.. note::

   JSON reports are just one of several reporting options available in SimpleBench.
   You can also generate Rich Table reports, CSV reports, and graph reports, each providing
   different perspectives on your benchmark results.

   Refer to the :doc:`../../command_line_options` section for more details on how to
   generate and customize these reports.

To generate a JSON report, you can use an option like `--json`
when running your benchmarks. For example:

.. code-block:: shell
  :caption: Running a benchmark with a JSON report
  :name: run-benchmark-json

    python my_benchmark_script.py --json --progress

This command executes the benchmarks in `my_benchmark_script.py` and generates
a JSON file containing all the results.

.. note:: **JSON reports are intended for programmatic consumption and analysis**

  Because of this, they are not as human-readable as other report formats like
  rich tables or CSV. They do not offer the options for 'sub-reporting' only
  specific result types (ops, timing, memory) like other report formats.

JSON Report Structure
---------------------
A JSON report consists of a structured representation of the benchmark results,
including various statistical metrics for each benchmark. The structure models
the data as a JSON serialization of a :class:`~simplebench.case.Case` object
which contains multiple :class:`~simplebench.result.Result` objects for each
benchmark case. 

Here is an example of a report generated from the ``--json`` option:

.. container:: scrollable-block

   .. literalinclude:: _static/examples/001_addition_benchmark.json
      :language: json
      :caption: JSON Report Example

Because JSON is a structured format intended for programmatic consumption, it is best
viewed using a JSON viewer or parsed using a programming language that supports JSON.

.. note::

    It saves the raw statistical data for each benchmark result, allowing for detailed analysis and custom processing.
    It does not apply significant figures rounding to the data, which is typically done for human-readable reports.
    It is the responsibility of the consumer of the JSON report to format or round the data if needed.

Report Variations and Destinations
----------------------------------

The example above shows a report saved to the filesystem.

SimpleBench provides two variations:

- `--json`:
    Generates JSON for all result types (ops, timing, and memory) but includes only summary statistics.
- `--json.full-data`:
    Generates JSON for all result types (ops, timing, and memory)
    and includes full raw results data for each iteration in addition to the summary statistics.
    This is useful for in-depth analysis down to the level of individual iterations of the tests
    or custom processing.
    
    .. warning:: **Potentially Gigantic Output**

        Be aware that this can produce *EXTREMELY* large files if you have many benchmarks or
        iterations. Multi-megabyte-sized JSON output is common when using this option.

By default, reports are saved to the filesystem. You can send a report to other
destinations, such as the console, or a callback by appending the destination name. For example,
to print the report to the terminal instead of saving it to a file:

.. code-block:: shell
  :caption: Printing a JSON report to the console
  :name: json-console

    python my_benchmark_script.py --json console

Advanced Features
-----------------

Beyond the basic fields shown above, the reports also support advanced features such as:

Parameterized Benchmarks
  Including results for benchmarks that take parameters,
  allowing for analysis of performance across different input sizes or configurations.

Custom Complexity Weightings
  Input complexity weight/size annotations to help analysis of how performance
  scales with input size and allow *O()* analysis by the consumer.

These features make these reports a powerful tool for understanding
the performance characteristics of your code in a clear and structured manner.

Parameterized Benchmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When benchmarks are parameterized, SimpleBench populates additional fields
in the JSON report to reflect the parameters used for each benchmark run.

This allows you to easily compare performance across different configurations.
For example, if you have a benchmark that takes an input size
parameter, the report can include how performance varies with different input sizes.

See the :doc:`defining_benchmarks` section for more details on defining and using
parameterized benchmarks.

Custom Complexity Weightings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Related to parameterized benchmarks, SimpleBench allows you to specify
custom complexity weightings (number/size weighting) for your benchmarks.

These weightings are included in the report as the N field value, helping you analyze
how performance scales with input size and parameterization.

For example, you might specify that a benchmark set covers input sizes 1, 20, 100, 1000,
which will be indicated in the N fields of the report with a row for each size.

When defining a parameterized benchmark, you can provide complexity weightings that
reflect the expected performance characteristics of the code being benchmarked and
are matched with the parameters being used. This helps in understanding how the performance
of the benchmarked code changes as the input size or other parameters vary.

These advanced features make these reports a powerful tool for analyzing
the performance of parameterized benchmarks and understanding the scalability
of your code.
