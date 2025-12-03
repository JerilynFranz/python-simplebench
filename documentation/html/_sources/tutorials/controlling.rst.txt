===============================
Controlling Benchmark Execution
===============================

.. _simplebench-tutorials-controlling-execution:

In addition to defining benchmarks, SimpleBench provides several mechanisms to
control how benchmarks are executed.

This tutorial covers some of the key options available.

Key Control Options
--------------------

**min_time**
  A float specifying the minimum time (in seconds) to spend on each benchmark run.
  By default, this is measured as wallclock time.

  This ensures that benchmarks run long enough to get accurate measurements,
  particularly for very fast functions. The benchmark will continue running
  iterations *at least* until this minimum wallclock time is reached. If it has not
  reached this time after the specified number of iterations, it will continue
  running additional iterations until the minimum wallclock time is satisfied.

  .. note:: Wallclock time refers to the actual elapsed time as measured by a clock on the wall,
     as opposed to CPU time which only counts the time the CPU was actively working
     on the benchmarked code. This means that 'Elapsed Time' in a report
     will generally NOT be the same as Wallclock Time, since Elapsed Time
     only counts the CPU time spent executing the benchmark function itself
     while Wallclock Time includes all time spent including overhead such as
     waiting for system resources, benchmark framework overhead, etc.

     It indicates the real-world time taken for the benchmark to complete, not
     the system CPU time used.

  The default is :data:`simplebench.defaults.DEFAULT_MIN_TIME`.

**max_time**
  A float specifying the maximum time (in seconds) to spend on each benchmark run.
  By default, this is measured as wallclock time.

  This helps ensure that benchmarks complete in a reasonable timeframe,
  especially for functions that may take longer to execute.

  If the benchmark reaches this maximum time before completing the specified
  number of iterations, it will stop early. It may run longer than this time
  if necessary to complete the current iteration.

  The default is :data:`simplebench.defaults.DEFAULT_MAX_TIME`.

**iterations**
  An integer specifying the minimum number of iterations to run for each benchmark.
  This controls how many statistical samples are collected for analysis.

  This interacts with the ``min_time`` and ``max_time`` settings to determine
  the actual number of iterations executed. SimpleBench will aim to run at least
  this many iterations, but may run more or fewer depending on the time constraints.

  It will run for *at least* this many iterations unless doing so would exceed
  the ``max_time`` limit.

  The default is :data:`simplebench.defaults.DEFAULT_ITERATIONS`.

**rounds**  
  An integer specifying the number of rounds to execute for each iteration.
  Each round is one complete execution of the benchmark function.

  More rounds can help improve measurement accuracy by aggregating timing
  reults across multiple executions. This is mainly useful for extremely fast 
  (defined as execution times of substantially less than 100 nanoseconds -
  or about 10 million operations per second) functions where
  individual execution times may be too small to measure accurately with
  timers of nanosecond resolution.

  For reference, executing a very simple function like 'sum(range(100))' takes around
  0.4 to 0.6 nanosecondson modern hardware (as measured on a 2023 Mac Studio with
  an M2 Ultra processor running Python 3.10.19). This is close to the limits of
  timer resolution on many systems.

  To get accurate timing measurements for such fast functions, increasing
  the number of rounds (e.g., to 100 or 1000) allows the benchmark to
  accumulate enough total execution time per iteration to be reliably measured.

  Precision varies based on the underlying hardware and operating system timer resolution,
  so the optimal number of rounds may differ between environments. But it generally
  holds true that to get a 10X improvement in timing accuracy for very fast functions,
  you need to increase the number of rounds by about 100X.

  If the benchmarked function is relatively slow (e.g., more than 100 nanoseconds
  per execution), increasing the number of rounds may not provide significant
  benefits and could lead to longer overall benchmark times without improving
  accuracy.

  The default is :data:`simplebench.defaults.DEFAULT_ROUNDS`.

**warmup_iterations**
  An integer specifying the number of warmup iterations to run before
  the actual benchmark measurements begin. Warmup iterations help to
  mitigate the effects of factors like CPU caching and JIT compilation,
  leading to more consistent and reliable benchmark results.

  The default is :data:`simplebench.defaults.DEFAULT_WARMUP_ITERATIONS`.

**timeout**
  A float specifying the maximum wallclock time (in seconds) allowed for the entire
  benchmark execution. If the benchmark exceeds this time, it will be
  terminated early. This terminates not just the individual benchmark,
  but the entire benchmark execution process. This is useful to prevent
  'hung' situations where a benchmark may take an unexpectedly long time
  to complete due to unforeseen issues.

  By default, the timeout is set to the ``max_time`` value plus an additional
  buffer of :data:`simplebench.defaults.DEFAULT_TIMEOUT_GRACE_PERIOD` seconds
  to allow for overhead.

Examples
--------

.. literalinclude:: controlling/controlling_benchmark.py
  :language: python
  :caption: Example of controlling benchmark execution parameters   
  :name: controlling-benchmark-example
  :linenos:


Save this code to a file, for example
:download:`controlling_benchmark.py <controlling/controlling_benchmark.py>`,
and then run it from your terminal:

.. code-block:: shell
   :caption: Generate a rich table report of per-round-timings
   :name: run-controlling-benchmark

    python controlling_benchmark.py --rich-table.timing --progress

This will execute the benchmark with the specified control parameters and generate
a Rich Table report showing the per-round timing statistics to the console
as the output.

You will see output similar to the following:

.. literalinclude:: controlling/controlling_benchmark_output.txt
   :caption: Expected Output from Running the Controlling Benchmark Example
   :name: expected-controlling-benchmark-output
   :language: text


..
   TO REGENERATE THE GOLDEN MASTER FILE FOR THIS TEST:
   
   From the 'controlling/' directory, run the following command:

       python controlling_benchmark.py --rich-table.timing > controlling_benchmark_output.txt

   The --progress option is omitted here because it produces dynamic output
   that changes as the benchmark runs and does not appear in the expected output file
   when piped to a file instead of the terminal anyway.

   The doctests will verify that the output of the benchmark script matches the
   format of the expected output: if the output format changes unexpectedly,
   the doctest will fail.

   Doctests are run from the 'documentation/' directory, so paths in the test
   configuration are relative to that directory: 'make doctest' handles this
   automatically.

.. testcode::
   :hide:

   # --- Test Configuration ---
   # Paths are relative to the 'documentation/' directory.

   script_to_run = "tutorials/controlling/controlling_benchmark.py"
   expected_output_file = "tutorials/controlling/controlling_benchmark_output.txt"
   script_args = ["--rich-table.timing"]
   
   # --------------------------

   actual_output = run_script_and_get_raw_output(
       script_path=script_to_run,
       args=script_args
   )
   assert_benchmark_output(actual_output, expected_output_file)