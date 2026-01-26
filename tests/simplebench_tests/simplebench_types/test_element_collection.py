"""Test suite for ElementCollection."""

import sys
from collections.abc import Iterable, Mapping, Sequence
from types import MappingProxyType
from typing import Any

import autopypath  # noqa: F401
import pytest
from testspec import PytestAction

from simplebench.simplebench_types._element_collection import ElementCollection, is_element_collection


class CustomIterable:
    """A custom iterable class for testing purposes."""
    def __init__(self, data: Iterable[Any]) -> None:
        self._data = data

    def __iter__(self) -> Iterable[Any]:
        return iter(self._data)


class CustomMapping(Mapping):
    """A custom mapping class for testing purposes."""
    def __init__(self, data: dict) -> None:
        self._data = data

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def __iter__(self) -> Iterable[Any]:  # type: ignore[override]
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

class CustomElementCollection:
    """A custom class that implements ElementCollection protocol."""
    def __init__(self, data: Sequence[Any]) -> None:
        self._data = data

    def __iter__(self) -> Iterable[Any]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, item: object, /) -> bool:
        return item in self._data

@pytest.mark.parametrize("testspec", [
    PytestAction('EC_001',
        name="list is ElementCollection",
        action=is_element_collection, args=[[1, 2, 3]],
        expected=True),
    PytestAction('EC_002',
        name="tuple is ElementCollection",
        action=is_element_collection, args=[(1, 2, 3)],
        expected=True),
    PytestAction('EC_003',
        name="set is ElementCollection",
        action=is_element_collection, args=[{1, 2, 3}],
        expected=True),
    PytestAction('EC_004',
        name="frozenset is ElementCollection",
        action=is_element_collection, args=[frozenset({1, 2, 3})],
        expected=True),
    PytestAction('EC_005',
        name="str is not ElementCollection",
        action=is_element_collection, args=["hello"],
        expected=False),
    PytestAction('EC_006',
        name="bytes is not ElementCollection",
        action=is_element_collection, args=[b"hello"],
        expected=False),
    PytestAction('EC_007',
        name="dict is not ElementCollection",
        action=is_element_collection, args=[{'a': 1, 'b': 2}],
        expected=False),
    PytestAction('EC_008',
        name="custom iterable is not ElementCollection",
        action=is_element_collection, args=[(x for x in range(3))],
        expected=False),
    PytestAction('EC_009',
        name="custom Mapping is not ElementCollection",
        action=is_element_collection, args=[MappingProxyType({'a': 1, 'b': 2})],
        expected=False),
    PytestAction('EC_010',
        name="custom ElementCollection is ElementCollection",
        action=is_element_collection, args=[CustomElementCollection([1, 2, 3])],
        expected=True),
    PytestAction('EC_011',
        name="custom Iterable is not ElementCollection",
        action=is_element_collection, args=[CustomIterable([1, 2, 3])],
        expected=False),
    PytestAction('EC_012',
        name="custom Mapping is not ElementCollection",
        action=is_element_collection, args=[CustomMapping({'a': 1, 'b': 2})],
        expected=False),
    PytestAction('EC_013',
        name="empty list is ElementCollection",
        action=is_element_collection, args=[[]],
        expected=True),
    PytestAction('EC_014',
        name="empty tuple is ElementCollection",
        action=is_element_collection, args=[()],
        expected=True),
    PytestAction('EC_015',
        name="empty set is ElementCollection",
        action=is_element_collection, args=[set()],
        expected=True),
    PytestAction('EC_016',
        name="empty frozenset is ElementCollection",
        action=is_element_collection, args=[frozenset()],
        expected=True),
    PytestAction('EC_017',
        name="None is not ElementCollection",
        action=is_element_collection, args=[None],
        expected=False),
    PytestAction('EC_018',
        name="CustomElementCollection with different data types",
        action=is_element_collection, args=[CustomElementCollection(['a', 1, 3.14, None])],
        expected=True),
    PytestAction('EC_019',
        name="isinstance fails to identify str as NOT an ElementCollection (python limitation)",
        action=isinstance, args=["test", ElementCollection],
        expected=True),
    PytestAction('EC_020',
        name="isinstance fails to identify bytes as NOT an ElementCollection (python limitation)",
        action=isinstance, args=[b'test', ElementCollection],
        expected=True),
    PytestAction('EC_021',
        name="isinstance fails to identify Mapping as NOT an ElementCollection (python limitation)",
        action=isinstance, args=[{'key': 'value'}, ElementCollection],
        expected=True),
])
def test_element_collection_protocol(testspec: PytestAction) -> None:
    """Test the ElementCollection Protocol and is_element_collection function."""
    testspec.run()


if __name__ == "__main__":
    try:
        pytest.main([__file__])
    except BaseException as e:
        print(f"An error occurred while running the tests: {e}")
        print(f"sys.path: {sys.path}")
        raise
