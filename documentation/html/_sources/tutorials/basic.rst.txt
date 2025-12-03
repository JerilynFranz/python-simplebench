===============
Basic Benchmark
===============

.. _simplebench-tutorials-basic:

This tutorial demonstrates how to create a simple benchmark using SimpleBench,
run it, and generate a report.

The minimal code required to create and run a benchmark using SimpleBench is creating
a script that defines a function to be benchmarked with `@simplebench.benchmark`
and that calls `simplebench.main()` and then running it.

When you run the code below, SimpleBench automatically runs the benchmark function
`addition_benchmark`, collecting performance and memory statistics, and generating
a report. By specifying :doc:`command_line_options` you can generate output in
multiple formats, including rich text tables (like the one below), graphs, CSV
files, and JSON reports and select which statistics to report.

It runs using defaults setting for number of iterations, warmup runs, etc. You can
customize these settings via parameters set on the `@simplebench.benchmark` decorator.

.. literalinclude:: basic/basic_benchmark.py
   :language: python
   :caption: A basic benchmark example
   :name: basic-benchmark-example
   :linenos:

Save this code to a file, for example :download:`basic_benchmark.py <basic/basic_benchmark.py>`, and then run it from
your terminal:

.. code-block:: shell
   :caption: Generate a rich table report of operations-per-second by running the benchmark
   :name: run-basic-benchmark

    python basic_benchmark.py --rich-table.ops --progress

This will produce output similar to the following:

.. literalinclude:: basic/basic_output.txt
   :caption: Expected Output from Running the Basic Benchmark
   :name: expected-basic-benchmark-output
   :language: text

A detailed explanation of the output format and displayed statistics shown in this
example report can be found in the :doc:`/reports/rich_table_report` section
of the documentation.

.. note:: The command shown above includes the ``--progress`` option to
   display a progress bar while the benchmark is running. This option is not
   required to run the benchmark, and can be omitted if you do not wish to see
   the progress bar. It is not included in the expected output file since it
   produces dynamic output that changes as the benchmark runs and is removed
   from the terminal once the benchmark completes.

..
   TO REGENERATE THE GOLDEN MASTER FILE FOR THIS TEST:
   From the basic/ directory, run the following command:

       python basic_benchmark.py --rich-table.ops > basic_output.txt

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

   script_to_run = "tutorials/basic/basic_benchmark.py"
   expected_output_file = "tutorials/basic/basic_output.txt"
   script_args = ["--rich-table.ops"]
   
   # --------------------------

   actual_output = run_script_and_get_raw_output(
       script_path=script_to_run,
       args=script_args
   )
   assert_benchmark_output(actual_output, expected_output_file)

