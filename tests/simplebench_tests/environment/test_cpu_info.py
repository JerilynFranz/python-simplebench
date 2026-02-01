"""Tests for simplebench.environment.CPUInfo."""
import pickle

import autopypath  # noqa: F401
import pytest
from testspec import Assert, PytestAction, TestSpec

from simplebench.environment import CPUInfo
from simplebench.environment._cpu_info import _CPUInfoErrorTag
from simplebench.exceptions import SimpleBenchTypeError, SimpleBenchValueError


@pytest.mark.parametrize("testspec", [
    PytestAction('INIT_001',
        name="Initialize CPUInfo without cache key",
        action=CPUInfo,
        assertion=Assert.ISINSTANCE,
        expected=CPUInfo),
    PytestAction('INIT_002',
        name="Initialize CPUInfo with invalid cache key value",
        action=CPUInfo, kwargs={'cache_key': 'test_cache_key'},
        exception=SimpleBenchValueError,
        exception_tag=_CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE),
    PytestAction('INIT_003',
        name="Initialize CPUInfo with None cache key",
        action=CPUInfo, kwargs={'cache_key': None},
        assertion=Assert.ISINSTANCE,
        expected=CPUInfo),
    PytestAction('INIT_004',
        name="Initialize CPUInfo with empty string cache key",
        action=CPUInfo, kwargs={'cache_key': ''},
        exception=SimpleBenchValueError,
        exception_tag=_CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE),
    PytestAction('INIT_005',
        name="Initialize CPUInfo with alphanumeric cache key",
        action=CPUInfo, kwargs={'cache_key': 'CacheKey123'},
        assertion=Assert.ISINSTANCE,
        expected=CPUInfo),
    PytestAction('INIT_006',
        name="New CPUInfo instances with same cache key are identical",
        action=CPUInfo, kwargs={'cache_key': 'test'},
        expected=CPUInfo(cache_key='test'),
        assertion=Assert.EQUAL),
    PytestAction('INIT_007',
        name="CPUInfo instances with same cache key share cached data instance",
        action=CPUInfo, kwargs={'cache_key': 'test'},
        validate_result=lambda result: result.to_dict()['data'] is CPUInfo(cache_key='test').to_dict()['data']),
    PytestAction('INIT_008',
        name="CPUInfo instance with cache key and without cache key have different data instances",
        action=CPUInfo,
        validate_result=lambda result: result.to_dict()['data'] is not CPUInfo(cache_key='test').to_dict()['data']),
    PytestAction('INIT_009',
        name="Two non-cached CPUInfo instances do not share data instances",
        action=CPUInfo,
        validate_result=lambda result: result.to_dict()['data'] is not CPUInfo().to_dict()['data']),
    PytestAction('INIT_010',
        name="CPUInfo instances with different cache keys have different data instances",
        action=CPUInfo, kwargs={'cache_key': 'different'},
        validate_result=lambda result: result.to_dict()['data'] is not CPUInfo(cache_key='test').to_dict()['data']),
    PytestAction('INIT_011',
        name="Initialize CPUInfo with positional cache key argument",
        action=CPUInfo, args=['positionalkey'],
        assertion=Assert.ISINSTANCE,
        expected=CPUInfo),
    PytestAction('INIT_012',
        name="Initialize CPUInfo with non-string cache key argument",
        action=CPUInfo, kwargs={'cache_key': 123},
        exception=SimpleBenchTypeError,
        exception_tag=_CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_TYPE),
    PytestAction('INIT_013',
        name="Initialize CPUInfo with empty string cache key argument",
        action=CPUInfo, kwargs={'cache_key': ''},
        exception=SimpleBenchValueError,
        exception_tag=_CPUInfoErrorTag.INVALID_CACHE_KEY_PARAM_VALUE),
])
def test_init(testspec: TestSpec) -> None:
    """Test initializing CPUInfo."""
    testspec.run()


@pytest.mark.parametrize("testspec", [
    PytestAction('PICKLE_001',
        name="CPUInfo can be pickled",
        action=pickle.dumps,
        args=[CPUInfo('test')],
        assertion=Assert.ISINSTANCE,
        expected=bytes),
    PytestAction('PICKLE_002',
        name="CPUInfo can be unpickled",
        action=pickle.loads,
        args=[pickle.dumps(CPUInfo('test'))],
        assertion=Assert.ISINSTANCE,
        expected=CPUInfo),
    PytestAction('PICKLE_003',
        name="Unpickled CPUInfo equals original",
        action=pickle.loads,
        args=[pickle.dumps(CPUInfo('test'))],
        expected=CPUInfo('test'),
        assertion=Assert.EQUAL),
])
def test_pickle_cpu_info(testspec: TestSpec) -> None:
    """Test that CPUInfo instances can be pickled and unpickled."""
    testspec.run()
