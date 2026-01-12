"""Benchmark decorators and functions."""

from .benchmark import benchmark, clear_registered_cases, get_registered_cases, validate_timer

__all__ = ['benchmark', 'get_registered_cases', 'clear_registered_cases', 'validate_timer']
