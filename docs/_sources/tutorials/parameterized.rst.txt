=======================
Parameterized Benchmark
=======================

.. _simplebench-tutorials-parameterized:

This tutorial demonstrates how to create a parameterized benchmark using SimpleBench, run it, and generate a report.

Parameterized benchmarks allow you to run the same benchmark function multiple times with different input parameters.

The key components of a parameterized benchmark are:

- **Benchmark Function**: A function decorated with `@simplebench.benchmark` that contains the code to be benchmarked.
  The function must accept parameters that will be varied during the benchmark runs. The parameters are defined
  as keyword arguments and passed to the function during each execution.

- **Parameters**: Defined as arguments for the decorator, which specifies different values or sets of values to be used as inputs to the benchmark function.

``kwarg_variations``
  A dictionary where the keys are parameter names to be passed to the benchmarked
  function and values are lists of possible values for those parameters.

  The benchmark will be executed for every combination of the provided parameter values.

  **Example**

  .. code-block:: python

    kwargs_variations={
        'arg1': [1, 2],
        'arg2': ['a', 'b']
    }

  will result in the following combinations being tested:

  .. code-block:: python

    {'arg1': 1, 'arg2': 'a'}
    {'arg1': 1, 'arg2': 'b'}
    {'arg1': 2, 'arg2': 'a'}
    {'arg1': 2, 'arg2': 'b'}

``variation_cols``  
    A dictionary where keys are parameter names and values are display names for reporting. Fields not
    included here will usually not display in a report. Fields specified here must be a subset of the
    keys in ``kwarg_variations``.

    **Example**

    .. code-block:: python

      variation_cols={
          'arg1': 'Argument 1',
          'arg2': 'Argument 2'
      }

   This will result in the report displaying columns/fields labeled 'Argument 1' and 'Argument 2'
   corresponding to the values of 'arg1' and 'arg2' used in each benchmark run.

``use_field_for_n``
    A string specifying a parameter to use as the 'N' field in reports, which is often used
    to indicate input size for complexity analysis. This parameter should be one of the keys in
    ``kwarg_variations``. It is optional; if not specified, the 'N' field will default to the value '1.0'.

    This is useful when you want to analyze how the performance of the benchmarked function
    scales with different input sizes or configurations. It is not required that the field be
    defined in ``variation_cols`` to be used as the 'N' field.

Minimal Example
---------------

The minimal code required to create and run a parameterized benchmark using SimpleBench is creating
a script that defines a function to be benchmarked with `@simplebench.benchmark`, specifying parameters using
the `@simplebench.parameter` decorator, and that calls `simplebench.main()`

.. literalinclude:: parameterized/minimal_parameterized_benchmark.py
   :language: python
   :caption: A minimal parameterized benchmark example
   :name: minimal-parameterized-benchmark-example
   :linenos:

Save this code to a file, for example :download:`minimal_parameterized_benchmark.py <parameterized/minimal_parameterized_benchmark.py>`, and then run it from
your terminal:

.. code-block:: shell
   :caption: Generate a rich table report for operations-per-second by running a parameterized benchmark    
   :name: run-minimal-parameterized-benchmark

    python minimal_parameterized_benchmark.py --rich-table.ops --progress

This will produce output similar to the following:

.. literalinclude:: parameterized/minimal_parameterized_output.txt
   :caption: Expected Output from Running the Parameterized Benchmark
   :name: expected-parameterized-benchmark-output
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
   
   From the 'parameterized/' directory, run the following command:

       python minimal_parameterized_benchmark.py --rich-table.ops > minimal_parameterized_output.txt

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

   script_to_run = "tutorials/parameterized/minimal_parameterized_benchmark.py"
   expected_output_file = "tutorials/parameterized/minimal_parameterized_output.txt"
   script_args = ["--rich-table.ops"]
   
   # --------------------------

   actual_output = run_script_and_get_raw_output(
       script_path=script_to_run,
       args=script_args
   )
   assert_benchmark_output(actual_output, expected_output_file)

Multi-dimensional Parameters
----------------------------

You can define multiple parameters for a benchmark function by defining multiple
parameters for the kwarg_variations