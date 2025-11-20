=================
Command-Line Options
=================

.. _command_line_options

SimpleBench provides a variety of command-line options to customize the behavior
of your benchmarks. You can specify these options when running your benchmark
scripts to control output formats, reporting styles, and other features.

Options
---------------------------

  -h, --help            show a help message and exit
  --verbose             Enable verbose output
  --quiet               Enable quiet output
  --debug               Enable debug output
  --progress            Enable progress output
  --list                List all available benchmarks
  --run <benchmark> [<benchmark> ...]
                        Run specific benchmarks selected by group name or "all" for all benchmarks (default: all)
  --output_path <path>  Output destination directory (default: .benchmarks)
  --csv [{callback,console,filesystem} ...]
                        Output all results to CSV (filesystem, console, callback, default=filesystem)
  --csv.ops [{callback,console,filesystem} ...]
                        Output ops/second results to CSV (filesystem, console, callback, default=filesystem)
  --csv.timing [{callback,console,filesystem} ...]
                        Output timing results to CSV (filesystem, console, callback, default=filesystem)
  --csv.memory [{callback,console,filesystem} ...]
                        Output memory results to CSV (filesystem, console, callback, default=filesystem)
  --scatter-plot [{callback,filesystem} ...]
                        Output scatter plot graphs of benchmark results
  --scatter-plot.ops [{callback,filesystem} ...]
                        Create scatter plots of operations per second results.
  --scatter-plot.timings [{callback,filesystem} ...]
                        Create scatter plots of timing results.
  --scatter-plot.memory [{callback,filesystem} ...]
                        Create scatter plots of memory usage results.
  --rich-table [{callback,console,filesystem} ...]
                        All results as rich text tables (filesystem, console, callback, default=console)
  --rich-table.ops [{callback,console,filesystem} ...]
                        Ops/second results as rich text tables (filesystem, console, callback, default=console)
  --rich-table.timing [{callback,console,filesystem} ...]
                        Timing results as rich text tables (filesystem, console, callback, default=console)
  --rich-table.memory [{callback,console,filesystem} ...]
                        Memory results as rich text tables (filesystem, console, callback, default=console)
  --json [{callback,console,filesystem} ...]
                        statistical results to JSON (filesystem, console, callback, default=filesystem)
  --json-data [{callback,console,filesystem} ...]
                        statistical results + full data to JSON (filesystem, console, callback, default=filesystem)

