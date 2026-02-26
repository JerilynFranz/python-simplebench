"""Tests for CoreDataSequence type."""
# ruff: noqa: F401
import pickle
from copy import deepcopy
from types import MappingProxyType

import autopypath
import pytest
import simplejson
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, CoreDataSet, ImmutableCoreDataTypes
from simplebench.simplebench_types._core._error_tags import _CoreDataErrorTag


@pytest.mark.parametrize('testspec', [
    PytestAction('INIT_001',
        name='Init with empty input',
        action=CoreDataSequence,
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_002',
        name='Init with list of integers',
        action=CoreDataSequence,
        args=[[1, 2, 3, 4, 5]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_003',
        name='Init with tuple of strings',
        action=CoreDataSequence,
        args=[('a', 'b', 'c')],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_004',
        name='Init with mixed primitive types',
        action=CoreDataSequence,
        args=[[1, 'two', 3.0, True, None]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_005',
        name='Init with nested CoreDataSequence',
        action=CoreDataSequence,
        args=[[CoreDataSequence([1, 2]), CoreDataSequence(['a', 'b'])]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_006',
        name='Init with invalid type (should raise error)',
        action=CoreDataSequence,
        args=[[object()]],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE),
    PytestAction('INIT_007',
        name='Init with non-iterable (should raise error)',
        action=CoreDataSequence,
        args=[42],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_008',
        name='Init with nested set',
        action=CoreDataSequence,
        args=[[1, [2, 3], {'four', 4}]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_009',
        name='Init with nested dictionary',
        action=CoreDataSequence,
        args=[[1, {'two': 2}, 3]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_010',
        name='Init with nested MappingProxyType',
        action=CoreDataSequence,
        args=[[1, MappingProxyType({'two': 2}), 3]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_011',
        name='Init with nested frozen set',
        action=CoreDataSequence,
        args=[[1, frozenset({2, 3}), 4]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_012',
        name='Init directly from set',
        action=CoreDataSequence,
        args=[{1, 2, 3}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_013',
        name='Init directly from frozenset',
        action=CoreDataSequence,
        args=[frozenset({1, 2, 3})],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
    PytestAction('INIT_014',
        name='Init with dict (should raise error)',
        action=CoreDataSequence,
        args=[{'a': 1, 'b': 2}],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_015',
        name='Init with string (should raise error)',
        action=CoreDataSequence,
        args=['not a sequence'],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_016',
        name='Init with bytes (should raise error)',
        action=CoreDataSequence,
        args=[b'not a sequence'],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_017',
        name='Init with nested CoreDataTypes',
        action=CoreDataSequence,
        args=[[CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}), CoreDataSet({4, 5})]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSequence),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('CONTAINS_001',
        name='Check containment of existing item',
        action=CoreDataSequence([1, 2, 3, 4, 5]).__contains__, args=[3],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_002',
        name='Check containment of non-existing item',
        action=CoreDataSequence([1, 2, 3, 4, 5]).__contains__, args=[6],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_003',
        name='Check containment of CoreDataSequence item',
        action=CoreDataSequence([CoreDataSequence([1, 2]), CoreDataSequence([3, 4])]).__contains__,
        args=[CoreDataSequence([1, 2])],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_004',
        name='Check containment of CoreDataMapping item',
        action=CoreDataSequence([CoreDataMapping({'a': 1}), CoreDataMapping({'b': 2})]).__contains__,
        args=[CoreDataMapping({'a': 1})],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_005',
        name='Check containment of CoreDataSet item',
        action=CoreDataSequence([CoreDataSet({1, 2}), CoreDataSet({3, 4})]).__contains__,
        args=[CoreDataSet({1, 2})],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_006',
        name='Check containment of invalid type',
        action=CoreDataSequence([1, 2, 3]).__contains__, args=[object()],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_007',
        name='Check containment in empty CoreDataSequence',
        action=CoreDataSequence([]).__contains__, args=[1],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_008',
        name='Check containment of None',
        action=CoreDataSequence([None, 1, 2]).__contains__, args=[None],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_009',
        name='Check containment of boolean True',
        action=CoreDataSequence([True, False, 0, 1]).__contains__, args=[True],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_010',
        name='Check containment of boolean False',
        action=CoreDataSequence([True, False, 0, 1]).__contains__, args=[False],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_011',
        name='Check containment of string item',
        action=CoreDataSequence(['a', 'b', 'c']).__contains__, args=['b'],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_012',
        name='Check containment of float item',
        action=CoreDataSequence([1.1, 2.2, 3.3]).__contains__, args=[2.2],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_013',
        name='Check "in" operator for existing item',
        action=lambda: 3 in CoreDataSequence([1, 2, 3, 4, 5]),
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_014',
        name='Check "in" operator for non-existing item',
        action=lambda: 6 in CoreDataSequence([1, 2, 3, 4, 5]),
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_015',
        name='Check "in" operator for CoreDataMapping item',
        action=lambda: CoreDataMapping(
            {'a': 1}) in CoreDataSequence(
                [CoreDataMapping({'a': 1}),
                CoreDataMapping({'b': 2})]),
        assertion=Assert.TRUE),
])
def test_contains(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name='Get length of non-empty CoreDataSequence',
        action=CoreDataSequence([1, 2, 3, 4, 5]).__len__,
        expected=5),
    PytestAction('LEN_002',
        name='Get length of empty CoreDataSequence',
        action=CoreDataSequence([]).__len__,
        expected=0),
    PytestAction('LEN_003',
        name='Get length of CoreDataSequence with mixed types',
        action=CoreDataSequence([1, 'two', 3.0, True, None]).__len__,
        expected=5),
    PytestAction('LEN_004',
        name='Get length of CoreDataSequence with nested CoreDataTypes',
        action=CoreDataSequence([CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}), CoreDataSet({4, 5})]).__len__,  # type: ignore
        expected=3),
])
def test_len(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('GETITEM_001',
        name='Get item at valid index',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[2],
        expected=30),
    PytestAction('GETITEM_002',
        name='Get item at negative index',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[-1],
        expected=50),
    PytestAction('GETITEM_003',
        name='Get item at out-of-bounds index (should raise error)',
        action=CoreDataSequence([10, 20, 30]).__getitem__,
        args=[5],
        exception=IndexError),
    PytestAction('GETITEM_004',
        name='Get item at negative out-of-bounds index (should raise error)',
        action=CoreDataSequence([10, 20, 30]).__getitem__,
        args=[-4],
        exception=IndexError),
    PytestAction('GETITEM_005',
        name='Get item from empty CoreDataSequence (should raise error)',
        action=CoreDataSequence([]).__getitem__,
        args=[0],
        exception=IndexError),
    PytestAction('GETITEM_006',
        name='Get item at index 0 using slice',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(0, 1)],
        expected=CoreDataSequence([10])),
    PytestAction('GETITEM_007',
        name='Get items using slice',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(1, 4)],
        expected=CoreDataSequence([20, 30, 40])),
    PytestAction('GETITEM_008',
        name='Get items using slice with step',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(0, 5, 2)],
        expected=CoreDataSequence([10, 30, 50])),
    PytestAction('GETITEM_009',
        name='Get items using slice with negative step',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(4, -1, -1)],
        expected=CoreDataSequence()),
    PytestAction('GETITEM_010',
        name='Get entire CoreDataSequence using slice',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(None, None, None)],
        expected=CoreDataSequence([10, 20, 30, 40, 50])),
    PytestAction('GETITEM_011',
        name='Get item at index 0 from single-item CoreDataSequence',
        action=CoreDataSequence([99]).__getitem__,
        args=[0],
        expected=99),
    PytestAction('GETITEM_012',
        name='Get item at index -1 from single-item CoreDataSequence',
        action=CoreDataSequence([99]).__getitem__,
        args=[-1],
        expected=99),
    PytestAction('GETITEM_013',
        name='Get items using slice that results in empty CoreDataSequence',
        action=CoreDataSequence([10, 20, 30]).__getitem__,
        args=[slice(2, 2)],
        expected=CoreDataSequence([])),
    PytestAction('GETITEM_014',
        name='Get items using slice with step larger than sequence',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(0, 5, 10)],
        expected=CoreDataSequence([10])),
    PytestAction('GETITEM_015',
        name='Get items using slice with negative indices',
        action=CoreDataSequence([10, 20, 30, 40, 50]).__getitem__,
        args=[slice(-4, -1)],
        expected=CoreDataSequence([20, 30, 40])),
    PytestAction('GETITEM_016',
        name='Get items using bracket form and slice',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[1:4],
        expected=CoreDataSequence([20, 30, 40])),
    PytestAction('GETITEM_017',
        name='Get item using bracket form and index',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[3],
        expected=40),
    PytestAction('GETITEM_018',
        name='Get items in reverse order using bracket form and slice',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[::-1],
        expected=CoreDataSequence([50, 40, 30, 20, 10])),
    PytestAction('GETITEM_019',
        name='Get items using slice with start greater than stop (should return empty)',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[4:2],
        expected=CoreDataSequence([])),
    PytestAction('GETITEM_020',
        name='Get items using slice with step of zero (should raise error)',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[::0],
        exception=ValueError),  # Python itself raises ValueError for slice step of zero
    PytestAction('GETITEM_021',
        name='Get item using invalid index type (should raise error)',
        action=lambda: CoreDataSequence([10, 20, 30])[1.5],  # type: ignore
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_INDEX_TYPE),
    PytestAction('GETITEM_022',
        name='Get items using invalid slice type (should raise error)',
        action=lambda: CoreDataSequence([10, 20, 30])[object()],  # type: ignore
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_INDEX_TYPE),
    PytestAction('GETITEM_023',
        name='Get items using slice with negative step in bracket form',
        action=lambda: CoreDataSequence([10, 20, 30, 40, 50])[4:-1:-1],  # type: ignore
        expected=CoreDataSequence([])),
])
def test_getitem(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('COUNT_001',
        name='Count existing item',
        action=CoreDataSequence([1, 2, 2, 3, 2, 4]).count,
        args=[2],
        expected=3),
    PytestAction('COUNT_002',
        name='Count non-existing item',
        action=CoreDataSequence([1, 2, 3, 4, 5]).count,
        args=[6],
        expected=0),
    PytestAction('COUNT_003',
        name='Count CoreDataSequence item',
        action=CoreDataSequence([
            CoreDataSequence([1, 2]),
            CoreDataSequence([1, 2]),
            CoreDataSequence([3, 4])]).count,
        args=[CoreDataSequence([1, 2])],
        expected=2),
    PytestAction('COUNT_004',
        name='Count CoreDataMapping item',
        action=CoreDataSequence([
            CoreDataMapping({'a': 1}),
            CoreDataMapping({'a': 1}),
            CoreDataMapping({'b': 2})]).count,
        args=[CoreDataMapping({'a': 1})],
        expected=2),
    PytestAction('COUNT_005',
        name='Count CoreDataSet item',
        action=CoreDataSequence([
            CoreDataSet({1, 2}),
            CoreDataSet({1, 2}),
            CoreDataSet({3, 4})]).count,
        args=[CoreDataSet({1, 2})],
        expected=2),
    PytestAction('COUNT_006',
        name='Count in empty CoreDataSequence',
        action=CoreDataSequence([]).count,
        args=[1],
        expected=0),
    PytestAction('COUNT_007',
        name='Count None item',
        action=CoreDataSequence([None, 1, None, 2]).count,
        args=[None],
        expected=2),
    PytestAction('COUNT_008',
        name='Count boolean True item',
        action=CoreDataSequence([True, False, True, 0, 1]).count,
        args=[True],
        expected=2),
    PytestAction('COUNT_009',
        name='Count boolean False item',
        action=CoreDataSequence([True, False, False, 0, 1]).count,
        args=[False],
        expected=2),
    PytestAction('COUNT_010',
        name='Count string item',
        action=CoreDataSequence(['a', 'b', 'a', 'c']).count,
        args=['a'],
        expected=2),
    PytestAction('COUNT_011',
        name='Count float item',
        action=CoreDataSequence([1.1, 2.2, 1.1, 3.3]).count,
        args=[1.1],
        expected=2),
    PytestAction('COUNT_012',
        name='Count invalid type item',
        action=CoreDataSequence([1, 2, 3]).count,
        args=[object()],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SEQUENCE_INVALID_ITEM_TYPE),
])
def test_count(testspec: TestSpec) -> None:
    """Test count method of CoreDataSequence."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='Test pickling and unpickling of CoreDataSequence with primitive types',
        action=lambda: pickle.loads(pickle.dumps(CoreDataSequence([1, 'two', 3.0, True, None]))),
        expected=CoreDataSequence([1, 'two', 3.0, True, None])),
    PytestAction('PICKLE_002',
        name='Test pickling and unpickling of nested CoreDataSequence',
        action=lambda: pickle.loads(
            pickle.dumps(
                CoreDataSequence([
                    CoreDataSequence([1, 2]),
                    CoreDataSequence(['a', 'b'])]))),
        expected=CoreDataSequence([
            CoreDataSequence([1, 2]), CoreDataSequence(['a', 'b'])])),
    PytestAction('PICKLE_003',
        name='Test pickling and unpickling of CoreDataSequence with CoreDataMapping',
        action=lambda: pickle.loads(
            pickle.dumps(CoreDataSequence([CoreDataMapping({'a': 1})]))),
        expected=CoreDataSequence([CoreDataMapping({'a': 1})])),
    PytestAction('PICKLE_004',
        name='Test pickling and unpickling of CoreDataSequence with CoreDataSet',
        action=lambda: pickle.loads(
            pickle.dumps(
                CoreDataSequence([CoreDataSet({2, 3})]))),
        expected=CoreDataSequence([CoreDataSet({2, 3})])),
])
def test_pickling(testspec: TestSpec) -> None:
    """Test pickling and unpickling of CoreDataSequence."""
    testspec.run()


def deep_copy_testspec() -> list[TestSpec]:
    core_seq = CoreDataSequence([1, 'two', 3.0, True, None])
    return [
        PytestAction('DEEPCOPY_001',
            name='Test deep copy of CoreDataSequence returns original object',
            action=deepcopy,
            args=[core_seq],
            assertion=Assert.IS,
            expected=core_seq),
    ]


@pytest.mark.parametrize('testspec', deep_copy_testspec())
def test_deep_copy(testspec: TestSpec) -> None:
    """Test deep copy of CoreDataSequence."""
    testspec.run()


def hash_testspec() -> list[TestSpec]:
    core_seq = CoreDataSequence([1, 2, 3])
    return [
        PytestAction('HASH_001',
            name='Test hashing of CoreDataSequence',
            action=hash,
            args=[core_seq],
            assertion=Assert.ISINSTANCE,
            expected=int),
        PytestAction('HASH_002',
            name='Test hashing of different CoreDataSequence instances with same content',
            action=hash, args=[CoreDataSequence([1, 2, 3])],
            assertion=Assert.EQUAL,
            expected=hash(core_seq)),
        PytestAction('HASH_003',
            name='Test hashing of CoreDataSequence different content',
            action=hash,
            args=[CoreDataSequence([1, 2, [3]])],
            assertion=Assert.NOT_EQUAL,
            expected=hash(core_seq)),
    ]


@pytest.mark.parametrize('testspec', hash_testspec())
def test_hash(testspec: TestSpec) -> None:
    """Test hashing of CoreDataSequence."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
        PytestAction('HASH_ID_001',
            name='Test content hashing of CoreDataSequence',
            action=CoreDataSequence([1, 2, 3]).hash_id,
            args=[],
            assertion=Assert.ISINSTANCE,
            expected=str),
        PytestAction('HASH_ID_002',
            name='Test content hashing of different CoreDataSequence instances with same content',
            action=CoreDataSequence([1, 2, 3]).hash_id,
            args=[],
            assertion=Assert.EQUAL,
            expected=CoreDataSequence([1, 2, 3]).hash_id()),
        PytestAction('HASH_ID_003',
            name='Test content hashing of CoreDataSequence different content',
            action=CoreDataSequence([1, 2, 3]).hash_id,
            args=[],
            assertion=Assert.NOT_EQUAL,
            expected=CoreDataSequence([1, 2, [3]]).hash_id()),
    ]
)
def test_hash_id(testspec: TestSpec) -> None:
    """Test content hashing of CoreDataSequence."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUAL_001',
        name='Test equality of identical CoreDataSequence instances',
        action=lambda: CoreDataSequence([1, 2, 3]) == CoreDataSequence([1, 2, 3]),
        expected=True),
    PytestAction('EQUAL_002',
        name='Test inequality of different CoreDataSequence instances',
        action=lambda: CoreDataSequence([1, 2, 3]) == CoreDataSequence([1, 2, 4]),
        expected=False),
])
def test_equal(testspec: TestSpec) -> None:
    """Test equality of CoreDataSequence."""
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('THAW_001',
        name='Test thaw method of CoreDataSequence with primitive types',
        action=CoreDataSequence([1, 'two', 3.0, True, None]).thaw,
        expected=[1, 'two', 3.0, True, None]),
    PytestAction('THAW_002',
        name='Test thaw method of nested CoreDataSequence',
        action=CoreDataSequence([CoreDataSequence([1, 2]), CoreDataSequence(['a', 'b'])]).thaw,
        expected=[[1, 2], ['a', 'b']]),
    PytestAction('THAW_003',
        name='Test thaw method of CoreDataSequence with CoreDataMapping',
        action=CoreDataSequence([CoreDataMapping({'a': 1})]).thaw,
        expected=[{'a': 1}]),
    PytestAction('THAW_004',
        name='Test thaw method of CoreDataSequence with CoreDataSet',
        action=CoreDataSequence([CoreDataSet({2, 3})]).thaw,
        expected=[{2, 3}]),
    PytestAction('THAW_005',
        name='Test thaw method of empty CoreDataSequence',
        action=CoreDataSequence([]).thaw,
        expected=[]),
    PytestAction('THAW_006',
        name='Test thaw method of CoreDataSequence with mixed CoreDataTypes',
        action=CoreDataSequence(
            [CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}),CoreDataSet({4, 5})]).thaw,  # type: ignore
        expected=[
            [1, 2],
            {'a': 3},
            {4, 5}
        ]),
    PytestAction('THAW_007',
        name='Test round-trip thawing and re-creation of CoreDataSequence',
        action=lambda: CoreDataSequence(
            CoreDataSequence([1, 'two', CoreDataSequence([3, 4])]).thaw()),
        assertion=Assert.EQUAL,
        expected=CoreDataSequence([1, 'two', CoreDataSequence([3, 4])])),
])
def test_thaw(testspec: TestSpec) -> None:
    """Test thaw method of CoreDataSequence."""
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('AS_JSON_001',
        name='Test as_json method of CoreDataSequence with primitive types',
        action=CoreDataSequence([1, 'two', 3.0, True, None]).as_json,
        expected=simplejson.dumps([1, 'two', 3.0, True, None], sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_002',
        name='Test as_json method of nested CoreDataSequence',
        action=CoreDataSequence([CoreDataSequence([1, 2]), CoreDataSequence(['a', 'b'])]).as_json,
        expected=simplejson.dumps([[1, 2], ['a', 'b']], sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_003',
        name='Test as_json method of CoreDataSequence with CoreDataMapping',
        action=CoreDataSequence([CoreDataMapping({'a': 1})]).as_json,
        expected=simplejson.dumps([{'a': 1}], sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_004',
        name='Test as_json method of CoreDataSequence with CoreDataSet',
        action=CoreDataSequence([CoreDataSet({2, 3})]).as_json,
        expected=simplejson.dumps([[2, 3]], sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_005',
        name='Test as_json method of empty CoreDataSequence',
        action=CoreDataSequence([]).as_json,
        expected=simplejson.dumps([], sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_006',
        name='Test as_json method of CoreDataSequence with mixed CoreDataTypes',
        action=CoreDataSequence(
            [CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}), CoreDataSet({4, 5})]).as_json,  # type: ignore
        expected=simplejson.dumps([
            [1, 2],
            {'a': 3},
            [4, 5]
        ], sort_keys=True, for_json=True, iterable_as_array=True)),
])
def test_as_json(testspec: TestSpec) -> None:
    """Test as_json method of CoreDataSequence."""
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
