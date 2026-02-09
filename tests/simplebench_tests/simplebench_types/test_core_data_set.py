"""Tests for CoreDataSet type."""
import pickle
from copy import deepcopy

import autopypath  # noqa: F401
import pytest
import simplejson
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, CoreDataSet
from simplebench.simplebench_types._core._error_tags import _CoreDataErrorTag


@pytest.mark.parametrize('testspec', [
    PytestAction('INIT_001',
        name='Init with empty input',
        action=CoreDataSet,
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_002',
        name='Init with set of integers',
        action=CoreDataSet,
        args=[{1, 2, 3, 4, 5}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_003',
        name='Init with set of strings',
        action=CoreDataSet,
        args=[{'a', 'b', 'c'}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_004',
        name='Init with mixed primitive types',
        action=CoreDataSet,
        args=[{1, 'two', 3.0, None}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_005',
        name='Init with nested CoreDataSet',
        action=CoreDataSet,
        args=[{CoreDataSet({1, 2}), CoreDataSet({'a', 'b'})}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_006',
        name='Init with invalid type (should raise error)',
        action=CoreDataSet,
        args=[{'a': 1}],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_007',
        name='Init with non-iterable (should raise error)',
        action=CoreDataSet,
        args=[42],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_SET_NOT_ELEMENT_COLLECTION),
    PytestAction('INIT_008',
        name='Init with nested sequence',
        action=CoreDataSet,
        args=[{1, (2, 3), ('four', 4)}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_009',
        name='Init with nested dictionary',
        action=CoreDataSet,
        args=[{1, CoreDataMapping({'two': 2}), 3}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_010',
        name='Init with nested frozenset',
        action=CoreDataSet,
        args=[{1, frozenset({2, 3}), 4}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_011',
        name='Init directly from list',
        action=CoreDataSet,
        args=[[1, 2, 3]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_012',
        name='Init with string',
        action=CoreDataSet,
        args=['a string'],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_013',
        name='Init with bytes',
        action=CoreDataSet,
        args=[b'some bytes'],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_014',
        name='Init with nested CoreDataTypes',
        action=CoreDataSet,
        args=[{CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}), CoreDataSet({4, 5})}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
    PytestAction('INIT_015',
        name='Init with dictionary item',
        action=CoreDataSet,
        args=[[{'str_key':  'value'}]],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataSet),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('CONTAINS_001',
        name='Check containment of existing item',
        action=CoreDataSet({1, 2, 3, 4, 5}).__contains__, args=[3],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_002',
        name='Check containment of non-existing item',
        action=CoreDataSet({1, 2, 3, 4, 5}).__contains__, args=[6],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_003',
        name='Check containment of CoreDataSet item',
        action=CoreDataSet({CoreDataSet({1, 2}), CoreDataSet({3, 4})}).__contains__,
        args=[CoreDataSet({1, 2})],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_004',
        name='Check containment of CoreDataMapping item',
        action=CoreDataSet({CoreDataMapping({'a': 1}), CoreDataMapping({'b': 2})}).__contains__,
        args=[CoreDataMapping({'a': 1})],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_005',
        name='Check containment of CoreDataSequence item',
        action=CoreDataSet({CoreDataSequence([1, 2]), CoreDataSequence([3, 4])}).__contains__,
        args=[CoreDataSequence([1, 2])],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_006',
        name='Check containment of invalid type',
        action=CoreDataSet({1, 2, 3}).__contains__, args=[object()],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_007',
        name='Check containment in empty CoreDataSet',
        action=CoreDataSet(set()).__contains__, args=[1],
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_008',
        name='Check containment of None',
        action=CoreDataSet({None, 1, 2}).__contains__, args=[None],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_009',
        name='Check containment of boolean True',
        action=CoreDataSet({True, False}).__contains__, args=[True],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_010',
        name='Check containment of boolean False',
        action=CoreDataSet({True, False}).__contains__, args=[False],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_011',
        name='Check containment of string item',
        action=CoreDataSet({'a', 'b', 'c'}).__contains__, args=['b'],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_012',
        name='Check containment of float item',
        action=CoreDataSet({1.1, 2.2, 3.3}).__contains__, args=[2.2],
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_013',
        name='Check "in" operator for existing item',
        action=lambda: 3 in CoreDataSet({1, 2, 3, 4, 5}),
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_014',
        name='Check "in" operator for non-existing item',
        action=lambda: 6 in CoreDataSet({1, 2, 3, 4, 5}),
        assertion=Assert.FALSE),
    PytestAction('CONTAINS_015',
        name='Check "in" operator for CoreDataMapping item',
        action=lambda: CoreDataMapping({'a': 1}) in CoreDataSet({CoreDataMapping({'a': 1}), CoreDataMapping({'b': 2})}),
        assertion=Assert.TRUE),
])
def test_contains(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name='Get length of non-empty CoreDataSet',
        action=CoreDataSet({1, 2, 3, 4, 5}).__len__,
        expected=5),
    PytestAction('LEN_002',
        name='Get length of empty CoreDataSet',
        action=CoreDataSet(set()).__len__,
        expected=0),
    PytestAction('LEN_003',
        name='Get length of CoreDataSet with mixed types',
        action=CoreDataSet({1, 'two', 3.0, None}).__len__,
        expected=4),
    PytestAction('LEN_004',
        name='Get length of CoreDataSet with nested CoreDataTypes',
        action=CoreDataSet({CoreDataSequence([1, 2]), CoreDataMapping({'a': 3}), CoreDataSet({4, 5})}).__len__,
        expected=3),
])
def test_len(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('THAW_001',
        name='Test thaw method of CoreDataSet with primitive types',
        action=CoreDataSet({1, 'two', 3.0, None}).thaw,
        expected={1, 'two', 3.0, None}),
    PytestAction('THAW_002',
        name='Test thaw method of nested CoreDataSet',
        action=CoreDataSet({CoreDataSet({1, 2}), CoreDataSet({'a', 'b'})}).thaw,
        expected={frozenset({1, 2}), frozenset({'a', 'b'})}),
    PytestAction('THAW_003',
        name='Test thaw method of CoreDataSet with CoreDataMapping',
        action=CoreDataSet({CoreDataMapping({'a': 1})}).thaw,
        expected={CoreDataMapping({'a': 1})}),
    PytestAction('THAW_004',
        name='Test thaw method of CoreDataSet with CoreDataSequence',
        action=CoreDataSet({CoreDataSequence([2, 3])}).thaw,
        expected={tuple([2, 3])}),
    PytestAction('THAW_005',
        name='Test thaw method of empty CoreDataSet',
        action=CoreDataSet(set()).thaw,
        expected=set()),
    PytestAction('THAW_006',
        name='Test thaw method of CoreDataSet with mixed CoreDataTypes',
        action=CoreDataSet({
            CoreDataSequence([1, 2]),
            CoreDataMapping({'a': 3}),
            CoreDataSet({4, 5})
        }).thaw,
        expected={
            tuple([1, 2]),
            CoreDataMapping({'a': 3}),
            frozenset({4, 5})
        }),
    PytestAction('THAW_007',
        name='Test round-trip thawing and re-creation of CoreDataSet',
        action=lambda: CoreDataSet(CoreDataSet({1, 'two', CoreDataSet({3, 4})}).thaw()),
        assertion=Assert.EQUAL,
        expected=CoreDataSet({1, 'two', CoreDataSet({3, 4})})),
])
def test_thaw(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('AS_JSON_001',
        name='Test as_json method with primitive types',
        action=CoreDataSet({1, 'two', 3.0, None}).as_json,
        expected=simplejson.dumps({1, 'two', 3.0, None}, sort_keys=True, for_json=True, iterable_as_array=True)),
    PytestAction('AS_JSON_002',
        name='Test as_json method of nested CoreDataSet',
        action=CoreDataSet({CoreDataSet({'a', 'b'})}).as_json,
        assertion=Assert.ISINSTANCE,
        expected=str),
    PytestAction('AS_JSON_003',
        name='Test as_json method with CoreDataMapping',
        action=CoreDataSet({CoreDataMapping({'a': 1})}).as_json,
        expected='[{"a": 1}]'),
    PytestAction('AS_JSON_004',
        name='Test as_json method with CoreDataSequence',
        action=CoreDataSet({CoreDataSequence([2, 3])}).as_json,
        expected="[[2, 3]]"),
    PytestAction('AS_JSON_005',
        name='Test as_json method with CoreDataSet',
        action=CoreDataSet({CoreDataSet({1, 2})}).as_json,
        assertion=Assert.REVERSE_IN,
        expected=('[[1, 2]]', '[[2, 1]]')),
    PytestAction('AS_JSON_006',
        name='Test as_json method with empty CoreDataSet',
        action=CoreDataSet(set()).as_json,
        expected="[]"),
])
def test_as_json(testspec: TestSpec) -> None:
    testspec.run()

def hash_testspec() -> list[TestSpec]:
    core_set = CoreDataSet({1, 2, 3})
    return [
        PytestAction('HASH_001',
            name='Test hashing of CoreDataSet',
            action=hash,
            args=[core_set],
            assertion=Assert.ISINSTANCE,
            expected=int),
        PytestAction('HASH_002',
            name='Test hashing of different CoreDataSet instances with same content',
            action=hash, args=[CoreDataSet({1, 2, 3})],
            assertion=Assert.EQUAL,
            expected=hash(core_set)),
        PytestAction('HASH_003',
            name='Test hashing of CoreDataSet different content',
            action=hash,
            args=[CoreDataSet({1, 2, frozenset({3})})],
            assertion=Assert.NOT_EQUAL,
            expected=hash(core_set)),
    ]

@pytest.mark.parametrize('testspec', hash_testspec())
def test_hash(testspec: TestSpec) -> None:
    testspec.run()

def deep_copy_testspec() -> list[TestSpec]:
    core_set = CoreDataSet({1, 'two', 3.0, None})
    return [
        PytestAction('DEEPCOPY_001',
            name='Test deep copy of CoreDataSet returns original object',
            action=deepcopy,
            args=[core_set],
            assertion=Assert.IS,
            expected=core_set),
    ]

@pytest.mark.parametrize('testspec', deep_copy_testspec())
def test_deep_copy(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='Test pickling and unpickling of CoreDataSet with primitive types',
        action=lambda: pickle.loads(pickle.dumps(CoreDataSet({1, 'two', 3.0, None}))),
        expected=CoreDataSet({1, 'two', 3.0, None})),
    PytestAction('PICKLE_002',
        name='Test pickling and unpickling of nested CoreDataSet',
        action=lambda: pickle.loads(pickle.dumps(CoreDataSet({CoreDataSet({1, 2}), CoreDataSet({'a', 'b'})}))),
        expected=CoreDataSet({CoreDataSet({1, 2}), CoreDataSet({'a', 'b'})})),
    PytestAction('PICKLE_003',
        name='Test pickling and unpickling of CoreDataSet with CoreDataMapping',
        action=lambda: pickle.loads(pickle.dumps(CoreDataSet({CoreDataMapping({'a': 1})}))),
        expected=CoreDataSet({CoreDataMapping({'a': 1})})),
    PytestAction('PICKLE_004',
        name='Test pickling and unpickling of CoreDataSet with CoreDataSequence',
        action=lambda: pickle.loads(pickle.dumps(CoreDataSet({CoreDataSequence([2, 3])}))),
        expected=CoreDataSet({CoreDataSequence([2, 3])})),
])
def test_pickling(testspec: TestSpec) -> None:
    testspec.run()


@pytest.mark.parametrize('testspec', [
    PytestAction('EQUAL_001',
        name='Test equality of identical CoreDataSet instances',
        action=lambda: CoreDataSet({1, 2, 3}) == CoreDataSet({1, 2, 3}),
        assertion=Assert.TRUE),
    PytestAction('EQUAL_002',
        name='Test inequality of different CoreDataSet instances',
        action=lambda: CoreDataSet({1, 2, 3}) == CoreDataSet({4, 5, 6}),
        assertion=Assert.FALSE),
])
def test_equality(testspec: TestSpec) -> None:
    testspec.run()


if __name__ == "__main__":
    pytest.main([__file__])
