SimpleBench
===========

A framework for building and running benchmarks.

* 0.3.1-alpha.0 2025-11-25 - Fifth alpha release
  * Fixed bug in rich tables report caused by switch to floats for 'n' complexity weights
  * Switched to a furo derived theme for Sphinx documentation
* 0.3.0-alpha.0 2025-11-24 - Fourth alpha release
  * Added enforced timeouts for benchmark runs
  * Updated 'n' complexity handling to allow floats as well as int
  * Changed 'progress' init parameter for Session() to 'show_progress'
* 0.2.1-alpha.0 2025-11-23 - Third alpha release
  * Changed _report_log format to use 'benchmark_id', 'benchmark_title', and 'benchmark_group'
  * Fixed oversharing issue with building tarball in dist
* 0.2.0-alpha.0 2025-11-23 - Second alpha release
  * Added support for tracking git commits and stable case_ids.
  * Added JSON structured _report_log for filesystem reports.
  * Restructured filesystem output directory
  * Added benchmark environment to _report_log entries
* 0.1.0-alpha.0 2025-11-21 - First public release to PyPI. First alpha release.
