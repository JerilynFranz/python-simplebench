"""Tests for CoreDataMapping type."""
import pickle
from copy import copy, deepcopy

import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.exceptions import SimpleBenchKeyError, SimpleBenchTypeError
from simplebench.simplebench_types import CoreDataMapping, CoreDataSequence, CoreDataSet
from simplebench.simplebench_types._core._error_tags import _CoreDataErrorTag


@pytest.mark.parametrize('testspec', [
    PytestAction('INIT_001',
        name='Init with empty input',
        action=CoreDataMapping,
        assertion=Assert.ISINSTANCE,
        expected=CoreDataMapping),
    PytestAction('INIT_002',
        name='Init with dict of primitives',
        action=CoreDataMapping,
        args=[{'a': 1, 'b': 'two', 'c': 3.0, 'd': True, 'e': None}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataMapping),
    PytestAction('INIT_003',
        name='Init with nested CoreDataMapping',
        action=CoreDataMapping,
        args=[{'nested': CoreDataMapping({'x': 1})}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataMapping),
    PytestAction('INIT_004',
        name='Init with CoreDataSequence and CoreDataSet values',
        action=CoreDataMapping,
        args=[{'seq': CoreDataSequence([1, 2]), 'set': CoreDataSet({3, 4})}],
        assertion=Assert.ISINSTANCE,
        expected=CoreDataMapping),
    PytestAction('INIT_005',
        name='Init with mapping containing invalid key type',
        action=CoreDataMapping,
        args=[{1: 'a'}],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_TYPE),
    PytestAction('INIT_006',
        name='Init with mapping containing invalid key value',
        action=CoreDataMapping,
        args=[{'': 1}],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_VALUE),
    PytestAction('INIT_007',
        name='Init with mapping containing invalid value type',
        action=CoreDataMapping,
        args=[{'a': object()}],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_VALUE_TYPE),
    PytestAction('INIT_008',
        name='Init with non-mapping type',
        action=CoreDataMapping,
        args=[['not', 'a', 'mapping']],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_ARG_TYPE),
    PytestAction('INIT_009',
        name='Init with non-mapping CoreDataTypes',
        action=CoreDataMapping,
        args=[CoreDataSequence([1, 2, 3])],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_ARG_TYPE),
    PytestAction('INIT_010',
        name='Init with non-mapping standard type',
        action=CoreDataMapping,
        args=[42],
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_ARG_TYPE),
    PytestAction('INIT_011',
        name='Init with mapping containing full range of valid types for values',
        action=CoreDataMapping,
        args=[{'int': 1, 'float': 2.0, 'str': 'three', 'bool': False, 'none': None,
               'core_mapping': CoreDataMapping({'key': 'value'}),
               'core_sequence': CoreDataSequence([1, 2, 3]),
               'core_set': CoreDataSet({4, 5, 6}),
               'mapping': {'a': 1},
               'sequence': [1, 2, 3],
               'set': {4, 5, 6}}]),
])
def test_init(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('GETITEM_001',
        name='Get item by key',
        action=CoreDataMapping({'a': 1}).__getitem__,
        args=['a'],
        expected=1),
    PytestAction('GETITEM_002',
        name='Get item with missing key (should raise error)',
        action=CoreDataMapping({'a': 1}).__getitem__,
        args=['b'],
        exception=SimpleBenchKeyError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_KEY_ERROR),
])
def test_getitem(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('CONTAINS_001',
        name='Check if key exists',
        action=lambda: 'a' in CoreDataMapping({'a': 1}),
        assertion=Assert.TRUE),
    PytestAction('CONTAINS_002',
        name='Check if key does not exist',
        action=lambda: 'b' in CoreDataMapping({'a': 1}),
        assertion=Assert.FALSE),
])
def test_contains(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('LEN_001',
        name='Get length of mapping',
        action=CoreDataMapping({'a': 1, 'b': 2}).__len__,
        expected=2),
    PytestAction('LEN_002',
        name='Get length of empty mapping',
        action=CoreDataMapping().__len__,
        expected=0),
])
def test_len(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('EQUALITY_001',
        name='Equality of identical mappings',
        action=lambda: CoreDataMapping({'a': 1}) == CoreDataMapping({'a': 1}),
        assertion=Assert.TRUE),
    PytestAction('EQUALITY_002',
        name='Inequality of different mappings',
        action=lambda: CoreDataMapping({'a': 1}) == CoreDataMapping({'b': 2}),
        assertion=Assert.FALSE),
])
def test_equality(testspec: TestSpec) -> None:
    testspec.run()


def copy_testspecs() -> list[TestSpec]:
    core_map: CoreDataMapping = CoreDataMapping({'a': 1})
    return [
        PytestAction('COPY_001',
            name='Copy returns self',
            action=copy,
            args=[core_map],
            assertion=Assert.IS,
            expected=core_map),
    ]
@pytest.mark.parametrize('testspec', copy_testspecs())
def test_copy(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('REPLACE_001',
        name='Replace value for existing key',
        action=lambda: CoreDataMapping({'a': 1}).replace(a=2),
        expected=CoreDataMapping({'a': 2})),
    PytestAction('REPLACE_002',
        name='Replace with new key',
        action=lambda: CoreDataMapping({'a': 1}).replace(b=2),
        expected=CoreDataMapping({'a': 1, 'b': 2})),
    PytestAction('REPLACE_003',
        name='Replace with invalid key type',
        action=lambda: CoreDataMapping({'a': 1}).replace(**{1: 2}),  # type: ignore
        exception=TypeError),
    PytestAction('REPLACE_004',
        name='Replace with invalid value type',
        action=lambda: CoreDataMapping({'a': 1}).replace(a=object()), # type: ignore
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_VALUE_TYPE),
    PytestAction('REPLACE_005',
        name='Replace multiple keys',
        action=lambda: CoreDataMapping({'a': 1, 'b': 2}).replace(a=10, b=20, c=30),
        expected=CoreDataMapping({'a': 10, 'b': 20, 'c': 30})),
    PytestAction('REPLACE_006',
        name='Replace with no changes (should return identical mapping)',
        action=lambda: CoreDataMapping({'a': 1}).replace(),
        expected=CoreDataMapping({'a': 1})),
    PytestAction('REPLACE_007',
        name='Replace invalid parameter (non-mapping type)',
        action=lambda: CoreDataMapping({'a': 1}).replace(42),  # type: ignore
        exception=TypeError),  # Python raises TypeError for invalid **kwargs)
    PytestAction('REPLACE_008',
        name='Replace with wrong value key (not an identifier)',
        action=lambda: CoreDataMapping({'a': 1}).replace(**{'a bad key': 'value'}),
        exception=SimpleBenchTypeError,
        exception_tag=_CoreDataErrorTag.CORE_DATA_MAPPING_INVALID_KEY_VALUE),
])
def test_replace(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('THAW_001',
        name='Thaw mapping with primitives',
        action=CoreDataMapping({'a': 1, 'b': 'two'}).thaw,
        expected={'a': 1, 'b': 'two'}),
    PytestAction('THAW_002',
        name='Thaw mapping with nested CoreDataMapping',
        action=CoreDataMapping({'nested': CoreDataMapping({'x': 1})}).thaw,
        expected={'nested': {'x': 1}}),
])
def test_thaw(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('AS_JSON_001',
        name='as_json with primitives',
        action=CoreDataMapping({'a': 1, 'b': 'two'}).as_json,
        expected='{"a": 1, "b": "two"}'),
    PytestAction('AS_JSON_002',
        name='as_json with nested CoreDataMapping',
        action=CoreDataMapping({'nested': CoreDataMapping({'x': 1})}).as_json,
        expected='{"nested": {"x": 1}}'),
    PytestAction('AS_JSON_003',
        name='as_json with nested CoreSequence and CoreDataSet',
        action=CoreDataMapping({'seq': CoreDataSequence([1, 2]), 'set': CoreDataSet({3, 4})}).as_json,
        expected='{"seq": [1, 2], "set": [3, 4]}'),
    PytestAction('AS_JSON_004',
        name='as_json with various primitives',
        action=CoreDataMapping({'int': 1, 'float': 2.0, 'bool': True, 'none': None}).as_json,
        expected='{"bool": true, "float": 2.0, "int": 1, "none": null}'),
])
def test_as_json(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('PICKLE_001',
        name='Pickle and unpickle mapping',
        action=lambda: pickle.loads(pickle.dumps(CoreDataMapping({'a': 1, 'b': 2}))),
        expected=CoreDataMapping({'a': 1, 'b': 2})),
])
def test_pickling(testspec: TestSpec) -> None:
    testspec.run()


def deepcopy_testspecs() -> list[TestSpec]:
    core_map: CoreDataMapping = CoreDataMapping({'a': 1})
    return [
        PytestAction('DEEPCOPY_001',
            name='Deepcopy returns self',
            action=deepcopy,
            args=[core_map],
            assertion=Assert.IS,
            expected=core_map),
    ]


@pytest.mark.parametrize('testspec', deepcopy_testspecs())
def test_deepcopy(testspec: TestSpec) -> None:
    testspec.run()

@pytest.mark.parametrize('testspec', [
    PytestAction('HASH_001',
        name='Hash is consistent for same content',
        action=hash,
        args=[CoreDataMapping({'a': 1, 'b': 2})],
        assertion=Assert.EQUAL,
        expected=hash(CoreDataMapping({'a': 1, 'b': 2}))),
    PytestAction('HASH_002',
        name='Hash differs for different content',
        action=hash,
        args=[CoreDataMapping({'a': 1, 'b': 3})],
        assertion=Assert.NOT_EQUAL,
        expected=hash(CoreDataMapping({'a': 1, 'b': 2}))),
])
def test_hash(testspec: TestSpec) -> None:
    testspec.run()

if __name__ == "__main__":
    pytest.main([__file__])
