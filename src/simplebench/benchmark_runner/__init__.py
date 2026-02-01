"""Runners for executing benchmarks"""
# ruff: noqa F401

from .benchmark_runner import BenchmarkRunner
from .simplerunner import SimpleRunner

# No * imports here
__all__: list[str] = []
