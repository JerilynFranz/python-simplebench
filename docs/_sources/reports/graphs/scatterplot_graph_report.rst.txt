Scatterplot Graph Report
=================

.. _scatterplot-graph-report:

Scatterplot Graphs are a good way to visualize the distribution and relationship of benchmark results
across a range of inputs or parameters.

SimpleBench leverages the `Seaborn <https://seaborn.pydata.org/>`_ and
`matplotlib <https://matplotlib.org/>`_ libraries to create scatterplot graphs that display 
benchmark results in a clear and informative manner.

.. note::

    Scatterplot Graph reports are just one of several reporting options available in SimpleBench.
    You can generate multiple other report types, including Rich Table reports, CSV reports, and JSON reports,
    each providing different perspectives on your benchmark results. See :doc:`../../reports/`
    for an overview of all available report types.

    Refer to the :doc:`../../command_line_options` section for more details on how to
    generate and customize these reports from the command line.


Example Usage
-------------

.. code-block:: python
  :caption: Defining a benchmark for a Scatterplot Graph report
  :name: scatterplot-graph-example-code
  :linenos:

  #!python3
  """Example Scatterplot Benchmark Script"""
  import simplebench


  @simplebench.benchmark(
      kwargs_variations={'size': [1, 10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]},
      variation_cols={'size': 'Size'},
      use_field_for_n='size')
  def addition_benchmark(**kwargs):
      """A simple benchmark that sums a range of numbers."""
      sum(range(kwargs['size']))


  if __name__ == "__main__":
      simplebench.main()


Saving the above code to a file named `my_benchmark_script.py`, you can run the benchmark
and generate a Scatterplot Graph report of operations per second using the following command:

.. code-block:: shell
  :caption: Running a benchmark with a Scatterplot Graph report
  :name: run-benchmark-scatterplot-graph

    python my_benchmark_script.py --scatterplot-graph.ops --progress

This command executes the benchmarks in `my_benchmark_script.py` and generates
a Scatterplot Graph displaying the operations-per-second results that is saved to a file.

The output graph will look something like this:

.. container:: image-block:

  .. container:: image-block-caption

    Scatterplot Graph of Addition Benchmark Operations Per Second

  .. container:: image-block-content

    .. image:: /_static/examples/001_addition_benchmark-operations_per_second.svg
      :alt: Scatterplot Graph of Addition Benchmark Operations Per Second
      :align: center

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

- `--scatterplot-graph`: Generates tables for all result types (ops, timing, and memory).
- `--scatterplot-graph.ops`: Generates tables only for operations-per-second results.
- `--scatterplot-graph.timing`: Generates tables only for timing results.
- `--scatterplot-graph.memory`: Generates tables only for memory usage results.

By default, reports are displayed in the console. You can send a report to other
destinations, such as the filesystem, by appending the destination name. For example,
to save the report to a file instead of printing it to the terminal:

.. code-block:: shell
  :caption: Saving a Scatterplot Graph report to the filesystem
  :name: scatterplot-graph-ops-filesystem

    python my_benchmark_script.py --scatterplot-graph.ops filesystem


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
