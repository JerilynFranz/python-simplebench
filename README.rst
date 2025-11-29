SimpleBench
===========

**SimpleBench** is a Python framework for benchmarking and performance testing of code.

As such it has the following goals:

- Simple to use for simple benchmarks
- Powerful enough to handle sophisticated benchmarking needs out-of-the-box
- Flexible enough to handle complex custom benchmarking scenarios
- Extensible to allow users to add their own functionality as needed
- Full API and command-line interface support

Current Status
--------------

Alpha release 0.4.1-alpha.0

Functionally complete but not yet 100% tested or documented.
There may be breaking changes before reaching version 1.0.

Additional report formats and benchmark options are planned.

Installing
------------

Minimum Python Version: 3.10

**From PyPI**

.. code-block:: shell
  :name: install-simplebench

    python3 -m pip install simplebench

**From Source**

.. code-block:: shell
  :name: install-simplebench-from-source

  git clone https://github.com/JerilynFranz/python-simplebench
  cd python-simplebench
  python3 -m pip install .

Documentation
-------------

* `Installation <https://python-simplebench.readthedocs.io/en/latest/installation.html>`_
* `Using SimpleBench <https://python-simplebench.readthedocs.io/en/latest/usage.html>`_
* `Tutorials <https://python-simplebench.readthedocs.io/en/latest/tutorials.html>`_
   * `Basic Usage Tutorial <https://python-simplebench.readthedocs.io/en/latest/tutorials/basic.html>`_
* `Command-Line Options <https://python-simplebench.readthedocs.io/en/latest/command_line_options.html>`_
* `Reports <https://python-simplebench.readthedocs.io/en/latest/reports.html>`_
   * `Rich Table Report <https://python-simplebench.readthedocs.io/en/latest/reports/rich_table_report.html>`_
   * `CSV Report <https://python-simplebench.readthedocs.io/en/latest/reports/csv_report.html>`_
   * `JSON Report <https://python-simplebench.readthedocs.io/en/latest/reports/json_report.html>`_
   * `Scatterplot Graph Report <https://python-simplebench.readthedocs.io/en/latest/reports/graphs/scatterplot_graph_report.html>`_
* `Documentation Index <https://python-simplebench.readthedocs.io/en/latest/genindex.html>`_
* `Module Index <https://python-simplebench.readthedocs.io/en/latest/py-modindex.html>`_

Basic Example
-------------

This is a basic example of creating and running a benchmark using SimpleBench.
It demonstrates how to define a benchmark function, run it, and view an output
report on the console. There are more detailed examples and tutorials in the
`documentation <https://python-simplebench.readthedocs.io/en/latest/>`_.

SimpleBench supports numerous benchmark options, report formats, command-line options,
and customization points - this example focuses on the simplest case.

Defining a Benchmark
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
  :name: simple-benchmark-example

  import simplebench

  @simplebench.benchmark
  def addition_benchmark():
      """A simple addition benchmark of Python's built-in sum function."""
     sum(range(1000))

  if __name__ == "__main__":
      simplebench.main()


Running a Benchmark
~~~~~~~~~~~~~~~~~~~
.. code-block:: shell
  :name: run-simple-benchmark

    python my_benchmark_script.py --rich-table.ops --progress

Benchmark Output
~~~~~~~~~~~~~~~~

This will run the `addition_benchmark` function and generate a rich table report of its performance.

.. code-block:: text
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

Authors and acknowledgments
---------------------------

- Jerilyn Franz

Inspiration
-----------

"Simple things should be simple and complex things should be possible." *Alan Kay*

"... with proper design, the features come cheaply. This approach is arduous,
but continues to succeed."  *Dennis Ritchie*

Copyright
---------

Copyright 2025 by Jerilyn Franz

License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
