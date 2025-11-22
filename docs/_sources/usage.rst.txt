=================
Using SimpleBench
=================

.. _simplebench-installation:

.. toctree::
   :maxdepth: 4

.. index::

.. container:: textblock

    The `simplebench` module provides a benchmarking framework to measure the performance
    of Python code. It is designed to be easy to use while providing powerful
    customization and extension capabilities.

    In the simplest case, you can create a benchmark by decorating a function with
    `@simplebench.benchmark` and adding a call to `simplebench.main()` to your
    script. This instantly gives you a full-featured benchmark suite that can be
    run from the command line.

    This is all the code you need to write to create a simple benchmark:

.. code-block:: python
  :caption: A simple benchmark example
  :name: simple-benchmark-example
  :linenos:

    import simplebench

    @simplebench.benchmark
    def addition_benchmark():
        """A simple addition benchmark of Python's built-in sum function."""
        total = 0
        for i in range(1000):
            total += i
        return total

    if __name__ == "__main__":
        simplebench.main()

.. container:: textblock

  Save this code to a file, for example `my_benchmark_script.py`, and run it from your terminal:

.. code-block:: shell
  :caption: Running the benchmark
  :name: run-simple-benchmark

    python my_benchmark_script.py --rich-table.ops --progress


.. container:: textblock
    
  When you run this code, SimpleBench automatically handles timing the execution of
  `addition_benchmark`, collecting performance and memory statistics, and generating
  a report. By specifying :doc:`command_line_options` you can generate output in
  multiple formats, including rich text tables (like the one below), graphs, CSV
  files, and JSON reports.

  Note that the docstring from the `addition_benchmark` function is automatically
  used as the description in the output.

  For example, the command above produces the following rich table:

.. code-block:: text
  :caption: Output
  :name: example-output

                                                                 addition_benchmark
                                                                operations per second

                                            A simple addition benchmark of Python's built-in sum function.
    ┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
    ┃        ┃            ┃        ┃ Elapsed ┃    mean    ┃   median   ┃           ┃            ┃            ┃             ┃  std dev   ┃        ┃
    ┃   N    ┃ Iterations ┃ Rounds ┃ Seconds ┃   kOps/s   ┃   kOps/s   ┃ min Ops/s ┃ max kOps/s ┃ 5th kOps/s ┃ 95th kOps/s ┃   kOps/s   ┃  rsd%  ┃
    ┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
    │      1 │    46701   │      1 │  0.32   │    148.00  │    149.00  │   876.00  │    153.00  │    143.00  │    151.00   │      8.99  │  6.08% │
    └────────┴────────────┴────────┴─────────┴────────────┴────────────┴───────────┴────────────┴────────────┴─────────────┴────────────┴────────┘


.. container:: textblock

  While this simple decorator is powerful, SimpleBench is built on a rich,
  extensible API. You can easily add more advanced features like setup and
  teardown functions, multi-dimensional parameterized benchmarks, and even create
  your own custom reporters. The library is designed to handle the boilerplate,
  so you can focus on writing and using your benchmarks.

  The sections below provide more examples of some of these advanced features.

Examples
--------



