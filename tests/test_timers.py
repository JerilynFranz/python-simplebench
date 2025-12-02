"""Test the simplebench.timers module"""
import time

import pytest

from simplebench.exceptions import SimpleBenchRuntimeError, SimpleBenchTypeError
from simplebench.timers import is_valid_timer, timer_overhead_ns, timer_precision_ns
from simplebench.timers.exceptions import _TimersErrorTag
from simplebench.timers.info import fake_timer

from .testspec import Assert, TestAction, TestSpec, idspec


@pytest.mark.parametrize("testspec", [
    idspec("TIMER_001", TestAction(
        name="Valid timer function (time.perf_counter_ns)",
        action=is_valid_timer,
        assertion=Assert.EQUAL,
        args=[time.perf_counter_ns],
        expected=True)),
    idspec("TIMER_002", TestAction(
        name="Valid timer function (time.monotonic_ns)",
        action=is_valid_timer,
        args=[time.monotonic_ns],
        expected=True)),
    idspec("TIMER_003", TestAction(
        name="Valid timer function (time.process_time_ns)",
        action=is_valid_timer,
        args=[time.process_time_ns],
        expected=True)),
    idspec("TIMER_004", TestAction(
        name="Valid timer function (time.thread_time_ns)",
        action=is_valid_timer,
        args=[time.thread_time_ns],
        expected=True)),
    idspec("TIMER_005", TestAction(
        name="Fake timer function (fake_timer)",
        action=is_valid_timer,
        args=[fake_timer],
        expected=True)),
    idspec("TIMER_006", TestAction(
        name="Invalid timer function (time.monotonic)",
        action=is_valid_timer,
        args=[time.monotonic],
        expected=False)),
    idspec("TIMER_007", TestAction(
        name="Invalid timer function (time.time_ns)",
        action=is_valid_timer,
        args=[time.time_ns],
        expected=False)),
    idspec("TIMER_008", TestAction(
        name="Invalid timer function (str)",
        action=is_valid_timer,
        args=["not a function"],
        expected=False)),
    ])
def test_is_valid_timer(testspec: TestSpec):
    """Test is_valid_timer() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("PRECISION_001", TestAction(
        name="Timer precision for time.perf_counter_ns is larger than 0",
        action=timer_precision_ns,
        args=[time.perf_counter_ns],
        assertion=Assert.GREATER_THAN,
        expected=0.0)),
    idspec("PRECISION_002", TestAction(
        name="Timer precision for time.perf_counter_ns is smaller than 1_000 ns",
        action=timer_precision_ns,
        args=[time.perf_counter_ns],
        assertion=Assert.LESS_THAN,
        expected=1000.0)),
    idspec("PRECISION_003", TestAction(
        name="Timer precision for fake_timer raises an exception because it is unusable",
        action=timer_precision_ns,
        args=[fake_timer],
        exception=SimpleBenchRuntimeError,
        exception_tag=_TimersErrorTag.TIMER_PRECISION_NS_UNUSABLE_TIMER)),
    idspec("PRECISION_004", TestAction(
        name="Timer precision for time.time_ns raises an exception because it is invalid",
        action=timer_precision_ns,
        args=[time.time_ns],
        exception=SimpleBenchTypeError,
        exception_tag=_TimersErrorTag.TIMER_PRECISION_NS_INVALID_TIMER_FUNCTION)),
])
def test_timer_precision_ns(testspec: TestSpec):
    """Test timer_precision_ns() function."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    idspec("OVERHEAD_001", TestAction(
        name="Timer overhead for time.perf_counter_ns is larger than 0 ns",
        action=timer_overhead_ns,
        args=[time.perf_counter_ns],
        assertion=Assert.GREATER_THAN,
        expected=0.0)),
    idspec("OVERHEAD_002", TestAction(
        name="Timer overhead for time.perf_counter_ns is smaller than 1_000 ns",
        action=timer_overhead_ns,
        args=[time.perf_counter_ns],
        assertion=Assert.LESS_THAN,
        expected=1000.0)),
    idspec("OVERHEAD_003", TestAction(
        name="Timer overhead for fake_timer raises an exception because it is unusable",
        action=timer_overhead_ns,
        args=[fake_timer],
        exception=SimpleBenchRuntimeError,
        exception_tag=_TimersErrorTag.TIMER_OVERHEAD_NS_UNUSABLE_TIMER)),
    idspec("OVERHEAD_004", TestAction(
        name="Timer overhead for time.time_ns raises an exception because it is invalid",
        action=timer_overhead_ns,
        args=[time.time_ns],
        exception=SimpleBenchTypeError,
        exception_tag=_TimersErrorTag.TIMER_OVERHEAD_NS_INVALID_TIMER_FUNCTION)),
])
def test_timer_overhead_ns(testspec: TestSpec):
    """Test timer_overhead_ns() function."""
    testspec.run()
