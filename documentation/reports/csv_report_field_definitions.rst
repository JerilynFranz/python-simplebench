CSV Field Definitions
---------------------

Each report conains a set of comments and fields that provide detailed
information about the benchmark results.

Metadata Comment Lines
~~~~~~~~~~~~~~~~~~~~~~

At the top of each report, there are comment lines that provide metadata
about the report generation. These comments are prefixed with a `#` character
and include important information for understanding the context of the report.

Most modern CSV parsers will ignore comment lines, but they can be useful
for humans reading the report or for tools that process the report files.

They will usually be read and included by spreadsheet applications to provide
context about the data contained in the report.

:``# title``: The title of the report. This is the name of the benchmarked
              function.

:``# description``: A brief description of the benchmarked function, if provided. This is
                   generated from the docstring of the benchmark function.

:``# unit``: The unit of measurement for the report (e.g., Ops/s, seconds, bytes).

Example of Metadata Comment Lines

.. code-block:: text
  :caption: Example Metadata Comments 
  :name: example-report-comments

    # title: addition_benchmark
    # description: A simple addition benchmark of Python's built-in sum function.
    # unit: Ops/s

First Line Of Data
~~~~~~~~~~~~~~~~~~

The first line of the report data contains the column headers that label
each field in the report. These headers provide context for the numerical
data that follows.

Example of First Line of Data

.. code-block:: text
  :caption: Example First Line of Report Data
  :name: example-report-header

    N,Iterations,Rounds,Elapsed Seconds,mean (Ops/s),median (Ops/s),min (Ops/s),max (Ops/s),5th (Ops/s),95th (Ops/s),std dev (Ops/s),rsd (%)

Common Report Fields
~~~~~~~~~~~~~~~~~~~~

The following report fields are present in all of the report types below.

N
  A complexity weighting used to indicate the input size for a benchmark.

  A Big-O (*O*\ (*n*), etc) complexity weighting. This is used to indicate the 'size' of the
  input to a parameterized benchmark. It defaults to 1 unless overridden by the benchmark.
  The N value is used to help compare performance across different input sizes (if applicable)
  and to analyze how the function scales with different input sizes.

Iterations
  The number of statistical samples taken for the benchmark.

  The total number of iterations executed during the benchmark. An iteration is an execution of the benchmarked
  function once for statistical reporting purposes. It may be composed of multiple actual rounds to improve accuracy
  and precision, but is reported as a single count for the purposes of the table.

Rounds
  The number of times the benchmarked function is executed within a single iteration.

  The number of rounds executed during an iteration. A round is a single execution of the benchmarked function.
  Multiple rounds are often executed within an iteration to gather more accurate timing and performance data.
  They are executed in rapid succession, and their results are aggregated to produce the final metrics for an iteration.

Elapsed Seconds
  The total CPU time spent executing the benchmarked code.

  The total measured elapsed time in seconds for all iterations of the benchmark. This metric provides an overview
  of how long the benchmark took to complete. This does not include any setup or teardown time, focusing solely
  on the execution time of the benchmarked code. By default, this measures *CPU time*, not *wall-clock time*, to provide
  a more accurate representation of the code's performance. It can be overridden to measure wall-clock time instead
  if so desired.

Operations Per Second
~~~~~~~~~~~~~~~~~~~~~

The `operations per second` report provides a detailed overview of
the performance of the benchmarked code in terms of how many operations it can
perform per second. This is a common metric used to evaluate the efficiency of
code, especially in performance-critical applications.

Output numbers are scaled to appropriate units (Ops/s, kOps/s, MOps/s, etc) for easier readability.

The fields always in an `operations per second` report are:

mean (Ops/s)
  The average number of operations per second.

  The arithmetic mean average number of of operations per second (Ops/s) performed during the benchmark.
  This metric is calculated by dividing the total number of operations executed by the total elapsed time,
  then scaling it an appropriate factor (for example, kOps/s) for easier readability. It provides a quick overview
  of the benchmark's performance.

median (Ops/s)
  The 50th percentile (middle value) of operations per second.

  The median (50th percentile) number of operations per second (Ops/s) performed during the benchmark.
  This metric represents the middle value of the Ops/s measurements collected during the benchmark,
  providing a robust measure of central tendency that is less affected by outliers compared to the mean.
 
min (Ops/s)
  The lowest (worst) performance recorded across all iterations.

  The minimum number of operations per second (Ops/s) recorded during the benchmark. This metric indicates the
  lowest performance observed during the benchmark runs, which can be useful for identifying potential bottlenecks
  or performance issues.

max (Ops/s)
  The highest (best) performance recorded across all iterations.

  The maximum number of operations per second (Ops/s) recorded during the benchmark. This metric indicates the
  highest performance observed during the benchmark runs, showcasing the best-case scenario for the benchmarked code.

5th (Ops/s)
  The 5th percentile of operations per second.

  The 5th percentile number of operations per second (Ops/s) recorded during the benchmark. This metric indicates
  that 5% of the Ops/s measurements were below this value, providing insight into the lower end of the typical
  performance distribution.

95th (Ops/s)
  The 95th percentile of operations per second.

  The 95th percentile number of operations per second (Ops/s) recorded during the benchmark. This metric indicates
  that 95% of the Ops/s measurements were below this value, providing insight into the upper end of the typical
  performance distribution.

std dev (Ops/s)
  A measure of the variation or inconsistency in performance.

  The standard deviation of the operations per second (Ops/s) measurements collected during the benchmark. This metric
  quantifies the amount of variation or dispersion in the Ops/s values, providing insight into the consistency of the
  benchmark's performance. A lower standard deviation indicates more consistent performance, while a higher standard
  deviation suggests greater variability in the results.

rsd (%)
  A normalized measure of performance inconsistency, expressed as a percentage.

  The relative standard deviation (RSD) expressed as a percentage. This metric is calculated by dividing the standard
  deviation by the mean and multiplying by 100. It provides a normalized measure of variability, allowing for easier 
  comparison of consistency across different benchmarks or parameter configurations. A lower RSD% indicates more consistent
  performance relative to the mean, while a higher RSD% suggests greater variability in the results.

Timing
~~~~~~

A `timing` report focuses on the time taken to execute the benchmarked
code, rather than the number of operations per second. It provides insights into
the average time per operation and other timing-related statistics. 

Output numbers are scaled to appropriate units (seconds, milliseconds, microseconds, etc)
for easier readability.

The fields in this report include:

mean (s)
  The average time in seconds per operation.

  The arithmetic mean average time in seconds per operation (s/op). This metric is calculated by dividing the total
  elapsed time by the total number of operations. It provides a direct measure of how long a single operation
  takes on average.

median (s)
  The 50th percentile (middle value) of seconds per operation.

  The median (50th percentile) time in seconds per operation. This metric represents the middle value of the timing
  measurements, providing a robust measure of central tendency that is less affected by unusually fast or slow
  iterations (outliers).

min (s)
  The lowest (fastest) time per operation recorded across all iterations.

  The minimum time in seconds per operation recorded during the benchmark. This metric indicates the best-case
  performance observed, showcasing the fastest execution time for a single operation.

max (s)
  The highest (slowest) time per operation recorded across all iterations.

  The maximum time in seconds per operation recorded during the benchmark. This metric indicates the worst-case
  performance observed, which can be useful for identifying potential bottlenecks or performance stalls.

5th (s)
  The 5th percentile of seconds per operation. 5% of iterations were faster than this.

  The 5th percentile time in seconds per operation. This metric indicates that 5% of the timing measurements were
  faster than this value, providing insight into the best-case end of the performance distribution.

95th (s)
  The 95th percentile of seconds per operation. 95% of iterations were faster than this.

  The 95th percentile time in seconds per operation. This metric indicates that 95% of the timing measurements were
  faster than this value, providing insight into the typical worst-case performance, excluding extreme outliers.

std dev (s)
  A measure of the variation or inconsistency in the time per operation.

  The standard deviation of the seconds per operation (s) measurements. This metric quantifies the amount of
  variation in the timing values. A lower standard deviation indicates more consistent, predictable execution times.

rsd (%)
  A normalized measure of timing inconsistency, expressed as a percentage.

  The relative standard deviation (RSD) expressed as a percentage. This metric is calculated by dividing the standard
  deviation by the mean time. It provides a normalized measure of variability, allowing for easier comparison of
  timing consistency across different benchmarks.

Memory Usage
~~~~~~~~~~~~

A `memory usage` report provides information about the memory consumption
of the benchmarked code. It includes statistics on average and peak memory usage
during the benchmark runs. Output numbers are scaled to appropriate units (bytes, kB, MB, etc)
for easier readability.

For a `memory usage` report, two tables are generated: one for average
memory usage and another for peak memory usage with each table having
its name ending in either `-memory_usage.csv` or `-peak_memory_usage.csv`
respectively.

The fields in these tables are the same,
with the distinction being whether they refer to average or peak memory usage.

The fields always in a `memory usage` report are:

mean (bytes)
  The average memory allocated per operation, in bytes.

  The arithmetic mean average memory allocated per operation. This metric provides a general overview of the
  benchmark's memory footprint under typical execution.

median (bytes)
  The 50th percentile (middle value) of memory allocated per operation.

  The median (50th percentile) of memory allocated per operation. This provides a robust measure of the typical
  memory usage that is less affected by iterations with unusually high or low memory consumption.

min (bytes)
  The minimum memory allocated per operation across all iterations.

  The minimum memory allocated per operation recorded during the benchmark. This metric indicates the lowest
  memory footprint observed, representing the best-case scenario for memory efficiency.

max (bytes)
  The maximum memory allocated per operation across all iterations.

  The maximum memory allocated per operation recorded during the benchmark. This metric indicates the highest
  memory footprint observed, which is crucial for understanding peak memory demand and potential memory-related issues.

5th (bytes)
  The 5th percentile of memory allocated per operation.

  The 5th percentile of memory allocated per operation. This metric indicates that 5% of the iterations used
  less memory than this value, providing insight into the lower end of the memory usage distribution.

95th (bytes)
  The 95th percentile of memory allocated per operation.

  The 95th percentile of memory allocated per operation. This metric indicates that 95% of the iterations used
  less memory than this value, which is useful for understanding the typical upper bound of memory usage, excluding
  extreme outliers.

std dev (bytes)
  A measure of the variation in memory allocation per operation.

  The standard deviation of the memory allocation measurements. This metric quantifies the amount of variation
  in memory usage across iterations. A lower value indicates more consistent and predictable memory behavior.

rsd (%)
  A normalized measure of memory usage inconsistency, expressed as a percentage.

  The relative standard deviation (RSD) expressed as a percentage. This metric is calculated by dividing the standard
  deviation by the mean memory usage. It provides a normalized measure of variability, allowing for easier comparison
  of memory consistency across different benchmarks.
