"""Tests the cache_factory module."""

import pytest

from .cache_factory import CACHE_DEFAULT, cached_factory, clear_cache, uncached_factory
from .testspec import TestAction, TestSpec, idspec

# TODO: Add tests for passthrough of additional arguments to the decorated factory functions


def uncached_factory_testspecs() -> list[TestSpec]:
    """Return the TestSpecs for uncached_factory() tests.

    :return: The TestSpecs for uncached_factory() tests.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def uncached_factory_does_not_cache_by_default() -> None:
        """Tests that uncached_factory does not cache by default."""
        clear_cache()  # Ensure cache is clear before running tests

        @uncached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory()
        obj2 = dummy_factory()
        assert obj1 is not obj2, "Uncached factory should produce different objects on each call."
    testspecs.append(idspec('UNCACHED_FACTORY_001', TestAction(
        name="uncached_factory() does not cache by default",
        action=uncached_factory_does_not_cache_by_default)))

    def uncached_factory_honors_same_cache_id() -> None:
        """Tests that uncached_factory produces the same object for the same cache_id."""
        clear_cache()  # Ensure cache is clear before running tests

        call_count = 0

        @uncached_factory
        def dummy_factory() -> object:
            nonlocal call_count
            call_count += 1
            return object()

        obj1 = dummy_factory(cache_id="test")
        obj2 = dummy_factory(cache_id="test")
        assert obj1 is obj2, "Uncached factory should produce the same object for the same cache_id."
        assert call_count == 1, "Factory should have been called once."
    testspecs.append(idspec('UNCACHED_FACTORY_002', TestAction(
        name="uncached_factory() honors cache_id parameter",
        action=uncached_factory_honors_same_cache_id)))

    def uncached_factory_different_cache_ids() -> None:
        """Tests that uncached_factory produces different objects for different cache_ids."""
        clear_cache()  # Ensure cache is clear before running tests

        @uncached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id="test1")
        obj2 = dummy_factory(cache_id="test2")
        assert obj1 is not obj2, "Uncached factory should produce different objects for different cache_ids."
    testspecs.append(idspec('UNCACHED_FACTORY_003', TestAction(
        name="uncached_factory() produces different objects for different cache_ids",
        action=uncached_factory_different_cache_ids)))

    def uncached_factory_none_cache_id() -> None:
        """Tests that uncached_factory produces different objects when cache_id is None."""
        clear_cache()  # Ensure cache is clear before running tests

        @uncached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id=None)
        obj2 = dummy_factory(cache_id=None)
        assert obj1 is not obj2, "Uncached factory should produce different objects when cache_id is None."
    testspecs.append(idspec('UNCACHED_FACTORY_004', TestAction(
        name="uncached_factory() produces different objects when cache_id is None",
        action=uncached_factory_none_cache_id)))

    def uncached_factory_cache_default() -> None:
        """Tests that uncached_factory produces same objects when cache_id is CACHE_DEFAULT."""
        clear_cache()  # Ensure cache is clear before running tests

        @uncached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id=CACHE_DEFAULT)
        obj2 = dummy_factory(cache_id=CACHE_DEFAULT)
        assert obj1 is obj2, "Uncached factory should produce same objects when cache_id is CACHE_DEFAULT."
    testspecs.append(idspec('UNCACHED_FACTORY_005', TestAction(
        name="uncached_factory() produces same objects when cache_id is CACHE_DEFAULT",
        action=uncached_factory_cache_default)))

    return testspecs


@pytest.mark.parametrize("testspec", uncached_factory_testspecs())
def test_uncached_factory(testspec: TestSpec) -> None:
    """Run the TestSpecs for uncached_factory() tests.

    :param testspec: The testspec to run.
    :type testspec: TestSpec
    """
    testspec.run()


def cached_factory_testspecs() -> list[TestSpec]:
    """Return the TestSpecs for cached_factory() tests.

    :return: The TestSpecs for cached_factory() tests.
    :rtype: list[TestSpec]
    """
    testspecs: list[TestSpec] = []

    def cached_factory_does_cache_by_default() -> None:
        """Tests that cached_factory caches by default."""
        clear_cache()  # Ensure cache is clear before running tests

        @cached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory()
        obj2 = dummy_factory()
        assert obj1 is obj2, "Cached factory should produce the same object on each call."
    testspecs.append(idspec('CACHED_FACTORY_001', TestAction(
        name="cached_factory() caches by default",
        action=cached_factory_does_cache_by_default)))

    def cached_factory_honors_same_cache_id() -> None:
        """Tests that cached_factory produces the same object for the same cache_id."""
        clear_cache()  # Ensure cache is clear before running tests

        call_count = 0

        @cached_factory
        def dummy_factory() -> object:
            nonlocal call_count
            call_count += 1
            return object()

        obj1 = dummy_factory(cache_id="test")
        obj2 = dummy_factory(cache_id="test")
        assert obj1 is obj2, "Cached factory should produce the same object for the same cache_id."
        assert call_count == 1, f"Factory should have been called once, actually called {call_count} times."
    testspecs.append(idspec('CACHED_FACTORY_002', TestAction(
        name="cached_factory() honors cache_id parameter",
        action=cached_factory_honors_same_cache_id)))

    def cached_factory_different_cache_ids() -> None:
        """Tests that cached_factory produces different objects for different cache_ids."""
        clear_cache()  # Ensure cache is clear before running tests

        @cached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id="test1")
        obj2 = dummy_factory(cache_id="test2")
        assert obj1 is not obj2, "Cached factory should produce different objects for different cache_ids."
    testspecs.append(idspec('CACHED_FACTORY_003', TestAction(
        name="cached_factory() produces different objects for different cache_ids",
        action=cached_factory_different_cache_ids)))

    def cached_factory_none_cache_id() -> None:
        """Tests that uncached_factory produces different objects when cache_id is None."""
        clear_cache()  # Ensure cache is clear before running tests

        @cached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id=None)
        obj2 = dummy_factory(cache_id=None)
        assert obj1 is not obj2, "Cached factory should produce different objects when cache_id is None."
    testspecs.append(idspec('CACHED_FACTORY_004', TestAction(
        name="cached_factory() produces different objects when cache_id is None",
        action=cached_factory_none_cache_id)))

    def cached_factory_cache_default() -> None:
        """Tests that cached_factory produces same objects when cache_id is CACHE_DEFAULT."""
        clear_cache()  # Ensure cache is clear before running tests

        @cached_factory
        def dummy_factory() -> object:
            return object()

        obj1 = dummy_factory(cache_id=CACHE_DEFAULT)
        obj2 = dummy_factory(cache_id=CACHE_DEFAULT)
        assert obj1 is obj2, "Cached factory should produce same objects when cache_id is CACHE_DEFAULT."
    testspecs.append(idspec('CACHED_FACTORY_005', TestAction(
        name="cached_factory() produces same objects when cache_id is CACHE_DEFAULT",
        action=cached_factory_cache_default)))

    return testspecs


@pytest.mark.parametrize("testspec", cached_factory_testspecs())
def test_cached_factory(testspec: TestSpec) -> None:
    """Run the TestSpecs for cached_factory() tests.

    :param testspec: The testspec to run.
    :type testspec: TestSpec
    """
    testspec.run()
